import React from 'react'
import { motion } from 'framer-motion'
import { Menu, X, Home, BarChart3, Zap, Map, TrendingUp, FileText, Settings, LogOut, Brain } from 'lucide-react'
import { cn } from '../../utils/cn'

interface SidebarProps {
  isOpen: boolean
  currentPage: string
  onPageChange: (page: any) => void
}

const Sidebar: React.FC<SidebarProps> = ({ isOpen, currentPage, onPageChange }) => {
  const menuItems = [
    { id: 'overview', label: 'Overview', icon: Home },
    { id: 'ai-modules', label: 'AI Modules', icon: Brain },
    { id: 'risk', label: 'Risk Intelligence', icon: Zap },
    { id: 'hotspot', label: 'Hotspot Predictions', icon: Map },
    { id: 'ward', label: 'Ward Analytics', icon: BarChart3 },
    { id: 'infrastructure', label: 'Infrastructure Trends', icon: TrendingUp },
    { id: 'reports', label: 'Reports', icon: FileText },
  ]

  return (
    <motion.div
      initial={{ x: -300 }}
      animate={{ x: 0 }}
      transition={{ duration: 0.3 }}
      className={cn(
        "w-72 h-full glass-dark border-r border-white/10 p-6 overflow-y-auto transition-all duration-300 flex flex-col",
      )}
    >
      {/* Premium Logo Section */}
      <div className="mb-12">
        <div className="flex items-center gap-2 mb-2">
          <div className="w-10 h-10 rounded-lg bg-white flex items-center justify-center font-bold text-black text-sm">
            ⚡
          </div>
          <div>
            <p className="font-bold text-lg text-white">GrievancePredict</p>
            <p className="text-xs text-white/60">Infrastructure Management</p>
          </div>
        </div>
      </div>

      {/* Main Menu */}
      <div className="space-y-2 mb-12">
        <p className="text-xs font-semibold text-white/50 uppercase tracking-widest mb-4">Main Menu</p>
        {menuItems.map((item) => {
          const Icon = item.icon
          const isActive = currentPage === item.id
          return (
            <motion.button
              key={item.id}
              onClick={() => onPageChange(item.id)}
              className={cn(
                "w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-300",
                isActive
                  ? "bg-white text-black font-semibold shadow-lg"
                  : "text-white/70 hover:bg-white/8 hover:text-white"
              )}
              whileHover={{ x: 4 }}
              whileTap={{ scale: 0.98 }}
            >
              <Icon size={20} />
              <span className="flex-1 text-left text-sm">{item.label}</span>
              {isActive && (
                <motion.div 
                  className="w-2 h-2 rounded-full bg-black"
                  layoutId="activeIndicator"
                />
              )}
            </motion.button>
          )
        })}
      </div>

      {/* Settings & Account */}
      <div className="space-y-2 pt-6 border-t border-white/10 mt-auto">
        <button className="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-white/70 hover:bg-white/8 hover:text-white transition-all duration-300 text-sm">
          <Settings size={20} />
          <span className="flex-1 text-left">Settings</span>
        </button>
        <button className="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-white/70 hover:bg-white/8 hover:text-white transition-all duration-300 text-sm">
          <LogOut size={20} />
          <span className="flex-1 text-left">Logout</span>
        </button>
      </div>

      {/* Premium Badge */}
      <motion.div
        className="mt-12 p-4 rounded-lg border border-white/10"
        style={{ backgroundColor: 'rgba(255, 255, 255, 0.03)' }}
        whileHover={{ borderColor: 'rgba(255, 255, 255, 0.2)' }}
      >
        <p className="text-xs text-white font-semibold mb-2">⚡ PREMIUM</p>
        <p className="text-xs text-white/60 leading-relaxed">
          AI-powered grievance prediction, risk assessment, and proactive infrastructure management.
        </p>
      </motion.div>
    </motion.div>
  )
}

export default Sidebar
