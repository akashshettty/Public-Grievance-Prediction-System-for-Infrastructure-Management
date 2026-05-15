import axios, { AxiosInstance } from 'axios'

const API_BASE_URL = process.env.REACT_APP_API_URL || '/api'

const api: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
})

export interface DashboardData {
  total_complaints: number
  open_complaints: number
  high_risk_areas: number
  infrastructure_health: number
  predicted_hotspots: number
  avg_response_time: number
  complaint_growth_percent: number
}

export interface ComplaintData {
  timestamp: string
  area: string
  issue_type: string
  status: string
  severity: number
  latitude: number
  longitude: number
}

export interface RiskData {
  area: string
  risk_score: number
  risk_level: 'Low' | 'Medium' | 'High' | 'Critical'
  open_complaints: number
}

export interface HotspotData {
  area: string
  prediction_probability: number
  trend: number
}

export interface AreaFeatures {
  area: string
  complaint_count: number
  avg_severity: number
  resolution_rate: number
}

export const dashboardAPI = {
  // Get dashboard KPI data
  getDashboardData: async (filters?: any) => {
    return api.get<DashboardData>('/dashboard/data', { params: filters })
  },

  // Get complaints data
  getComplaints: async (filters?: any) => {
    return api.get<ComplaintData[]>('/complaints', { params: filters })
  },

  // Get risk scores
  getRiskData: async (filters?: any) => {
    return api.get<RiskData[]>('/risk-data', { params: filters })
  },

  // Get hotspot predictions
  getHotspots: async (filters?: any) => {
    return api.get<HotspotData[]>('/hotspots', { params: filters })
  },

  // Get area features
  getAreaFeatures: async () => {
    return api.get<AreaFeatures[]>('/area-features')
  },

  // Get heatmap data
  getHeatmapData: async (filters?: any) => {
    return api.get('/heatmap', { params: filters })
  },

  // Get insights
  getInsights: async (filters?: any) => {
    return api.get<string[]>('/insights', { params: filters })
  },

  // Get trends
  getTrends: async (filters?: any) => {
    return api.get('/trends', { params: filters })
  },
}

export const aiIntelligenceAPI = {
  // NLP Analysis for custom text
  analyzeText: async (text: string) => {
    return api.post('/ai/analyze-text', { text })
  },

  // Get complete Digital Twin summary
  getDigitalTwinSummary: async () => {
    return api.get('/ai/digital-twin/summary')
  },

  // Get failure predictions
  getFailurePredictions: async () => {
    return api.get('/ai/failure-prediction')
  },

  // Get fraud alerts
  getFraudAlerts: async () => {
    return api.get('/ai/fraud-detection')
  },

  // Get resource optimization recommendations
  getResourceOptimizations: async () => {
    return api.get('/ai/resource-optimization')
  },

  // Get escalation risks
  getEscalationRisks: async () => {
    return api.get('/ai/escalation-risks')
  }
}

export default api
