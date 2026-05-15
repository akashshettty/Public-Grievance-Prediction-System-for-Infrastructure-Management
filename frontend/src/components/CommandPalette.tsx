import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { ChevronRight, Command } from 'lucide-react'

interface CommandPaletteItem {
  id: string
  title: string
  description: string
  action: () => void
  category: string
  shortcut?: string
}

interface CommandPaletteProps {
  items: CommandPaletteItem[]
  open: boolean
  onClose: () => void
}

const CommandPalette: React.FC<CommandPaletteProps> = ({ items, open, onClose }) => {
  const [search, setSearch] = useState('')
  const [selectedIdx, setSelectedIdx] = useState(0)

  const filtered = items.filter(
    (item) =>
      item.title.toLowerCase().includes(search.toLowerCase()) ||
      item.description.toLowerCase().includes(search.toLowerCase())
  )

  return (
    <motion.div
      className={`fixed inset-0 z-50 flex items-center justify-center ${open ? '' : 'pointer-events-none'}`}
      initial={{ opacity: 0 }}
      animate={{ opacity: open ? 1 : 0 }}
      transition={{ duration: 0.2 }}
    >
      {/* Backdrop */}
      <motion.div
        className="absolute inset-0 bg-black/50 backdrop-blur-sm"
        onClick={onClose}
        initial={{ opacity: 0 }}
        animate={{ opacity: open ? 1 : 0 }}
      />

      {/* Command Palette */}
      <motion.div
        className="relative w-full max-w-2xl bg-grey-900 border border-white/10 rounded-2xl shadow-2xl"
        initial={{ opacity: 0, scale: 0.95, y: -20 }}
        animate={{ opacity: open ? 1 : 0, scale: open ? 1 : 0.95, y: open ? 0 : -20 }}
        transition={{ duration: 0.2 }}
      >
        {/* Search Input */}
        <div className="flex items-center gap-3 px-6 py-4 border-b border-white/10">
          <Command size={20} className="text-white" />
          <input
            type="text"
            placeholder="Search commands..."
            value={search}
            onChange={(e) => {
              setSearch(e.target.value)
              setSelectedIdx(0)
            }}
            className="flex-1 bg-transparent text-white placeholder-gray-500 outline-none text-lg"
            autoFocus
          />
          <span className="text-xs text-gray-500">ESC to close</span>
        </div>

        {/* Results */}
        <div className="max-h-96 overflow-y-auto">
          {filtered.length === 0 ? (
            <div className="px-6 py-12 text-center text-gray-400">
              No commands found for "{search}"
            </div>
          ) : (
            filtered.map((item, idx) => (
              <motion.button
                key={item.id}
                className={`w-full px-6 py-3 text-left border-b border-white/5 transition-colors duration-200 ${
                  idx === selectedIdx ? 'bg-white/10' : 'hover:bg-white/5'
                }`}
                onClick={() => {
                  item.action()
                  onClose()
                }}
                whileHover={{ x: 4 }}
              >
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-semibold text-white">{item.title}</p>
                    <p className="text-xs text-gray-400">{item.description}</p>
                  </div>
                  {item.shortcut && (
                    <span className="text-xs text-gray-500 font-mono">{item.shortcut}</span>
                  )}
                </div>
              </motion.button>
            ))
          )}
        </div>
      </motion.div>
    </motion.div>
  )
}

export default CommandPalette
