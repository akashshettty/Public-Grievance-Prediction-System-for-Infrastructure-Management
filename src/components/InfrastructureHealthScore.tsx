import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Heart, Zap, AlertTriangle, TrendingUp } from 'lucide-react'

interface HealthMetric {
  category: string
  score: number
  status: 'excellent' | 'good' | 'fair' | 'poor' | 'critical'
  trend: number
}

const getHealthColor = (status: string) => {
  switch (status) {
    case 'excellent':
      return { bg: 'bg-emerald-500/20', text: 'text-emerald-300', icon: '😊' }
    case 'good':
      return { bg: 'bg-cyan-500/20', text: 'text-cyan-300', icon: '👍' }
    case 'fair':
      return { bg: 'bg-yellow-500/20', text: 'text-yellow-300', icon: '⚠️' }
    case 'poor':
      return { bg: 'bg-orange-500/20', text: 'text-orange-300', icon: '⚡' }
    case 'critical':
      return { bg: 'bg-red-500/20', text: 'text-red-300', icon: '🚨' }
    default:
      return { bg: 'bg-grey-600/20', text: 'text-grey-300', icon: '❓' }
  }
}

export function InfrastructureHealthScore() {
  const [metrics, setMetrics] = useState<HealthMetric[]>([
    { category: 'Road Infrastructure', score: 72, status: 'fair', trend: -5.2 },
    { category: 'Drainage System', score: 65, status: 'fair', trend: 2.1 },
    { category: 'Water Supply', score: 81, status: 'good', trend: -1.3 },
    { category: 'Streetlights', score: 88, status: 'excellent', trend: 3.5 },
  ])

  const overallScore = Math.round(metrics.reduce((sum, m) => sum + m.score, 0) / metrics.length)

  const getOverallStatus = (score: number): HealthMetric['status'] => {
    if (score >= 80) return 'excellent'
    if (score >= 60) return 'good'
    if (score >= 40) return 'fair'
    if (score >= 20) return 'poor'
    return 'critical'
  }

  const overallStatus = getOverallStatus(overallScore)
  const colors = getHealthColor(overallStatus)

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Overall Health */}
      <motion.div
        className={`col-span-1 rounded-xl border border-grey-700/50 p-6 backdrop-blur-xl ${colors.bg}`}
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
      >
        <div className="flex items-start justify-between mb-4">
          <div>
            <p className="text-grey-400 text-sm mb-2">Infrastructure Health</p>
            <div className="flex items-baseline gap-2">
              <span className="text-5xl font-bold text-white">{overallScore}</span>
              <span className="text-lg text-grey-400">/100</span>
            </div>
          </div>
          <motion.div
            className="text-4xl"
            animate={{ scale: [1, 1.1, 1] }}
            transition={{ duration: 2, repeat: Infinity }}
          >
            {colors.icon}
          </motion.div>
        </div>

        <div className="w-full bg-white/10 rounded-full h-2 mb-4 overflow-hidden">
          <motion.div
            className={`h-full ${colors.text.replace('text-', 'bg-')} rounded-full`}
            initial={{ width: 0 }}
            animate={{ width: `${overallScore}%` }}
            transition={{ duration: 1.5, ease: 'easeOut' }}
          />
        </div>

        <p className={`text-sm font-semibold ${colors.text}`}>
          Status: {overallStatus.toUpperCase()}
        </p>
      </motion.div>

      {/* Detailed Metrics */}
      <div className="col-span-1 lg:col-span-2">
        <div className="space-y-3">
          {metrics.map((metric, idx) => {
            const metricColors = getHealthColor(metric.status)
            return (
              <motion.div
                key={metric.category}
                className="bg-grey-800/40 border border-grey-700/30 rounded-lg p-4 backdrop-blur-xl"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: idx * 0.1 }}
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="font-medium text-white">{metric.category}</span>
                  <span className={`text-sm font-semibold px-2 py-1 rounded ${metricColors.bg} ${metricColors.text}`}>
                    {metric.score}%
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="flex-1 bg-white/5 rounded-full h-1.5 overflow-hidden">
                    <motion.div
                      className={`h-full ${metricColors.text.replace('text-', 'bg-')}`}
                      initial={{ width: 0 }}
                      animate={{ width: `${metric.score}%` }}
                      transition={{ duration: 1 }}
                    />
                  </div>
                  <div className={`flex items-center gap-1 ${metric.trend > 0 ? 'text-red-400' : 'text-emerald-400'}`}>
                    <TrendingUp className="w-3 h-3" />
                    <span className="text-xs font-semibold">{Math.abs(metric.trend).toFixed(1)}%</span>
                  </div>
                </div>
              </motion.div>
            )
          })}
        </div>
      </div>
    </div>
  )
}

export default InfrastructureHealthScore
