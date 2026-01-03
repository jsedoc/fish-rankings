'use client'

import { useState, useEffect } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { ArrowLeft } from 'lucide-react'
import Link from 'next/link'

interface Food {
  id: string
  name: string
  slug: string
  description: string
}

export default function CategoryPage() {
  const params = useParams()
  const router = useRouter()
  const categorySlug = params.slug as string

  const [foods, setFoods] = useState<Food[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const categoryNames: Record<string, string> = {
    seafood: 'Seafood',
    produce: 'Produce',
    'meat-poultry': 'Meat & Poultry',
    dairy: 'Dairy',
  }

  useEffect(() => {
    fetchCategoryFoods()
  }, [categorySlug])

  const fetchCategoryFoods = async () => {
    setLoading(true)
    setError('')

    try {
      const response = await fetch(`/api/v1/foods?category=${categorySlug}&limit=100`)

      if (!response.ok) {
        throw new Error('Failed to load foods')
      }

      const data = await response.json()
      setFoods(data)
    } catch (err) {
      setError('Failed to load category foods. Please try again.')
      console.error(err)
    } finally {
      setLoading(false)
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
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <button onClick={() => router.push('/')} className="flex items-center text-gray-600 hover:text-gray-900">
            <ArrowLeft className="w-5 h-5 mr-2" />
            Back to Home
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            {categoryNames[categorySlug] || 'Category'}
          </h1>
          <p className="text-gray-600 mt-2">
            Browse all {categoryNames[categorySlug]?.toLowerCase()} items in our database
          </p>
        </div>

        {loading ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading...</p>
          </div>
        ) : error ? (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-800">
            {error}
          </div>
        ) : foods.length === 0 ? (
          <div className="text-center py-12 bg-white rounded-lg border border-gray-200">
            <p className="text-gray-600">No foods found in this category.</p>
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
                  <h3 className="text-lg font-semibold text-gray-900">{food.name}</h3>
                  <span
                    className={`px-2 py-1 rounded text-xs font-medium border ${getRiskColor(
                      food.description || ''
                    )}`}
                  >
                    {getRiskLabel(food.description || '')}
                  </span>
                </div>
                <p className="text-sm text-gray-600 line-clamp-2">{food.description}</p>
              </Link>
            ))}
          </div>
        )}
      </main>
    </div>
  )
}
