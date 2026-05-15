import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import HeroSection from '../components/HeroSection'
import KPICard from '../components/KPICard'
import PremiumChart from '../components/PremiumChart'
import PremiumTable from '../components/PremiumTable'
import AIInsightCard from '../components/AIInsightCard'
import { AlertTriangle, TrendingDown, Shield, Zap } from 'lucide-react'

const RiskIntelligence: React.FC = () => {
  const [loading, setLoading] = useState(true)
  const [healthData, setHealthData] = useState<any>(null)
  const [riskStats, setRiskStats] = useState<any>(null)
  const [filters, setFilters] = useState({
    riskLevel: 'all',
    areas: [],
    dateRange: { start: '', end: '' },
  })

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true)
      try {
        const [healthRes, riskRes] = await Promise.all([
          fetch('http://localhost:5000/api/ai/infrastructure-health'),
          fetch('http://localhost:5000/api/ai/escalation-risks')
        ])
        
        const health = await healthRes.json()
        const risks = await riskRes.json()
        
        setHealthData(health)
        setRiskStats(risks)
      } catch (error) {
        console.error('Error fetching risk intelligence:', error)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])

  const riskAreaData = healthData?.health_scores?.map((s: any, i: number) => ({
    id: i.toString(),
    area: s.ward,
    riskScore: 100 - s.health_score,
    riskLevel: s.status === 'Poor' ? 'CRITICAL' : s.status === 'Fair' ? 'HIGH' : 'MEDIUM',
    openComplaints: s.total_issues,
    hotspotProb: `${(100 - s.health_score + 10).toFixed(0)}%`,
    recommendation: s.status === 'Poor' ? 'Immediate intervention required' : 'Monitor closely'
  })) || []

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

  if (loading) {
    return <div className="h-screen flex items-center justify-center text-white">Loading Risk Intelligence...</div>
  }

  return (
    <div className="space-y-12">
      {/* Hero */}
      <HeroSection
        title="Risk Intelligence Center"
        subtitle="Advanced Risk Scoring & Area Assessment"
        summary={`Our AI risk engine has identified ${healthData?.stats?.critical_areas || 0} areas with elevated risk levels. Total monitored wards: ${healthData?.stats?.areas_monitored || 0}. Current trend shows system-wide health index at ${healthData?.stats?.overall_health_score || 0}%.`}
        alerts={[
          { count: healthData?.stats?.critical_areas || 0, label: 'Critical Areas', severity: 'critical' },
          { count: riskStats?.stats?.critical_count || 0, label: 'High Risk Zones', severity: 'warning' },
          { count: (healthData?.stats?.areas_monitored || 0) - (healthData?.stats?.critical_areas || 0), label: 'Normal Areas', severity: 'info' },
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
          value={100 - (healthData?.stats?.overall_health_score || 0)}
          unit="/100"
          icon={<AlertTriangle size={24} />}
          trend={18.5}
          status="warning"
          gradient="rose"
        />
        <KPICard
          title="Critical Areas"
          value={healthData?.stats?.critical_areas || 0}
          unit="zones"
          icon={<Zap size={24} />}
          trend={25.0}
          status="critical"
          gradient="gold"
        />
        <KPICard
          title="Risk Escalation"
          value={riskStats?.stats?.critical_count || 0}
          unit="cases"
          icon={<TrendingDown size={24} />}
          trend={-12.3}
          status="normal"
          gradient="emerald"
        />
        <KPICard
          title="Accuracy"
          value={riskStats?.stats?.accuracy * 100 || 88}
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
          {riskStats?.risks?.slice(0, 2).map((risk: any, i: number) => (
            <AIInsightCard
              key={i}
              severity={risk.risk_level === 'critical' ? 'critical' : 'warning'}
              title={`${risk.ward} ${risk.issue_type} Alert`}
              description={`Infrastructure deterioration detected in ${risk.ward}. High escalation probability of ${(risk.escalation_probability * 100).toFixed(0)}%. News coverage detected: ${risk.news_coverage ? 'YES' : 'NO'}.`}
              metrics={[
                { label: 'Days Until Escalation', value: `${risk.days_until_escalation} days` },
                { label: 'Social Mentions', value: risk.social_mentions.toString() },
                { label: 'Sentiment', value: risk.sentiment },
              ]}
              action="Escalate to Management"
            />
          ))}
          {(!riskStats?.risks || riskStats.risks.length === 0) && (
            <p className="text-gray-400">No active AI risk alerts detected at this time.</p>
          )}
        </div>
      </motion.div>
    </div>
  )
}

export default RiskIntelligence
