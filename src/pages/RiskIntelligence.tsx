import React, { useState } from 'react'
import { motion } from 'framer-motion'
import HeroSection from '../components/HeroSection'
import KPICard from '../components/KPICard'
import PremiumChart from '../components/PremiumChart'
import PremiumTable from '../components/PremiumTable'
import AIInsightCard from '../components/AIInsightCard'
import AdvancedFilters from '../components/AdvancedFilters'
import { AlertTriangle, TrendingDown, Shield, Zap } from 'lucide-react'

const RiskIntelligence: React.FC = () => {
  const [filters, setFilters] = useState({
    riskLevel: 'all',
    areas: [],
    dateRange: { start: '', end: '' },
  })

  const riskAreaData = [
    { id: '1', area: 'KR Puram', riskScore: 87, riskLevel: 'CRITICAL', openComplaints: 145, hotspotProb: '94%', recommendation: 'Immediate intervention required' },
    { id: '2', area: 'Indiranagar', riskScore: 76, riskLevel: 'HIGH', openComplaints: 98, hotspotProb: '78%', recommendation: 'Schedule preventive maintenance' },
    { id: '3', area: 'Whitefield', riskScore: 54, riskLevel: 'MEDIUM', openComplaints: 42, hotspotProb: '45%', recommendation: 'Monitor closely' },
    { id: '4', area: 'Marathahalli', riskScore: 42, riskLevel: 'MEDIUM', openComplaints: 31, hotspotProb: '28%', recommendation: 'Routine check recommended' },
    { id: '5', area: 'Electronic City', riskScore: 28, riskLevel: 'LOW', openComplaints: 12, hotspotProb: '12%', recommendation: 'Standard monitoring' },
  ]

  const riskTrendData = [
    { month: 'Jan', highRisk: 18, mediumRisk: 32, lowRisk: 50 },
    { month: 'Feb', highRisk: 21, mediumRisk: 35, lowRisk: 44 },
    { month: 'Mar', highRisk: 24, mediumRisk: 38, lowRisk: 38 },
    { month: 'Apr', highRisk: 26, mediumRisk: 40, lowRisk: 34 },
    { month: 'May', highRisk: 28, mediumRisk: 42, lowRisk: 30 },
    { month: 'Jun', highRisk: 32, mediumRisk: 45, lowRisk: 23 },
  ]

  const riskFactorData = [
    { factor: 'Road Damage', frequency: 240, severity: 8.2, trend: 15 },
    { factor: 'Water Issues', frequency: 185, severity: 7.5, trend: 22 },
    { factor: 'Drainage Blocks', frequency: 142, severity: 6.8, trend: -5 },
    { factor: 'Street Lights', frequency: 98, severity: 5.2, trend: 8 },
    { factor: 'Park Maintenance', frequency: 76, severity: 4.1, trend: -12 },
  ]

  return (
    <div className="space-y-12">
      {/* Hero */}
      <HeroSection
        title="Risk Intelligence Center"
        subtitle="Advanced Risk Scoring & Area Assessment"
        summary="Our AI risk engine has identified 28 areas with elevated risk levels. KR Puram requires immediate intervention with 94% hotspot probability. Current trend shows risk escalation in 65% of monitored areas. Recommend deploying resources to high-risk zones."
        alerts={[
          { count: 5, label: 'Critical Areas', severity: 'critical' },
          { count: 12, label: 'High Risk Zones', severity: 'warning' },
          { count: 43, label: 'Normal Areas', severity: 'info' },
        ]}
      />

      {/* KPI Cards */}
      <motion.div
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
      >
        <KPICard
          title="Avg Risk Score"
          value={62}
          unit="/100"
          icon={<AlertTriangle size={24} />}
          trend={18.5}
          status="warning"
          gradient="rose"
        />
        <KPICard
          title="Critical Areas"
          value={5}
          unit="zones"
          icon={<Zap size={24} />}
          trend={25.0}
          status="critical"
          gradient="gold"
        />
        <KPICard
          title="Risk Escalation"
          value={32}
          unit="%"
          icon={<TrendingDown size={24} />}
          trend={-12.3}
          status="normal"
          gradient="emerald"
        />
        <KPICard
          title="Coverage"
          value={98}
          unit="%"
          icon={<Shield size={24} />}
          trend={2.1}
          status="normal"
          gradient="cyan"
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
          title="Risk Area Distribution Trend"
          type="bar"
          data={riskTrendData}
          xAxisKey="month"
          yAxisKey={['highRisk', 'mediumRisk', 'lowRisk']}
          colors={['#ff006e', '#ffd700', '#00d98e']}
        />
        <PremiumChart
          title="Top Risk Factors & Severity"
          type="bar"
          data={riskFactorData}
          xAxisKey="factor"
          yAxisKey={['severity']}
          colors={['#ff006e']}
        />
      </motion.div>

      {/* Risk Areas Table */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
      >
        <h2 className="text-3xl font-bold text-white mb-6">High-Risk Areas Overview</h2>
        <PremiumTable
          columns={[
            { key: 'area', label: 'Ward/Area', width: '200px' },
            { key: 'riskScore', label: 'Risk Score', align: 'center' },
            { key: 'riskLevel', label: 'Risk Level', align: 'center' },
            { key: 'openComplaints', label: 'Open Issues', align: 'center' },
            { key: 'hotspotProb', label: 'Hotspot Prob.', align: 'center' },
            { key: 'recommendation', label: 'AI Recommendation' },
          ]}
          rows={riskAreaData}
          expandable
          expandRender={(row) => (
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-xs text-gray-400 mb-1">Risk Score Breakdown</p>
                <div className="space-y-1">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-300">Infrastructure: </span>
                    <span className="text-neon-cyan font-semibold">78/100</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-300">Complaint Volume: </span>
                    <span className="text-neon-cyan font-semibold">85/100</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-300">Resolution Rate: </span>
                    <span className="text-emerald-accent font-semibold">62/100</span>
                  </div>
                </div>
              </div>
              <div>
                <p className="text-xs text-gray-400 mb-1">Recommended Actions</p>
                <ul className="space-y-1 text-sm text-gray-300">
                  <li>• Increase field teams by 30%</li>
                  <li>• Priority maintenance schedule</li>
                  <li>• Weekly oversight meetings</li>
                </ul>
              </div>
            </div>
          )}
        />
      </motion.div>

      {/* AI Insights */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
      >
        <h2 className="text-3xl font-bold text-white mb-6">AI Risk Analysis</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <AIInsightCard
            severity="critical"
            title="KR Puram Crisis Alert"
            description="Infrastructure deterioration rate of 0.8%/day detected. At current rate, critical failure likely within 8-12 days. Immediate large-scale intervention essential."
            metrics={[
              { label: 'Failure Risk Timeline', value: '8-12 days' },
              { label: 'Required Budget', value: '₹2.4 Cr' },
              { label: 'Team Size Needed', value: '250+' },
            ]}
            action="Escalate to Management"
          />
          <AIInsightCard
            severity="warning"
            title="Water Supply Bottleneck"
            description="Correlation detected between complaint volume and seasonal water shortage. Predictive maintenance shows potential 40% issue reduction with proactive supply enhancement."
            metrics={[
              { label: 'Potential Reduction', value: '40%' },
              { label: 'Intervention Cost', value: '₹1.2 Cr' },
              { label: 'Implementation Time', value: '4-6 weeks' },
            ]}
            action="View Plan"
          />
        </div>
      </motion.div>
    </div>
  )
}

export default RiskIntelligence
