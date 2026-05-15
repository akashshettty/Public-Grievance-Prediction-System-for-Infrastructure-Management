import React from 'react'
import { motion } from 'framer-motion'
import { Zap, TrendingUp, AlertTriangle, Brain } from 'lucide-react'

interface AIInsightProps {
  severity: 'info' | 'warning' | 'critical'
  title: string
  description: string
  metrics?: { label: string; value: string }[]
  action?: string
}

const AIInsightCard: React.FC<AIInsightProps> = ({ severity, title, description, metrics, action }) => {
  const severityConfig = {
    info: {
      bg: 'from-grey-700/20 to-grey-600/20',
      border: 'border-grey-700/30',
      icon: Brain,
      badge: 'INFO',
      badgeBg: 'bg-grey-700/20 text-white',
    },
    warning: {
      bg: 'from-grey-600/20 to-grey-500/20',
      border: 'border-grey-600/30',
      icon: AlertTriangle,
      badge: 'WARNING',
      badgeBg: 'bg-grey-600/20 text-grey-300',
    },
    critical: {
      bg: 'from-grey-700/20 to-grey-600/20',
      border: 'border-grey-700/30',
      icon: Zap,
      badge: 'CRITICAL',
      badgeBg: 'bg-grey-700/20 text-white',
    },
  }

  const config = severityConfig[severity]
  const Icon = config.icon

  return (
    <motion.div
      className={`glass-premium rounded-xl p-5 border ${config.border} overflow-hidden`}
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.5 }}
      whileHover={{ borderColor: 'rgba(255, 255, 255, 0.3)' }}
    >
      <div className={`absolute inset-0 bg-gradient-to-br ${config.bg} opacity-50 pointer-events-none`} />

      <div className="relative z-10">
        {/* Header */}
        <div className="flex items-start gap-3 mb-3">
          <motion.div
            animate={{ rotate: severity === 'critical' ? [0, 10, -10, 0] : 0 }}
            transition={{ duration: 2, repeat: severity === 'critical' ? Infinity : 0 }}
          >
            <Icon size={20} className={config.badgeBg.split(' ')[1]} />
          </motion.div>
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-1">
              <h4 className="font-semibold text-white">{title}</h4>
              <span className={`text-xs font-bold px-2 py-0.5 rounded ${config.badgeBg}`}>
                {config.badge}
              </span>
            </div>
          </div>
        </div>

        {/* Description */}
        <p className="text-sm text-grey-200 mb-3 leading-relaxed">{description}</p>

        {/* Metrics */}
        {metrics && metrics.length > 0 && (
          <div className="grid grid-cols-2 gap-2 mb-3">
            {metrics.map((metric, idx) => (
              <div key={idx} className="bg-white/5 rounded-lg p-2">
                <p className="text-xs text-grey-400">{metric.label}</p>
                <p className="text-sm font-bold text-white">{metric.value}</p>
              </div>
            ))}
          </div>
        )}

        {/* Action Button */}
        {action && (
          <motion.button
            className="w-full py-2 px-3 rounded-lg bg-white/10 hover:bg-white/20 text-sm font-semibold text-white transition-all duration-300 text-center"
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            {action}
          </motion.button>
        )}
      </div>
    </motion.div>
  )
}

export default AIInsightCard
