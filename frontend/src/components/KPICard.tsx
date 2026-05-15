import React from 'react'
import { motion } from 'framer-motion'
import { TrendingUp, TrendingDown, AlertCircle } from 'lucide-react'
import { cn } from '../utils/cn'

interface KPICardProps {
  title: string
  value: string | number
  unit?: string
  icon?: React.ReactNode
  trend?: number
  status?: 'normal' | 'warning' | 'critical'
  sparkline?: number[]
  gradient?: 'cyan' | 'gold' | 'purple' | 'emerald' | 'rose'
}

const gradientStyles = {
  cyan: 'from-grey-400 to-grey-500',
  gold: 'from-white to-grey-200',
  purple: 'from-grey-500 to-grey-600',
  emerald: 'from-grey-400 to-grey-500',
  rose: 'from-grey-500 to-grey-600',
}

const KPICard: React.FC<KPICardProps> = ({
  title,
  value,
  unit,
  icon,
  trend,
  status = 'normal',
  sparkline,
  gradient = 'cyan',
}) => {
  const statusColors = {
    normal: 'border-white/10 hover:border-white/20',
    warning: 'border-grey-500/30 hover:border-grey-500/50',
    critical: 'border-grey-600/30 hover:border-grey-600/50',
  }

  const trendColor = trend !== undefined && trend >= 0 ? 'text-white' : 'text-grey-400'
  const trendIcon = trend !== undefined && trend >= 0 ? <TrendingUp size={16} /> : <TrendingDown size={16} />

  return (
    <motion.div
      className={cn(
        "glass-premium rounded-lg p-5 border transition-all duration-300 relative overflow-hidden",
        statusColors[status]
      )}
      whileHover={{ borderColor: 'rgba(255, 255, 255, 0.2)', y: -2 }}
      whileTap={{ scale: 0.98 }}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      {/* Background gradient effect */}
      <motion.div
        className={`absolute inset-0 bg-gradient-to-br ${gradientStyles[gradient]} opacity-0 pointer-events-none`}
      />

      {/* Content */}
      <div className="relative z-10">
        {/* Header with icon and status */}
        <div className="flex items-start justify-between mb-3">
          <div className="flex-1">
            <p className="text-xs font-semibold text-white/70 uppercase tracking-wider mb-1">
              {title}
            </p>
          </div>
          <div className="flex items-center gap-2">
            {status === 'critical' && (
              <motion.div animate={{ rotate: [0, 10, -10, 0] }} transition={{ duration: 2, repeat: Infinity }}>
                <AlertCircle size={16} className="text-white/50" />
              </motion.div>
            )}
            {icon && <div className="text-white/60">{icon}</div>}
          </div>
        </div>

        {/* Main value */}
        <div className="flex items-baseline gap-2 mb-3">
          <motion.span
            className="text-3xl font-bold text-white"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          >
            {value}
          </motion.span>
          {unit && <span className="text-xs text-white/60">{unit}</span>}
        </div>

        {/* Trend indicator */}
        {trend !== undefined && (
          <div className={cn('flex items-center gap-1 text-sm font-semibold', trendColor)}>
            {trendIcon}
            <span>{Math.abs(trend)}% vs last period</span>
          </div>
        )}

        {/* Sparkline chart */}
        {sparkline && (
          <div className="mt-4 h-12 flex items-end gap-1">
            {sparkline.map((value, idx) => {
              const maxValue = Math.max(...sparkline)
              const height = (value / maxValue) * 100
              return (
                <motion.div
                  key={idx}
                  className={`flex-1 rounded-sm bg-gradient-to-t ${gradientStyles[gradient]} opacity-50`}
                  initial={{ height: 0 }}
                  animate={{ height: `${height}%` }}
                  transition={{ delay: idx * 0.05, duration: 0.5 }}
                />
              )
            })}
          </div>
        )}
      </div>

      {/* Glow effect */}
      <motion.div
        className={`absolute inset-0 rounded-2xl bg-gradient-to-r ${gradientStyles[gradient]} opacity-0 group-hover:opacity-10 blur-xl transition-opacity duration-300 pointer-events-none`}
      />
    </motion.div>
  )
}

export default KPICard
