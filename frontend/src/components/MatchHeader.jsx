import React from 'react'

export default function MatchHeader({ matchState, user }) {
  if (!matchState || !matchState.info) {
    return (
      <div className="bg-cricket-ink/60 border border-white/5 rounded-2xl p-5 text-center">
        <div className="text-white/40 text-sm">Connecting to the match…</div>
      </div>
    )
  }

  const { info, current_ball, innings_totals, target, status } = matchState
  const teams = info.teams
  const colors = info.team_colors
  const shorts = info.team_short

  // Determine batting team and order display
  const battingTeam = current_ball?.batting_team || teams[0]
  const battingShort = shorts[battingTeam]
  const battingColor = colors[battingTeam]

  const bowlingTeam = current_ball?.bowling_team || teams[1]
  const bowlingShort = shorts[bowlingTeam]
  const bowlingColor = colors[bowlingTeam]

  const innings1 = innings_totals?.['1']
  const innings2 = innings_totals?.['2']
  const currentInnings = current_ball?.innings || 1

  const isMatchEnd = status === 'ended'

  return (
    <div className="bg-cricket-ink/70 border border-white/5 rounded-2xl overflow-hidden">
      {/* Header strip */}
      <div className="flex items-stretch">
        {/* Team A side */}
        <div className="flex-1 p-3.5 relative overflow-hidden">
          <div className="absolute inset-0 opacity-15" style={{ background: colors[teams[0]] }} />
          <div className="relative z-10">
            <div className="font-display text-2xl leading-none" style={{ color: colors[teams[0]] }}>
              {shorts[teams[0]]}
            </div>
            <div className="text-white/50 text-[10px] uppercase tracking-widest mt-1">
              {innings1 ? (battingTeam === teams[0] && currentInnings === 1 ? 'BATTING' : 'INNINGS 1') : '—'}
            </div>
            <div className="score-display text-3xl mt-1 font-bold tabular-nums">
              {innings1 ? `${innings1.score}` : '—'}
              {innings1 && <span className="text-white/40 text-xl">/{innings1.wickets}</span>}
            </div>
          </div>
        </div>

        {/* Center divider with VS or live ball */}
        <div className="flex flex-col items-center justify-center px-3 py-2 border-x border-white/5">
          {current_ball ? (
            <>
              <div className="text-[10px] text-white/40 uppercase tracking-widest">Over</div>
              <div className="font-display text-2xl text-cricket-gold tabular-nums">
                {current_ball.over - 1}.{current_ball.ball_in_over}
              </div>
            </>
          ) : (
            <div className="font-display text-cricket-blood text-3xl">VS</div>
          )}
        </div>

        {/* Team B side */}
        <div className="flex-1 p-3.5 relative overflow-hidden text-right">
          <div className="absolute inset-0 opacity-15" style={{ background: colors[teams[1]] }} />
          <div className="relative z-10">
            <div className="font-display text-2xl leading-none" style={{ color: colors[teams[1]] }}>
              {shorts[teams[1]]}
            </div>
            <div className="text-white/50 text-[10px] uppercase tracking-widest mt-1">
              {currentInnings === 2 && battingTeam === teams[1] ? 'CHASING' : innings2 ? 'INNINGS 2' : '—'}
            </div>
            <div className="score-display text-3xl mt-1 font-bold tabular-nums">
              {innings2 && innings2.score > 0 ? `${innings2.score}` : (innings2 && currentInnings === 2 ? '0' : '—')}
              {innings2 && (innings2.score > 0 || currentInnings === 2) && <span className="text-white/40 text-xl">/{innings2.wickets}</span>}
            </div>
          </div>
        </div>
      </div>

      {/* Bottom strip — current ball detail */}
      {current_ball && !isMatchEnd && (
        <div className="bg-black/30 border-t border-white/5 px-4 py-2.5">
          <div className="flex items-center justify-between text-xs">
            <div className="flex items-center gap-2">
              <span className="text-white/40">BAT</span>
              <span className="font-semibold tracking-wide text-cricket-chalk">{current_ball.batter}</span>
            </div>
            <div className="text-white/30 text-[10px]">·</div>
            <div className="flex items-center gap-2">
              <span className="text-white/40">BWL</span>
              <span className="font-semibold tracking-wide text-cricket-chalk">{current_ball.bowler}</span>
            </div>
          </div>
          {target && currentInnings === 2 && innings2 && (
            <div className="mt-1.5 text-center text-[11px]">
              <span className="text-white/40">NEED </span>
              <span className="text-cricket-gold font-mono font-semibold">{Math.max(0, target - innings2.score)}</span>
              <span className="text-white/40"> TO WIN</span>
            </div>
          )}
        </div>
      )}

      {isMatchEnd && (
        <div className="bg-cricket-gold/10 border-t border-cricket-gold/30 px-4 py-3 text-center">
          <div className="font-display text-cricket-gold text-2xl tracking-wider">MATCH OVER</div>
        </div>
      )}
    </div>
  )
}
