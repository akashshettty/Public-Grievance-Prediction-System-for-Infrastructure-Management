import React from 'react'
import { motion } from 'framer-motion'
import HeroSection from '../components/HeroSection'
import KPICard from '../components/KPICard'
import PremiumChart from '../components/PremiumChart'
import { TrendingUp, AlertTriangle, Shield, Zap } from 'lucide-react'

const InfrastructureTrends: React.FC = () => {
  const infrastructureData = [
    { month: 'Jan', roads: 72, water: 58, drainage: 45, lights: 82 },
    { month: 'Feb', roads: 68, water: 62, drainage: 48, lights: 80 },
    { month: 'Mar', roads: 65, water: 65, drainage: 50, lights: 79 },
    { month: 'Apr', roads: 62, water: 68, drainage: 52, lights: 78 },
    { month: 'May', roads: 58, water: 72, drainage: 55, lights: 76 },
    { month: 'Jun', roads: 55, water: 75, drainage: 58, lights: 74 },
  ]

  const maintenanceData = [
    { category: 'Road Infrastructure', current: 58, target: 85, variance: -27, trend: 'Declining' },
    { category: 'Water Supply', current: 75, target: 90, variance: -15, trend: 'Stable' },
    { category: 'Drainage System', current: 55, target: 80, variance: -25, trend: 'Declining' },
    { category: 'Street Lighting', current: 74, target: 95, variance: -21, trend: 'Stable' },
    { category: 'Park Maintenance', current: 68, target: 85, variance: -17, trend: 'Improving' },
  ]

  const degradationData = [
    { area: 'KR Puram', rate: 2.8, yearlyLoss: '₹12.5 Cr', recommendation: 'Urgent rehabilitation' },
    { area: 'Indiranagar', rate: 1.9, yearlyLoss: '₹8.3 Cr', recommendation: 'Preventive maintenance' },
    { area: 'Whitefield', rate: 1.2, yearlyLoss: '₹5.1 Cr', recommendation: 'Regular monitoring' },
    { area: 'Marathahalli', rate: 0.8, yearlyLoss: '₹3.2 Cr', recommendation: 'Routine maintenance' },
    { area: 'Koramangala', rate: 0.5, yearlyLoss: '₹1.8 Cr', recommendation: 'Standard care' },
  ]

  return (
    <div className="space-y-12">
      {/* Hero */}
      <HeroSection
        title="Infrastructure Trends & Degradation"
        subtitle="Long-term Health Assessment & Predictive Maintenance"
        summary="Infrastructure health declining 1.4% monthly across all categories. Road infrastructure worst affected (declining 3%/month). Cumulative annual degradation loss estimated at ₹30+ Cr. Preventive maintenance intervention can reduce degradation by 35-40%. Water supply shows relative stability. Urgent rehabilitation needed for KR Puram (2.8%/month degradation)."
        alerts={[
          { count: 55, label: 'Avg Health Score', severity: 'warning' },
          { count: 27, label: 'Points Below Target', severity: 'warning' },
          { count: '₹30 Cr', label: 'Yearly Loss Estimate', severity: 'critical' },
        ]}
      />

      {/* KPIs */}
      <motion.div
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
      >
        <KPICard
          title="Avg Infrastructure Score"
          value={65}
          unit="/100"
          icon={<Shield size={24} />}
          trend={-5.2}
          status="warning"
          gradient="gold"
        />
        <KPICard
          title="Degradation Rate"
          value={1.4}
          unit="%/month"
          icon={<TrendingUp size={24} />}
          trend={12.3}
          status="critical"
          gradient="rose"
        />
        <KPICard
          title="Yearly Loss"
          value={30}
          unit="₹ Cr"
          icon={<AlertTriangle size={24} />}
          gradient="gold"
        />
        <KPICard
          title="Maintenance Coverage"
          value={68}
          unit="%"
          icon={<Zap size={24} />}
          trend={8.5}
          gradient="emerald"
        />
      </motion.div>

      {/* Charts */}
      <motion.div
        className="grid grid-cols-1 lg:grid-cols-2 gap-6"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
      >
        <PremiumChart
          title="Infrastructure Health Trajectory"
          type="area"
          data={infrastructureData}
          xAxisKey="month"
          yAxisKey={['roads', 'water', 'drainage', 'lights']}
          colors={['#ff006e', '#00d9ff', '#ffd700', '#00d98e']}
        />
        <PremiumChart
          title="Current vs Target Health Scores"
          type="bar"
          data={maintenanceData.map(m => ({ category: m.category, current: m.current, target: m.target }))}
          xAxisKey="category"
          yAxisKey={['current', 'target']}
          colors={['#00d9ff', '#d4af37']}
        />
      </motion.div>

      {/* Degradation Analysis */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
      >
        <h2 className="text-3xl font-bold text-white mb-6">Infrastructure Degradation Analysis</h2>
        <div className="grid grid-cols-1 gap-4">
          {degradationData.map((item, idx) => (
            <motion.div
              key={idx}
              className="glass-premium rounded-xl p-6 border border-white/10"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: idx * 0.05 }}
            >
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h4 className="text-lg font-bold text-white">{item.area}</h4>
                  <p className="text-sm text-gray-400">Degradation Rate: {item.rate}%/month</p>
                </div>
                <div className="text-right">
                  <p className="text-2xl font-bold text-rose-accent">{item.rate}%</p>
                  <p className="text-xs text-gray-400">Monthly Loss</p>
                </div>
              </div>
              <div className="grid grid-cols-3 gap-4">
                <div className="bg-white/5 rounded-lg p-3">
                  <p className="text-xs text-gray-400 mb-1">Yearly Loss</p>
                  <p className="text-lg font-bold text-neon-cyan">{item.yearlyLoss}</p>
                </div>
                <div className="bg-white/5 rounded-lg p-3">
                  <p className="text-xs text-gray-400 mb-1">Projection (2 yrs)</p>
                  <p className="text-lg font-bold text-rose-accent">
                    {(item.rate * 24).toFixed(1)}%
                  </p>
                </div>
                <div className="bg-white/5 rounded-lg p-3">
                  <p className="text-xs text-gray-400 mb-1">Recommendation</p>
                  <p className="text-xs font-semibold text-emerald-accent">{item.recommendation}</p>
                </div>
              </div>

              {/* Progress Bar */}
              <div className="mt-4">
                <p className="text-xs text-gray-400 mb-2">Critical Degradation Risk</p>
                <div className="h-2 bg-white/10 rounded-full overflow-hidden">
                  <motion.div
                    className="h-full bg-gradient-to-r from-rose-accent to-red-500"
                    initial={{ width: 0 }}
                    animate={{ width: `${item.rate * 10}%` }}
                    transition={{ duration: 1, delay: 0.3 }}
                  />
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* Preventive Measures */}
      <motion.div
        className="glass-premium rounded-2xl p-8 border border-white/10"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
      >
        <h3 className="text-2xl font-bold text-white mb-6">Recommended Preventive Maintenance Strategy</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white/5 rounded-xl p-4">
            <p className="font-semibold text-neon-cyan mb-3">🔧 Immediate Actions (Next 30 Days)</p>
            <ul className="space-y-2 text-sm text-gray-300">
              <li>• Intensive inspection: KR Puram</li>
              <li>• Emergency repairs for critical zones</li>
              <li>• Deploy additional maintenance teams</li>
              <li>• Budget allocation: ₹5 Cr</li>
            </ul>
          </div>
          <div className="bg-white/5 rounded-xl p-4">
            <p className="font-semibold text-royal mb-3">📋 Short-term Plan (3-6 Months)</p>
            <ul className="space-y-2 text-sm text-gray-300">
              <li>• Systematic rehabilitation schedule</li>
              <li>• Upgrade drainage infrastructure</li>
              <li>• Preventive road resurfacing</li>
              <li>• Budget allocation: ₹15 Cr</li>
            </ul>
          </div>
          <div className="bg-white/5 rounded-xl p-4">
            <p className="font-semibold text-emerald-accent mb-3">🎯 Long-term Vision (1-2 Years)</p>
            <ul className="space-y-2 text-sm text-gray-300">
              <li>• Complete infrastructure modernization</li>
              <li>• Smart monitoring systems</li>
              <li>• Reduce degradation by 40%+</li>
              <li>• Budget allocation: ₹40 Cr</li>
            </ul>
          </div>
        </div>
      </motion.div>
    </div>
  )
}

export default InfrastructureTrends
