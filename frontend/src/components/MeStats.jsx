import React from 'react'

export default function MeStats({ me, matchState }) {
  if (!me) {
    return (
      <div className="bg-cricket-ink/50 border border-white/5 rounded-2xl p-4 animate-pulse">
        <div className="h-3 bg-white/10 rounded w-1/3 mb-2"></div>
        <div className="h-8 bg-white/10 rounded w-1/2"></div>
      </div>
    )
  }

  const accuracy = me.total > 0 ? Math.round(me.accuracy * 100) : 0
  const teamColor = matchState?.info?.team_colors?.[me.team] || '#FFB400'
  const teamShort = matchState?.info?.team_short?.[me.team] || '??'

  return (
    <div className="bg-cricket-ink/70 border border-white/5 rounded-2xl p-4 relative overflow-hidden">
      {/* Accent strip in team color */}
      <div className="absolute left-0 top-0 bottom-0 w-1" style={{ background: teamColor }} />

      <div className="flex items-center justify-between mb-3">
        <div>
          <div className="text-[10px] uppercase tracking-widest text-white/40">Playing as</div>
          <div className="flex items-center gap-2 mt-0.5">
            <span className="font-semibold text-cricket-chalk">{me.display_name}</span>
            <span
              className="text-[10px] font-bold px-1.5 py-0.5 rounded uppercase tracking-wider"
              style={{ background: `${teamColor}30`, color: teamColor }}
            >
              {teamShort}
            </span>
          </div>
        </div>
        {me.streak >= 2 && (
          <div className="bg-cricket-gold/15 border border-cricket-gold/40 rounded-full px-3 py-1 flex items-center gap-1">
            <span className="text-cricket-gold text-sm">🔥</span>
            <span className="font-bold text-cricket-gold text-sm tabular-nums">{me.streak}</span>
          </div>
        )}
      </div>

      <div className="grid grid-cols-4 gap-2 mt-3">
        <Stat label="Points" value={me.points} highlight />
        <Stat label="Rank" value={me.global_rank ? `#${me.global_rank}` : '—'} />
        <Stat label={`${teamShort} Rank`} value={me.team_rank ? `#${me.team_rank}` : '—'} />
        <Stat label="Accuracy" value={`${accuracy}%`} />
      </div>

      {me.badges && me.badges.length > 0 && (
        <div className="mt-3 flex flex-wrap gap-1.5">
          {me.badges.map((b, i) => (
            <span key={i} className="text-[10px] uppercase tracking-wider bg-white/5 border border-white/10 rounded px-2 py-0.5 text-cricket-gold">
              {b}
            </span>
          ))}
        </div>
      )}

      {me.power_ups && (me.power_ups.double_down > 0 || me.power_ups.insurance > 0) && (
        <div className="mt-3 pt-3 border-t border-white/5 flex items-center gap-3 text-[11px]">
          <span className="text-white/40 uppercase tracking-wider">Power-ups:</span>
          {me.power_ups.double_down > 0 && (
            <span className="text-cyan-300">× {me.power_ups.double_down} Double Down</span>
          )}
        </div>
      )}
    </div>
  )
}

function Stat({ label, value, highlight }) {
  return (
    <div>
      <div className="text-[9px] uppercase tracking-widest text-white/40 leading-tight">{label}</div>
      <div className={`mt-0.5 score-display tabular-nums leading-none ${highlight ? 'text-cricket-gold text-2xl' : 'text-cricket-chalk text-xl'}`}>
        {value}
      </div>
    </div>
  )
}
