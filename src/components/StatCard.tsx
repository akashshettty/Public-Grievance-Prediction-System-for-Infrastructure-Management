import React from 'react'
import { motion } from 'framer-motion'

interface StatCardProps {
  label: string
  value: string | number
  change?: number
  icon: React.ReactNode
}

const StatCard: React.FC<StatCardProps> = ({ label, value, change, icon }) => {
  const isPositive = !change || change >= 0

  return (
    <motion.div
      className="glass-dark rounded-xl p-4 border border-white/10 hover:border-neon-cyan/30 transition-colors duration-300"
      whileHover={{ y: -2 }}
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
    >
      <div className="flex items-center justify-between mb-2">
        <span className="text-xs text-gray-400 uppercase tracking-wider">{label}</span>
        <div className="text-neon-cyan">{icon}</div>
      </div>
      <div className="flex items-baseline gap-2">
        <span className="text-2xl font-bold text-white">{value}</span>
        {change !== undefined && (
          <span className={`text-xs font-semibold ${isPositive ? 'text-emerald-accent' : 'text-rose-accent'}`}>
            {isPositive ? '+' : ''}{change}%
          </span>
        )}
      </div>
    </motion.div>
  )
}

export default StatCard
