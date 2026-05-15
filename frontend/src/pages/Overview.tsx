import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import HeroSection from '../components/HeroSection'
import KPICard from '../components/KPICard'
import AIInsightCard from '../components/AIInsightCard'
import PremiumChart from '../components/PremiumChart'
import AdvancedFilters from '../components/AdvancedFilters'
import SkeletonLoader from '../components/SkeletonLoader'
import { FraudDetectionPanel } from '../components/FraudDetectionPanel'
import { EscalationRiskMonitor } from '../components/EscalationRiskMonitor'
import {
  Activity,
  AlertTriangle,
  AlertCircle,
  Sparkles,
  Clock,
  TrendingUp,
  Users,
  Shield,
  MapPin,
  Zap,
} from 'lucide-react'

interface OverviewProps {
  onPageChange: (page: any) => void
}

const Overview: React.FC<OverviewProps> = ({ onPageChange }) => {
  const [loading, setLoading] = useState(true)
  const [liveFeed, setLiveFeed] = useState<any[]>([
    { id: 1, type: 'prediction', text: 'New hotspot detected in Ward 84', time: 'Just now', severity: 'critical' },
    { id: 2, type: 'anomaly', text: 'Unusual complaint volume in Ward 1', time: '2 mins ago', severity: 'warning' },
    { id: 3, type: 'resolution', text: 'Resolution rate target reached for Road Maintenance', time: '5 mins ago', severity: 'success' },
  ])

  useEffect(() => {
    const interval = setInterval(() => {
      const wards = ['Ward 15', 'Ward 50', 'Ward 115', 'Ward 130']
      const types = ['Infrastructure Alert', 'Prediction Update', 'Anomaly Flag']
      const ward = wards[Math.floor(Math.random() * wards.length)]
      const type = types[Math.floor(Math.random() * types.length)]
      
      const newAlert = {
        id: Date.now(),
        type: 'prediction',
        text: `${type}: ${ward} requires assessment`,
        time: 'Just now',
        severity: Math.random() > 0.5 ? 'critical' : 'warning'
      }
      
      setLiveFeed(prev => [newAlert, ...prev.slice(0, 4)])
    }, 15000)
    
    return () => clearInterval(interval)
  }, [])
  const [dashboardData, setDashboardData] = useState<any>(null)
  const [trends, setTrends] = useState<any[]>([])
  const [filters, setFilters] = useState({
    dateRange: { start: '', end: '' },
    issueTypes: [],
    areas: [],
    severity: 3,
  })

  const fetchData = async () => {
    setLoading(true)
    try {
      const areaParams = filters.areas.length > 0 ? `&areas=${filters.areas.join(',')}` : ''
      const issueParams = filters.issueTypes.length > 0 ? `&issue_types=${filters.issueTypes.join(',')}` : ''
      const dateParams = filters.dateRange.start ? `&start_date=${filters.dateRange.start}&end_date=${filters.dateRange.end}` : ''
      const severityParam = `&severity=${filters.severity}`
      
      const [metricsRes, trendsRes] = await Promise.all([
        fetch(`/api/dashboard/data?${areaParams}${issueParams}${dateParams}${severityParam}`),
        fetch(`/api/dashboard/trends?days=30`)
      ])
      
      const metrics = await metricsRes.json()
      const trendsData = await trendsRes.json()
      
      setDashboardData(metrics)
      setTrends(trendsData.data)
    } catch (error) {
      console.error('Error fetching dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
  }, [filters])

  const handleFilterChange = (id: string, value: any) => {
    setFilters((prev) => ({ ...prev, [id]: value }))
  }

  const handleGenerateReport = () => {
    onPageChange('reports')
  }

  if (loading && !dashboardData) {
    return <SkeletonLoader count={6} />
  }

  // Map real data to KPI cards
  const kpiData = [
    {
      title: 'Total Complaints',
      value: dashboardData?.total_complaints || 0,
      unit: 'filed',
      icon: <Activity size={24} />,
      trend: dashboardData?.complaint_growth_percent || 0,
      status: 'normal' as const,
      sparkline: [45, 52, 48, 61, 55, 67, 72],
      gradient: 'cyan' as const,
    },
    {
      title: 'Open Issues',
      value: dashboardData?.open_complaints || 0,
      unit: 'pending',
      icon: <AlertTriangle size={24} />,
      trend: -8.2,
      status: 'warning' as const,
      sparkline: [80, 72, 68, 75, 62, 58, 52],
      gradient: 'rose' as const,
    },
    {
      title: 'High-Risk Areas',
      value: dashboardData?.high_risk_areas || 0,
      unit: 'zones',
      icon: <Zap size={24} />,
      trend: 15.3,
      status: 'critical' as const,
      sparkline: [12, 14, 16, 18, 20, 22, 24],
      gradient: 'gold' as const,
    },
    {
      title: 'Avg Response Time',
      value: dashboardData?.avg_response_time || 0,
      unit: 'hours',
      icon: <Clock size={24} />,
      trend: -22.1,
      status: 'normal' as const,
      sparkline: [8, 7.5, 6.8, 6.2, 5.5, 4.8, 4.2],
      gradient: 'purple' as const,
    },
    {
      title: 'Infrastructure Health',
      value: dashboardData?.infrastructure_health || 0,
      unit: '%',
      icon: <Shield size={24} />,
      trend: 5.4,
      status: 'normal' as const,
      sparkline: [65, 68, 70, 72, 75, 77, 78],
      gradient: 'emerald' as const,
    },
    {
      title: 'Predicted Hotspots',
      value: dashboardData?.predicted_hotspots || 0,
      unit: 'areas',
      icon: <MapPin size={24} />,
      trend: 33.7,
      status: 'warning' as const,
      sparkline: [2, 3, 4, 5, 6, 7, 8],
      gradient: 'cyan' as const,
    },
  ]

  const insights = [
    {
      severity: 'critical' as const,
      title: 'KR Puram Infrastructure Alert',
      description:
        'KR Puram ward is showing a 45% increase in road infrastructure complaints over the last 14 days. Predictive model indicates escalation risk of HIGH. Immediate field inspection recommended.',
      metrics: [
        { label: 'New Complaints', value: '156' },
        { label: 'Escalation Risk', value: 'HIGH' },
        { label: 'Recommended Action', value: 'Urgent' },
      ],
      action: 'View Details',
    },
    {
      severity: 'warning' as const,
      title: 'Water Supply Issues Trending',
      description:
        'Water supply complaints are trending upward across 12 wards. Current resolution rate is 34%, below the target of 65%. Supply chain review needed.',
      metrics: [
        { label: 'Affected Wards', value: '12' },
        { label: 'Resolution Rate', value: '34%' },
        { label: 'Target Rate', value: '65%' },
      ],
      action: 'Review Wards',
    },
    {
      severity: 'info' as const,
      title: 'System Performance Optimal',
      description:
        'Overall system performance metrics are within expected ranges. Park maintenance completion rate reached 89%. Continue regular monitoring.',
      metrics: [
        { label: 'Completion Rate', value: '89%' },
        { label: 'System Health', value: 'Optimal' },
        { label: 'Status', value: 'Stable' },
      ],
      action: 'View Report',
    },
  ]

  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <HeroSection
        title="Smart City Intelligence Dashboard"
        subtitle="Real-time Infrastructure & Complaint Analytics"
        summary={`Bengaluru is experiencing stable infrastructure metrics with ${dashboardData?.total_complaints.toLocaleString()} registered complaints across all wards. ${dashboardData?.high_risk_areas} areas flagged as high-risk requiring immediate attention. Overall system health at ${dashboardData?.infrastructure_health}%.`}
        alerts={[
          { count: dashboardData?.high_risk_areas || 0, label: 'Critical Areas', severity: 'critical' },
          { count: 156, label: 'New Issues (24h)', severity: 'warning' },
          { count: dashboardData?.open_complaints || 0, label: 'Open Tickets', severity: 'info' },
        ]}
      />

      {/* Filters */}
      <AdvancedFilters
        filters={[
          {
            id: 'dateRange',
            label: 'Date Range',
            value: filters.dateRange,
            type: 'date',
          },
          {
            id: 'issueTypes',
            label: 'Issue Type',
            value: filters.issueTypes,
            type: 'multiselect',
            options: [
              { label: 'Road Damage', value: 'Road Damage' },
              { label: 'Drainage Issues', value: 'Drainage Issues' },
              { label: 'Street Light Out', value: 'Street Light Out' },
              { label: 'Pothole', value: 'Pothole' },
              { label: 'Garbage Accumulation', value: 'Garbage Accumulation' },
            ],
          },
          {
            id: 'areas',
            label: 'Ward/Area',
            value: filters.areas,
            type: 'multiselect',
            options: [
              { label: 'Ward 1', value: 'Ward 1' },
              { label: 'Ward 5', value: 'Ward 5' },
              { label: 'Ward 10', value: 'Ward 10' },
              { label: 'Ward 15', value: 'Ward 15' },
              { label: 'Ward 50', value: 'Ward 50' },
            ],
          },
          {
            id: 'severity',
            label: 'Risk Level',
            value: filters.severity,
            type: 'slider',
            min: 0,
            max: 10,
          },
        ]}
        onFilterChange={handleFilterChange}
        onReset={() => setFilters({
          dateRange: { start: '', end: '' },
          issueTypes: [],
          areas: [],
          severity: 3,
        })}
      />

      {/* KPI Grid */}
      <motion.div
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
      >
        {kpiData.map((kpi, idx) => (
          <KPICard key={idx} {...kpi} />
        ))}
      </motion.div>

      {/* AI Insights Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
      >
        <h2 className="text-3xl font-bold text-white mb-6">AI-Driven Insights & Alerts</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {insights.map((insight, idx) => (
            <AIInsightCard key={idx} {...insight} />
          ))}
        </div>
      </motion.div>

      {/* Live Intelligence Feed */}
      <motion.div
        className="glass-premium rounded-2xl border border-white/10 p-6"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.35 }}
      >
        <div className="flex items-center gap-2 mb-6">
          <Activity className="text-cyan-400" size={24} />
          <h2 className="text-2xl font-bold text-white">Live Intelligence Feed</h2>
          <div className="ml-auto flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-red-500 animate-pulse" />
            <span className="text-[10px] text-white/50 uppercase tracking-widest font-bold">Real-time Stream</span>
          </div>
        </div>

        <div className="space-y-4">
          <AnimatePresence mode="popLayout">
            {liveFeed.map((item) => (
              <motion.div
                key={item.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, scale: 0.95 }}
                className="flex items-center gap-4 p-4 rounded-xl bg-white/5 border border-white/5 hover:bg-white/8 transition-all group"
              >
                <div className={`p-2 rounded-lg ${
                  item.severity === 'critical' ? 'bg-red-500/20 text-red-400' : 
                  item.severity === 'warning' ? 'bg-orange-500/20 text-orange-400' : 'bg-emerald-500/20 text-emerald-400'
                }`}>
                  {item.type === 'prediction' ? <Sparkles size={18} /> : <AlertCircle size={18} />}
                </div>
                <div className="flex-1">
                  <p className="text-sm text-white font-medium">{item.text}</p>
                  <p className="text-xs text-white/40">{item.time}</p>
                </div>
                <button className="opacity-0 group-hover:opacity-100 px-3 py-1 rounded-md bg-white/10 text-[10px] text-white font-bold transition-all uppercase tracking-wider">
                  Investigate
                </button>
              </motion.div>
            ))}
          </AnimatePresence>
        </div>
      </motion.div>

      {/* Trend Charts */}
      <motion.div
        className="grid grid-cols-1 lg:grid-cols-2 gap-6"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
      >
        <PremiumChart
          title="Complaint Trends & Predictions"
          type="area"
          data={trends}
          xAxisKey="date"
          yAxisKey={['complaint_count']}
          colors={['#00d9ff', '#00d98e']}
          height={300}
        />
        <PremiumChart
          title="Predicted vs Actual (Next 7 Days)"
          type="line"
          data={trends}
          xAxisKey="date"
          yAxisKey={['complaint_count']}
          colors={['#d4af37', '#00d9ff']}
          height={300}
        />
      </motion.div>

      {/* Fraud Detection & Escalation Monitoring */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.45 }}
          className="glass-premium rounded-2xl p-6 border border-white/10"
        >
          <FraudDetectionPanel />
        </motion.div>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.45 }}
          className="glass-premium rounded-2xl p-6 border border-white/10"
        >
          <EscalationRiskMonitor />
        </motion.div>
      </div>


      {/* Bottom Section - Call to Action */}
      <motion.div
        className="glass-premium rounded-2xl p-8 border border-white/10 text-center"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
      >
        <h3 className="text-2xl font-bold text-white mb-3">Need Detailed Analysis?</h3>
        <p className="text-gray-300 mb-6 max-w-2xl mx-auto">
          Explore advanced risk intelligence, hotspot predictions, ward analytics, and infrastructure trends in detail.
        </p>
        <div className="flex gap-4 justify-center">
          <motion.button
            className="btn-primary"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => window.location.hash = '#/risk-intelligence'}
          >
            View Risk Intelligence
          </motion.button>
          <motion.button
            className="btn-secondary"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleGenerateReport}
          >
            Generate Report
          </motion.button>
        </div>
      </motion.div>
    </div>
  )
}

export default Overview
