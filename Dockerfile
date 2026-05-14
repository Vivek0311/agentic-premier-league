# Stage 1: build the React frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /app
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install --no-audit --no-fund
COPY frontend/ ./
RUN npm run build

# Stage 2: Python runtime serving the FastAPI app + built static frontend
FROM python:3.11-slim

# Don't run as root — Cloud Run best practice
RUN groupadd -r app && useradd -r -g app app

WORKDIR /app

# Install Python deps
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./

# Copy the built frontend into the static dir the FastAPI app serves
COPY --from=frontend-builder /app/dist /app/static

# Cloud Run sets PORT env var — default to 8080 if unset
ENV PORT=8080
EXPOSE 8080

USER app

# Use Uvicorn directly; FastAPI lifespan handles the simulator background task
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
