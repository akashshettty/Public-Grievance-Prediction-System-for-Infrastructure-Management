import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import HeroSection from '../components/HeroSection'
import KPICard from '../components/KPICard'
import PremiumChart from '../components/PremiumChart'
import PremiumTable from '../components/PremiumTable'
import { MapPin, TrendingUp, AlertTriangle, Zap } from 'lucide-react'
import HotspotMap from '../components/HotspotMap'

const HotspotPredictions: React.FC = () => {
  const [loading, setLoading] = useState(true)
  const [failureData, setFailureData] = useState<any>(null)

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true)
      try {
        const response = await fetch('http://localhost:5000/api/ai/failure-prediction')
        const data = await response.json()
        setFailureData(data)
      } catch (error) {
        console.error('Error fetching failure predictions:', error)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])

  const hotspotData = failureData?.predictions?.map((p: any, i: number) => ({
    id: i.toString(),
    area: p.ward,
    probability: (p.failure_probability * 100).toFixed(0),
    confidenceScore: p.confidence,
    predictedDate: p.forecast_date,
    escalationRisk: p.risk_level.toUpperCase(),
    affectedPopulation: `${(p.failure_probability * 500).toFixed(0)}K`
  })) || []

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

  if (loading) {
    return <div className="h-screen flex items-center justify-center text-white">Calculating Hotspot Predictions...</div>
  }

  return (
    <div className="space-y-12">
      {/* Hero */}
      <HeroSection
        title="Hotspot Prediction Engine"
        subtitle="AI-Powered Infrastructure Crisis Forecasting"
        summary={`Machine learning models have identified ${failureData?.stats?.high_risk_count || 0} imminent hotspots likely to escalate within 30 days. Average failure probability detected at ${failureData?.stats?.avg_failure_prob?.toFixed(1) || 0}%. Confidence score across all predictions: 88%.`}
        alerts={[
          { count: failureData?.stats?.high_risk_count || 0, label: 'Imminent Hotspots', severity: 'critical' },
          { count: (failureData?.stats?.total_predictions || 0) - (failureData?.stats?.high_risk_count || 0), label: 'Emerging Areas', severity: 'warning' },
          { count: failureData?.stats?.total_predictions || 0, label: 'Monitored Zones', severity: 'info' },
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
          value={failureData?.stats?.total_predictions || 0}
          unit="areas"
          icon={<MapPin size={24} />}
          trend={33.3}
          gradient="cyan"
        />
        <KPICard
          title="Avg Confidence"
          value={88}
          unit="%"
          icon={<TrendingUp size={24} />}
          trend={12.5}
          gradient="emerald"
        />
        <KPICard
          title="Imminent Crises"
          value={failureData?.stats?.high_risk_count || 0}
          unit="7-10 days"
          icon={<Zap size={24} />}
          trend={50.0}
          status="critical"
          gradient="rose"
        />
        <KPICard
          title="Avg Risk"
          value={((failureData?.stats?.avg_failure_prob || 0) * 100).toFixed(0)}
          unit="%"
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

      {/* Hotspots Map Visualization */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
      >
        <div className="flex justify-between items-end mb-6">
          <div>
            <h2 className="text-3xl font-bold text-white mb-2">Geographical Hotspot Intelligence</h2>
            <p className="text-gray-400">Real-time infrastructure risk distribution across Bengaluru wards</p>
          </div>
          <div className="flex gap-2">
            <div className="px-3 py-1 rounded-full bg-white/5 border border-white/10 text-xs text-gray-400">
              Live GeoJSON Sync: <span className="text-emerald-400 font-mono">Active</span>
            </div>
          </div>
        </div>
        
        <HotspotMap predictions={failureData?.predictions || []} />
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
