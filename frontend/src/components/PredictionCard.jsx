import React, { useEffect, useMemo, useRef, useState } from 'react'

const OUTCOMES = [
  { key: 'dot',    label: 'DOT',    sub: '0',     accent: '#94A3B8' },
  { key: 'runs',   label: '1-3',    sub: 'RUNS',  accent: '#60A5FA' },
  { key: 'four',   label: '4',      sub: 'FOUR',  accent: '#22D3EE' },
  { key: 'six',    label: '6',      sub: 'SIX',   accent: '#FBBF24' },
  { key: 'wicket', label: 'W',      sub: 'WKT',   accent: '#EF4444' },
  { key: 'extra',  label: 'EX',     sub: 'EXTRA', accent: '#A78BFA' },
]

export default function PredictionCard({ matchState, onPredict, captainsCall, lastResolution }) {
  const [selected, setSelected] = useState(null)
  const [locked, setLocked] = useState(false)
  const [error, setError] = useState('')
  const [progress, setProgress] = useState(0)
  const [windowOpen, setWindowOpen] = useState(false)
  const submitRef = useRef(false)

  const nextBallAt = matchState?.next_ball_at_unix
  const status = matchState?.status

  // Timer: progress goes 0→100 over the window between balls.
  // Window opens after a ball is delivered, closes ~1.5s before the next ball.
  useEffect(() => {
    if (status !== 'live' || !nextBallAt) return

    // We don't have the exact "last_ball_at", but we know:
    //   - Total interval between balls = BALL_INTERVAL (e.g. 6s)
    //   - Window closes ~1.5s before next ball (PREDICTION_WINDOW < BALL_INTERVAL)
    // We approximate: window opens immediately after a ball, closes when timeLeft < 1.5s.

    let raf
    const tick = () => {
      const now = Date.now() / 1000
      const timeLeft = nextBallAt - now
      const WINDOW_CLOSES_BEFORE = 1.5  // matches server PREDICTION_WINDOW_SECS approx
      if (timeLeft > WINDOW_CLOSES_BEFORE) {
        setWindowOpen(true)
        // progress: 0 right after ball, 100 when window is about to close
        // assume total window is ~5s for visual purposes
        const assumedTotal = 5
        const elapsed = assumedTotal - (timeLeft - WINDOW_CLOSES_BEFORE)
        setProgress(Math.min(100, Math.max(0, (elapsed / assumedTotal) * 100)))
      } else {
        setWindowOpen(false)
        setProgress(100)
      }
      raf = requestAnimationFrame(tick)
    }
    raf = requestAnimationFrame(tick)
    return () => cancelAnimationFrame(raf)
  }, [nextBallAt, status])

  // Reset selection when a new ball arrives
  useEffect(() => {
    if (matchState?.current_ball) {
      setSelected(null)
      setLocked(false)
      submitRef.current = false
      setError('')
    }
  }, [matchState?.current_ball?.index])

  const handleSelect = async (outcomeKey) => {
    if (locked || !windowOpen || submitRef.current) return
    submitRef.current = true
    setSelected(outcomeKey)
    setError('')
    const result = await onPredict(outcomeKey)
    if (result.ok) {
      setLocked(true)
    } else {
      setError(result.error)
      setSelected(null)
      submitRef.current = false
    }
  }

  const isMatchEnd = status === 'ended'
  const showResult = lastResolution && Date.now() / 1000 - (lastResolution._at || 0) < 4

  return (
    <div className={`relative rounded-2xl border ${captainsCall ? 'captains-call-glow border-cricket-gold' : 'border-white/10 bg-cricket-ink/70'} overflow-hidden`}>
      {/* Captain's Call banner */}
      {captainsCall && (
        <div className="bg-cricket-gold text-cricket-night text-center py-2 px-3 font-display tracking-widest text-sm">
          ⚡ CAPTAIN'S CALL · 5× POINTS ⚡
        </div>
      )}

      <div className="p-4">
        {/* Status line and timer */}
        <div className="flex items-center justify-between mb-3">
          <div className="text-[11px] uppercase tracking-widest text-white/50">
            {isMatchEnd ? 'Match Ended' :
              !windowOpen ? 'Ball incoming…' :
              locked ? 'Locked in' : 'Predict the next ball'}
          </div>
          {!isMatchEnd && (
            <div className="relative w-8 h-8">
              <div
                className="timer-ring rounded-full w-full h-full"
                style={{ '--progress': progress }}
              />
              <div className="absolute inset-1 rounded-full bg-cricket-ink flex items-center justify-center">
                {nextBallAt && windowOpen && (
                  <span className="text-[10px] font-mono text-cricket-gold tabular-nums">
                    {Math.max(0, Math.ceil(nextBallAt - Date.now() / 1000 - 1.5))}
                  </span>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Tile grid */}
        <div className="grid grid-cols-3 gap-2.5">
          {OUTCOMES.map((o) => {
            const isSelected = selected === o.key
            const isDisabled = locked || !windowOpen || isMatchEnd

            return (
              <button
                key={o.key}
                onClick={() => handleSelect(o.key)}
                disabled={isDisabled}
                className={`tile-press relative rounded-xl border-2 py-5 px-2 transition ${
                  isSelected ? 'tile-glow-active' : 'border-white/10'
                } ${isDisabled && !isSelected ? 'opacity-30' : ''} ${isDisabled ? 'cursor-not-allowed' : ''}`}
                style={{
                  background: isSelected
                    ? `linear-gradient(180deg, ${o.accent}40 0%, ${o.accent}20 100%)`
                    : `${o.accent}10`,
                  borderColor: isSelected ? '#FFB400' : `${o.accent}40`,
                }}
              >
                <div className="font-display text-3xl leading-none" style={{ color: o.accent }}>
                  {o.label}
                </div>
                <div className="text-[10px] uppercase tracking-widest text-white/60 mt-1">
                  {o.sub}
                </div>
                {isSelected && locked && (
                  <div className="absolute top-1 right-2 text-[10px] text-cricket-gold">✓</div>
                )}
              </button>
            )
          })}
        </div>

        {error && (
          <div className="text-cricket-blood text-xs mt-3 text-center animate-shake">{error}</div>
        )}

        {locked && !showResult && (
          <div className="text-cricket-gold/80 text-xs mt-3 text-center uppercase tracking-widest animate-fade-up">
            Locked · waiting for the ball
          </div>
        )}

        {!locked && windowOpen && !isMatchEnd && (
          <div className="text-white/30 text-[10px] mt-3 text-center uppercase tracking-widest">
            Tap a tile to lock in your call
          </div>
        )}
      </div>
    </div>
  )
}
