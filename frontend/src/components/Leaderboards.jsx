import React, { useState } from 'react'

export default function Leaderboards({ leaderboards, user, meStats, matchState }) {
  const [tab, setTab] = useState('myteam')

  if (!leaderboards || !user) {
    return (
      <div className="bg-cricket-ink/50 border border-white/5 rounded-2xl p-6 text-center text-white/40 text-sm">
        Loading leaderboards…
      </div>
    )
  }

  const myTeam = user.team
  const myTeamRows = leaderboards.team_top10?.[myTeam] || []
  const globalRows = leaderboards.global_top10 || []
  const agg = leaderboards.team_aggregate || {}
  const teams = matchState?.info?.teams || Object.keys(agg)
  const colors = matchState?.info?.team_colors || {}
  const myTeamShort = matchState?.info?.team_short?.[myTeam] || '??'

  // Team vs Team aggregate widget
  const teamA = teams[0]
  const teamB = teams[1]
  const aggA = agg[teamA] || { avg_points: 0, total_points: 0, player_count: 0 }
  const aggB = agg[teamB] || { avg_points: 0, total_points: 0, player_count: 0 }
  const totalAgg = aggA.avg_points + aggB.avg_points
  const aPct = totalAgg > 0 ? (aggA.avg_points / totalAgg) * 100 : 50
  const aLeading = aggA.avg_points > aggB.avg_points
  const bLeading = aggB.avg_points > aggA.avg_points

  return (
    <div className="space-y-3">
      {/* Team-vs-Team aggregate fan-war bar */}
      <div className="bg-cricket-ink/70 border border-white/5 rounded-2xl p-4">
        <div className="flex items-center justify-between mb-2">
          <div className="text-[10px] uppercase tracking-widest text-white/40">Fan war · avg points per player</div>
          <div className="text-[10px] uppercase tracking-widest text-white/30">{leaderboards.total_players} playing</div>
        </div>
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-2">
            <span className="font-display text-xl" style={{ color: colors[teamA] }}>
              {matchState?.info?.team_short?.[teamA]}
            </span>
            <span className="score-display text-xl tabular-nums text-cricket-chalk">{aggA.avg_points}</span>
            {aLeading && <span className="text-[10px] text-cricket-gold uppercase tracking-wider">leading</span>}
          </div>
          <div className="flex items-center gap-2">
            {bLeading && <span className="text-[10px] text-cricket-gold uppercase tracking-wider">leading</span>}
            <span className="score-display text-xl tabular-nums text-cricket-chalk">{aggB.avg_points}</span>
            <span className="font-display text-xl" style={{ color: colors[teamB] }}>
              {matchState?.info?.team_short?.[teamB]}
            </span>
          </div>
        </div>
        <div className="h-2 rounded-full bg-white/5 overflow-hidden flex">
          <div
            className="h-full transition-all duration-700"
            style={{ width: `${aPct}%`, background: colors[teamA] }}
          />
          <div
            className="h-full transition-all duration-700"
            style={{ width: `${100 - aPct}%`, background: colors[teamB] }}
          />
        </div>
        <div className="flex items-center justify-between text-[10px] text-white/40 mt-1.5">
          <span>{aggA.player_count} fans</span>
          <span>{aggB.player_count} fans</span>
        </div>
      </div>

      {/* Reward tier legend */}
      <div className="bg-gradient-to-br from-cricket-gold/10 to-cricket-blood/10 border border-cricket-gold/20 rounded-2xl p-3">
        <div className="text-[10px] uppercase tracking-widest text-cricket-gold mb-1.5 font-bold">
          Reward tiers (per team)
        </div>
        <div className="grid grid-cols-3 gap-2 text-[11px]">
          <div className="text-center bg-black/30 rounded-lg py-1.5">
            <div className="text-cricket-gold font-bold">TOP 10</div>
            <div className="text-white/60 text-[10px]">Jersey</div>
          </div>
          <div className="text-center bg-black/30 rounded-lg py-1.5">
            <div className="text-orange-300 font-bold">TOP 50</div>
            <div className="text-white/60 text-[10px]">Scarf</div>
          </div>
          <div className="text-center bg-black/30 rounded-lg py-1.5">
            <div className="text-blue-300 font-bold">TOP 100</div>
            <div className="text-white/60 text-[10px]">Badge</div>
          </div>
        </div>
      </div>

      {/* Leaderboard tabs */}
      <div className="bg-cricket-ink/70 border border-white/5 rounded-2xl overflow-hidden">
        <div className="flex border-b border-white/5">
          <button
            onClick={() => setTab('myteam')}
            className={`flex-1 py-2.5 text-[11px] uppercase tracking-widest font-semibold transition relative ${
              tab === 'myteam' ? 'text-cricket-gold' : 'text-white/40 hover:text-white/70'
            }`}
          >
            {myTeamShort} Top 10
            {tab === 'myteam' && (
              <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-cricket-gold" />
            )}
          </button>
          <button
            onClick={() => setTab('global')}
            className={`flex-1 py-2.5 text-[11px] uppercase tracking-widest font-semibold transition relative ${
              tab === 'global' ? 'text-cricket-gold' : 'text-white/40 hover:text-white/70'
            }`}
          >
            Global Top 10
            {tab === 'global' && (
              <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-cricket-gold" />
            )}
          </button>
        </div>

        <div className="divide-y divide-white/5">
          {(tab === 'myteam' ? myTeamRows : globalRows).map((row) => (
            <Row key={row.user_id} row={row} isMe={row.user_id === user.user_id} matchState={matchState} showTeam={tab === 'global'} />
          ))}
          {(tab === 'myteam' ? myTeamRows : globalRows).length === 0 && (
            <div className="py-6 text-center text-white/30 text-xs uppercase tracking-widest">
              No predictions yet — you could be #1
            </div>
          )}
        </div>

        {/* Pinned "your rank" row if user is not in the visible top 10 */}
        {meStats && (() => {
          const rows = tab === 'myteam' ? myTeamRows : globalRows
          const rank = tab === 'myteam' ? meStats.team_rank : meStats.global_rank
          const inList = rows.some(r => r.user_id === user.user_id)
          if (!inList && rank) {
            return (
              <div className="border-t-2 border-cricket-gold/30 bg-cricket-gold/5">
                <div className="px-4 py-3 flex items-center gap-3">
                  <div className="font-mono text-sm tabular-nums text-cricket-gold w-8">#{rank}</div>
                  <div className="flex-1 text-sm text-cricket-chalk font-semibold">You</div>
                  <div className="score-display text-lg text-cricket-gold tabular-nums">{meStats.points}</div>
                </div>
              </div>
            )
          }
          return null
        })()}
      </div>
    </div>
  )
}

function Row({ row, isMe, matchState, showTeam }) {
  const teamColor = matchState?.info?.team_colors?.[row.team] || row.team_short && '#FFB400'
  const isTopThree = row.rank <= 3
  const rankColors = ['', 'text-cricket-gold', 'text-gray-300', 'text-orange-400']

  return (
    <div className={`px-4 py-2.5 flex items-center gap-3 transition ${isMe ? 'bg-cricket-gold/10' : ''}`}>
      <div className={`font-display tabular-nums text-base w-8 ${isTopThree ? rankColors[row.rank] : 'text-white/40'}`}>
        {row.rank <= 3 ? ['🥇', '🥈', '🥉'][row.rank - 1] : `#${row.rank}`}
      </div>
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2">
          <span className={`truncate font-semibold text-sm ${isMe ? 'text-cricket-gold' : 'text-cricket-chalk'}`}>
            {row.display_name}{isMe && ' (you)'}
          </span>
          {showTeam && (
            <span
              className="text-[9px] font-bold px-1.5 py-0.5 rounded uppercase tracking-wider flex-shrink-0"
              style={{ background: `${teamColor}30`, color: teamColor }}
            >
              {row.team_short}
            </span>
          )}
          {row.streak >= 2 && (
            <span className="text-[10px] text-cricket-gold flex-shrink-0">🔥{row.streak}</span>
          )}
        </div>
      </div>
      <div className="score-display tabular-nums text-base text-cricket-chalk">
        {row.points}
      </div>
    </div>
  )
}
