import React from 'react'
import { motion } from 'framer-motion'
import { Menu, Bell, User, Settings } from 'lucide-react'
import { cn } from '../../utils/cn'

interface NavbarProps {
  onMenuClick: () => void
  sidebarOpen: boolean
}

const Navbar: React.FC<NavbarProps> = ({ onMenuClick, sidebarOpen }) => {
  return (
    <motion.nav
      className="fixed top-0 left-0 right-0 h-20 glass-dark border-b border-white/10 flex items-center justify-between px-8 z-50"
      initial={{ y: -80 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.5 }}
    >
      {/* Left Section - Logo & Menu */}
      <div className="flex items-center gap-8">
        <button
          onClick={onMenuClick}
          className="lg:hidden p-2 hover:bg-white/10 rounded-lg transition-all duration-300"
        >
          <Menu size={24} className="text-white" />
        </button>

        <motion.div
          className="flex items-center gap-3 cursor-pointer"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <motion.div
            className="w-12 h-12 rounded-xl bg-white flex items-center justify-center font-bold text-black text-lg tracking-tighter"
            whileHover={{ scale: 1.05 }}
          >
            ⚡
          </motion.div>
          <div>
            <p className="text-xl font-bold text-white">GrievancePredict</p>
            <p className="text-xs text-white/70">Infrastructure Management</p>
          </div>
        </motion.div>
      </div>

      {/* Center Section - Status */}
      <motion.div
        className="hidden md:flex items-center gap-6"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3 }}
      >
        <div className="text-center">
          <p className="text-xs text-grey-400 uppercase tracking-wider">System Status</p>
          <div className="flex items-center gap-2 mt-1">
            <motion.div
              className="w-2 h-2 bg-white rounded-full"
              animate={{ opacity: [1, 0.5, 1] }}
              transition={{ duration: 2, repeat: Infinity }}
            />
            <span className="text-sm font-semibold text-white">Live</span>
          </div>
        </div>
      </motion.div>

      {/* Right Section - Actions */}
      <motion.div
        className="flex items-center gap-4"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4 }}
      >
        {/* Notification Bell */}
        <motion.button
          className="relative p-2 hover:bg-white/10 rounded-lg transition-all duration-300"
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.95 }}
        >
          <Bell size={20} className="text-gray-300" />
          <motion.span
            className="absolute top-1 right-1 w-2 h-2 bg-rose-accent rounded-full"
            animate={{ scale: [1, 1.2, 1] }}
            transition={{ duration: 2, repeat: Infinity }}
          />
        </motion.button>

        {/* Settings */}
        <motion.button
          className="p-2 hover:bg-white/10 rounded-lg transition-all duration-300"
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.95 }}
        >
          <Settings size={20} className="text-gray-300" />
        </motion.button>

        {/* User Profile */}
        <motion.button
          className="flex items-center gap-3 px-4 py-2 rounded-lg hover:bg-white/5 transition-all duration-300 ml-4 pl-4 border-l border-white/10"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <motion.div
            className="w-8 h-8 rounded-full bg-gradient-cyan flex items-center justify-center font-bold text-midnight text-sm"
            whileHover={{ boxShadow: '0 0 20px rgba(0, 217, 255, 0.4)' }}
          >
            A
          </motion.div>
          <div className="hidden sm:block text-left">
            <p className="text-sm font-semibold text-white">Admin</p>
            <p className="text-xs text-gray-400">City Manager</p>
          </div>
        </motion.button>
      </motion.div>
    </motion.nav>
  )
}

export default Navbar
