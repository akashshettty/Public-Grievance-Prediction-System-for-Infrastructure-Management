import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Shield, AlertTriangle, CheckCircle, XCircle, Eye } from 'lucide-react'

interface FraudAlert {
  id: string
  complaint_id: string
  fraud_score: number
  anomaly_type: string
  reason: string
  flag_time: string
  severity: 'low' | 'medium' | 'high' | 'critical'
  ward?: string
}

export function FraudDetectionPanel() {
  const [fraudAlerts, setFraudAlerts] = useState<FraudAlert[]>([])
  const [loading, setLoading] = useState(true)
  const [expandedId, setExpandedId] = useState<string | null>(null)

  useEffect(() => {
    const fetchFraudData = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/ai/fraud-detection')
        const data = await response.json()
        setFraudAlerts(data.alerts || [])
      } catch (error) {
        console.error('Error fetching fraud detection data:', error)
        // Fallback to default data
        setFraudAlerts([
          {
            id: '1',
            complaint_id: 'COMP-2025-0501',
            fraud_score: 0.82,
            anomaly_type: 'Premature Closure',
            reason: 'High severity complaint closed in 2.3 hours - unusually fast',
            flag_time: '2 hours ago',
            severity: 'high'
          },
          {
            id: '2',
            complaint_id: 'COMP-2025-0498',
            fraud_score: 0.65,
            anomaly_type: 'Recurring Issue',
            reason: 'Reopened 5 times in 30 days - unresolved root cause',
            flag_time: '5 hours ago',
            severity: 'medium'
          },
          {
            id: '3',
            complaint_id: 'COMP-2025-0495',
            fraud_score: 0.44,
            anomaly_type: 'Pattern Deviation',
            reason: 'Closure pattern deviates from historical norms',
            flag_time: '1 day ago',
            severity: 'low'
          }
        ])
      } finally {
        setLoading(false)
      }
    }

    fetchFraudData()
  }, [])

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'bg-red-500/20 border-red-500/30 text-red-300'
      case 'high':
        return 'bg-orange-500/20 border-orange-500/30 text-orange-300'
      case 'medium':
        return 'bg-yellow-500/20 border-yellow-500/30 text-yellow-300'
      default:
        return 'bg-blue-500/20 border-blue-500/30 text-blue-300'
    }
  }

  const dismissAlert = (id: string) => {
    setFraudAlerts(fraudAlerts.filter(alert => alert.id !== id))
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-xl font-bold text-white mb-1 flex items-center gap-2">
            <Shield className="w-5 h-5 text-cyan-400" />
            Fraud & Anomaly Detection
          </h3>
          <p className="text-sm text-grey-400">Suspicious complaint closures and patterns</p>
        </div>
        <motion.div
          className="flex items-center gap-2 px-3 py-1 rounded-lg bg-white/10"
          animate={{ scale: [1, 1.05, 1] }}
          transition={{ duration: 2, repeat: Infinity }}
        >
          <Eye className="w-4 h-4 text-white" />
          <span className="text-sm font-semibold text-white">{fraudAlerts.length} Flagged</span>
        </motion.div>
      </div>

      <AnimatePresence>
        {fraudAlerts.map((alert, idx) => (
          <motion.div
            key={alert.id}
            layout
            className={`border rounded-lg p-4 backdrop-blur-xl transition-all ${getSeverityColor(alert.severity)}`}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: idx * 0.1 }}
          >
            <div className="flex items-start justify-between gap-4">
              <div className="flex items-start gap-3 flex-1">
                <motion.div
                  animate={{ scale: [1, 1.2, 1] }}
                  transition={{ duration: 2, repeat: Infinity }}
                >
                  <AlertTriangle className="w-5 h-5 mt-1" />
                </motion.div>

                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <h4 className="font-semibold text-white">{alert.anomaly_type}</h4>
                    <span className="text-xs px-2 py-0.5 rounded-full bg-white/20 font-mono text-grey-200">
                      {alert.complaint_id}
                    </span>
                  </div>

                  <p className="text-sm text-grey-300 mb-3">{alert.reason}</p>

                  <div className="flex items-center gap-4 text-xs">
                    <div className="flex items-center gap-1">
                      <span className="text-grey-400">Fraud Score:</span>
                      <div className="w-16 h-1.5 bg-white/10 rounded-full overflow-hidden">
                        <motion.div
                          className="h-full bg-gradient-to-r from-yellow-500 to-red-500 rounded-full"
                          initial={{ width: 0 }}
                          animate={{ width: `${alert.fraud_score * 100}%` }}
                          transition={{ duration: 1 }}
                        />
                      </div>
                      <span className="font-mono">{(alert.fraud_score * 100).toFixed(0)}%</span>
                    </div>
                    <div className="flex items-center gap-1 text-grey-400">
                      <span>Flagged:</span>
                      <span className="text-grey-300">{alert.flag_time}</span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex gap-2">
                <motion.button
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                  onClick={() => setExpandedId(expandedId === alert.id ? null : alert.id)}
                  className="p-2 hover:bg-white/10 rounded-lg transition-colors"
                >
                  {expandedId === alert.id ? (
                    <XCircle className="w-5 h-5" />
                  ) : (
                    <Eye className="w-5 h-5" />
                  )}
                </motion.button>
                <motion.button
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                  onClick={() => dismissAlert(alert.id)}
                  className="p-2 hover:bg-white/10 rounded-lg transition-colors"
                >
                  <CheckCircle className="w-5 h-5" />
                </motion.button>
              </div>
            </div>

            {/* Expandable Details */}
            <AnimatePresence>
              {expandedId === alert.id && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                  transition={{ duration: 0.3 }}
                  className="mt-4 pt-4 border-t border-white/10"
                >
                  <div className="space-y-3 text-sm">
                    <div>
                      <p className="text-grey-400 mb-2">Investigation Steps</p>
                      <ol className="list-decimal list-inside space-y-1 text-grey-300">
                        <li>Review complaint closure timeline and supporting evidence</li>
                        <li>Verify assigned worker completed work as documented</li>
                        <li>Check citizen satisfaction feedback and follow-up reviews</li>
                        <li>Compare with similar complaints and resolution times</li>
                        <li>Make final determination of fraud/legitimacy</li>
                      </ol>
                    </div>
                    <div className="flex gap-2 pt-2">
                      <motion.button
                        whileHover={{ scale: 1.05 }}
                        className="px-3 py-2 rounded-lg bg-emerald-500/20 text-emerald-300 text-xs font-semibold hover:bg-emerald-500/30 transition-colors"
                      >
                        Verify Legitimate
                      </motion.button>
                      <motion.button
                        whileHover={{ scale: 1.05 }}
                        className="px-3 py-2 rounded-lg bg-red-500/20 text-red-300 text-xs font-semibold hover:bg-red-500/30 transition-colors"
                      >
                        Confirm Fraud
                      </motion.button>
                    </div>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>
        ))}
      </AnimatePresence>

      {fraudAlerts.length === 0 && (
        <motion.div
          className="text-center py-12 px-4 rounded-lg bg-emerald-500/10 border border-emerald-500/30"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          <CheckCircle className="w-8 h-8 mx-auto mb-2 text-emerald-300" />
          <p className="text-emerald-300 font-semibold">All complaint closures verified as legitimate</p>
        </motion.div>
      )}
    </div>
  )
}

export default FraudDetectionPanel
