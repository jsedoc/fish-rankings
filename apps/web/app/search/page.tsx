'use client'

import { useState, useEffect } from 'react'
import { useSearchParams, useRouter } from 'next/navigation'
import { Search, ArrowLeft } from 'lucide-react'
import Link from 'next/link'

interface Food {
  id: string
  name: string
  slug: string
  description: string
  category_id: number
}

export default function SearchPage() {
  const searchParams = useSearchParams()
  const router = useRouter()
  const query = searchParams.get('q') || ''
  const [searchInput, setSearchInput] = useState(query)
  const [foods, setFoods] = useState<Food[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [total, setTotal] = useState(0)

  useEffect(() => {
    if (query) {
      searchFoods(query)
    }
  }, [query])

  const searchFoods = async (searchQuery: string) => {
    setLoading(true)
    setError('')

    try {
      const response = await fetch(
        `/api/v1/search?q=${encodeURIComponent(searchQuery)}`
      )

      if (!response.ok) {
        throw new Error('Search failed')
      }

      const data = await response.json()
      setFoods(data.foods || [])
      setTotal(data.total || 0)
    } catch (err) {
      setError('Failed to search foods. Please try again.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    if (searchInput.trim()) {
      router.push(`/search?q=${encodeURIComponent(searchInput)}`)
    }
  }

  const getRiskColor = (description: string) => {
    const lower = description.toLowerCase()
    if (lower.includes('best choice') || lower.includes('clean fifteen')) {
      return 'bg-green-100 text-green-800 border-green-300'
    } else if (lower.includes('avoid') || lower.includes('dirty dozen')) {
      return 'bg-red-100 text-red-800 border-red-300'
    } else {
      return 'bg-yellow-100 text-yellow-800 border-yellow-300'
    }
  }

  const getRiskLabel = (description: string) => {
    const lower = description.toLowerCase()
    if (lower.includes('best choice') || lower.includes('clean fifteen')) {
      return 'Low Risk'
    } else if (lower.includes('avoid') || lower.includes('dirty dozen')) {
      return 'High Risk'
    } else {
      return 'Moderate Risk'
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center space-x-4">
            <Link href="/" className="text-gray-600 hover:text-gray-900">
              <ArrowLeft className="w-5 h-5" />
            </Link>
            <form onSubmit={handleSearch} className="flex-1 max-w-2xl">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  type="text"
                  value={searchInput}
                  onChange={(e) => setSearchInput(e.target.value)}
                  placeholder="Search for any food..."
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                />
              </div>
            </form>
          </div>
        </div>
      </header>

      {/* Results */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {loading ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 mx-auto"></div>
            <p className="mt-4 text-gray-600">Searching...</p>
          </div>
        ) : error ? (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-800">
            {error}
          </div>
        ) : (
          <>
            <div className="mb-6">
              <h1 className="text-2xl font-bold text-gray-900">
                Search Results for "{query}"
              </h1>
              <p className="text-gray-600 mt-1">
                Found {total} {total === 1 ? 'result' : 'results'}
              </p>
            </div>

            {foods.length === 0 ? (
              <div className="text-center py-12 bg-white rounded-lg border border-gray-200">
                <p className="text-gray-600">
                  No foods found. Try a different search term.
                </p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {foods.map((food) => (
                  <Link
                    key={food.id}
                    href={`/food/${food.slug}`}
                    className="card p-6 hover:scale-105 transition-transform"
                  >
                    <div className="flex items-start justify-between mb-3">
                      <h3 className="text-lg font-semibold text-gray-900">
                        {food.name}
                      </h3>
                      <span
                        className={`px-2 py-1 rounded text-xs font-medium border ${getRiskColor(
                          food.description || ''
                        )}`}
                      >
                        {getRiskLabel(food.description || '')}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 line-clamp-2">
                      {food.description}
                    </p>
                  </Link>
                ))}
              </div>
            )}
          </>
        )}
      </main>
    </div>
  )
}
