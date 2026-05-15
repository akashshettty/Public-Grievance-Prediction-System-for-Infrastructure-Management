import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { ChevronUp, ChevronDown, Download, Filter } from 'lucide-react'
import { cn } from '../utils/cn'

interface Column {
  key: string
  label: string
  width?: string
  align?: 'left' | 'center' | 'right'
}

interface Row {
  id: string
  [key: string]: any
}

interface PremiumTableProps {
  columns: Column[]
  rows: Row[]
  onRowClick?: (row: Row) => void
  expandable?: boolean
  expandRender?: (row: Row) => React.ReactNode
  sortable?: boolean
  defaultSort?: { key: string; direction: 'asc' | 'desc' }
  onSort?: (key: string, direction: 'asc' | 'desc') => void
}

const PremiumTable: React.FC<PremiumTableProps> = ({
  columns,
  rows,
  onRowClick,
  expandable = false,
  expandRender,
  sortable = true,
  defaultSort,
  onSort,
}) => {
  const [expandedRows, setExpandedRows] = useState<string[]>([])
  const [sortConfig, setSortConfig] = useState(defaultSort)

  const handleSort = (key: string) => {
    if (!sortable) return
    let direction: 'asc' | 'desc' = 'asc'
    if (sortConfig?.key === key && sortConfig.direction === 'asc') {
      direction = 'desc'
    }
    setSortConfig({ key, direction })
    onSort?.(key, direction)
  }

  const toggleRow = (id: string) => {
    setExpandedRows((prev) =>
      prev.includes(id) ? prev.filter((r) => r !== id) : [...prev, id]
    )
  }

  const getSortIcon = (key: string) => {
    if (sortConfig?.key !== key) return <ChevronUp size={16} className="text-gray-500" />
    return sortConfig.direction === 'asc' ? (
      <ChevronUp size={16} className="text-neon-cyan" />
    ) : (
      <ChevronDown size={16} className="text-neon-cyan" />
    )
  }

  return (
    <motion.div
      className="glass-premium rounded-2xl border border-white/10 overflow-hidden"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full">
          {/* Header */}
          <thead>
            <tr className="border-b border-white/10 bg-white/5">
              {expandable && <th className="w-12 px-4 py-4" />}
              {columns.map((col) => (
                <th
                  key={col.key}
                  className={cn(
                    'px-6 py-4 text-left font-semibold text-gray-300 uppercase tracking-wider text-xs',
                    col.width && `w-${col.width}`,
                    col.align && `text-${col.align}`
                  )}
                  onClick={() => handleSort(col.key)}
                  style={{ cursor: sortable ? 'pointer' : 'default' }}
                >
                  <div className="flex items-center gap-2 hover:text-white transition-colors duration-300">
                    {col.label}
                    {sortable && getSortIcon(col.key)}
                  </div>
                </th>
              ))}
            </tr>
          </thead>

          {/* Body */}
          <tbody>
            {rows.map((row, idx) => (
              <motion.tr
                key={row.id}
                className="border-b border-white/5 hover:bg-white/5 transition-colors duration-300 cursor-pointer"
                onClick={() => onRowClick?.(row)}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: idx * 0.05, duration: 0.3 }}
              >
                {expandable && (
                  <td className="w-12 px-4 py-4">
                    <motion.button
                      onClick={(e) => {
                        e.stopPropagation()
                        toggleRow(row.id)
                      }}
                      whileHover={{ scale: 1.1 }}
                      whileTap={{ scale: 0.95 }}
                      className="flex items-center justify-center w-8 h-8 rounded-lg hover:bg-white/10"
                    >
                      <motion.div
                        animate={{ rotate: expandedRows.includes(row.id) ? 180 : 0 }}
                        transition={{ duration: 0.3 }}
                      >
                        <ChevronDown size={16} className="text-neon-cyan" />
                      </motion.div>
                    </motion.button>
                  </td>
                )}

                {columns.map((col) => (
                  <td
                    key={`${row.id}-${col.key}`}
                    className={cn('px-6 py-4 text-sm text-gray-300', col.align && `text-${col.align}`)}
                  >
                    {row[col.key]}
                  </td>
                ))}
              </motion.tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Expanded Rows */}
      {expandable &&
        rows.map((row) =>
          expandedRows.includes(row.id) ? (
            <motion.div
              key={`expanded-${row.id}`}
              className="border-b border-white/10 bg-white/2.5 px-6 py-4"
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              transition={{ duration: 0.3 }}
            >
              {expandRender?.(row)}
            </motion.div>
          ) : null
        )}

      {/* Footer with pagination or stats */}
      {rows.length > 0 && (
        <div className="px-6 py-4 border-t border-white/10 bg-white/2.5 flex items-center justify-between text-sm text-gray-400">
          <span>Showing {rows.length} results</span>
          <motion.button
            className="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-white/10 transition-colors duration-300"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <Download size={16} />
            Export
          </motion.button>
        </div>
      )}
    </motion.div>
  )
}

export default PremiumTable
