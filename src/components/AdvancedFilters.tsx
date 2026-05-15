import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { ChevronDown, X } from 'lucide-react'
import { cn } from '../utils/cn'

interface FilterItem {
  id: string
  label: string
  value: string | string[]
  type: 'date' | 'multiselect' | 'checkbox' | 'slider'
  options?: { label: string; value: string }[]
  min?: number
  max?: number
}

interface AdvancedFiltersProps {
  filters: FilterItem[]
  onFilterChange: (id: string, value: any) => void
  onReset: () => void
}

const AdvancedFilters: React.FC<AdvancedFiltersProps> = ({ filters, onFilterChange, onReset }) => {
  const [expandedId, setExpandedId] = useState<string | null>(null)
  const [tempDateRange, setTempDateRange] = useState({ start: '', end: '' })

  return (
    <motion.div
      className="glass-premium rounded-xl border border-white/10 p-6"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-lg font-bold text-white mb-1">Advanced Filters</h3>
          <p className="text-sm text-gray-400">Refine your data with intelligent filters</p>
        </div>
        <motion.button
          onClick={onReset}
          className="px-4 py-2 rounded-lg bg-white/5 hover:bg-white/10 text-sm font-semibold text-gray-300 transition-all duration-300"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          Reset All
        </motion.button>
      </div>

      {/* Filter Items */}
      <div className="space-y-3">
        {filters.map((filter) => (
          <motion.div
            key={filter.id}
            className="border border-white/5 rounded-lg overflow-hidden"
            layout
          >
            {/* Filter Header */}
            <motion.button
              onClick={() => setExpandedId(expandedId === filter.id ? null : filter.id)}
              className="w-full px-4 py-3 flex items-center justify-between bg-white/5 hover:bg-white/10 transition-colors duration-300"
              whileHover={{ x: 4 }}
            >
              <span className="font-semibold text-white text-left">{filter.label}</span>
              <motion.div
                animate={{ rotate: expandedId === filter.id ? 180 : 0 }}
                transition={{ duration: 0.3 }}
              >
                <ChevronDown size={20} className="text-white" />
              </motion.div>
            </motion.button>

            {/* Filter Content */}
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{
                height: expandedId === filter.id ? 'auto' : 0,
                opacity: expandedId === filter.id ? 1 : 0,
              }}
              transition={{ duration: 0.3 }}
              className="overflow-hidden"
            >
              <div className="p-4 bg-white/2.5 border-t border-white/5">
                {filter.type === 'date' && (
                  <div className="flex gap-3">
                    <input
                      type="date"
                      className="flex-1 bg-white/10 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:ring-2 focus:ring-grey-400"
                      onChange={(e) => setTempDateRange({ ...tempDateRange, start: e.target.value })}
                    />
                    <input
                      type="date"
                      className="flex-1 bg-white/10 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:ring-2 focus:ring-grey-400"
                      onChange={(e) => setTempDateRange({ ...tempDateRange, end: e.target.value })}
                    />
                    <button
                      onClick={() => onFilterChange(filter.id, tempDateRange)}
                      className="px-4 py-2 bg-white text-black font-semibold rounded-lg hover:shadow-glow transition-all duration-300"
                    >
                      Apply
                    </button>
                  </div>
                )}

                {filter.type === 'multiselect' && filter.options && (
                  <div className="space-y-2">
                    {filter.options.map((option) => (
                      <label
                        key={option.value}
                        className="flex items-center gap-3 p-2 rounded-lg hover:bg-white/5 cursor-pointer transition-colors duration-300"
                      >
                        <input
                          type="checkbox"
                          className="w-4 h-4 rounded accent-white"
                          onChange={(e) => {
                            const currentValues = Array.isArray(filter.value) ? filter.value : []
                            if (e.target.checked) {
                              onFilterChange(filter.id, [...currentValues, option.value])
                            } else {
                              onFilterChange(
                                filter.id,
                                currentValues.filter((v) => v !== option.value)
                              )
                            }
                          }}
                        />
                        <span className="text-sm text-gray-300">{option.label}</span>
                      </label>
                    ))}
                  </div>
                )}

                {filter.type === 'slider' && filter.min !== undefined && filter.max !== undefined && (
                  <div className="space-y-4">
                    <input
                      type="range"
                      min={filter.min}
                      max={filter.max}
                      className="w-full h-2 bg-white/20 rounded-lg appearance-none cursor-pointer accent-white"
                      onChange={(e) => onFilterChange(filter.id, e.target.value)}
                    />
                    <div className="text-sm text-gray-300">
                      {filter.min} - {filter.value} {filter.max}
                    </div>
                  </div>
                )}
              </div>
            </motion.div>
          </motion.div>
        ))}
      </div>
    </motion.div>
  )
}

export default AdvancedFilters
