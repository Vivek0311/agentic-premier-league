"""
Rating engine — the heart of the prediction game.

Given the current match state, compute the probability of each outcome
on the next ball. Points awarded = base / probability, so rare correct
predictions pay much more than common ones. Points are HIDDEN from the
user before resolution (Option B from our design discussion) — they only
see the magnitude after their prediction resolves.

This is intentionally rule-based, not ML. The point isn't to be the
world's best cricket model — it's to feel alive and contextual so the
same prediction at different moments pays differently.
"""

from typing import Dict, Optional, Tuple

OUTCOMES = ["dot", "runs", "four", "six", "wicket", "extra"]

# Base IPL ball-by-ball distribution (rough, but realistic).
BASE_PROBS = {
    "dot":    0.36,
    "runs":   0.36,
    "four":   0.10,
    "six":    0.05,
    "wicket": 0.05,
    "extra":  0.08,
}

# Point scale — `base / prob` gives raw points. We multiply by this for readability.
BASE_POINTS = 10.0

# Combo multipliers when the previous correctly-predicted outcome chains with this one.
# Two-ball patterns. Symmetric except where noted.
TWO_BALL_COMBOS = {
    ("wicket", "wicket"): 3.5,   # Two wickets in a row — true rarity
    ("six", "six"):       2.5,
    ("four", "four"):     1.8,
    ("six", "four"):      1.8,
    ("four", "six"):      1.8,
    ("six", "wicket"):    2.2,   # Aggression then dismissal
    ("wicket", "six"):    2.2,   # New batter aggression
    ("wicket", "four"):   1.8,
    ("dot", "dot"):       1.5,   # Maiden potential
}

# Three-ball patterns get even bigger multipliers when the user predicts all three correctly.
THREE_BALL_COMBOS = {
    ("wicket", "wicket", "wicket"): 8.0,   # Hat-trick
    ("six", "six", "six"):          6.0,
    ("dot", "dot", "dot"):          3.0,
}


def get_phase(over: int) -> str:
    """T20 phase based on over number (1-indexed)."""
    if over <= 6:
        return "powerplay"
    elif over <= 15:
        return "middle"
    else:
        return "death"


def compute_probabilities(state: Dict) -> Dict[str, float]:
    """
    Compute outcome probabilities given current match state.
    State is a dict with: over (1..20), wickets, balls_since_wicket,
    target (Optional), score, innings, recent_outcomes (list of recent ball outcomes).
    """
    probs = dict(BASE_PROBS)
    phase = get_phase(state.get("over", 1))

    # Phase modifiers
    if phase == "powerplay":
        probs["four"]   *= 1.6
        probs["six"]    *= 1.3
        probs["dot"]    *= 0.85
        probs["wicket"] *= 1.1
    elif phase == "middle":
        probs["dot"]    *= 1.15
        probs["four"]   *= 0.85
        probs["six"]    *= 0.8
        probs["runs"]   *= 1.1
    else:  # death
        probs["six"]    *= 2.4
        probs["four"]   *= 1.3
        probs["wicket"] *= 1.8
        probs["dot"]    *= 0.65
        probs["runs"]   *= 0.85

    # Post-wicket spike: pressure ball, new batter
    balls_since_wicket = state.get("balls_since_wicket", 99)
    if balls_since_wicket == 0:  # the ball right after a wicket
        probs["dot"]    *= 1.6
        probs["wicket"] *= 1.7
        probs["four"]   *= 0.6
        probs["six"]    *= 0.6
    elif balls_since_wicket == 1:
        probs["dot"]    *= 1.25
        probs["wicket"] *= 1.3

    # Recent boundary momentum — if last 2 balls were boundaries, six prob goes up
    # but so does wicket (batter aggression cuts both ways)
    recent = state.get("recent_outcomes", [])
    if len(recent) >= 2 and recent[-1] in ("four", "six") and recent[-2] in ("four", "six"):
        probs["six"]    *= 1.5
        probs["wicket"] *= 1.4
        probs["dot"]    *= 0.7

    # Late-chase desperation: required rate climbs, sixes and wickets both spike
    target = state.get("target")
    if target and state.get("innings") == 2:
        balls_left = max(1, (20 - state["over"] + 1) * 6 - (state.get("ball_in_over", 0) - 1))
        runs_needed = target - state.get("score", 0)
        req_rate = (runs_needed / balls_left) * 6 if balls_left > 0 else 0
        if req_rate > 12:
            probs["six"]    *= 1.6
            probs["wicket"] *= 1.5
            probs["dot"]    *= 0.7

    # Renormalize so probabilities sum to 1
    total = sum(probs.values())
    return {k: v / total for k, v in probs.items()}


def compute_points(outcome: str, state: Dict) -> int:
    """Base points for predicting `outcome` correctly given current state."""
    probs = compute_probabilities(state)
    prob = max(probs[outcome], 0.01)  # floor to avoid runaway
    raw = BASE_POINTS / prob
    return int(round(raw))


def compute_combo_multiplier(
    last_predictions: list,   # most recent first — list of (predicted_outcome, was_correct)
    current_outcome: str,
) -> Tuple[float, Optional[str]]:
    """
    Check if the user's chain of recent CORRECT predictions matches a combo pattern.
    Returns (multiplier, pattern_name) where pattern_name is e.g. "W → W" for display.
    """
    if not last_predictions:
        return 1.0, None

    # Build the chain of recent correct outcomes leading up to current
    chain = [current_outcome]
    for predicted, was_correct in last_predictions:
        if was_correct:
            chain.insert(0, predicted)
        else:
            break  # any incorrect break ends the chain

    if len(chain) >= 3:
        triple = tuple(chain[-3:])
        if triple in THREE_BALL_COMBOS:
            return THREE_BALL_COMBOS[triple], format_pattern(triple)

    if len(chain) >= 2:
        pair = tuple(chain[-2:])
        if pair in TWO_BALL_COMBOS:
            return TWO_BALL_COMBOS[pair], format_pattern(pair)

    return 1.0, None


def format_pattern(pattern: tuple) -> str:
    """Pretty-print a combo pattern: ('wicket', 'wicket') -> 'W → W'."""
    short = {"dot": "•", "runs": "1-3", "four": "4", "six": "6", "wicket": "W", "extra": "EX"}
    return " → ".join(short.get(p, p) for p in pattern)


def streak_multiplier(streak: int) -> float:
    """Streak bonus on top of base points. Caps at 3x."""
    if streak < 3:
        return 1.0
    if streak < 5:
        return 1.5
    if streak < 8:
        return 2.0
    if streak < 12:
        return 2.5
    return 3.0
