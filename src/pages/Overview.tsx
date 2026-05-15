import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
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
  Clock,
  TrendingUp,
  Users,
  Shield,
  MapPin,
  Zap,
} from 'lucide-react'

const Overview: React.FC = () => {
  const [loading, setLoading] = useState(true)
  const [filters, setFilters] = useState({
    dateRange: { start: '', end: '' },
    issueTypes: [],
    areas: [],
    severity: 3,
  })

  useEffect(() => {
    // Simulate data loading
    const timer = setTimeout(() => setLoading(false), 1500)
    return () => clearTimeout(timer)
  }, [])

  const handleFilterChange = (id: string, value: any) => {
    setFilters((prev) => ({ ...prev, [id]: value }))
  }

  if (loading) {
    return <SkeletonLoader count={6} />
  }

  // Mock data
  const kpiData = [
    {
      title: 'Total Complaints',
      value: 12458,
      unit: 'filed',
      icon: <Activity size={24} />,
      trend: 12.5,
      status: 'normal' as const,
      sparkline: [45, 52, 48, 61, 55, 67, 72],
      gradient: 'cyan' as const,
    },
    {
      title: 'Open Issues',
      value: 3247,
      unit: 'pending',
      icon: <AlertTriangle size={24} />,
      trend: -8.2,
      status: 'warning' as const,
      sparkline: [80, 72, 68, 75, 62, 58, 52],
      gradient: 'rose' as const,
    },
    {
      title: 'High-Risk Areas',
      value: 24,
      unit: 'zones',
      icon: <Zap size={24} />,
      trend: 15.3,
      status: 'critical' as const,
      sparkline: [12, 14, 16, 18, 20, 22, 24],
      gradient: 'gold' as const,
    },
    {
      title: 'Avg Response Time',
      value: 4.2,
      unit: 'hours',
      icon: <Clock size={24} />,
      trend: -22.1,
      status: 'normal' as const,
      sparkline: [8, 7.5, 6.8, 6.2, 5.5, 4.8, 4.2],
      gradient: 'purple' as const,
    },
    {
      title: 'Infrastructure Health',
      value: 78,
      unit: '%',
      icon: <Shield size={24} />,
      trend: 5.4,
      status: 'normal' as const,
      sparkline: [65, 68, 70, 72, 75, 77, 78],
      gradient: 'emerald' as const,
    },
    {
      title: 'Predicted Hotspots',
      value: 8,
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

  const trendData = [
    { date: 'Jan 1', complaints: 420, resolved: 380, predicted: 410 },
    { date: 'Jan 8', complaints: 450, resolved: 395, predicted: 440 },
    { date: 'Jan 15', complaints: 480, resolved: 410, predicted: 470 },
    { date: 'Jan 22', complaints: 510, resolved: 430, predicted: 520 },
    { date: 'Jan 29', complaints: 540, resolved: 450, predicted: 550 },
    { date: 'Feb 5', complaints: 580, resolved: 480, predicted: 600 },
    { date: 'Feb 12', complaints: 620, resolved: 510, predicted: 640 },
  ]

  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <HeroSection
        title="Smart City Intelligence Dashboard"
        subtitle="Real-time Infrastructure & Complaint Analytics"
        summary="Bengaluru is experiencing stable infrastructure metrics with 12,458 registered complaints across all wards. 24 areas flagged as high-risk requiring immediate attention. Overall system health at 78%. AI recommends prioritizing water supply and road infrastructure interventions."
        alerts={[
          { count: 24, label: 'Critical Areas', severity: 'critical' },
          { count: 156, label: 'New Issues (24h)', severity: 'warning' },
          { count: 3247, label: 'Open Tickets', severity: 'info' },
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
              { label: 'Road Maintenance', value: 'road' },
              { label: 'Water Supply', value: 'water' },
              { label: 'Street Light', value: 'light' },
              { label: 'Park Maintenance', value: 'park' },
              { label: 'Others', value: 'other' },
            ],
          },
          {
            id: 'areas',
            label: 'Ward/Area',
            value: filters.areas,
            type: 'multiselect',
            options: [
              { label: 'KR Puram', value: 'kr_puram' },
              { label: 'Indiranagar', value: 'indiranagar' },
              { label: 'Whitefield', value: 'whitefield' },
              { label: 'Marathahalli', value: 'marathahalli' },
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
          data={trendData}
          xAxisKey="date"
          yAxisKey={['complaints', 'resolved']}
          colors={['#00d9ff', '#00d98e']}
          height={300}
        />
        <PremiumChart
          title="Predicted vs Actual (Next 7 Days)"
          type="line"
          data={trendData}
          xAxisKey="date"
          yAxisKey={['predicted', 'complaints']}
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
          >
            View Risk Intelligence
          </motion.button>
          <motion.button
            className="btn-secondary"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            Generate Report
          </motion.button>
        </div>
      </motion.div>
    </div>
  )
}

export default Overview
