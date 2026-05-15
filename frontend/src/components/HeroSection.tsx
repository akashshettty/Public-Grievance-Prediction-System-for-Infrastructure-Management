import React from 'react'
import { motion } from 'framer-motion'
import { AlertCircle, Brain, Zap, TrendingUp } from 'lucide-react'

interface HeroSectionProps {
  title: string
  subtitle: string
  summary: string
  alerts: { count: number; label: string; severity: 'critical' | 'warning' | 'info' }[]
}

const HeroSection: React.FC<HeroSectionProps> = ({ title, subtitle, summary, alerts }) => {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.2,
      },
    },
  }

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
  }

  return (
    <motion.div
      className="mb-12 relative overflow-hidden"
      initial="hidden"
      animate="visible"
      variants={containerVariants}
    >
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-r from-white/5 via-white/3 to-white/5 rounded-2xl pointer-events-none" />

      <motion.div
        className="glass-premium rounded-2xl border border-white/10 p-8 relative z-10"
        variants={itemVariants}
      >
        {/* Header */}
        <div className="mb-8">
          <motion.h1
            className="text-5xl font-bold text-white mb-2"
            variants={itemVariants}
          >
            {title}
          </motion.h1>
          <motion.p
            className="text-xl text-white font-semibold"
            variants={itemVariants}
          >
            {subtitle}
          </motion.p>
        </div>

        {/* AI Summary */}
        <motion.div
          className="mb-6 p-5 rounded-lg border border-white/10"
          style={{ backgroundColor: 'rgba(255, 255, 255, 0.03)' }}
          variants={itemVariants}
        >
          <div className="flex items-start gap-3">
            <Brain size={20} className="text-white flex-shrink-0 mt-0.5" />
            <div>
              <p className="text-xs font-semibold text-white/80 uppercase tracking-wider mb-1">Summary</p>
              <p className="text-sm text-white/80 leading-relaxed">{summary}</p>
            </div>
          </div>
        </motion.div>

        {/* Alert Cards */}
        <motion.div
          className="grid grid-cols-1 md:grid-cols-3 gap-4"
          variants={itemVariants}
        >
          {alerts.map((alert, idx) => {
            const colors = {
              critical: 'rgba(255, 255, 255, 0.08)',
              warning: 'rgba(255, 255, 255, 0.06)',
              info: 'rgba(255, 255, 255, 0.05)',
            }

            const icons = {
              critical: <AlertCircle className="text-white/70" size={18} />,
              warning: <Zap className="text-white/60" size={18} />,
              info: <TrendingUp className="text-white/60" size={18} />,
            }

            return (
              <motion.div
                key={idx}
                className="rounded-lg p-3 border border-white/10"
                style={{ backgroundColor: colors[alert.severity] }}
                whileHover={{ scale: 1.02, y: -2 }}
                transition={{ duration: 0.2 }}
              >
                <div className="flex items-center gap-2">
                  {icons[alert.severity]}
                  <div>
                    <p className="text-xs font-semibold text-white">{alert.count}</p>
                    <p className="text-xs text-white/70">{alert.label}</p>
                  </div>
                </div>
              </motion.div>
            )
          })}
        </motion.div>
      </motion.div>
    </motion.div>
  )
}

export default HeroSection
