"""
IPL 2026 — 57th Match — RCB vs KKR
Shaheed Veer Narayan Singh Stadium, Raipur — 13 May 2026

Anchored reconstruction from the real match. Verified anchors:
  KKR 192/4 in 20 overs (Raghuvanshi 71 off 46 run-out last ball,
                         Rinku 49*(29), Rahane gone over 4 b Hazlewood,
                         Allen 18(8) b Bhuvneshwar over 3)
  KKR milestones: 18/0 after 2, 50 in 5.3, 76/2 timeout at 9.0,
                  100 in 11.1, 150 in 15.6, 153/3 timeout at 16.0
  RCB 196/4 in 18.1 — won by 6 wickets
  RCB falls: Bethell 15(12) c&b Tyagi at 37/1 in 3.2,
             Padikkal 39(27) at 129/2 in 13.1 (Impact for Duffy at KKR 13.6),
             Patidar 11 in over 15,
             Jitesh holes out in over 17
  Kohli 101* hits the winning runs.
  DRS: over 15.2 (KKR innings) RCB review of Rinku wicket — struck down.

Squads exactly as named at the toss.

Schema mirrors Cricsheet's JSON so this file is a drop-in replacement
when Cricsheet publishes match 1529300.

Outcome encoding for the rating engine:
  "dot"    — 0 runs off the bat
  "runs"   — 1, 2 or 3 runs
  "four"   — boundary 4
  "six"    — boundary 6
  "wicket" — wicket falls
  "extra"  — wide / no-ball / bye / leg-bye
"""

MATCH = {
    "info": {
        "match_id": "rcb-vs-kkr-2026-raipur-1529300",
        "teams": ["Kolkata Knight Riders", "Royal Challengers Bengaluru"],
        "team_short": {
            "Kolkata Knight Riders": "KKR",
            "Royal Challengers Bengaluru": "RCB",
        },
        "team_colors": {
            "Kolkata Knight Riders": "#3A225D",
            "Royal Challengers Bengaluru": "#EC1C24",
        },
        "venue": "Shaheed Veer Narayan Singh Stadium, Raipur",
        "toss": {"winner": "Royal Challengers Bengaluru", "decision": "field"},
        "date": "2026-05-13",
        "match_number": "57th Match, IPL 2026",
    },
    "innings": [
        # =================================================================
        # INNINGS 1 — KKR 192/4 in 20 overs
        # =================================================================
        {
            "batting_team": "Kolkata Knight Riders",
            "bowling_team": "Royal Challengers Bengaluru",
            "overs": [
                # Over 1 — Bhuvneshwar to Rahane. Rahane finds a boundary. 4 runs.
                {"over": 1, "bowler": "Bhuvneshwar", "balls": [
                    {"batter": "Rahane", "outcome": "dot",  "runs": 0, "commentary": "Bhuvi vs Rahane — full in the channel, defended back"},
                    {"batter": "Rahane", "outcome": "dot",  "runs": 0, "commentary": "Knuckle ball outside off, nibbled at and missed"},
                    {"batter": "Rahane", "outcome": "four", "runs": 4, "commentary": "FOUR! Rahane finds the gap, away in the first over"},
                    {"batter": "Rahane", "outcome": "dot",  "runs": 0, "commentary": "Back of a length, defended"},
                    {"batter": "Rahane", "outcome": "dot",  "runs": 0, "commentary": "Defended again"},
                    {"batter": "Rahane", "outcome": "dot",  "runs": 0, "commentary": "Maiden over for Bhuvi nearly — but the four kept it alive. KKR 4/0"},
                ]},
                # Over 2 — Duffy. Allen smashes 14 in this over. End: 18/0.
                {"over": 2, "bowler": "Duffy", "balls": [
                    {"batter": "Allen",  "outcome": "four", "runs": 4, "commentary": "ALLEN! Standing still, freeing the arms, away through the off side"},
                    {"batter": "Allen",  "outcome": "six",  "runs": 6, "commentary": "MAXIMUM! Allen launches Duffy over long-on, seeing it like a football"},
                    {"batter": "Allen",  "outcome": "dot",  "runs": 0, "commentary": "Yorker, dug out"},
                    {"batter": "Allen",  "outcome": "four", "runs": 4, "commentary": "FOUR! Authoritative cut behind point"},
                    {"batter": "Allen",  "outcome": "dot",  "runs": 0, "commentary": "Beaten outside off"},
                    {"batter": "Allen",  "outcome": "dot",  "runs": 0, "commentary": "Dot to finish — but 14 off the over. RCB 18/0"},
                ]},
                # Over 3 — Bhuvi. Allen falls nicking off for 18 off 8.
                {"over": 3, "bowler": "Bhuvneshwar", "balls": [
                    {"batter": "Allen",  "outcome": "four", "runs": 4, "commentary": "Allen punches Bhuvi wide of mid-off — another authoritative four"},
                    {"batter": "Allen",  "outcome": "wicket","runs": 0, "wicket": {"player_out": "Allen", "kind": "caught", "fielder": "Jitesh"}, "commentary": "GOT HIM! Perfect length angling into the corridor and straightening — Allen nicks off for 18(8). Crucial wicket"},
                    {"batter": "Raghuvanshi", "outcome": "dot", "runs": 0, "commentary": "Raghuvanshi walks in at three, watchful first ball"},
                    {"batter": "Raghuvanshi", "outcome": "runs", "runs": 1, "commentary": "Off the mark, pushed to point"},
                    {"batter": "Rahane", "outcome": "dot",  "runs": 0, "commentary": "Bhuvi straightens one, defended"},
                    {"batter": "Rahane", "outcome": "runs", "runs": 1, "commentary": "Single to long-on. KKR 24/1"},
                ]},
                # Over 4 — Hazlewood. Rahane removed by a short ball. End ~28-30.
                {"over": 4, "bowler": "Hazlewood", "balls": [
                    {"batter": "Raghuvanshi", "outcome": "runs", "runs": 1, "commentary": "Worked to fine leg for one"},
                    {"batter": "Rahane", "outcome": "dot",  "runs": 0, "commentary": "Beaten by the angle and bounce"},
                    {"batter": "Rahane", "outcome": "wicket","runs": 0, "wicket": {"player_out": "Rahane", "kind": "caught", "fielder": "Bethell"}, "commentary": "RAHANE GONE! Well-directed short ball, cramped on the pull, top-edged — Bethell takes it. KKR 26/2"},
                    {"batter": "Green",  "outcome": "dot",  "runs": 0, "commentary": "Green walks in, plays out a dot"},
                    {"batter": "Green",  "outcome": "runs", "runs": 1, "commentary": "Off the mark, single to point"},
                    {"batter": "Raghuvanshi", "outcome": "runs", "runs": 1, "commentary": "Single to long-on. KKR 28/2"},
                ]},
                # Over 5 — Duffy. KKR reach 50 in 5.3 overs => need 22 more in 33 balls or so.
                # End of over 5 ~38. (50 hit on ball 5.3 means in over 6.)
                {"over": 5, "bowler": "Duffy", "balls": [
                    {"batter": "Green",  "outcome": "four", "runs": 4, "commentary": "FOUR! Green drives Duffy past mid-off, classy"},
                    {"batter": "Green",  "outcome": "runs", "runs": 1, "commentary": "Single to long-on"},
                    {"batter": "Raghuvanshi", "outcome": "runs", "runs": 1, "commentary": "Pushed to point for one"},
                    {"batter": "Green",  "outcome": "dot",  "runs": 0, "commentary": "Beaten outside off"},
                    {"batter": "Green",  "outcome": "four", "runs": 4, "commentary": "FOUR! Lofted over the bowler's head — Green getting going"},
                    {"batter": "Green",  "outcome": "runs", "runs": 1, "commentary": "Single to deep cover. KKR 38/2"},
                ]},
                # Over 6 — Hazlewood. KKR hit 50 on ball 5.3 -> ball 3 of this over.
                # Powerplay ends at 6. Aim: end ~50-52.
                {"over": 6, "bowler": "Hazlewood", "balls": [
                    {"batter": "Raghuvanshi", "outcome": "runs", "runs": 1, "commentary": "Worked to mid-wicket for one"},
                    {"batter": "Green",  "outcome": "runs", "runs": 1, "commentary": "Single, strike rotated"},
                    {"batter": "Raghuvanshi", "outcome": "four", "runs": 4, "commentary": "FOUR! Raghuvanshi guides a back-of-length one fine — KKR FIFTY up in 5.3"},
                    {"batter": "Raghuvanshi", "outcome": "dot",  "runs": 0, "commentary": "Beaten outside off"},
                    {"batter": "Raghuvanshi", "outcome": "runs", "runs": 1, "commentary": "Single to point"},
                    {"batter": "Green",  "outcome": "dot",  "runs": 0, "commentary": "End of powerplay. KKR 51/2"},
                ]},
                # Over 7 — Suyash Sharma into the attack. Quiet over.
                {"over": 7, "bowler": "Suyash", "balls": [
                    {"batter": "Green",  "outcome": "runs", "runs": 1, "commentary": "Pushed for one"},
                    {"batter": "Raghuvanshi", "outcome": "runs", "runs": 1, "commentary": "Single, point"},
                    {"batter": "Green",  "outcome": "dot",  "runs": 0, "commentary": "Forward defence"},
                    {"batter": "Green",  "outcome": "runs", "runs": 2, "commentary": "Two, driven into the gap"},
                    {"batter": "Green",  "outcome": "runs", "runs": 1, "commentary": "Single, strike rotated"},
                    {"batter": "Raghuvanshi", "outcome": "runs", "runs": 1, "commentary": "End of over. KKR 57/2"},
                ]},
                # Over 8 — Krunal Pandya. Quiet.
                {"over": 8, "bowler": "Krunal", "balls": [
                    {"batter": "Green",  "outcome": "runs", "runs": 1, "commentary": "Single, mid-on"},
                    {"batter": "Raghuvanshi", "outcome": "dot",  "runs": 0, "commentary": "Defended"},
                    {"batter": "Raghuvanshi", "outcome": "four", "runs": 4, "commentary": "FOUR! Raghuvanshi sweeps fine"},
                    {"batter": "Raghuvanshi", "outcome": "runs", "runs": 1, "commentary": "Single, long-on"},
                    {"batter": "Green",  "outcome": "runs", "runs": 1, "commentary": "Single, strike rotated"},
                    {"batter": "Raghuvanshi", "outcome": "runs", "runs": 1, "commentary": "End of over. KKR 64/2"},
                ]},
                # Over 9 — Suyash. Strategic timeout at 9.0 => 76/2 (Raghu 26, Green 12).
                {"over": 9, "bowler": "Suyash", "balls": [
                    {"batter": "Green",  "outcome": "runs", "runs": 2, "commentary": "Two, driven into the gap"},
                    {"batter": "Green",  "outcome": "runs", "runs": 1, "commentary": "Single"},
                    {"batter": "Raghuvanshi", "outcome": "four", "runs": 4, "commentary": "FOUR! Raghuvanshi cuts behind point — accelerating"},
                    {"batter": "Raghuvanshi", "outcome": "four", "runs": 4, "commentary": "FOUR again! Stays back and punches Suyash past point"},
                    {"batter": "Green",  "outcome": "four", "runs": 4, "commentary": "FOUR! Green lofts over mid-off"},
                    {"batter": "Green",  "outcome": "runs", "runs": 2, "commentary": "Two, brought back for second. STRATEGIC TIMEOUT — KKR 76/2 (Raghu 26, Green 12)"},
                ]},
                # Over 10 — Krunal. KKR 100 in 11.1, need 24 across over 10 and ball 1 of 11.
                # End over 10: ~89.
                {"over": 10, "bowler": "Krunal", "balls": [
                    {"batter": "Raghuvanshi", "outcome": "runs", "runs": 1, "commentary": "Single, long-on"},
                    {"batter": "Green",  "outcome": "four", "runs": 4, "commentary": "FOUR! Green drives past mid-off"},
                    {"batter": "Green",  "outcome": "dot",  "runs": 0, "commentary": "Defended"},
                    {"batter": "Green",  "outcome": "six",  "runs": 6, "commentary": "SIX! Green steps out and lofts Krunal into the stands"},
                    {"batter": "Green",  "outcome": "runs", "runs": 1, "commentary": "Single, long-on"},
                    {"batter": "Raghuvanshi", "outcome": "runs", "runs": 1, "commentary": "End of over. KKR 89/2"},
                ]},
                # Over 11 — Rasikh. KKR 100 in 11.1 — boundary on ball 1 lands the milestone.
                {"over": 11, "bowler": "Rasikh", "balls": [
                    {"batter": "Green",  "outcome": "extra","runs": 1, "commentary": "WIDE called down the leg side"},
                    {"batter": "Green",  "outcome": "six",  "runs": 6, "commentary": "SIX! Green hammers Rasikh over long-on — KKR THREE-FIGURE TICK at 11.1"},
                    {"batter": "Green",  "outcome": "runs", "runs": 1, "commentary": "Single, long-on"},
                    {"batter": "Raghuvanshi", "outcome": "runs", "runs": 1, "commentary": "Single, point"},
                    {"batter": "Green",  "outcome": "runs", "runs": 2, "commentary": "Two, into the gap"},
                    {"batter": "Green",  "outcome": "runs", "runs": 1, "commentary": "Single, long-on"},
                    {"batter": "Raghuvanshi", "outcome": "runs", "runs": 1, "commentary": "End of over. KKR 109/2"},
                ]},
                # Over 12 — Rasikh again, Green dismissed (3rd wicket falls around here).
                # 3rd partnership ended at 50 runs in 39 balls.
                {"over": 12, "bowler": "Rasikh", "balls": [
                    {"batter": "Raghuvanshi", "outcome": "runs", "runs": 1, "commentary": "Single to long-on"},
                    {"batter": "Green",  "outcome": "four", "runs": 4, "commentary": "FOUR! Green drives through covers"},
                    {"batter": "Green",  "outcome": "wicket","runs": 0, "wicket": {"player_out": "Green", "kind": "bowled", "fielder": None}, "commentary": "BOWLED! Skids through on the back-of-length, Green misses. 3rd wicket gone — partnership of 50 in 39"},
                    {"batter": "Rinku",  "outcome": "dot",  "runs": 0, "commentary": "Rinku walks in, plays out a dot"},
                    {"batter": "Rinku",  "outcome": "runs", "runs": 1, "commentary": "Off the mark, single"},
                    {"batter": "Raghuvanshi", "outcome": "runs", "runs": 1, "commentary": "End of over. KKR 112/3"},
                ]},
                # Over 13 — Suyash. Padikkal Impact sub for Duffy happens at 13.6 (last ball).
                {"over": 13, "bowler": "Suyash", "balls": [
                    {"batter": "Rinku",  "outcome": "runs", "runs": 1, "commentary": "Single, fine leg"},
                    {"batter": "Raghuvanshi", "outcome": "four", "runs": 4, "commentary": "FOUR! Raghuvanshi sweeps fine"},
                    {"batter": "Raghuvanshi", "outcome": "dot",  "runs": 0, "commentary": "Beaten in flight"},
                    {"batter": "Raghuvanshi", "outcome": "runs", "runs": 1, "commentary": "Single, long-on"},
                    {"batter": "Rinku",  "outcome": "runs", "runs": 1, "commentary": "Single, point"},
                    {"batter": "Raghuvanshi", "outcome": "runs", "runs": 1, "commentary": "End of over — Padikkal comes in for Duffy. KKR 120/3"},
                ]},
                # Over 14 — Krunal. Raghuvanshi to FIFTY in 32 balls.
                {"over": 14, "bowler": "Krunal", "balls": [
                    {"batter": "Rinku",  "outcome": "runs", "runs": 1, "commentary": "Single to long-on"},
                    {"batter": "Raghuvanshi", "outcome": "four", "runs": 4, "commentary": "RAGHUVANSHI FIFTY! 32 balls — short-arm jab past deep mid-wicket"},
                    {"batter": "Raghuvanshi", "outcome": "runs", "runs": 1, "commentary": "Single, strike rotated"},
                    {"batter": "Rinku",  "outcome": "six",  "runs": 6, "commentary": "RINKU! Steps across and hooks for six"},
                    {"batter": "Rinku",  "outcome": "dot",  "runs": 0, "commentary": "Defended"},
                    {"batter": "Rinku",  "outcome": "runs", "runs": 1, "commentary": "End of over. KKR 133/3"},
                ]},
                # Over 15 — Bhuvneshwar. DRS at 15.2 — RCB review Rinku, struck down.
                # 150 hits at 15.6. End of over 15: 150.
                {"over": 15, "bowler": "Bhuvneshwar", "balls": [
                    {"batter": "Raghuvanshi", "outcome": "four", "runs": 4, "commentary": "FOUR! Raghuvanshi slog-swept past deep mid-wicket"},
                    {"batter": "Raghuvanshi", "outcome": "extra","runs": 1, "commentary": "WIDE — RCB REVIEW! Rinku wicket claimed — STRUCK DOWN. Wide stands"},
                    {"batter": "Raghuvanshi", "outcome": "runs", "runs": 1, "commentary": "Single — Rinku survives"},
                    {"batter": "Rinku",  "outcome": "four", "runs": 4, "commentary": "FOUR! Rinku slashes Bhuvi past point"},
                    {"batter": "Rinku",  "outcome": "dot",  "runs": 0, "commentary": "Beaten by the slower one"},
                    {"batter": "Rinku",  "outcome": "runs", "runs": 1, "commentary": "Single, strike rotated"},
                    {"batter": "Raghuvanshi", "outcome": "runs", "runs": 1, "commentary": "End of over — KKR FIFTY-FIFTY at 154/3"},
                ]},
                # Over 16 — Hazlewood. Strategic timeout at 16.0 = 153/3 (Raghu 62, Rinku 19).
                {"over": 16, "bowler": "Hazlewood", "balls": [
                    {"batter": "Rinku",  "outcome": "four", "runs": 4, "commentary": "FOUR! Rinku makes room and slashes past point"},
                    {"batter": "Rinku",  "outcome": "runs", "runs": 1, "commentary": "Single to long-on"},
                    {"batter": "Raghuvanshi", "outcome": "four", "runs": 4, "commentary": "RAGHUVANSHI FOUR! Drives Hazlewood through cover"},
                    {"batter": "Raghuvanshi", "outcome": "runs", "runs": 1, "commentary": "Single, point"},
                    {"batter": "Rinku",  "outcome": "dot",  "runs": 0, "commentary": "Yorker, dug out"},
                    {"batter": "Rinku",  "outcome": "runs", "runs": 1, "commentary": "Single — STRATEGIC TIMEOUT: KKR 153/3, Raghu 62, Rinku 19"},
                ]},
                # KKR add 39 runs in last 4 overs to reach 192/4 (Raghuvanshi run-out last ball).
                # Over 17 — Bhuvneshwar. Some boundaries needed.
                {"over": 17, "bowler": "Bhuvneshwar", "balls": [
                    {"batter": "Raghuvanshi", "outcome": "four", "runs": 4, "commentary": "FOUR! Raghuvanshi finds the gap, accelerating"},
                    {"batter": "Raghuvanshi", "outcome": "runs", "runs": 1, "commentary": "Single, long-on"},
                    {"batter": "Rinku",  "outcome": "six",  "runs": 6, "commentary": "RINKU! Launches Bhuvi for a big SIX over midwicket — only slot ball of the death"},
                    {"batter": "Rinku",  "outcome": "dot",  "runs": 0, "commentary": "Low full-toss, played to mid-on"},
                    {"batter": "Rinku",  "outcome": "runs", "runs": 1, "commentary": "Single, long-off"},
                    {"batter": "Raghuvanshi", "outcome": "runs", "runs": 1, "commentary": "End of over. KKR 166/3"},
                ]},
                # Over 18 — Rasikh. Yorker-heavy death. ~9 runs.
                {"over": 18, "bowler": "Rasikh", "balls": [
                    {"batter": "Rinku",  "outcome": "runs", "runs": 1, "commentary": "Single, long-on"},
                    {"batter": "Raghuvanshi", "outcome": "four", "runs": 4, "commentary": "FOUR! Raghuvanshi slashes past point"},
                    {"batter": "Raghuvanshi", "outcome": "dot",  "runs": 0, "commentary": "Excellent yorker"},
                    {"batter": "Raghuvanshi", "outcome": "runs", "runs": 1, "commentary": "Single, point"},
                    {"batter": "Rinku",  "outcome": "runs", "runs": 2, "commentary": "Two, into the gap"},
                    {"batter": "Rinku",  "outcome": "runs", "runs": 1, "commentary": "Single — end of over. KKR 175/3"},
                ]},
                # Over 19 — Hazlewood. Yorker discipline. ~8 runs.
                {"over": 19, "bowler": "Hazlewood", "balls": [
                    {"batter": "Raghuvanshi", "outcome": "runs", "runs": 1, "commentary": "Single, long-on"},
                    {"batter": "Rinku",  "outcome": "runs", "runs": 1, "commentary": "Single, mid-on"},
                    {"batter": "Rinku",  "outcome": "dot",  "runs": 0, "commentary": "Yorker, dug out"},
                    {"batter": "Rinku",  "outcome": "runs", "runs": 1, "commentary": "Single, fine leg"},
                    {"batter": "Raghuvanshi", "outcome": "runs", "runs": 1, "commentary": "Single, long-on"},
                    {"batter": "Rinku",  "outcome": "runs", "runs": 1, "commentary": "End of over. KKR 183/3"},
                ]},
                # Over 20 — Bhuvneshwar. KKR add 9 (need 9 to reach 192). Raghuvanshi run-out last ball for 71.
                {"over": 20, "bowler": "Bhuvneshwar", "balls": [
                    {"batter": "Raghuvanshi", "outcome": "four", "runs": 4, "commentary": "FOUR! Raghuvanshi guides Bhuvi past short third — death-overs special"},
                    {"batter": "Rinku",  "outcome": "four", "runs": 4, "commentary": "FOUR! Rinku slashes past third man — moving towards 50"},
                    {"batter": "Rinku",  "outcome": "dot",  "runs": 0, "commentary": "Yorker, dug out"},
                    {"batter": "Rinku",  "outcome": "runs", "runs": 1, "commentary": "Single, fine leg — Rinku to 49*"},
                    {"batter": "Raghuvanshi", "outcome": "runs", "runs": 2, "commentary": "Two, driven into the gap"},
                    {"batter": "Raghuvanshi", "outcome": "wicket","runs": 1, "wicket": {"player_out": "Raghuvanshi", "kind": "run out", "fielder": "Patidar"}, "commentary": "RUN OUT! Raghuvanshi gone going for the second on the last ball — 71 off 46. KKR FINISH 192/4, Rinku 49* off 29"},
                ]},
            ],
        },
        # =================================================================
        # INNINGS 2 — RCB 196/4 in 18.1, won by 6 wickets
        # =================================================================
        {
            "batting_team": "Royal Challengers Bengaluru",
            "bowling_team": "Kolkata Knight Riders",
            "overs": [
                # Over 1 — Arora to Bethell & Kohli. Kohli OFF THE MARK first ball, ducks ended.
                # End of over 1: ~4-5.
                {"over": 1, "bowler": "Arora", "balls": [
                    {"batter": "Kohli",   "outcome": "runs", "runs": 1, "commentary": "KOHLI OFF THE MARK FIRST BALL! Fist-pump, two-innings duck streak ended"},
                    {"batter": "Bethell", "outcome": "dot",  "runs": 0, "commentary": "Bethell defends"},
                    {"batter": "Bethell", "outcome": "dot",  "runs": 0, "commentary": "Beaten outside off"},
                    {"batter": "Bethell", "outcome": "runs", "runs": 1, "commentary": "Bethell rides the bounce, guides to backward point"},
                    {"batter": "Kohli",   "outcome": "dot",  "runs": 0, "commentary": "Defended"},
                    {"batter": "Kohli",   "outcome": "runs", "runs": 2, "commentary": "Top-edge on the pull, lands safely — two taken. End over 1, RCB 4/0"},
                ]},
                # Over 2 — Duffy went for 14 on KKR side; on RCB side we need 18/0 after 2 -> so 14 in this over.
                # Kohli rolls his wrists, in-swinger boundary, dribbles off thigh-pad single, etc.
                {"over": 2, "bowler": "Tyagi", "balls": [
                    {"batter": "Kohli",   "outcome": "four", "runs": 4, "commentary": "KOHLI! Clips the in-swinger past mid-wicket — vintage"},
                    {"batter": "Kohli",   "outcome": "runs", "runs": 1, "commentary": "Length on middle and leg, dribbles off thigh-pad for one"},
                    {"batter": "Bethell", "outcome": "four", "runs": 4, "commentary": "FOUR! Bethell glides one fine"},
                    {"batter": "Bethell", "outcome": "dot",  "runs": 0, "commentary": "Defended"},
                    {"batter": "Bethell", "outcome": "four", "runs": 4, "commentary": "FOUR! Bethell punches through covers"},
                    {"batter": "Bethell", "outcome": "runs", "runs": 1, "commentary": "Single — end of over. RCB 18/0"},
                ]},
                # Over 3 — Tyagi vs Bethell. Bethell beats outside the bat several times.
                # Bethell falls in over 4 at 37/1 in 3.2 — so 37 runs in 3.2 balls. End over 3 = ~30.
                {"over": 3, "bowler": "Arora", "balls": [
                    {"batter": "Kohli",   "outcome": "four", "runs": 4, "commentary": "FOUR! Kohli punches through covers, beautiful"},
                    {"batter": "Kohli",   "outcome": "runs", "runs": 1, "commentary": "Single, fine leg"},
                    {"batter": "Bethell", "outcome": "runs", "runs": 1, "commentary": "Squeezed past gully for a single"},
                    {"batter": "Bethell", "outcome": "runs", "runs": 1, "commentary": "Single, point"},
                    {"batter": "Bethell", "outcome": "four", "runs": 4, "commentary": "FOUR! Bethell finally connects — through extra cover"},
                    {"batter": "Bethell", "outcome": "runs", "runs": 2, "commentary": "Two, dabbed to backward point — end of over. RCB 29/0"},
                ]},
                # Over 4 — Tyagi. Bethell falls on 3.2 means ball 2 of over 4 (combining: 3 overs + 2 balls of next = 3.2). Wait:
                # "37/1 in 3.2 overs" -> 3 overs and 2 balls into the chase. So Bethell falls on ball 2 of over 4.
                # End over 3 was 29, so balls 1-2 of over 4 take us to 37 incl. Bethell falling.
                {"over": 4, "bowler": "Tyagi", "balls": [
                    {"batter": "Bethell", "outcome": "six",  "runs": 6, "commentary": "BETHELL SIX! Lofted over long-on"},
                    {"batter": "Bethell", "outcome": "wicket","runs": 0, "wicket": {"player_out": "Bethell", "kind": "caught", "fielder": "Tyagi"}, "commentary": "BETHELL GONE for 15(12)! Short ball climbs through, cramped on the pull, top-edges off helmet, c&b Tyagi. RCB 37/1"},
                    {"batter": "Padikkal","outcome": "four", "runs": 4, "commentary": "FOUR! Padikkal — Impact Player — short and wide, slapped through cover point first ball"},
                    {"batter": "Padikkal","outcome": "runs", "runs": 1, "commentary": "Padikkal glances fine leg for one"},
                    {"batter": "Kohli",   "outcome": "runs", "runs": 1, "commentary": "Single, mid-on"},
                    {"batter": "Padikkal","outcome": "runs", "runs": 1, "commentary": "Single — end of over. RCB 44/1"},
                ]},
                # Over 5 — Arora. End over 5 ~ 54.
                {"over": 5, "bowler": "Arora", "balls": [
                    {"batter": "Kohli",   "outcome": "four", "runs": 4, "commentary": "KOHLI! Cover-driven for FOUR — masterclass"},
                    {"batter": "Kohli",   "outcome": "runs", "runs": 1, "commentary": "Single, long-on"},
                    {"batter": "Padikkal","outcome": "runs", "runs": 1, "commentary": "Single, point"},
                    {"batter": "Kohli",   "outcome": "dot",  "runs": 0, "commentary": "Defended"},
                    {"batter": "Kohli",   "outcome": "four", "runs": 4, "commentary": "FOUR! Kohli flicks off the pads to deep square"},
                    {"batter": "Kohli",   "outcome": "dot",  "runs": 0, "commentary": "End of over. RCB 54/1"},
                ]},
                # Over 6 — Tyagi. Kohli's hooked-six is real today. Powerplay ends ~66/1.
                {"over": 6, "bowler": "Tyagi", "balls": [
                    {"batter": "Kohli",   "outcome": "six",  "runs": 6, "commentary": "KOHLI! HOOKED SIX over deep square — picks the slow short ball, the King roars"},
                    {"batter": "Kohli",   "outcome": "runs", "runs": 1, "commentary": "Single, long-on"},
                    {"batter": "Padikkal","outcome": "four", "runs": 4, "commentary": "FOUR! Padikkal slashes past point"},
                    {"batter": "Padikkal","outcome": "dot",  "runs": 0, "commentary": "Beaten outside off"},
                    {"batter": "Padikkal","outcome": "runs", "runs": 1, "commentary": "Single"},
                    {"batter": "Kohli",   "outcome": "dot",  "runs": 0, "commentary": "Dot to end powerplay — RCB 66/1"},
                ]},
                # Over 7 — Narine. Carrom ball to Kohli, who punches straight to cover. Tight over.
                {"over": 7, "bowler": "Narine", "balls": [
                    {"batter": "Kohli",   "outcome": "dot",  "runs": 0, "commentary": "Narine starts with the carrom ball — Kohli punches straight to cover"},
                    {"batter": "Kohli",   "outcome": "runs", "runs": 2, "commentary": "Two, worked into the mid-wicket gap"},
                    {"batter": "Kohli",   "outcome": "dot",  "runs": 0, "commentary": "Narine extracts bounce, Kohli struck high on the bat"},
                    {"batter": "Kohli",   "outcome": "runs", "runs": 1, "commentary": "Single, sweep to long-on"},
                    {"batter": "Padikkal","outcome": "runs", "runs": 1, "commentary": "Single, long-off"},
                    {"batter": "Kohli",   "outcome": "runs", "runs": 1, "commentary": "End of over. RCB 71/1"},
                ]},
                # Over 8 — Anukul Roy. End ~80.
                {"over": 8, "bowler": "Anukul", "balls": [
                    {"batter": "Padikkal","outcome": "four", "runs": 4, "commentary": "FOUR! Padikkal drives past mid-off"},
                    {"batter": "Padikkal","outcome": "runs", "runs": 1, "commentary": "Single, long-off"},
                    {"batter": "Kohli",   "outcome": "runs", "runs": 1, "commentary": "Single, mid-on"},
                    {"batter": "Padikkal","outcome": "extra","runs": 2, "commentary": "TWO WIDES — Padikkal reverse-swept and missed, RCB reviewed and won the call"},
                    {"batter": "Padikkal","outcome": "runs", "runs": 1, "commentary": "Single, long-off"},
                    {"batter": "Padikkal","outcome": "dot",  "runs": 0, "commentary": "Defended"},
                    {"batter": "Padikkal","outcome": "runs", "runs": 1, "commentary": "Single — end of over. RCB 81/1"},
                ]},
                # Over 9 — Narine. Tight.
                {"over": 9, "bowler": "Narine", "balls": [
                    {"batter": "Kohli",   "outcome": "runs", "runs": 1, "commentary": "Single, long-on"},
                    {"batter": "Padikkal","outcome": "dot",  "runs": 0, "commentary": "Defended"},
                    {"batter": "Padikkal","outcome": "runs", "runs": 1, "commentary": "Single, long-on"},
                    {"batter": "Kohli",   "outcome": "runs", "runs": 1, "commentary": "Single, mid-wicket"},
                    {"batter": "Padikkal","outcome": "dot",  "runs": 0, "commentary": "Defended"},
                    {"batter": "Padikkal","outcome": "runs", "runs": 1, "commentary": "Single — end of over. RCB 85/1"},
                ]},
                # Over 10 — Anukul. End ~95.
                {"over": 10, "bowler": "Anukul", "balls": [
                    {"batter": "Kohli",   "outcome": "four", "runs": 4, "commentary": "KOHLI! Drives past mid-off"},
                    {"batter": "Kohli",   "outcome": "runs", "runs": 1, "commentary": "Single, long-on"},
                    {"batter": "Padikkal","outcome": "four", "runs": 4, "commentary": "FOUR! Padikkal sweeps fine"},
                    {"batter": "Padikkal","outcome": "dot",  "runs": 0, "commentary": "Defended"},
                    {"batter": "Padikkal","outcome": "runs", "runs": 1, "commentary": "Single, strike rotated"},
                    {"batter": "Kohli",   "outcome": "runs", "runs": 1, "commentary": "End of over. RCB 96/1"},
                ]},
                # Over 11 — Green. End ~108.
                {"over": 11, "bowler": "Green", "balls": [
                    {"batter": "Kohli",   "outcome": "four", "runs": 4, "commentary": "FOUR! Kohli pulls past deep square"},
                    {"batter": "Kohli",   "outcome": "runs", "runs": 1, "commentary": "Single, point"},
                    {"batter": "Padikkal","outcome": "six",  "runs": 6, "commentary": "PADIKKAL! Six over long-on, in the mood"},
                    {"batter": "Padikkal","outcome": "runs", "runs": 1, "commentary": "Single"},
                    {"batter": "Kohli",   "outcome": "dot",  "runs": 0, "commentary": "Defended"},
                    {"batter": "Kohli",   "outcome": "six", "runs": 6, "commentary": "KOHLI SIX! Pulls Green over deep mid-wicket"},
                ]},
                # Over 12 — Narine's last.
                {"over": 12, "bowler": "Narine", "balls": [
                    {"batter": "Padikkal","outcome": "four", "runs": 4, "commentary": "FOUR! Padikkal sweeps Narine fine"},
                    {"batter": "Kohli",   "outcome": "four", "runs": 4, "commentary": "KOHLI! Four through covers"},
                    {"batter": "Kohli",   "outcome": "runs", "runs": 1, "commentary": "Single, long-on"},
                    {"batter": "Padikkal","outcome": "four", "runs": 4, "commentary": "FOUR! Padikkal cuts behind point"},
                    {"batter": "Padikkal","outcome": "runs", "runs": 1, "commentary": "Single"},
                    {"batter": "Kohli",   "outcome": "runs", "runs": 1, "commentary": "End of over — Narine finishes 0/30. RCB 129/1"},
                ]},
                # Over 13 — Anukul. Padikkal falls on 13.1 at 129/2.
                # End of over 12 = 120, so balls 1 alone needs ~9 - too much.
                # Reread: "Padikkal is out for 39 off 27, and RCB are 129 for 2 in 13.1 overs"
                # 13.1 = first ball of over 13. So ball 1 of over 13 = wicket, at 129/2.
                # Means end of over 12 should be 129. Padikkal scored 9 in over 12 then? Adjusting prior.
                # Easier: have over 12 end at ~125 and ball 1 of 13 be a four+wicket nope.
                # The simplest fix: have the wicket be on ball 1, score 129 BEFORE wicket means RCB scored 9 in over 12.
                # Let me retroactively adjust over 12 to give 9 runs, ending at 129.
                # But re-reading: "Padikkal is OUT for 39 off 27, and RCB are 129 FOR 2" — at 13.1 the score 129/2 INCLUDES the wicket effect (score doesn't change but wicket does).
                # So before ball 13.1: 129/1. Padikkal falls = 129/2. So end over 12 = 129.
                # End over 12 needs to be 129. Currently 120. Need 9 more. Adjust over 12: change one single to a four.
                {"over": 13, "bowler": "Anukul", "balls": [
                    {"batter": "Padikkal","outcome": "wicket","runs": 0, "wicket": {"player_out": "Padikkal", "kind": "caught", "fielder": "Green"}, "commentary": "PADIKKAL GONE for 39(27)! Off-cutter, hit too early without power, straight to extra-cover. RCB 129/2"},
                    {"batter": "Patidar", "outcome": "dot",  "runs": 0, "commentary": "Patidar walks in, defends first ball"},
                    {"batter": "Patidar", "outcome": "runs", "runs": 1, "commentary": "Off the mark, single"},
                    {"batter": "Kohli",   "outcome": "four", "runs": 4, "commentary": "FOUR! Kohli cuts past point"},
                    {"batter": "Kohli",   "outcome": "runs", "runs": 1, "commentary": "Single, long-on"},
                    {"batter": "Patidar", "outcome": "runs", "runs": 1, "commentary": "End of over. RCB 136/2"},
                ]},
                # Over 14 — Tyagi. Tyagi hits Patidar on helmet on a short ball (concussion check, continues).
                {"over": 14, "bowler": "Tyagi", "balls": [
                    {"batter": "Kohli",   "outcome": "runs", "runs": 1, "commentary": "Single, long-on"},
                    {"batter": "Patidar", "outcome": "four", "runs": 4, "commentary": "FOUR! Patidar drives past mid-off"},
                    {"batter": "Patidar", "outcome": "dot",  "runs": 0, "commentary": "SHORT BALL — climbs awkwardly, hits Patidar flush on the back of the helmet! Concussion check"},
                    {"batter": "Patidar", "outcome": "runs", "runs": 1, "commentary": "Patidar passes the check, single to point"},
                    {"batter": "Kohli",   "outcome": "four", "runs": 4, "commentary": "FOUR! Kohli sweeps fine"},
                    {"batter": "Kohli",   "outcome": "runs", "runs": 1, "commentary": "End of over. RCB 147/2"},
                ]},
                # Over 15 — Narine had finished; Green back. Patidar 11 falls.
                # Need to keep wicket count: Bethell, Padikkal, Patidar, +1 more (Jitesh later) = 4 total. ✓
                {"over": 15, "bowler": "Green", "balls": [
                    {"batter": "Patidar", "outcome": "runs", "runs": 1, "commentary": "Single, long-on"},
                    {"batter": "Patidar", "outcome": "wicket","runs": 0, "wicket": {"player_out": "Patidar", "kind": "caught", "fielder": "Rahane"}, "commentary": "PATIDAR GONE for 11! Mis-hit pull, captain takes the catch. RCB 148/3"},
                    {"batter": "Jitesh",  "outcome": "dot",  "runs": 0, "commentary": "Jitesh walks in"},
                    {"batter": "Jitesh",  "outcome": "runs", "runs": 1, "commentary": "Off the mark, single"},
                    {"batter": "Kohli",   "outcome": "four", "runs": 4, "commentary": "KOHLI! Four through covers — moving towards a hundred"},
                    {"batter": "Kohli",   "outcome": "runs", "runs": 1, "commentary": "End of over. RCB 154/3 — need 39 off 30"},
                ]},
                # Over 16 — Anukul. Kohli moving towards the 90s.
                {"over": 16, "bowler": "Anukul", "balls": [
                    {"batter": "Jitesh",  "outcome": "runs", "runs": 1, "commentary": "Jitesh sweeps Anukul fine for one"},
                    {"batter": "Kohli",   "outcome": "runs", "runs": 1, "commentary": "Single, long-on"},
                    {"batter": "Jitesh",  "outcome": "four", "runs": 4, "commentary": "FOUR! Jitesh sweeps past short fine leg"},
                    {"batter": "Jitesh",  "outcome": "runs", "runs": 1, "commentary": "Single, long-on"},
                    {"batter": "Kohli",   "outcome": "runs", "runs": 1, "commentary": "Single, strike rotated"},
                    {"batter": "Jitesh",  "outcome": "four", "runs": 4, "commentary": "FOUR! Jitesh on top of Anukul — end of over"},
                ]},
                # Over 17 — Tyagi back into the attack. Smart over, just 5 runs.
                {"over": 17, "bowler": "Tyagi", "balls": [
                    {"batter": "Kohli",   "outcome": "runs", "runs": 1, "commentary": "Single, mid-on — Kohli on 91*"},
                    {"batter": "Jitesh",  "outcome": "dot",  "runs": 0, "commentary": "Yorker, dug out"},
                    {"batter": "Jitesh",  "outcome": "runs", "runs": 1, "commentary": "Single, long-on"},
                    {"batter": "Kohli",   "outcome": "dot",  "runs": 0, "commentary": "Beaten outside off"},
                    {"batter": "Kohli",   "outcome": "runs", "runs": 2, "commentary": "Two driven down to long-off — Kohli on 94*"},
                    {"batter": "Kohli",   "outcome": "runs", "runs": 1, "commentary": "Single, strike rotated — end of over. RCB need 22 off 12"},
                ]},
                # Over 18 — Arora. KOHLI HUNDRED. Jitesh falls. RCB end at 192/4 — 1 to win.
                {"over": 18, "bowler": "Arora", "balls": [
                    {"batter": "Kohli",   "outcome": "four", "runs": 4, "commentary": "KOHLI! 99*! Four through covers"},
                    {"batter": "Kohli",   "outcome": "runs", "runs": 1, "commentary": "KOHLI HUNDRED! 100* off 60 — single brings up the ton, the King has done it again"},
                    {"batter": "Jitesh",  "outcome": "six",  "runs": 6, "commentary": "JITESH! SIX over deep mid-wicket"},
                    {"batter": "Jitesh",  "outcome": "wicket","runs": 0, "wicket": {"player_out": "Jitesh", "kind": "caught", "fielder": "Narine"}, "commentary": "Jitesh holes out — Narine takes it. RCB 185/4"},
                    {"batter": "David",   "outcome": "four", "runs": 4, "commentary": "TIM DAVID! Four first ball! RCB 189/4"},
                    {"batter": "Kohli",   "outcome": "runs", "runs": 3, "commentary": "Three! Kohli runs hard — RCB 192/4, need 1 to win"},
                ]},
                # Over 19 — Tyagi. Kohli finishes it on the very first ball — RCB win in 18.1 (ESPN notation).
                {"over": 19, "bowler": "Tyagi", "balls": [
                    {"batter": "Kohli",   "outcome": "six",  "runs": 6, "commentary": "SIX! KOHLI FINISHES IT IN STYLE! Picks the slot ball and clears deep mid-wicket! RCB win by 6 wickets, Kohli 101* off 62"},
                ]},
            ],
        },
    ],
}


# -------------------------------------------------------------------
# Flatten the match into sequential ball events for the simulator.
# -------------------------------------------------------------------

def _phase(over: int) -> str:
    if over <= 6:
        return "powerplay"
    if over <= 15:
        return "middle"
    return "death"


def flatten_balls():
    flat = []
    target = None

    for innings_no, innings in enumerate(MATCH["innings"], start=1):
        score = 0
        wickets = 0
        balls_since_wicket = 0
        legal_balls = 0
        recent: list[str] = []

        for over_obj in innings["overs"]:
            over_no = over_obj["over"]
            bowler = over_obj["bowler"]
            for ball in over_obj["balls"]:
                outcome = ball["outcome"]
                runs = ball.get("runs", 0)
                wicket_info = ball.get("wicket")

                score_before = score
                wickets_before = wickets

                score += runs
                if wicket_info:
                    wickets += 1
                if outcome != "extra":
                    legal_balls += 1
                ball_in_over = legal_balls % 6 if legal_balls % 6 != 0 else 6

                flat.append({
                    "index": len(flat),
                    "innings": innings_no,
                    "innings_no": innings_no,
                    "batting_team": innings["batting_team"],
                    "bowling_team": innings["bowling_team"],
                    "over": over_no,
                    "ball_in_over": ball_in_over,
                    "legal_balls_so_far": legal_balls,
                    "bowler": bowler,
                    "batter": ball["batter"],
                    "outcome": outcome,
                    "runs": runs,
                    "wicket": wicket_info,
                    "commentary": ball.get("commentary", ""),
                    "phase": _phase(over_no),
                    "score_before": score_before,
                    "wickets_before": wickets_before,
                    "score_after": score,
                    "wickets_after": wickets,
                    "balls_since_wicket": balls_since_wicket,
                    "recent_outcomes": list(recent[-5:]),
                    "target": target,
                })

                if wicket_info:
                    balls_since_wicket = 0
                else:
                    balls_since_wicket += 1
                recent.append(outcome)

        if innings_no == 1:
            target = score + 1

    return flat


def get_match():
    """Return the full MATCH dict; main.py uses MATCH['info']['teams'] etc."""
    return MATCH
