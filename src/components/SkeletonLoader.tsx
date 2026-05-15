import React from 'react'
import { motion } from 'framer-motion'

interface LoadingSkeleton {
  count?: number
  variant?: 'card' | 'table' | 'chart'
}

const SkeletonLoader: React.FC<LoadingSkeleton> = ({ count = 3, variant = 'card' }) => {
  if (variant === 'card') {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {Array.from({ length: count }).map((_, idx) => (
          <motion.div
            key={idx}
            className="glass-premium rounded-2xl p-6 border border-white/10"
            animate={{ opacity: [0.5, 0.8, 0.5] }}
            transition={{ duration: 1.5, repeat: Infinity }}
          >
            <div className="h-6 bg-gradient-to-r from-white/10 to-white/5 rounded-lg mb-4 w-3/4" />
            <div className="h-12 bg-gradient-to-r from-white/10 to-white/5 rounded-lg mb-3" />
            <div className="h-4 bg-gradient-to-r from-white/10 to-white/5 rounded-lg w-1/2" />
          </motion.div>
        ))}
      </div>
    )
  }

  if (variant === 'table') {
    return (
      <motion.div
        className="glass-premium rounded-2xl p-6 border border-white/10"
        animate={{ opacity: [0.5, 0.8, 0.5] }}
        transition={{ duration: 1.5, repeat: Infinity }}
      >
        {Array.from({ length: 5 }).map((_, idx) => (
          <div key={idx} className="py-4 border-b border-white/5">
            <div className="h-6 bg-gradient-to-r from-white/10 to-white/5 rounded-lg" />
          </div>
        ))}
      </motion.div>
    )
  }

  return (
    <motion.div
      className="glass-premium rounded-2xl p-6 border border-white/10 h-80"
      animate={{ opacity: [0.5, 0.8, 0.5] }}
      transition={{ duration: 1.5, repeat: Infinity }}
    />
  )
}

export default SkeletonLoader
