import React from 'react'
import { motion } from 'framer-motion'
import { MapPin, AlertTriangle } from 'lucide-react'

interface MapTooltipProps {
  title: string
  value: string
  severity?: 'low' | 'medium' | 'high' | 'critical'
  position: { x: number; y: number }
}

const MapTooltip: React.FC<MapTooltipProps> = ({ title, value, severity = 'medium', position }) => {
  const colors = {
    low: 'bg-emerald-accent/20 border-emerald-accent/50 text-emerald-accent',
    medium: 'bg-yellow-500/20 border-yellow-500/50 text-yellow-400',
    high: 'bg-orange-500/20 border-orange-500/50 text-orange-400',
    critical: 'bg-rose-accent/20 border-rose-accent/50 text-rose-accent',
  }

  return (
    <motion.div
      className={`glass-premium rounded-lg p-3 border ${colors[severity]} absolute pointer-events-none z-50`}
      style={{
        left: `${position.x}px`,
        top: `${position.y}px`,
        transform: 'translate(-50%, -100%)',
      }}
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.2 }}
    >
      <p className="text-xs font-semibold">{title}</p>
      <p className="text-sm font-bold">{value}</p>
    </motion.div>
  )
}

export default MapTooltip
