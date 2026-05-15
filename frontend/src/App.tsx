import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import Sidebar from './components/layout/Sidebar'
import Overview from './pages/Overview'
import RiskIntelligence from './pages/RiskIntelligence'
import HotspotPredictions from './pages/HotspotPredictions'
import WardAnalytics from './pages/WardAnalytics'
import InfrastructureTrends from './pages/InfrastructureTrends'
import Reports from './pages/Reports'
import AIModules from './pages/AIModules'
import AIChatAssistant from './components/AIChatAssistant'

type PageType = 'overview' | 'risk' | 'hotspot' | 'ward' | 'infrastructure' | 'reports' | 'ai-modules'

function App() {
  const [currentPage, setCurrentPage] = useState<PageType>('overview')
  const [sidebarOpen, setSidebarOpen] = useState(true)

  const renderPage = () => {
    switch (currentPage) {
      case 'overview':
        return <Overview onPageChange={setCurrentPage} />
      case 'risk':
        return <RiskIntelligence />
      case 'hotspot':
        return <HotspotPredictions />
      case 'ward':
        return <WardAnalytics />
      case 'infrastructure':
        return <InfrastructureTrends />
      case 'reports':
        return <Reports />
      case 'ai-modules':
        return <AIModules />
      default:
        return <Overview />
    }
  }

  return (
    <div className="min-h-screen bg-midnight">
      <div className="flex h-screen">
        {sidebarOpen && (
          <Sidebar 
            isOpen={sidebarOpen}
            currentPage={currentPage}
            onPageChange={setCurrentPage}
          />
        )}
        
        <motion.main 
          className="flex-1 overflow-y-auto bg-midnight pt-0"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5 }}
        >
          <div className="p-6 md:p-8">
            {renderPage()}
          </div>
        </motion.main>
      </div>

      <AIChatAssistant />

      {/* Floating background elements */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        <motion.div 
          className="absolute top-1/4 left-1/4 w-96 h-96 bg-white/3 rounded-full blur-3xl"
          animate={{ x: [0, 50, 0], y: [0, 30, 0] }}
          transition={{ duration: 8, repeat: Infinity }}
        />
        <motion.div 
          className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-gray-400/3 rounded-full blur-3xl"
          animate={{ x: [0, -50, 0], y: [0, -30, 0] }}
          transition={{ duration: 10, repeat: Infinity }}
        />
      </div>
    </div>
  )
}

export default App
