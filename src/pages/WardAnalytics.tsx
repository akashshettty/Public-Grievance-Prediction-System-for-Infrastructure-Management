import React from 'react'
import { motion } from 'framer-motion'
import HeroSection from '../components/HeroSection'
import KPICard from '../components/KPICard'
import PremiumChart from '../components/PremiumChart'
import PremiumTable from '../components/PremiumTable'
import { BarChart3, Users, Zap, TrendingDown } from 'lucide-react'

const WardAnalytics: React.FC = () => {
  const wardData = [
    { id: '1', ward: 'KR Puram', complaints: 156, open: 45, resolved: 111, resolutionRate: 71, severity: 8.2, population: '450K' },
    { id: '2', ward: 'Indiranagar', complaints: 124, open: 32, resolved: 92, resolutionRate: 74, severity: 7.1, population: '380K' },
    { id: '3', ward: 'Whitefield', complaints: 98, open: 18, resolved: 80, resolutionRate: 82, severity: 5.8, population: '320K' },
    { id: '4', ward: 'Marathahalli', complaints: 72, open: 12, resolved: 60, resolutionRate: 83, severity: 4.5, population: '280K' },
    { id: '5', ward: 'Koramangala', complaints: 56, open: 8, resolved: 48, resolutionRate: 86, severity: 3.2, population: '200K' },
  ]

  const comparisonData = [
    { ward: 'KR Puram', complaints: 156, avgResTime: 4.2, efficiency: 71 },
    { ward: 'Indiranagar', complaints: 124, avgResTime: 3.8, efficiency: 74 },
    { ward: 'Whitefield', complaints: 98, avgResTime: 2.9, efficiency: 82 },
    { ward: 'Marathahalli', complaints: 72, avgResTime: 2.4, efficiency: 83 },
    { ward: 'Koramangala', complaints: 56, avgResTime: 1.9, efficiency: 86 },
  ]

  const issueTypeData = [
    { ward: 'KR Puram', road: 62, water: 45, drainage: 28, lights: 21 },
    { ward: 'Indiranagar', road: 48, water: 38, drainage: 22, lights: 16 },
    { ward: 'Whitefield', road: 35, water: 28, drainage: 18, lights: 17 },
    { ward: 'Marathahalli', road: 28, water: 22, drainage: 14, lights: 8 },
    { ward: 'Koramangala', road: 22, water: 18, drainage: 10, lights: 6 },
  ]

  return (
    <div className="space-y-12">
      {/* Hero */}
      <HeroSection
        title="Ward-Level Analytics"
        subtitle="Granular Performance & Complaint Analysis by Area"
        summary="Comprehensive analysis across 5 major wards shows KR Puram with highest complaint volume (156) but improving resolution rate (71%). Indiranagar demonstrates better performance with 74% resolution rate. Road infrastructure is consistent top issue across all wards (38% of complaints). Population-weighted insights guide resource allocation."
        alerts={[
          { count: 506, label: 'Total Complaints', severity: 'info' },
          { count: 115, label: 'Open Issues', severity: 'warning' },
          { count: 391, label: 'Resolved', severity: 'info' },
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
          title="Total Wards"
          value={5}
          unit="monitored"
          icon={<BarChart3 size={24} />}
          gradient="cyan"
        />
        <KPICard
          title="Avg Resolution Rate"
          value={79}
          unit="%"
          icon={<TrendingDown size={24} />}
          trend={8.3}
          gradient="emerald"
        />
        <KPICard
          title="Avg Response Time"
          value={3.0}
          unit="hours"
          icon={<Zap size={24} />}
          trend={-18.5}
          gradient="gold"
        />
        <KPICard
          title="Population Served"
          value={1.63}
          unit="M+  people"
          icon={<Users size={24} />}
          gradient="purple"
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
          title="Ward Comparison - Complaint Volume vs Resolution"
          type="bar"
          data={comparisonData}
          xAxisKey="ward"
          yAxisKey={['complaints', 'efficiency']}
          colors={['#00d9ff', '#00d98e']}
        />
        <PremiumChart
          title="Issue Type Distribution by Ward"
          type="bar"
          data={issueTypeData}
          xAxisKey="ward"
          yAxisKey={['road', 'water', 'drainage', 'lights']}
          colors={['#ff006e', '#ffd700', '#00d9ff', '#00d98e']}
        />
      </motion.div>

      {/* Ward Details Table */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
      >
        <h2 className="text-3xl font-bold text-white mb-6">Ward Performance Details</h2>
        <PremiumTable
          columns={[
            { key: 'ward', label: 'Ward/Area', width: '150px' },
            { key: 'complaints', label: 'Total Complaints', align: 'center' },
            { key: 'open', label: 'Open', align: 'center' },
            { key: 'resolved', label: 'Resolved', align: 'center' },
            { key: 'resolutionRate', label: 'Resolution %', align: 'center' },
            { key: 'severity', label: 'Avg Severity', align: 'center' },
            { key: 'population', label: 'Population' },
          ]}
          rows={wardData}
          expandable
          expandRender={(row) => (
            <div className="grid grid-cols-3 gap-4">
              <div>
                <p className="text-xs text-gray-400 mb-2">Key Metrics</p>
                <div className="space-y-1 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-300">Open Rate: </span>
                    <span className="text-rose-accent font-semibold">{Math.round(row.open / row.complaints * 100)}%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-300">Severity Avg: </span>
                    <span className="text-neon-cyan font-semibold">{row.severity}/10</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-300">Status: </span>
                    <span className="text-emerald-accent font-semibold">On Track</span>
                  </div>
                </div>
              </div>
              <div>
                <p className="text-xs text-gray-400 mb-2">Top Issues</p>
                <ul className="space-y-1 text-sm text-gray-300">
                  <li>1. Road Maintenance</li>
                  <li>2. Water Supply</li>
                  <li>3. Drainage System</li>
                </ul>
              </div>
              <div>
                <p className="text-xs text-gray-400 mb-2">Recommendations</p>
                <ul className="space-y-1 text-sm text-gray-300">
                  <li>✓ Increase maintenance frequency</li>
                  <li>✓ Staff 2-3 more teams</li>
                  <li>✓ Infrastructure inspection</li>
                </ul>
              </div>
            </div>
          )}
        />
      </motion.div>
    </div>
  )
}

export default WardAnalytics
