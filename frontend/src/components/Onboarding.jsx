import React, { useEffect, useState } from 'react'

const TEAMS = [
  { name: 'Royal Challengers Bengaluru', short: 'RCB', color: '#EC1C24', textColor: '#fff', accent: 'Ee Sala Cup Namde' },
  { name: 'Kolkata Knight Riders',       short: 'KKR', color: '#3A225D', textColor: '#FFD700', accent: 'Korbo Lorbo Jeetbo' },
]

export default function Onboarding({ onJoin }) {
  const [name, setName] = useState('')
  const [selected, setSelected] = useState(null)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')
  const [stage, setStage] = useState(0)  // 0 = team, 1 = name

  // Stage 0 = team picker; advance to stage 1 once picked
  const pickTeam = (team) => {
    setSelected(team)
    setTimeout(() => setStage(1), 350)
  }

  const submit = async () => {
    setError('')
    if (!name.trim()) { setError('A name to go on the leaderboard'); return }
    if (!selected) { setError('Pick a team first'); return }
    setSubmitting(true)
    try {
      await onJoin(name.trim(), selected.name)
    } catch (e) {
      setError(String(e.message || e))
      setSubmitting(false)
    }
  }

  return (
    <div className="relative min-h-screen flex flex-col" style={{ zIndex: 2 }}>
      {/* Background spotlights */}
      {selected && (
        <div
          className="absolute inset-0 transition-opacity duration-700 pointer-events-none"
          style={{
            background: `radial-gradient(ellipse at center top, ${selected.color}33 0%, transparent 50%)`,
          }}
        />
      )}

      {/* Top brand */}
      <div className="pt-12 px-6 text-center relative z-10">
        <div className="inline-flex items-center gap-3 mb-2">
          <div className="w-9 h-9 rounded-full bg-cricket-blood relative overflow-hidden">
            <div className="absolute inset-0 seam-line opacity-50"></div>
          </div>
          <span className="font-display text-3xl tracking-wider">IPL PULSE</span>
        </div>
        <div className="text-[11px] uppercase tracking-[0.3em] text-white/50">Live prediction · ball by ball</div>
      </div>

      {/* Stage 0: team picker */}
      {stage === 0 && (
        <div className="flex-1 flex flex-col justify-center px-6 relative z-10 animate-fade-up">
          <div className="text-center mb-8">
            <div className="font-display text-4xl mb-2">PICK YOUR SIDE</div>
            <div className="text-white/60 text-sm">Defend your team. Top the leaderboard. Win the swag.</div>
          </div>

          <div className="space-y-3">
            {TEAMS.map((t) => (
              <button
                key={t.short}
                onClick={() => pickTeam(t)}
                className={`w-full relative overflow-hidden rounded-2xl p-5 border-2 transition-all tile-press ${selected?.short === t.short ? 'border-cricket-gold' : 'border-white/10 hover:border-white/30'}`}
                style={{ background: `linear-gradient(135deg, ${t.color}E6 0%, ${t.color}80 100%)` }}
              >
                <div className="flex items-center justify-between relative z-10">
                  <div className="text-left">
                    <div className="font-display text-5xl tracking-wider" style={{ color: t.textColor }}>
                      {t.short}
                    </div>
                    <div className="text-sm font-semibold opacity-80" style={{ color: t.textColor }}>
                      {t.name}
                    </div>
                    <div className="text-xs italic mt-1 opacity-60" style={{ color: t.textColor }}>
                      "{t.accent}"
                    </div>
                  </div>
                  <div className="w-12 h-12 rounded-full flex items-center justify-center" style={{ background: t.textColor, color: t.color }}>
                    <span className="font-display text-2xl">→</span>
                  </div>
                </div>
                {/* Diagonal accent stripe */}
                <div
                  className="absolute -right-8 -top-8 w-32 h-32 rounded-full opacity-20"
                  style={{ background: t.textColor }}
                />
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Stage 1: name */}
      {stage === 1 && selected && (
        <div className="flex-1 flex flex-col justify-center px-6 relative z-10 animate-fade-up">
          {/* Selected team badge */}
          <div className="text-center mb-8">
            <div
              className="inline-block rounded-2xl px-6 py-4"
              style={{ background: `${selected.color}20`, border: `1px solid ${selected.color}80` }}
            >
              <div className="text-[10px] uppercase tracking-widest text-white/50 mb-1">Riding with</div>
              <div className="font-display text-4xl" style={{ color: selected.color }}>{selected.short}</div>
            </div>
          </div>

          <div className="text-center mb-6">
            <div className="font-display text-3xl mb-1">YOUR NAME</div>
            <div className="text-white/60 text-xs">This is how you'll appear on the leaderboard</div>
          </div>

          <div className="relative mb-4">
            <input
              autoFocus
              value={name}
              onChange={(e) => setName(e.target.value)}
              maxLength={24}
              placeholder="e.g. SuperKing07"
              onKeyDown={(e) => { if (e.key === 'Enter') submit() }}
              className="w-full bg-white/5 border-2 border-white/10 focus:border-cricket-gold rounded-xl px-5 py-4 text-lg font-mono text-cricket-chalk placeholder:text-white/30 outline-none transition"
            />
            <div className="absolute right-4 top-1/2 -translate-y-1/2 text-[10px] text-white/30 font-mono">
              {name.length}/24
            </div>
          </div>

          {error && (
            <div className="text-cricket-blood text-xs mb-3 text-center animate-shake">{error}</div>
          )}

          <button
            onClick={submit}
            disabled={submitting}
            className="w-full bg-cricket-gold text-cricket-night font-display text-2xl tracking-widest py-4 rounded-xl tile-press disabled:opacity-50 hover:bg-yellow-300 transition"
          >
            {submitting ? 'JOINING…' : 'ENTER THE MATCH'}
          </button>

          <button
            onClick={() => { setStage(0); setSelected(null); }}
            className="w-full mt-3 text-white/40 hover:text-white/70 text-xs uppercase tracking-widest py-2 transition"
          >
            ← Change team
          </button>
        </div>
      )}

      {/* Bottom note */}
      <div className="pb-6 px-6 text-center text-[10px] uppercase tracking-widest text-white/30 relative z-10">
        Top 10 of your team wins exclusive team swag
      </div>
    </div>
  )
}
