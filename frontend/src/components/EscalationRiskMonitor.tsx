import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { AlertTriangle, TrendingUp, MessageSquare, AlertCircle, Clock } from 'lucide-react'

interface EscalationAlert {
  id: string
  complaint_id: string
  ward: string
  issue_type: string
  risk_level: 'low' | 'medium' | 'high' | 'critical'
  escalation_probability: number
  days_until_escalation: number
  social_mentions: number
  news_coverage: boolean
  sentiment: 'negative' | 'neutral' | 'positive'
}

const riskColorMap = {
  low: { bg: 'bg-emerald-500/10', border: 'border-emerald-500/30', text: 'text-emerald-300', badge: 'bg-emerald-500/20' },
  medium: { bg: 'bg-yellow-500/10', border: 'border-yellow-500/30', text: 'text-yellow-300', badge: 'bg-yellow-500/20' },
  high: { bg: 'bg-orange-500/10', border: 'border-orange-500/30', text: 'text-orange-300', badge: 'bg-orange-500/20' },
  critical: { bg: 'bg-red-500/10', border: 'border-red-500/30', text: 'text-red-300', badge: 'bg-red-500/20' }
}

export function EscalationRiskMonitor() {
  const [alerts, setAlerts] = useState<EscalationAlert[]>([])
  const [loading, setLoading] = useState(true)
  const [expandedAlert, setExpandedAlert] = useState<string | null>(null)

  useEffect(() => {
    const fetchEscalationData = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/ai/escalation-risks')
        const data = await response.json()
        setAlerts(data.risks || [])
      } catch (error) {
        console.error('Error fetching escalation data:', error)
        // Fallback to default data
        setAlerts([
          {
            id: '1',
            complaint_id: 'COMP-2025-0451',
            ward: 'Ward 5',
            issue_type: 'Drainage Overflow',
            risk_level: 'critical',
            escalation_probability: 0.92,
            days_until_escalation: 2,
            social_mentions: 247,
            news_coverage: true,
            sentiment: 'negative'
          },
          {
            id: '2',
            complaint_id: 'COMP-2025-0412',
            ward: 'Ward 12',
            issue_type: 'Road Collapse',
            risk_level: 'high',
            escalation_probability: 0.78,
            days_until_escalation: 5,
            social_mentions: 89,
            news_coverage: false,
            sentiment: 'negative'
          },
          {
            id: '3',
            complaint_id: 'COMP-2025-0389',
            ward: 'Ward 3',
            issue_type: 'Water Contamination',
            risk_level: 'high',
            escalation_probability: 0.65,
            days_until_escalation: 7,
            social_mentions: 34,
            news_coverage: false,
            sentiment: 'negative'
          }
        ])
      } finally {
        setLoading(false)
      }
    }

    fetchEscalationData()
  }, [])

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-xl font-bold text-white mb-1">Escalation Risk Monitor</h3>
          <p className="text-sm text-grey-400">AI-powered escalation prediction and tracking</p>
        </div>
        <motion.div
          className="flex items-center gap-2 px-4 py-2 rounded-lg bg-red-500/10 border border-red-500/30"
          animate={{ scale: [1, 1.05, 1] }}
          transition={{ duration: 2, repeat: Infinity }}
        >
          <AlertTriangle className="w-4 h-4 text-red-300" />
          <span className="text-sm font-semibold text-red-300">{alerts.filter(a => a.risk_level === 'critical').length} Critical</span>
        </motion.div>
      </div>

      <AnimatePresence>
        {alerts.map((alert, idx) => {
          const colors = riskColorMap[alert.risk_level]
          const isExpanded = expandedAlert === alert.id

          return (
            <motion.div
              key={alert.id}
              layout
              className={`border rounded-lg p-4 backdrop-blur-xl cursor-pointer transition-all ${colors.bg} ${colors.border}`}
              onClick={() => setExpandedAlert(isExpanded ? null : alert.id)}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: idx * 0.1 }}
            >
              {/* Header */}
              <div className="flex items-start justify-between">
                <div className="flex items-start gap-3 flex-1">
                  <motion.div
                    animate={{ rotate: alert.risk_level === 'critical' ? [0, 15, -15, 0] : 0 }}
                    transition={{ duration: 2, repeat: alert.risk_level === 'critical' ? Infinity : 0 }}
                  >
                    <AlertCircle className={`w-5 h-5 ${colors.text}`} />
                  </motion.div>

                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <h4 className={`font-semibold ${colors.text}`}>{alert.ward}</h4>
                      <span className={`px-2 py-1 rounded text-xs font-bold ${colors.badge} ${colors.text}`}>
                        {alert.risk_level.toUpperCase()}
                      </span>
                    </div>
                    <p className="text-sm text-grey-300 mb-3">{alert.issue_type}</p>

                    {/* Quick Stats */}
                    <div className="grid grid-cols-3 gap-2 mb-3">
                      <div className="bg-white/5 rounded p-2">
                        <p className="text-xs text-grey-400">Risk Score</p>
                        <p className={`font-bold ${colors.text}`}>{(alert.escalation_probability * 100).toFixed(0)}%</p>
                      </div>
                      <div className="bg-white/5 rounded p-2">
                        <p className="text-xs text-grey-400">Days to Escalate</p>
                        <div className="flex items-center gap-1">
                          <Clock className="w-3 h-3" />
                          <p className="font-bold text-white">{alert.days_until_escalation}d</p>
                        </div>
                      </div>
                      <div className="bg-white/5 rounded p-2">
                        <p className="text-xs text-grey-400">Social Mentions</p>
                        <div className="flex items-center gap-1">
                          <MessageSquare className="w-3 h-3" />
                          <p className="font-bold text-white">{alert.social_mentions}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <motion.div
                  animate={{ rotate: isExpanded ? 180 : 0 }}
                  transition={{ duration: 0.3 }}
                  className={`${colors.text}`}
                >
                  <TrendingUp className="w-5 h-5" />
                </motion.div>
              </div>

              {/* Expandable Details */}
              <AnimatePresence>
                {isExpanded && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: 'auto' }}
                    exit={{ opacity: 0, height: 0 }}
                    transition={{ duration: 0.3 }}
                    className="mt-4 pt-4 border-t border-white/10"
                  >
                    <div className="space-y-3">
                      <div>
                        <p className="text-xs text-grey-400 mb-1">Escalation Channels</p>
                        <div className="flex gap-2 flex-wrap">
                          {alert.news_coverage && (
                            <span className="px-2 py-1 bg-white/10 rounded text-xs text-white font-medium">
                              📰 News Media
                            </span>
                          )}
                          {alert.social_mentions > 50 && (
                            <span className="px-2 py-1 bg-white/10 rounded text-xs text-white font-medium">
                              📱 Social Trending
                            </span>
                          )}
                          <span className="px-2 py-1 bg-white/10 rounded text-xs text-white font-medium">
                            😠 {alert.sentiment === 'negative' ? 'Negative' : 'Neutral'} Sentiment
                          </span>
                        </div>
                      </div>

                      <div>
                        <p className="text-xs text-grey-400 mb-2">Recommended Actions</p>
                        <ul className="space-y-1 text-sm">
                          <li className="flex items-center gap-2">
                            <span className="w-1.5 h-1.5 bg-cyan-400 rounded-full" />
                            <span className="text-grey-300">Escalate to senior management immediately</span>
                          </li>
                          <li className="flex items-center gap-2">
                            <span className="w-1.5 h-1.5 bg-cyan-400 rounded-full" />
                            <span className="text-grey-300">Assign dedicated resolution team</span>
                          </li>
                          {alert.news_coverage && (
                            <li className="flex items-center gap-2">
                              <span className="w-1.5 h-1.5 bg-cyan-400 rounded-full" />
                              <span className="text-grey-300">Prepare media statement and transparency report</span>
                            </li>
                          )}
                        </ul>
                      </div>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.div>
          )
        })}
      </AnimatePresence>

      {alerts.length === 0 && (
        <motion.div
          className="text-center py-12 px-4 rounded-lg bg-emerald-500/10 border border-emerald-500/30"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          <p className="text-emerald-300 font-semibold">✨ All clear! No escalation risks detected</p>
        </motion.div>
      )}
    </div>
  )
}

export default EscalationRiskMonitor
