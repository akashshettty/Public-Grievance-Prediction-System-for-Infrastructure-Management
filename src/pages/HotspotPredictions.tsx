import React from 'react'
import { motion } from 'framer-motion'
import HeroSection from '../components/HeroSection'
import KPICard from '../components/KPICard'
import PremiumChart from '../components/PremiumChart'
import PremiumTable from '../components/PremiumTable'
import { MapPin, TrendingUp, AlertTriangle, Zap } from 'lucide-react'

const HotspotPredictions: React.FC = () => {
  const hotspotData = [
    { id: '1', area: 'KR Puram', probability: 94, confidenceScore: 0.96, predictedDate: '2025-05-15', escalationRisk: 'CRITICAL', affectedPopulation: '450K' },
    { id: '2', area: 'Indiranagar', probability: 78, confidenceScore: 0.89, predictedDate: '2025-05-22', escalationRisk: 'HIGH', affectedPopulation: '380K' },
    { id: '3', area: 'Whitefield', probability: 62, confidenceScore: 0.78, predictedDate: '2025-06-01', escalationRisk: 'MEDIUM', affectedPopulation: '320K' },
    { id: '4', area: 'Marathahalli', probability: 45, confidenceScore: 0.65, predictedDate: '2025-06-10', escalationRisk: 'MEDIUM', affectedPopulation: '280K' },
    { id: '5', area: 'Koramangala', probability: 38, confidenceScore: 0.58, predictedDate: '2025-06-15', escalationRisk: 'LOW', affectedPopulation: '200K' },
  ]

  const timelineData = [
    { date: 'May 15', critical: 2, high: 4, medium: 8, low: 12 },
    { date: 'May 22', critical: 3, high: 6, medium: 9, low: 10 },
    { date: 'Jun 1', critical: 4, high: 7, medium: 10, low: 8 },
    { date: 'Jun 10', critical: 5, high: 8, medium: 11, low: 6 },
    { date: 'Jun 20', critical: 6, high: 9, medium: 10, low: 5 },
  ]

  const patternData = [
    { pattern: 'Road Surface', frequency: 156, trend: 'Escalating', leadTime: '7-10 days' },
    { pattern: 'Water Infrastructure', frequency: 134, trend: 'Escalating', leadTime: '5-7 days' },
    { pattern: 'Drainage System', frequency: 98, trend: 'Stable', leadTime: '10-14 days' },
    { pattern: 'Street Lighting', frequency: 67, trend: 'Declining', leadTime: '14-21 days' },
  ]

  return (
    <div className="space-y-12">
      {/* Hero */}
      <HeroSection
        title="Hotspot Prediction Engine"
        subtitle="AI-Powered Infrastructure Crisis Forecasting"
        summary="Machine learning models have identified 8 emerging hotspots likely to escalate within 30 days. KR Puram shows 94% probability of critical infrastructure failure. Advanced pattern recognition reveals water and road infrastructure as primary risk factors. Confidence score across all predictions: 79%."
        alerts={[
          { count: 2, label: 'Imminent Hotspots', severity: 'critical' },
          { count: 4, label: 'Emerging Areas', severity: 'warning' },
          { count: 12, label: 'Monitored Zones', severity: 'info' },
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
          title="Predicted Hotspots"
          value={8}
          unit="areas"
          icon={<MapPin size={24} />}
          trend={33.3}
          gradient="cyan"
        />
        <KPICard
          title="Avg Confidence"
          value={79}
          unit="%"
          icon={<TrendingUp size={24} />}
          trend={12.5}
          gradient="emerald"
        />
        <KPICard
          title="Imminent Crises"
          value={2}
          unit="7-10 days"
          icon={<Zap size={24} />}
          trend={50.0}
          status="critical"
          gradient="rose"
        />
        <KPICard
          title="Avg Lead Time"
          value={9}
          unit="days"
          icon={<AlertTriangle size={24} />}
          trend={-15.2}
          gradient="gold"
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
          title="Hotspot Escalation Timeline"
          type="area"
          data={timelineData}
          xAxisKey="date"
          yAxisKey={['critical', 'high', 'medium', 'low']}
          colors={['#ff006e', '#ffd700', '#ffb703', '#00d98e']}
        />
        <PremiumChart
          title="Escalation Pattern Analysis"
          type="bar"
          data={patternData.map((p, i) => ({
            name: p.pattern,
            frequency: p.frequency,
            index: i,
          }))}
          xAxisKey="name"
          yAxisKey={['frequency']}
          colors={['#00d9ff']}
        />
      </motion.div>

      {/* Hotspots Table */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
      >
        <h2 className="text-3xl font-bold text-white mb-6">Predicted Hotspots</h2>
        <PremiumTable
          columns={[
            { key: 'area', label: 'Predicted Area', width: '150px' },
            { key: 'probability', label: 'Probability', align: 'center' },
            { key: 'confidenceScore', label: 'Confidence', align: 'center' },
            { key: 'predictedDate', label: 'Est. Date', align: 'center' },
            { key: 'escalationRisk', label: 'Risk Level', align: 'center' },
            { key: 'affectedPopulation', label: 'Population' },
          ]}
          rows={hotspotData}
          expandable
          expandRender={(row) => (
            <div className="grid grid-cols-3 gap-4">
              <div>
                <p className="text-xs text-gray-400 mb-2">Prediction Factors</p>
                <ul className="space-y-1 text-sm text-gray-300">
                  <li>✓ Complaint volume trending</li>
                  <li>✓ Weather correlation</li>
                  <li>✓ Seasonal patterns</li>
                </ul>
              </div>
              <div>
                <p className="text-xs text-gray-400 mb-2">Recommended Actions</p>
                <ul className="space-y-1 text-sm text-gray-300">
                  <li>• Stage equipment & teams</li>
                  <li>• Alert stakeholders</li>
                  <li>• Plan contingencies</li>
                </ul>
              </div>
              <div>
                <p className="text-xs text-gray-400 mb-2">Resource Estimate</p>
                <div className="space-y-1 text-sm">
                  <div>Budget: <span className="text-neon-cyan font-semibold">₹1.8 Cr</span></div>
                  <div>Team: <span className="text-neon-cyan font-semibold">120 members</span></div>
                  <div>Duration: <span className="text-neon-cyan font-semibold">5-7 days</span></div>
                </div>
              </div>
            </div>
          )}
        />
      </motion.div>

      {/* Pattern Analysis */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
      >
        <h2 className="text-3xl font-bold text-white mb-6">Pattern Recognition & Trends</h2>
        <PremiumTable
          columns={[
            { key: 'pattern', label: 'Issue Pattern', width: '180px' },
            { key: 'frequency', label: 'Frequency', align: 'center' },
            { key: 'trend', label: 'Trend', align: 'center' },
            { key: 'leadTime', label: 'Lead Time', align: 'center' },
          ]}
          rows={patternData}
        />
      </motion.div>
    </div>
  )
}

export default HotspotPredictions
