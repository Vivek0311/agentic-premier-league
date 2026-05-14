"""
IPL Pulse — backend service.

Single Cloud Run service that:
  - Runs the match simulator as a background task (replays embedded IPL match)
  - Serves the React UI as static files
  - Handles user creation, team selection, predictions
  - Streams live ball events to all connected clients via SSE
  - Maintains real-time leaderboards (global, team-specific, team-vs-team)

In-memory state is intentional. For a demo with one running match, in-memory
state on a single instance is the simplest correct choice. Firestore can be
swapped in by replacing the State class.
"""

import asyncio
import json
import os
import random
import time
import uuid
from contextlib import asynccontextmanager
from typing import Dict, List, Optional, Set

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import match_data
import rating_engine as engine


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

# Seconds between balls in the simulator. 6 = realistic pace, 3 = brisk demo, 1 = blast.
BALL_INTERVAL_SECS = float(os.environ.get("BALL_INTERVAL_SECS", "6"))
# Seconds to allow predictions before locking, must be < BALL_INTERVAL_SECS
PREDICTION_WINDOW_SECS = float(os.environ.get("PREDICTION_WINDOW_SECS", "4.5"))
# Captain's Call fires once per innings at a dramatic moment — multiplier on points
CAPTAINS_CALL_MULTIPLIER = 5.0


# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------

class State:
    def __init__(self):
        self.match = match_data.get_match()
        self.balls = match_data.flatten_balls()
        self.current_ball_index = -1  # -1 = match not started; 0 = first ball delivered
        self.match_status = "ready"   # "ready" | "live" | "ended"
        self.last_ball_at: float = 0.0
        self.next_ball_at: float = 0.0
        self.captains_call_ball_index: Optional[int] = None  # which ball is the Captain's Call

        # users: user_id -> {display_name, team, points, streak, best_streak, badges,
        #                    correct, total, power_ups, last_predictions (list of (outcome, correct))}
        self.users: Dict[str, dict] = {}

        # predictions: ball_index -> {user_id -> outcome}
        self.predictions: Dict[int, Dict[str, str]] = {}

        # resolved_predictions: ball_index -> {user_id -> {correct, points, combo, combo_name}}
        self.resolved: Dict[int, Dict[str, dict]] = {}

        # SSE subscribers
        self.subscribers: Set[asyncio.Queue] = set()

        # ticker moments — recent dramatic events for the moments banner
        self.ticker: List[dict] = []

        # Pre-pick captain's call: a dramatic-looking ball in each innings
        self._pick_captains_calls()

    def _pick_captains_calls(self):
        """Pick one dramatic ball per innings as the Captain's Call."""
        innings_starts = {}
        for i, ball in enumerate(self.balls):
            innings_starts.setdefault(ball["innings"], []).append(i)

        chosen = []
        for innings_id, indices in innings_starts.items():
            # Pick a ball in the death overs or post-wicket — high drama
            candidates = [
                i for i in indices
                if self.balls[i]["over"] >= 16
                or (self.balls[i]["balls_since_wicket"] == 0 and self.balls[i]["over"] >= 8)
            ]
            if candidates:
                chosen.append(candidates[len(candidates) // 3])
            else:
                chosen.append(indices[-3])

        # Store only the first one for now; can extend to multiple
        self.captains_calls = set(chosen)


STATE = State()


# ---------------------------------------------------------------------------
# Pydantic schemas
# ---------------------------------------------------------------------------

class JoinRequest(BaseModel):
    display_name: str
    team: str  # full team name e.g. "Chennai Super Kings"


class JoinResponse(BaseModel):
    user_id: str
    display_name: str
    team: str


class PredictRequest(BaseModel):
    user_id: str
    outcome: str  # one of OUTCOMES


# ---------------------------------------------------------------------------
# SSE helpers
# ---------------------------------------------------------------------------

async def publish(event: dict):
    """Push event to every connected SSE subscriber."""
    dead = []
    for q in STATE.subscribers:
        try:
            q.put_nowait(event)
        except asyncio.QueueFull:
            dead.append(q)
    for q in dead:
        STATE.subscribers.discard(q)


def build_match_state_for_engine(ball_index: int) -> dict:
    """Build the state dict the rating engine needs for the UPCOMING ball at ball_index."""
    if ball_index >= len(STATE.balls):
        return {}
    ball = STATE.balls[ball_index]
    recent = [STATE.balls[i]["outcome"] for i in range(max(0, ball_index - 5), ball_index)]
    return {
        "over": ball["over"],
        "ball_in_over": ball["ball_in_over"],
        "wickets": ball["wickets_before"],
        "balls_since_wicket": ball["balls_since_wicket"],
        "score": ball["score_before"],
        "innings": ball["innings"],
        "target": ball.get("target"),
        "recent_outcomes": recent,
    }


def build_public_match_state() -> dict:
    """The condensed match state we publish to clients on each ball."""
    if STATE.current_ball_index < 0:
        return {
            "status": STATE.match_status,
            "info": {
                "teams": STATE.match["info"]["teams"],
                "team_short": STATE.match["info"]["team_short"],
                "team_colors": STATE.match["info"]["team_colors"],
                "venue": STATE.match["info"]["venue"],
            },
            "current_ball": None,
            "next_ball_at_unix": STATE.next_ball_at,
        }

    ball = STATE.balls[STATE.current_ball_index]
    # Build innings totals up to this ball
    innings_totals = {1: {"score": 0, "wickets": 0}, 2: {"score": 0, "wickets": 0}}
    for i in range(STATE.current_ball_index + 1):
        b = STATE.balls[i]
        innings_totals[b["innings"]]["score"] = b["score_after"]
        innings_totals[b["innings"]]["wickets"] = b["wickets_after"]

    return {
        "status": STATE.match_status,
        "info": {
            "teams": STATE.match["info"]["teams"],
            "team_short": STATE.match["info"]["team_short"],
            "team_colors": STATE.match["info"]["team_colors"],
            "venue": STATE.match["info"]["venue"],
        },
        "current_ball": {
            "index": STATE.current_ball_index,
            "innings": ball["innings"],
            "batting_team": ball["batting_team"],
            "bowling_team": ball["bowling_team"],
            "over": ball["over"],
            "ball_in_over": ball["ball_in_over"],
            "bowler": ball["bowler"],
            "batter": ball["batter"],
            "outcome": ball["outcome"],
            "runs": ball["runs"],
            "commentary": ball["commentary"],
            "wicket": ball.get("wicket"),
        },
        "innings_totals": innings_totals,
        "target": STATE.balls[STATE.current_ball_index].get("target") if ball["innings"] == 2 else None,
        "next_ball_at_unix": STATE.next_ball_at,
        "captains_call_next": (STATE.current_ball_index + 1) in STATE.captains_calls,
    }


# ---------------------------------------------------------------------------
# The simulator loop
# ---------------------------------------------------------------------------

async def simulator_loop():
    """Background task — ticks through the embedded match and emits ball events."""
    print(f"Simulator starting. {len(STATE.balls)} balls to play. Interval={BALL_INTERVAL_SECS}s")
    # Wait a few seconds at start so clients can connect
    await asyncio.sleep(3)

    STATE.match_status = "live"
    STATE.last_ball_at = time.time()
    STATE.next_ball_at = STATE.last_ball_at + BALL_INTERVAL_SECS

    # Emit the initial "prediction window opens" event for ball 0
    await publish({
        "type": "match_start",
        "state": build_public_match_state(),
        "next_ball_index": 0,
        "captains_call": 0 in STATE.captains_calls,
    })

    for ball_index in range(len(STATE.balls)):
        # Wait until next ball is due
        sleep_for = max(0.0, STATE.next_ball_at - time.time())
        await asyncio.sleep(sleep_for)

        # Deliver the ball — advance state
        STATE.current_ball_index = ball_index
        STATE.last_ball_at = time.time()
        STATE.next_ball_at = STATE.last_ball_at + BALL_INTERVAL_SECS

        # Resolve all predictions for this ball
        resolutions = resolve_predictions(ball_index)

        # Build ticker moments for dramatic events
        ball = STATE.balls[ball_index]
        update_ticker(ball, resolutions)

        # Publish the ball event
        await publish({
            "type": "ball",
            "state": build_public_match_state(),
            "resolutions": resolutions,
            "ticker": STATE.ticker[-5:],  # last 5 moments
            "next_ball_index": ball_index + 1 if ball_index + 1 < len(STATE.balls) else None,
            "captains_call_next": (ball_index + 1) in STATE.captains_calls,
            "leaderboards": build_leaderboards(),
        })

    STATE.match_status = "ended"
    await publish({
        "type": "match_end",
        "leaderboards": build_leaderboards(),
        "final_state": build_public_match_state(),
    })
    print("Match ended.")


def resolve_predictions(ball_index: int) -> dict:
    """When a ball is delivered, resolve every user's prediction for that ball."""
    ball = STATE.balls[ball_index]
    actual = ball["outcome"]
    is_captains_call = ball_index in STATE.captains_calls

    user_predictions = STATE.predictions.get(ball_index, {})
    state_for_engine = build_match_state_for_engine(ball_index)
    resolutions = {}

    for user_id, predicted in user_predictions.items():
        user = STATE.users.get(user_id)
        if not user:
            continue

        correct = predicted == actual
        base_points = engine.compute_points(predicted, state_for_engine) if correct else 0

        combo_mult, combo_name = (1.0, None)
        if correct:
            combo_mult, combo_name = engine.compute_combo_multiplier(
                user["last_predictions"][-2:][::-1],  # most recent first
                actual,
            )

        streak_mult = engine.streak_multiplier(user["streak"] + 1) if correct else 1.0
        captains_mult = CAPTAINS_CALL_MULTIPLIER if (correct and is_captains_call) else 1.0

        points_awarded = int(round(base_points * combo_mult * streak_mult * captains_mult))

        # Update user state
        user["points"] += points_awarded
        user["total"] += 1
        if correct:
            user["correct"] += 1
            user["streak"] += 1
            user["best_streak"] = max(user["best_streak"], user["streak"])
        else:
            user["streak"] = 0

        # Track last_predictions for combo chain detection
        user["last_predictions"].append((predicted, correct))
        if len(user["last_predictions"]) > 5:
            user["last_predictions"] = user["last_predictions"][-5:]

        # Award badges for milestones
        badges_earned = []
        if correct and predicted == "wicket" and ball_index in STATE.captains_calls:
            if "Captain's Call wicket" not in user["badges"]:
                user["badges"].append("Captain's Call wicket")
                badges_earned.append("Captain's Call wicket")
        if user["best_streak"] == 5 and "🔥 5-streak" not in user["badges"]:
            user["badges"].append("🔥 5-streak")
            badges_earned.append("🔥 5-streak")
        if user["best_streak"] == 10 and "🔥🔥 10-streak" not in user["badges"]:
            user["badges"].append("🔥🔥 10-streak")
            badges_earned.append("🔥🔥 10-streak")

        # Award power-ups every 3rd correct prediction (max 3 each kind)
        if correct and user["correct"] % 3 == 0:
            if user["power_ups"]["double_down"] < 3:
                user["power_ups"]["double_down"] += 1

        resolutions[user_id] = {
            "correct": correct,
            "predicted": predicted,
            "actual": actual,
            "points": points_awarded,
            "combo_name": combo_name,
            "combo_multiplier": combo_mult,
            "streak_multiplier": streak_mult,
            "captains_call": is_captains_call,
            "streak": user["streak"],
            "total_points": user["points"],
            "badges_earned": badges_earned,
        }

    STATE.resolved[ball_index] = resolutions
    return resolutions


def update_ticker(ball: dict, resolutions: dict):
    """Generate dramatic ticker moments."""
    moments = []

    # Top scorer of the resolution
    if resolutions:
        top = max(resolutions.items(), key=lambda x: x[1]["points"])
        if top[1]["points"] >= 100:
            user = STATE.users[top[0]]
            moments.append({
                "kind": "big_hit",
                "text": f"{user['display_name']} ({STATE.match['info']['team_short'].get(user['team'], '??')}) nailed it for +{top[1]['points']}!",
                "at": time.time(),
            })

    # Combo callouts
    for user_id, r in resolutions.items():
        if r["combo_name"]:
            user = STATE.users[user_id]
            moments.append({
                "kind": "combo",
                "text": f"🔥 COMBO {r['combo_name']} — {user['display_name']} +{r['points']}!",
                "at": time.time(),
            })

    # Match drama callouts
    if ball.get("wicket"):
        moments.append({
            "kind": "wicket",
            "text": f"WICKET! {ball['wicket']['player_out']} {ball['wicket']['kind']}",
            "at": time.time(),
        })
    elif ball["outcome"] == "six":
        moments.append({
            "kind": "six",
            "text": f"SIX! {ball['batter']} clears the rope",
            "at": time.time(),
        })

    STATE.ticker.extend(moments)
    if len(STATE.ticker) > 50:
        STATE.ticker = STATE.ticker[-50:]


# ---------------------------------------------------------------------------
# Leaderboards
# ---------------------------------------------------------------------------

def build_leaderboards() -> dict:
    """Build all the leaderboards we expose."""
    users_list = list(STATE.users.values())
    users_list.sort(key=lambda u: u["points"], reverse=True)

    # Global top 10
    global_top = [
        {
            "rank": i + 1,
            "display_name": u["display_name"],
            "team": u["team"],
            "team_short": STATE.match["info"]["team_short"].get(u["team"], "??"),
            "points": u["points"],
            "streak": u["streak"],
            "best_streak": u["best_streak"],
            "user_id": u["id"],
        }
        for i, u in enumerate(users_list[:10])
    ]

    # Per-team top 10
    teams = STATE.match["info"]["teams"]
    team_tops = {}
    for team in teams:
        team_users = [u for u in users_list if u["team"] == team]
        team_tops[team] = [
            {
                "rank": i + 1,
                "display_name": u["display_name"],
                "team_short": STATE.match["info"]["team_short"][team],
                "points": u["points"],
                "streak": u["streak"],
                "best_streak": u["best_streak"],
                "user_id": u["id"],
            }
            for i, u in enumerate(team_users[:10])
        ]

    # Team vs team aggregate (average points per user with at least 1 prediction)
    team_agg = {}
    for team in teams:
        team_users = [u for u in users_list if u["team"] == team and u["total"] > 0]
        if team_users:
            team_agg[team] = {
                "team": team,
                "team_short": STATE.match["info"]["team_short"][team],
                "color": STATE.match["info"]["team_colors"][team],
                "avg_points": int(sum(u["points"] for u in team_users) / len(team_users)),
                "total_points": sum(u["points"] for u in team_users),
                "player_count": len(team_users),
            }
        else:
            team_agg[team] = {
                "team": team,
                "team_short": STATE.match["info"]["team_short"][team],
                "color": STATE.match["info"]["team_colors"][team],
                "avg_points": 0,
                "total_points": 0,
                "player_count": 0,
            }

    return {
        "global_top10": global_top,
        "team_top10": team_tops,
        "team_aggregate": team_agg,
        "total_players": len(users_list),
    }


# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start simulator on app boot
    task = asyncio.create_task(simulator_loop())
    yield
    task.cancel()


app = FastAPI(lifespan=lifespan, title="IPL Pulse")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health():
    return {"ok": True, "status": STATE.match_status, "ball": STATE.current_ball_index}


@app.get("/api/match")
async def get_match_state():
    return {
        "state": build_public_match_state(),
        "leaderboards": build_leaderboards(),
        "ticker": STATE.ticker[-5:],
    }


@app.post("/api/join", response_model=JoinResponse)
async def join(req: JoinRequest):
    teams = STATE.match["info"]["teams"]
    if req.team not in teams:
        raise HTTPException(400, f"Team must be one of {teams}")
    if not req.display_name or len(req.display_name.strip()) == 0:
        raise HTTPException(400, "Display name required")

    user_id = str(uuid.uuid4())
    STATE.users[user_id] = {
        "id": user_id,
        "display_name": req.display_name.strip()[:24],
        "team": req.team,
        "points": 0,
        "streak": 0,
        "best_streak": 0,
        "correct": 0,
        "total": 0,
        "badges": [],
        "power_ups": {"double_down": 0, "insurance": 0, "insider": 0},
        "last_predictions": [],
    }
    return JoinResponse(user_id=user_id, display_name=req.display_name.strip(), team=req.team)


@app.post("/api/predict")
async def predict(req: PredictRequest):
    if req.user_id not in STATE.users:
        raise HTTPException(404, "User not found")
    if req.outcome not in engine.OUTCOMES:
        raise HTTPException(400, f"Outcome must be one of {engine.OUTCOMES}")
    if STATE.match_status != "live":
        raise HTTPException(400, "Match not live")

    next_ball = STATE.current_ball_index + 1
    if next_ball >= len(STATE.balls):
        raise HTTPException(400, "No more balls")

    # Check prediction window — must be more than (BALL_INTERVAL - PREDICTION_WINDOW) past last ball
    now = time.time()
    elapsed_since_last = now - STATE.last_ball_at
    if elapsed_since_last > PREDICTION_WINDOW_SECS:
        raise HTTPException(400, "Prediction window closed")

    STATE.predictions.setdefault(next_ball, {})[req.user_id] = req.outcome
    return {"ok": True, "ball_index": next_ball, "outcome": req.outcome}


@app.get("/api/me/{user_id}")
async def me(user_id: str):
    user = STATE.users.get(user_id)
    if not user:
        raise HTTPException(404, "User not found")
    # Find user's global rank
    sorted_users = sorted(STATE.users.values(), key=lambda u: u["points"], reverse=True)
    rank = next((i + 1 for i, u in enumerate(sorted_users) if u["id"] == user_id), None)
    team_users = [u for u in sorted_users if u["team"] == user["team"]]
    team_rank = next((i + 1 for i, u in enumerate(team_users) if u["id"] == user_id), None)
    return {
        "id": user["id"],
        "display_name": user["display_name"],
        "team": user["team"],
        "points": user["points"],
        "streak": user["streak"],
        "best_streak": user["best_streak"],
        "correct": user["correct"],
        "total": user["total"],
        "accuracy": (user["correct"] / user["total"]) if user["total"] else 0,
        "badges": user["badges"],
        "power_ups": user["power_ups"],
        "global_rank": rank,
        "team_rank": team_rank,
    }


@app.get("/api/stream")
async def stream(request: Request):
    """Server-Sent Events — pushes ball events, resolutions, ticker, leaderboards."""
    queue: asyncio.Queue = asyncio.Queue(maxsize=100)
    STATE.subscribers.add(queue)

    async def event_gen():
        try:
            # Send a snapshot on connect
            initial = {
                "type": "snapshot",
                "state": build_public_match_state(),
                "leaderboards": build_leaderboards(),
                "ticker": STATE.ticker[-5:],
            }
            yield f"data: {json.dumps(initial)}\n\n"

            while True:
                if await request.is_disconnected():
                    break
                try:
                    event = await asyncio.wait_for(queue.get(), timeout=15.0)
                    yield f"data: {json.dumps(event)}\n\n"
                except asyncio.TimeoutError:
                    # heartbeat to keep connection alive on Cloud Run
                    yield ": heartbeat\n\n"
        finally:
            STATE.subscribers.discard(queue)

    return StreamingResponse(
        event_gen(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",  # disable proxy buffering
            "Connection": "keep-alive",
        },
    )


# ---------------------------------------------------------------------------
# Static frontend (served from the same Cloud Run service)
# ---------------------------------------------------------------------------

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if os.path.isdir(STATIC_DIR):
    app.mount("/assets", StaticFiles(directory=os.path.join(STATIC_DIR, "assets")), name="assets")

    @app.get("/")
    async def root():
        return FileResponse(os.path.join(STATIC_DIR, "index.html"))

    @app.get("/{full_path:path}")
    async def spa_catchall(full_path: str):
        # Anything that isn't an API route serves the SPA
        index = os.path.join(STATIC_DIR, "index.html")
        return FileResponse(index)


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
