import React, { useEffect, useState } from 'react'

export default function ResultBanner({ resolution }) {
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    if (resolution) {
      setVisible(true)
      const t = setTimeout(() => setVisible(false), 3500)
      return () => clearTimeout(t)
    }
  }, [resolution])

  if (!resolution || !visible) return null

  const { correct, points, combo_name, combo_multiplier, streak_multiplier, captains_call, predicted, actual, streak } = resolution

  const labels = { dot: 'DOT', runs: '1-3', four: 'FOUR', six: 'SIX', wicket: 'WICKET', extra: 'EXTRA' }

  if (correct) {
    return (
      <div className="result-correct rounded-2xl border-2 border-green-400/60 bg-gradient-to-br from-green-500/20 to-green-700/10 p-4 animate-fade-up">
        <div className="flex items-center justify-between">
          <div>
            <div className="text-green-300 text-xs uppercase tracking-widest">Correct!</div>
            <div className="font-display text-4xl text-cricket-chalk leading-none mt-0.5">
              +{points}
            </div>
            <div className="text-white/60 text-xs mt-1">
              You called <span className="font-bold">{labels[predicted]}</span>
              {streak >= 2 && <span className="ml-2 text-cricket-gold">🔥 {streak}-streak</span>}
            </div>
          </div>
          <div className="text-right space-y-0.5">
            {combo_multiplier > 1 && combo_name && (
              <div className="text-xs text-cricket-gold uppercase tracking-wider">
                COMBO {combo_name} · {combo_multiplier}×
              </div>
            )}
            {streak_multiplier > 1 && (
              <div className="text-xs text-orange-300 uppercase tracking-wider">
                Streak × {streak_multiplier}
              </div>
            )}
            {captains_call && (
              <div className="text-xs text-cricket-gold uppercase tracking-wider font-bold">
                ⚡ Captain's Call 5×
              </div>
            )}
          </div>
        </div>
      </div>
    )
  } else {
    return (
      <div className="result-wrong rounded-2xl border-2 border-cricket-blood/40 bg-cricket-blood/10 p-4 animate-fade-up">
        <div className="flex items-center justify-between">
          <div>
            <div className="text-cricket-blood text-xs uppercase tracking-widest">Wrong call</div>
            <div className="text-white/70 text-sm mt-1">
              You said <span className="font-bold">{labels[predicted]}</span>, actual was <span className="font-bold text-cricket-chalk">{labels[actual]}</span>
            </div>
          </div>
          <div className="font-display text-3xl text-cricket-blood/70">—</div>
        </div>
      </div>
    )
  }
}
