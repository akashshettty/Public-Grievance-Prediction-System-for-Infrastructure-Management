import React from 'react'
import { motion } from 'framer-motion'
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'

interface ChartProps {
  data: any[]
  type: 'line' | 'area' | 'bar'
  title: string
  xAxisKey: string
  yAxisKey: string | string[]
  colors?: string[]
  height?: number
}

const PremiumChart: React.FC<ChartProps> = ({
  data,
  type,
  title,
  xAxisKey,
  yAxisKey,
  colors = ['#00d9ff', '#9d4edd', '#d4af37'],
  height = 300,
}) => {
  const chartProps = {
    data,
    margin: { top: 10, right: 30, left: 0, bottom: 0 },
    height,
  }

  const yAxisKeys = Array.isArray(yAxisKey) ? yAxisKey : [yAxisKey]

  return (
    <motion.div
      className="glass-premium rounded-2xl p-6 border border-white/10"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <h3 className="text-lg font-bold text-white mb-6">{title}</h3>

      <ResponsiveContainer width="100%" height={height}>
        {type === 'line' && (
          <LineChart {...chartProps}>
            <defs>
              {colors.map((color, idx) => (
                <linearGradient key={idx} id={`color${idx}`} x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor={color} stopOpacity={0.8} />
                  <stop offset="95%" stopColor={color} stopOpacity={0} />
                </linearGradient>
              ))}
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
            <XAxis dataKey={xAxisKey} stroke="rgba(255,255,255,0.5)" />
            <YAxis stroke="rgba(255,255,255,0.5)" />
            <Tooltip
              contentStyle={{
                backgroundColor: 'rgba(10, 14, 39, 0.8)',
                border: '1px solid rgba(0, 217, 255, 0.3)',
                borderRadius: '8px',
              }}
            />
            <Legend />
            {yAxisKeys.map((key, idx) => (
              <Line
                key={key}
                type="monotone"
                dataKey={key}
                stroke={colors[idx]}
                strokeWidth={2}
                dot={false}
                isAnimationActive={true}
              />
            ))}
          </LineChart>
        )}

        {type === 'area' && (
          <AreaChart {...chartProps}>
            <defs>
              {colors.map((color, idx) => (
                <linearGradient key={idx} id={`color${idx}`} x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor={color} stopOpacity={0.8} />
                  <stop offset="95%" stopColor={color} stopOpacity={0.1} />
                </linearGradient>
              ))}
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
            <XAxis dataKey={xAxisKey} stroke="rgba(255,255,255,0.5)" />
            <YAxis stroke="rgba(255,255,255,0.5)" />
            <Tooltip
              contentStyle={{
                backgroundColor: 'rgba(10, 14, 39, 0.8)',
                border: '1px solid rgba(0, 217, 255, 0.3)',
                borderRadius: '8px',
              }}
            />
            <Legend />
            {yAxisKeys.map((key, idx) => (
              <Area
                key={key}
                type="monotone"
                dataKey={key}
                stroke={colors[idx]}
                fillOpacity={0.6}
                fill={`url(#color${idx})`}
                isAnimationActive={true}
              />
            ))}
          </AreaChart>
        )}

        {type === 'bar' && (
          <BarChart {...chartProps}>
            <defs>
              {colors.map((color, idx) => (
                <linearGradient key={idx} id={`color${idx}`} x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor={color} stopOpacity={1} />
                  <stop offset="95%" stopColor={color} stopOpacity={0.8} />
                </linearGradient>
              ))}
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
            <XAxis dataKey={xAxisKey} stroke="rgba(255,255,255,0.5)" />
            <YAxis stroke="rgba(255,255,255,0.5)" />
            <Tooltip
              contentStyle={{
                backgroundColor: 'rgba(10, 14, 39, 0.8)',
                border: '1px solid rgba(0, 217, 255, 0.3)',
                borderRadius: '8px',
              }}
            />
            <Legend />
            {yAxisKeys.map((key, idx) => (
              <Bar
                key={key}
                dataKey={key}
                fill={`url(#color${idx})`}
                isAnimationActive={true}
                radius={[8, 8, 0, 0]}
              />
            ))}
          </BarChart>
        )}
      </ResponsiveContainer>
    </motion.div>
  )
}

export default PremiumChart
