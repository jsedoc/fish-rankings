'use client'

import { useState, useEffect } from 'react'
import { Shield, AlertTriangle, MapPin, Fish, ArrowLeft, Search } from 'lucide-react'
import Link from 'next/link'

interface Advisory {
  id: string
  state_code: string
  state_name: string
  waterbody_name: string
  waterbody_type: string
  fish_species: string[]
  contaminant_type: string
  advisory_level: string
  consumption_limit?: string
  sensitive_populations: string[]
  geographic_area?: string
  advisory_text: string
  issue_date: string
  source_url?: string
}

const US_STATES = [
  { code: 'AL', name: 'Alabama' },
  { code: 'AK', name: 'Alaska' },
  { code: 'AZ', name: 'Arizona' },
  { code: 'AR', name: 'Arkansas' },
  { code: 'CA', name: 'California' },
  { code: 'CO', name: 'Colorado' },
  { code: 'CT', name: 'Connecticut' },
  { code: 'DE', name: 'Delaware' },
  { code: 'FL', name: 'Florida' },
  { code: 'GA', name: 'Georgia' },
  // Add more states as needed
]

export default function AdvisoriesPage() {
  const [advisories, setAdvisories] = useState<Advisory[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedState, setSelectedState] = useState<string>('')
  const [searchQuery, setSearchQuery] = useState('')

  useEffect(() => {
    fetchAdvisories()
  }, [selectedState])

  const fetchAdvisories = async () => {
    setLoading(true)
    try {
      // Note: This endpoint would need to be implemented on the backend
      // For now, we'll show a placeholder
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/advisories${
          selectedState ? `?state=${selectedState}` : ''
        }`
      )

      if (response.ok) {
        const data = await response.json()
        setAdvisories(data.advisories || [])
      } else {
        // Show sample data for now
        setAdvisories([])
      }
    } catch (err) {
      console.error('Failed to fetch advisories:', err)
      setAdvisories([])
    } finally {
      setLoading(false)
    }
  }

  const getAdvisoryLevelColor = (level: string) => {
    const colors: Record<string, string> = {
      'Do Not Eat': 'bg-red-100 text-red-800 border-red-300',
      'Limited Consumption': 'bg-orange-100 text-orange-800 border-orange-300',
      'Restricted': 'bg-yellow-100 text-yellow-800 border-yellow-300',
      'Advisory': 'bg-blue-100 text-blue-800 border-blue-300',
    }
    return colors[level] || 'bg-gray-100 text-gray-800 border-gray-300'
  }

  const filteredAdvisories = advisories.filter(advisory =>
    searchQuery === '' ||
    advisory.waterbody_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    advisory.fish_species.some(fish => fish.toLowerCase().includes(searchQuery.toLowerCase())) ||
    advisory.state_name.toLowerCase().includes(searchQuery.toLowerCase())
  )

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <Link href="/" className="flex items-center space-x-2 text-gray-600 hover:text-gray-900">
              <ArrowLeft className="w-5 h-5" />
              <span>Back to Home</span>
            </Link>
            <h1 className="text-xl font-bold text-gray-900">EPA Fish Advisories</h1>
            <div className="w-24"></div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 py-12">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <div className="w-20 h-20 bg-gradient-to-br from-green-500 to-emerald-500 rounded-2xl flex items-center justify-center mx-auto mb-6">
            <Shield className="w-10 h-10 text-white" />
          </div>
          <h2 className="text-4xl font-bold text-gray-900 mb-4">EPA Fish Consumption Advisories</h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            State-specific advisories on safe fish consumption based on contaminant levels. Protect your health and that of your family.
          </p>
        </div>

        {/* Info Banner */}
        <div className="bg-blue-50 border border-blue-200 rounded-xl p-6 mb-8">
          <div className="flex items-start">
            <Shield className="w-6 h-6 text-blue-600 mt-1 mr-4 flex-shrink-0" />
            <div>
              <h3 className="font-semibold text-blue-900 mb-2">Understanding Fish Advisories</h3>
              <p className="text-blue-800 mb-4">
                Fish advisories are recommendations about eating fish caught in specific waterbodies. They're issued when
                contaminants like mercury, PCBs, or dioxins are found at levels that may pose health risks.
              </p>
              <div className="grid md:grid-cols-3 gap-4 text-sm">
                <div>
                  <div className="font-semibold text-blue-900 mb-1">Do Not Eat</div>
                  <p className="text-blue-800">Avoid consumption entirely due to high contamination</p>
                </div>
                <div>
                  <div className="font-semibold text-orange-900 mb-1">Limited Consumption</div>
                  <p className="text-orange-800">Safe to eat in limited amounts (e.g., once per month)</p>
                </div>
                <div>
                  <div className="font-semibold text-yellow-900 mb-1">Advisory</div>
                  <p className="text-yellow-800">General guidance for specific populations</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Filters */}
        <div className="bg-white rounded-xl shadow-sm p-6 mb-8">
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Filter by State</label>
              <select
                value={selectedState}
                onChange={(e) => setSelectedState(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
              >
                <option value="">All States</option>
                {US_STATES.map((state) => (
                  <option key={state.code} value={state.code}>
                    {state.name}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Search</label>
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search by waterbody, fish species, or location..."
                  className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                />
              </div>
            </div>
          </div>
        </div>

        {/* Coming Soon Notice */}
        <div className="bg-gradient-to-br from-green-50 to-emerald-50 border-2 border-green-200 rounded-xl p-12 text-center">
          <Shield className="w-16 h-16 text-green-600 mx-auto mb-6" />
          <h3 className="text-2xl font-bold text-gray-900 mb-4">EPA Advisory Data Integration In Progress</h3>
          <p className="text-lg text-gray-600 mb-6 max-w-2xl mx-auto">
            We're currently integrating comprehensive EPA fish consumption advisory data from all 50 states.
            This feature will provide detailed information about:
          </p>
          <div className="grid md:grid-cols-2 gap-4 max-w-3xl mx-auto mb-8 text-left">
            <div className="bg-white rounded-lg p-4">
              <div className="flex items-start space-x-3">
                <MapPin className="w-5 h-5 text-green-600 mt-1 flex-shrink-0" />
                <div>
                  <div className="font-semibold text-gray-900 mb-1">Waterbody-Specific Advisories</div>
                  <p className="text-sm text-gray-600">Detailed guidance for rivers, lakes, and coastal waters</p>
                </div>
              </div>
            </div>
            <div className="bg-white rounded-lg p-4">
              <div className="flex items-start space-x-3">
                <Fish className="w-5 h-5 text-green-600 mt-1 flex-shrink-0" />
                <div>
                  <div className="font-semibold text-gray-900 mb-1">Species-Specific Recommendations</div>
                  <p className="text-sm text-gray-600">Safe consumption limits for each fish species</p>
                </div>
              </div>
            </div>
            <div className="bg-white rounded-lg p-4">
              <div className="flex items-start space-x-3">
                <AlertTriangle className="w-5 h-5 text-green-600 mt-1 flex-shrink-0" />
                <div>
                  <div className="font-semibold text-gray-900 mb-1">Contaminant Information</div>
                  <p className="text-sm text-gray-600">Mercury, PCBs, and other pollutant levels</p>
                </div>
              </div>
            </div>
            <div className="bg-white rounded-lg p-4">
              <div className="flex items-start space-x-3">
                <Shield className="w-5 h-5 text-green-600 mt-1 flex-shrink-0" />
                <div>
                  <div className="font-semibold text-gray-900 mb-1">Sensitive Population Guidance</div>
                  <p className="text-sm text-gray-600">Special recommendations for pregnant women and children</p>
                </div>
              </div>
            </div>
          </div>
          <div className="text-sm text-gray-500">
            <p className="mb-2">Backend data is ready with 100+ state advisories.</p>
            <p>Frontend integration coming soon!</p>
          </div>
        </div>
      </div>
    </div>
  )
}
