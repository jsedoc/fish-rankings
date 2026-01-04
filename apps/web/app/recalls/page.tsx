'use client'

export const dynamic = 'force-dynamic'

import { useState, useEffect } from 'react'

import { AlertTriangle, AlertCircle, Info, ArrowLeft, Calendar, MapPin, Building, Search } from 'lucide-react'
import Link from 'next/link'

interface Recall {
  id: string
  recall_number: string
  product_description: string
  reason_for_recall: string
  recall_date: string
  report_date: string
  company_name: string
  city?: string | null
  state?: string | null
  classification: string
  status: string
  distribution_pattern?: string | null
  product_quantity?: string
}

interface RecallStats {
  period_days: number
  total_recalls: number
  by_classification: Record<string, number>
  by_status: Record<string, number>
  top_states: Record<string, number>
  critical_recalls: number
}

interface RecallResponse {
  recalls: Recall[]
  total: number
  skip: number
  limit: number
}

export default function RecallsPage() {
  const [recalls, setRecalls] = useState<Recall[]>([])
  const [stats, setStats] = useState<RecallStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState<'all' | 'Class I' | 'Class II' | 'Class III'>('all')
  const [searchQuery, setSearchQuery] = useState('')
  const [debouncedQuery, setDebouncedQuery] = useState('')

  // Debounced search from main branch
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedQuery(searchQuery)
    }, 500)
    return () => clearTimeout(timer)
  }, [searchQuery])

  useEffect(() => {
    fetchRecalls()
    fetchStats()
  }, [filter, debouncedQuery])

  const fetchRecalls = async () => {
    setLoading(true)
    try {
      let url: string
      if (debouncedQuery) {
        // Use search endpoint when searching
        url = `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/recalls?search=${encodeURIComponent(debouncedQuery)}&limit=50`
      } else if (filter === 'all') {
        url = `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/recalls?limit=50&days=90`
      } else {
        url = `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/recalls?classification=${filter}&limit=50&days=90`
      }

      const response = await fetch(url)
      const data = await response.json()

      // Handle both response formats
      const recallList = Array.isArray(data) ? data : (data.recalls || [])
      setRecalls(recallList)
    } catch (err) {
      console.error('Failed to fetch recalls:', err)
    } finally {
      setLoading(false)
    }
  }

  const fetchStats = async () => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/recalls/stats/summary?days=90`)
      const data = await response.json()
      setStats(data)
    } catch (err) {
      console.error('Failed to fetch stats:', err)
    }
  }

  const getClassificationColor = (classification: string) => {
    const colors: Record<string, string> = {
      'Class I': 'bg-red-100 text-red-800 border-red-300',
      'Class II': 'bg-orange-100 text-orange-800 border-orange-300',
      'Class III': 'bg-yellow-100 text-yellow-800 border-yellow-300',
    }
    return colors[classification] || 'bg-gray-100 text-gray-800 border-gray-300'
  }

  const getSeverityIcon = (classification: string) => {
    if (classification === 'Class I') return <AlertTriangle className="w-5 h-5 text-red-600" />
    if (classification === 'Class II') return <AlertCircle className="w-5 h-5 text-orange-600" />
    return <Info className="w-5 h-5 text-yellow-600" />
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header - Sticky from main branch */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <Link href="/" className="flex items-center space-x-2 text-gray-600 hover:text-gray-900">
              <ArrowLeft className="w-5 h-5" />
              <span>Back to Home</span>
            </Link>
            <h1 className="text-xl font-bold text-gray-900">FDA Food Recalls</h1>
            <div className="w-24"></div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 py-12">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <div className="w-20 h-20 bg-gradient-to-br from-red-500 to-orange-500 rounded-2xl flex items-center justify-center mx-auto mb-6">
            <AlertTriangle className="w-10 h-10 text-white" />
          </div>
          <h2 className="text-4xl font-bold text-gray-900 mb-4">FDA Food Recalls</h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Stay informed about food safety recalls from the FDA. Check if products you purchased are affected.
          </p>
        </div>

        {/* Stats Cards */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div className="bg-white rounded-xl shadow-sm p-6">
              <div className="text-3xl font-bold text-gray-900">{stats.total_recalls}</div>
              <div className="text-sm text-gray-600 mt-1">Total Recalls (90 days)</div>
            </div>
            <div className="bg-red-50 rounded-xl shadow-sm p-6 border border-red-200">
              <div className="text-3xl font-bold text-red-900">{stats.critical_recalls}</div>
              <div className="text-sm text-red-700 mt-1">Critical (Class I)</div>
            </div>
            <div className="bg-orange-50 rounded-xl shadow-sm p-6 border border-orange-200">
              <div className="text-3xl font-bold text-orange-900">{stats.by_classification['Class II'] || 0}</div>
              <div className="text-sm text-orange-700 mt-1">High Risk (Class II)</div>
            </div>
            <div className="bg-yellow-50 rounded-xl shadow-sm p-6 border border-yellow-200">
              <div className="text-3xl font-bold text-yellow-900">{stats.by_classification['Class III'] || 0}</div>
              <div className="text-sm text-yellow-700 mt-1">Moderate (Class III)</div>
            </div>
          </div>
        )}

        {/* Filters & Search */}
        <div className="bg-white rounded-xl shadow-sm p-6 mb-8">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search recalls by product, company, or reason..."
                  className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
                />
              </div>
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => setFilter('all')}
                className={`px-4 py-3 rounded-lg font-medium transition-colors ${filter === 'all' ? 'bg-red-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
              >
                All
              </button>
              <button
                onClick={() => setFilter('Class I')}
                className={`px-4 py-3 rounded-lg font-medium transition-colors ${filter === 'Class I' ? 'bg-red-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
              >
                Critical
              </button>
              <button
                onClick={() => setFilter('Class II')}
                className={`px-4 py-3 rounded-lg font-medium transition-colors ${filter === 'Class II' ? 'bg-red-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
              >
                High
              </button>
              <button
                onClick={() => setFilter('Class III')}
                className={`px-4 py-3 rounded-lg font-medium transition-colors ${filter === 'Class III' ? 'bg-red-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
              >
                Moderate
              </button>
            </div>
          </div>
        </div>

        {/* Classification Legend */}
        <div className="bg-blue-50 border border-blue-200 rounded-xl p-6 mb-8">
          <h3 className="font-semibold text-blue-900 mb-4">Understanding Recall Classifications</h3>
          <div className="grid md:grid-cols-3 gap-4 text-sm">
            <div>
              <div className="font-semibold text-red-800 mb-1">Class I - Critical</div>
              <p className="text-gray-700">Dangerous products that may cause serious health problems or death</p>
            </div>
            <div>
              <div className="font-semibold text-orange-800 mb-1">Class II - High Risk</div>
              <p className="text-gray-700">May cause temporary health problems or slight threat of serious nature</p>
            </div>
            <div>
              <div className="font-semibold text-yellow-800 mb-1">Class III - Moderate</div>
              <p className="text-gray-700">Unlikely to cause adverse health consequences</p>
            </div>
          </div>
        </div>

        {/* Recalls List */}
        {loading ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-red-600 mx-auto"></div>
            <p className="text-gray-600 mt-4">Loading recalls...</p>
          </div>
        ) : recalls.length === 0 ? (
          <div className="bg-white rounded-xl shadow-sm p-12 text-center">
            <Info className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 mb-2">No Recalls Found</h3>
            <p className="text-gray-600">Try adjusting your search or filters.</p>
          </div>
        ) : (
          <div className="space-y-4">
            {recalls.map((recall) => (
              <div key={recall.id} className="bg-white rounded-xl shadow-sm border-l-4 border-red-500 p-6 hover:shadow-md transition-shadow">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-start space-x-3">
                    {getSeverityIcon(recall.classification)}
                    <div>
                      <span className={`inline-block px-3 py-1 rounded-full text-xs font-semibold border ${getClassificationColor(recall.classification)}`}>
                        {recall.classification}
                      </span>
                      <span className="ml-2 text-xs text-gray-500">#{recall.recall_number}</span>
                    </div>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-xs font-medium ${recall.status === 'Ongoing' ? 'bg-red-100 text-red-800' : 'bg-gray-100 text-gray-800'
                    }`}>
                    {recall.status}
                  </span>
                </div>

                <h3 className="text-lg font-semibold text-gray-900 mb-2">{recall.product_description}</h3>

                <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
                  <div className="font-medium text-red-900 mb-1">Recall Reason:</div>
                  <p className="text-red-800">{recall.reason_for_recall}</p>
                </div>

                <div className="grid md:grid-cols-2 gap-4 text-sm">
                  <div className="flex items-start space-x-2">
                    <Building className="w-4 h-4 text-gray-400 mt-0.5 flex-shrink-0" />
                    <div>
                      <div className="text-gray-600">Company</div>
                      <div className="font-medium text-gray-900">{recall.company_name}</div>
                    </div>
                  </div>
                  {recall.city && recall.state && (
                    <div className="flex items-start space-x-2">
                      <MapPin className="w-4 h-4 text-gray-400 mt-0.5 flex-shrink-0" />
                      <div>
                        <div className="text-gray-600">Location</div>
                        <div className="font-medium text-gray-900">{recall.city}, {recall.state}</div>
                      </div>
                    </div>
                  )}
                  <div className="flex items-start space-x-2">
                    <Calendar className="w-4 h-4 text-gray-400 mt-0.5 flex-shrink-0" />
                    <div>
                      <div className="text-gray-600">Recall Date</div>
                      <div className="font-medium text-gray-900">
                        {new Date(recall.recall_date).toLocaleDateString()}
                      </div>
                    </div>
                  </div>
                  {recall.distribution_pattern && (
                    <div className="flex items-start space-x-2">
                      <MapPin className="w-4 h-4 text-gray-400 mt-0.5 flex-shrink-0" />
                      <div>
                        <div className="text-gray-600">Distribution</div>
                        <div className="font-medium text-gray-900">{recall.distribution_pattern}</div>
                      </div>
                    </div>
                  )}
                </div>

                {recall.product_quantity && (
                  <div className="mt-4 text-sm">
                    <span className="text-gray-600">Quantity: </span>
                    <span className="text-gray-900">{recall.product_quantity}</span>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
