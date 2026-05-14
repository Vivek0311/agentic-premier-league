import React from 'react'

const KIND_STYLES = {
  big_hit: 'text-cricket-gold',
  combo:   'text-cyan-300 font-bold',
  wicket:  'text-cricket-blood font-bold',
  six:     'text-yellow-300',
}

export default function Ticker({ items }) {
  if (!items || items.length === 0) {
    return null
  }

  const recent = items.slice(-5)

  return (
    <div className="relative bg-black/40 border border-white/5 rounded-full overflow-hidden h-9 flex items-center">
      <div className="absolute left-0 top-0 bottom-0 w-12 bg-gradient-to-r from-cricket-night to-transparent pointer-events-none z-10" />
      <div className="absolute right-0 top-0 bottom-0 w-12 bg-gradient-to-l from-cricket-night to-transparent pointer-events-none z-10" />
      <div className="absolute left-2 z-20">
        <div className="bg-cricket-blood text-white text-[9px] font-bold uppercase tracking-widest px-2 py-0.5 rounded-full">
          LIVE
        </div>
      </div>
      <div className="ticker-track whitespace-nowrap pl-20 pr-8 text-xs">
        {recent.map((m, i) => (
          <span key={i} className={`mx-6 ${KIND_STYLES[m.kind] || 'text-white/70'}`}>
            {m.text}
          </span>
        ))}
        {/* Duplicate for continuous loop feel */}
        {recent.map((m, i) => (
          <span key={`dup-${i}`} className={`mx-6 ${KIND_STYLES[m.kind] || 'text-white/70'}`}>
            {m.text}
          </span>
        ))}
      </div>
    </div>
  )
}
