import React, { useEffect, useState, useRef } from 'react'
import Onboarding from './components/Onboarding'
import MatchHeader from './components/MatchHeader'
import PredictionCard from './components/PredictionCard'
import MeStats from './components/MeStats'
import Leaderboards from './components/Leaderboards'
import Ticker from './components/Ticker'
import ResultBanner from './components/ResultBanner'

const STORAGE_KEY = 'ipl-pulse-user'

export default function App() {
  const [user, setUser] = useState(null)
  const [matchState, setMatchState] = useState(null)
  const [leaderboards, setLeaderboards] = useState(null)
  const [ticker, setTicker] = useState([])
  const [lastResolution, setLastResolution] = useState(null)
  const [meStats, setMeStats] = useState(null)
  const [captainsCallNext, setCaptainsCallNext] = useState(false)
  const [connectionState, setConnectionState] = useState('connecting')
  const esRef = useRef(null)

  // Restore user on mount
  useEffect(() => {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (stored) {
      try { setUser(JSON.parse(stored)) } catch { localStorage.removeItem(STORAGE_KEY) }
    }
  }, [])

  // Open SSE stream when user is set
  useEffect(() => {
    if (!user) return

    const es = new EventSource('/api/stream')
    esRef.current = es

    es.onopen = () => setConnectionState('connected')
    es.onerror = () => setConnectionState('reconnecting')

    es.onmessage = (e) => {
      const event = JSON.parse(e.data)

      if (event.type === 'snapshot' || event.type === 'match_start' || event.type === 'ball' || event.type === 'match_end') {
        if (event.state) setMatchState(event.state)
        if (event.final_state) setMatchState(event.final_state)
        if (event.leaderboards) setLeaderboards(event.leaderboards)
        if (event.ticker) setTicker(event.ticker)
        if ('captains_call_next' in event) setCaptainsCallNext(event.captains_call_next)
        if ('captains_call' in event) setCaptainsCallNext(event.captains_call)
      }

      // Look for our user's resolution
      if (event.type === 'ball' && event.resolutions && event.resolutions[user.user_id]) {
        setLastResolution(event.resolutions[user.user_id])
        // Refresh me stats
        refreshMe()
        // Clear after a few seconds
        setTimeout(() => setLastResolution(null), 4000)
      }
    }

    return () => es.close()
  }, [user])

  const refreshMe = async () => {
    if (!user) return
    try {
      const r = await fetch(`/api/me/${user.user_id}`)
      if (r.ok) setMeStats(await r.json())
    } catch {}
  }

  useEffect(() => { refreshMe() }, [user])

  const handleJoin = async (display_name, team) => {
    const r = await fetch('/api/join', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ display_name, team }),
    })
    if (!r.ok) throw new Error(await r.text())
    const data = await r.json()
    setUser(data)
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data))
  }

  const handleLogout = () => {
    localStorage.removeItem(STORAGE_KEY)
    setUser(null)
    setMatchState(null)
    setLeaderboards(null)
    if (esRef.current) esRef.current.close()
  }

  const handlePredict = async (outcome) => {
    if (!user) return { ok: false, error: 'no user' }
    try {
      const r = await fetch('/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: user.user_id, outcome }),
      })
      if (r.ok) return { ok: true }
      const err = await r.json().catch(() => ({}))
      return { ok: false, error: err.detail || 'failed' }
    } catch (e) {
      return { ok: false, error: 'network' }
    }
  }

  if (!user) return <Onboarding onJoin={handleJoin} />

  return (
    <div className="relative min-h-screen text-cricket-chalk pb-8" style={{ zIndex: 2 }}>
      {/* Top app bar */}
      <header className="sticky top-0 z-30 backdrop-blur-md bg-cricket-night/85 border-b border-white/5">
        <div className="max-w-md mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-full bg-cricket-blood relative overflow-hidden flex-shrink-0">
              <div className="absolute inset-0 seam-line opacity-40"></div>
            </div>
            <div className="leading-none">
              <div className="font-display text-lg tracking-wider">IPL PULSE</div>
              <div className="text-[10px] text-white/40 uppercase tracking-widest">Predict every ball</div>
            </div>
          </div>
          <button
            onClick={handleLogout}
            className="text-[11px] uppercase tracking-wider text-white/40 hover:text-white/80 px-2 py-1 transition"
            title="Sign out"
          >
            Exit
          </button>
        </div>
      </header>

      <main className="max-w-md mx-auto px-4 pt-3 space-y-4">
        {/* Connection state */}
        {connectionState !== 'connected' && (
          <div className="text-[11px] text-cricket-gold/80 text-center uppercase tracking-widest">
            ● {connectionState}
          </div>
        )}

        {/* Match header — score, batter, bowler */}
        <MatchHeader matchState={matchState} user={user} />

        {/* Ticker for live moments */}
        <Ticker items={ticker} />

        {/* The big prediction card with timer */}
        <PredictionCard
          matchState={matchState}
          onPredict={handlePredict}
          captainsCall={captainsCallNext}
          lastResolution={lastResolution}
        />

        {/* Result banner (overlay-style, slides in after a ball) */}
        <ResultBanner resolution={lastResolution} />

        {/* My personal stats */}
        <MeStats me={meStats} matchState={matchState} />

        {/* Leaderboards: team vs team agg + global + team top 10 */}
        <Leaderboards leaderboards={leaderboards} user={user} meStats={meStats} matchState={matchState} />

        {/* Footer */}
        <div className="text-center text-[10px] text-white/30 uppercase tracking-widest pt-4 pb-2">
          {matchState?.info?.venue || ''}
        </div>
      </main>
    </div>
  )
}
