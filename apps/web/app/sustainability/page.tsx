'use client'

import { useState, useEffect } from 'react'
import { Waves, Star, AlertCircle, CheckCircle, ArrowLeft, Search, Award } from 'lucide-react'
import Link from 'next/link'

interface SustainabilityRating {
  id: string
  species_name: string
  rating: string
  rating_score: number
  source: string
  fishing_method?: string
  location?: string
  is_farmed: boolean
  is_wild_caught: boolean
  overfished: boolean
  overfishing_occurring: boolean
  habitat_impact?: string
  bycatch_impact?: string
  management_rating?: string
  sustainability_notes?: string
  certifications?: string[]
  last_updated: string
}

export default function SustainabilityPage() {
  const [ratings, setRatings] = useState<SustainabilityRating[]>([])
  const [filter, setFilter] = useState<'all' | 'Best Choice' | 'Good Alternative' | 'Avoid'>('all')
  const [searchQuery, setSearchQuery] = useState('')

  useEffect(() => {
    fetchRatings()
  }, [filter])

  const fetchRatings = async () => {
    try {
      // Note: This endpoint would need to be implemented on the backend
      const baseUrl = `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/sustainability`
      const params = new URLSearchParams()

      if (filter !== 'all') {
        params.set('rating', filter)
      }

      const queryString = params.toString()
      const url = queryString ? `${baseUrl}?${queryString}` : baseUrl

      const response = await fetch(url)
      if (response.ok) {
        const data = await response.json()
        setRatings(data.ratings || [])
      } else {
        setRatings([])
      }
    } catch (err) {
      console.error('Failed to fetch sustainability ratings:', err)
      setRatings([])
    }
  }


  const getRatingIcon = (rating: string) => {
    if (rating === 'Best Choice') return <CheckCircle className="w-5 h-5 text-green-600" />
    if (rating === 'Good Alternative') return <Star className="w-5 h-5 text-yellow-600" />
    return <AlertCircle className="w-5 h-5 text-red-600" />
  }

  const filteredRatings = ratings.filter(rating =>
    searchQuery === '' ||
    rating.species_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    rating.location?.toLowerCase().includes(searchQuery.toLowerCase()) ||
    rating.fishing_method?.toLowerCase().includes(searchQuery.toLowerCase())
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
            <h1 className="text-xl font-bold text-gray-900">Seafood Sustainability</h1>
            <div className="w-24"></div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 py-12">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-2xl flex items-center justify-center mx-auto mb-6">
            <Waves className="w-10 h-10 text-white" />
          </div>
          <h2 className="text-4xl font-bold text-gray-900 mb-4">Sustainable Seafood Guide</h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Make ocean-friendly choices with NOAA FishWatch sustainability ratings. Support healthy fisheries and marine ecosystems.
          </p>
        </div>

        {/* Info Banner */}
        <div className="bg-blue-50 border border-blue-200 rounded-xl p-6 mb-8">
          <div className="flex items-start">
            <Waves className="w-6 h-6 text-blue-600 mt-1 mr-4 flex-shrink-0" />
            <div>
              <h3 className="font-semibold text-blue-900 mb-2">Why Sustainability Matters</h3>
              <p className="text-blue-800 mb-4">
                Sustainable seafood comes from fisheries and farms that maintain healthy fish populations, habitats, and ecosystems.
                Your choices can help protect ocean health for future generations.
              </p>
              <div className="grid md:grid-cols-3 gap-4 text-sm">
                <div>
                  <div className="flex items-center space-x-2 mb-1">
                    <CheckCircle className="w-4 h-4 text-green-600" />
                    <div className="font-semibold text-green-900">Best Choice</div>
                  </div>
                  <p className="text-gray-700">Well-managed, abundant populations, minimal environmental impact</p>
                </div>
                <div>
                  <div className="flex items-center space-x-2 mb-1">
                    <Star className="w-4 h-4 text-yellow-600" />
                    <div className="font-semibold text-yellow-900">Good Alternative</div>
                  </div>
                  <p className="text-gray-700">Good option but some concerns about stock or fishing methods</p>
                </div>
                <div>
                  <div className="flex items-center space-x-2 mb-1">
                    <AlertCircle className="w-4 h-4 text-red-600" />
                    <div className="font-semibold text-red-900">Avoid</div>
                  </div>
                  <p className="text-gray-700">Overfished, poorly managed, or high environmental impact</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Filters */}
        <div className="bg-white rounded-xl shadow-sm p-6 mb-8">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search by species, location, or fishing method..."
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => setFilter('all')}
                className={`px-4 py-3 rounded-lg font-medium transition-colors ${
                  filter === 'all' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                All
              </button>
              <button
                onClick={() => setFilter('Best Choice')}
                className={`px-4 py-3 rounded-lg font-medium transition-colors ${
                  filter === 'Best Choice' ? 'bg-green-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Best
              </button>
              <button
                onClick={() => setFilter('Good Alternative')}
                className={`px-4 py-3 rounded-lg font-medium transition-colors ${
                  filter === 'Good Alternative' ? 'bg-yellow-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Good
              </button>
              <button
                onClick={() => setFilter('Avoid')}
                className={`px-4 py-3 rounded-lg font-medium transition-colors ${
                  filter === 'Avoid' ? 'bg-red-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Avoid
              </button>
            </div>
          </div>
        </div>

        {/* Coming Soon Notice */}
        <div className="bg-gradient-to-br from-blue-50 to-cyan-50 border-2 border-blue-200 rounded-xl p-12 text-center">
          <Waves className="w-16 h-16 text-blue-600 mx-auto mb-6" />
          <h3 className="text-2xl font-bold text-gray-900 mb-4">NOAA Sustainability Data Integration In Progress</h3>
          <p className="text-lg text-gray-600 mb-6 max-w-2xl mx-auto">
            We're integrating comprehensive sustainability ratings from NOAA FishWatch and partner organizations.
            This feature will help you make informed, ocean-friendly seafood choices with data on:
          </p>
          <div className="grid md:grid-cols-2 gap-4 max-w-3xl mx-auto mb-8 text-left">
            <div className="bg-white rounded-lg p-4">
              <div className="flex items-start space-x-3">
                <CheckCircle className="w-5 h-5 text-blue-600 mt-1 flex-shrink-0" />
                <div>
                  <div className="font-semibold text-gray-900 mb-1">Stock Health</div>
                  <p className="text-sm text-gray-600">Overfishing status and population abundance</p>
                </div>
              </div>
            </div>
            <div className="bg-white rounded-lg p-4">
              <div className="flex items-start space-x-3">
                <Waves className="w-5 h-5 text-blue-600 mt-1 flex-shrink-0" />
                <div>
                  <div className="font-semibold text-gray-900 mb-1">Fishing Methods</div>
                  <p className="text-sm text-gray-600">Environmental impact of harvesting techniques</p>
                </div>
              </div>
            </div>
            <div className="bg-white rounded-lg p-4">
              <div className="flex items-start space-x-3">
                <Star className="w-5 h-5 text-blue-600 mt-1 flex-shrink-0" />
                <div>
                  <div className="font-semibold text-gray-900 mb-1">Habitat Impact</div>
                  <p className="text-sm text-gray-600">Effects on marine ecosystems and seafloor</p>
                </div>
              </div>
            </div>
            <div className="bg-white rounded-lg p-4">
              <div className="flex items-start space-x-3">
                <Award className="w-5 h-5 text-blue-600 mt-1 flex-shrink-0" />
                <div>
                  <div className="font-semibold text-gray-900 mb-1">Certifications</div>
                  <p className="text-sm text-gray-600">MSC, ASC, and other sustainability certifications</p>
                </div>
              </div>
            </div>
          </div>
          <div className="bg-white rounded-lg p-6 max-w-2xl mx-auto">
            <div className="flex items-start space-x-4">
              <div className="flex-shrink-0">
                <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                  <CheckCircle className="w-6 h-6 text-blue-600" />
                </div>
              </div>
              <div className="text-left">
                <h4 className="font-semibold text-gray-900 mb-2">What's Ready Now</h4>
                <ul className="text-sm text-gray-600 space-y-1">
                  <li>• Backend API with 14+ sustainability ratings</li>
                  <li>• NOAA FishWatch data integration</li>
                  <li>• Database schema for comprehensive ratings</li>
                  <li>• Rating scores and environmental impact metrics</li>
                </ul>
              </div>
            </div>
          </div>
          <div className="mt-6 text-sm text-gray-500">
            <p>Frontend UI integration coming soon!</p>
          </div>
        </div>
      </div>
    </div>
  )
}
