# IPL Pulse

A live second-screen IPL prediction game. Predict every ball, climb your team's leaderboard, win swag.

- **Single page React app** (Vite + Tailwind) styled with an IPL stadium-night theme
- **FastAPI backend** with a built-in match simulator that replays a dramatic RCB vs KKR match
- **Context-aware rating engine** — points shift based on phase, recent balls, post-wicket pressure, late-chase desperation, and combo patterns like W → W and 6 → 6 → 6
- **Server-sent events** push every ball, every resolution, every leaderboard change to all connected clients in real time
- **Captain's Call** moments multiply correct predictions by 5×
- **Team-vs-team fan war** + per-team top 10 + global top 10
- **Single container** — one Dockerfile, one Cloud Run service, one URL

## What's in the box

```
ipl-pulse/
├── backend/
│   ├── main.py            # FastAPI app, SSE stream, simulator loop
│   ├── rating_engine.py   # The probability-based scoring brain
│   ├── match_data.py      # Embedded RCB vs KKR ball-by-ball
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/    # Onboarding, MatchHeader, PredictionCard, Leaderboards, Ticker, ResultBanner, MeStats
│   │   └── index.css      # IPL-themed styles
│   ├── index.html
│   └── package.json
├── Dockerfile             # Multi-stage: builds frontend, packages with backend
└── .dockerignore
```

## How it works

1. The **simulator** runs as a background task inside the FastAPI app, ticking through the embedded match one ball at a time at a configurable interval.
2. After each ball, the API **resolves every open prediction** — checks correctness, applies the rating engine's points (which depend on match state), applies streak and combo multipliers.
3. Updates push to every connected client via **SSE** — match state, ticker moments, all leaderboards.
4. The React app **subscribes once** and reactively updates all UI: prediction tiles, score header, fan-war bar, leaderboards.

## Run locally

You need Python 3.11+ and Node 20+.

```bash
# Terminal 1 — backend
cd backend
pip install -r requirements.txt
BALL_INTERVAL_SECS=6 PREDICTION_WINDOW_SECS=4.5 uvicorn main:app --reload --port 8080

# Terminal 2 — frontend (proxies /api to backend)
cd frontend
npm install
npm run dev
# open http://localhost:5173
```

To run as a single container locally (the production setup):

```bash
docker build -t ipl-pulse .
docker run -p 8080:8080 ipl-pulse
# open http://localhost:8080
```

## Deploy to Google Cloud Run — step by step

These steps assume you have a Google Cloud account with billing enabled. You'll deploy a single Cloud Run service that serves both the React frontend and the FastAPI backend from one URL.

### 1. One-time setup

Install the `gcloud` CLI if you don't have it:
- macOS / Linux: https://cloud.google.com/sdk/docs/install
- Windows: https://cloud.google.com/sdk/docs/install#windows

Then log in and set up:

```bash
gcloud auth login
gcloud auth configure-docker
```

### 2. Set your project

```bash
# Either use an existing project
gcloud config set project YOUR_PROJECT_ID

# Or create a new one
gcloud projects create ipl-pulse-demo --name="IPL Pulse"
gcloud config set project ipl-pulse-demo
# Then link billing in the console: https://console.cloud.google.com/billing
```

Set a region close to your users (Mumbai is ideal for IPL):

```bash
gcloud config set run/region asia-south1
```

### 3. Enable the required APIs

```bash
gcloud services enable \
  run.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com
```

### 4. Create an Artifact Registry repo to hold the container image

```bash
gcloud artifacts repositories create ipl-pulse \
  --repository-format=docker \
  --location=asia-south1 \
  --description="IPL Pulse containers"
```

### 5. Build and push the image

The simplest path is to let Cloud Build do the build remotely (no Docker needed locally):

```bash
# From the project root (where the Dockerfile is)
gcloud builds submit \
  --tag asia-south1-docker.pkg.dev/$(gcloud config get-value project)/ipl-pulse/app:latest
```

That takes ~3-5 minutes the first time.

(If you'd rather build locally and push:)
```bash
docker build -t asia-south1-docker.pkg.dev/$(gcloud config get-value project)/ipl-pulse/app:latest .
docker push asia-south1-docker.pkg.dev/$(gcloud config get-value project)/ipl-pulse/app:latest
```

### 6. Deploy to Cloud Run

```bash
gcloud run deploy ipl-pulse \
  --image asia-south1-docker.pkg.dev/$(gcloud config get-value project)/ipl-pulse/app:latest \
  --region asia-south1 \
  --platform managed \
  --allow-unauthenticated \
  --port 8080 \
  --memory 512Mi \
  --cpu 1 \
  --min-instances 1 \
  --max-instances 1 \
  --timeout 3600 \
  --set-env-vars BALL_INTERVAL_SECS=6,PREDICTION_WINDOW_SECS=4.5
```

**Important flags explained:**

- `--min-instances 1` — keeps one instance always warm. Critical because the simulator is a background task; scaling to zero would pause the match.
- `--max-instances 1` — we keep state in-memory in a single instance, so we must not let Cloud Run spin up more. (Adding Firestore would let us scale; for the demo, one instance is correct.)
- `--timeout 3600` — extends request timeout to 60 minutes for long SSE connections.
- `--allow-unauthenticated` — anyone on the internet can play.

Cloud Run prints a URL when it's done. Open it.

### 7. Demo speed knob

If you want to demo faster than real-time, redeploy with smaller intervals:

```bash
gcloud run services update ipl-pulse \
  --region asia-south1 \
  --update-env-vars BALL_INTERVAL_SECS=2.5,PREDICTION_WINDOW_SECS=1.8
```

The match has 188 balls. At 6s per ball that's ~19 minutes — about the pace of a TV broadcast. At 2.5s it finishes in 8 minutes.

### 8. Reset the match

The match runs once per container. To start a fresh match, restart the service:

```bash
gcloud run services update ipl-pulse --region asia-south1 --update-env-vars NOOP=$(date +%s)
```

(The `NOOP` trick forces a fresh revision and restarts the instance.)

## Costs

For a demo, **negligible** — well within Cloud Run's free tier:
- 2 million requests/month free
- 360,000 GB-seconds free
- 180,000 vCPU-seconds free

A single 512MB / 1 vCPU instance running 24/7 is around \$15-25/month before free tier. Within the free tier most of that is covered.

## Configuration reference

Environment variables the backend respects:

| Variable | Default | Purpose |
| --- | --- | --- |
| `PORT` | 8080 | Cloud Run sets this automatically |
| `BALL_INTERVAL_SECS` | 6 | Seconds between balls in the simulator |
| `PREDICTION_WINDOW_SECS` | 4.5 | Window during which predictions can be submitted between balls |

## Swap in real Cricsheet data later

The `match_data.MATCH` dict in `backend/match_data.py` follows the same shape as Cricsheet's JSON. Replace it with a parsed Cricsheet file (https://cricsheet.org/downloads/) and the rest of the system works unchanged.
