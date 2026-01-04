'use client'

export const dynamic = 'force-dynamic'

import { useState, useEffect } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { ArrowLeft, AlertTriangle } from 'lucide-react'
import Link from 'next/link'

interface Food {
  id: string
  name: string
  slug: string
  description: string
}

interface Recall {
  recall_number: string
  product_description: string
  classification: string
  company_name: string
  recall_date: string
  reason_for_recall: string
}

export default function CategoryPage() {
  const params = useParams()
  const router = useRouter()
  const categorySlug = params.slug as string

  const [foods, setFoods] = useState<Food[]>([])
  const [recalls, setRecalls] = useState<Recall[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const categoryNames: Record<string, string> = {
    seafood: 'Seafood',
    produce: 'Produce',
    'meat-poultry': 'Meat & Poultry',
    dairy: 'Dairy',
  }

  const categoryKeywords: Record<string, string[]> = {
    seafood: ['fish', 'seafood', 'salmon', 'tuna', 'shrimp', 'crab'],
    produce: ['salad', 'lettuce', 'vegetable', 'fruit', 'spinach'],
    'meat-poultry': ['meat', 'beef', 'chicken', 'pork', 'turkey', 'poultry'],
    dairy: ['milk', 'cheese', 'dairy', 'yogurt', 'cream', 'butter'],
  }

  useEffect(() => {
    fetchCategoryFoods()
    fetchCategoryRecalls()
  }, [categorySlug])

  const fetchCategoryFoods = async () => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/foods?category=${categorySlug}&limit=100`)

      if (!response.ok) {
        throw new Error('Failed to load foods')
      }

      const data = await response.json()
      setFoods(data)
    } catch (err) {
      console.error('Error fetching foods:', err)
    }
  }

  const fetchCategoryRecalls = async () => {
    setLoading(true)
    setError('')

    try {
      const keywords = categoryKeywords[categorySlug] || []

      // Fetch recalls for each keyword and combine results
      const allRecalls: Recall[] = []

      for (const keyword of keywords) {
        const response = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/recalls?search=${encodeURIComponent(keyword)}&limit=20&days=90`
        )

        if (response.ok) {
          const data = await response.json()
          // Handle both array and object responses
          const recallsList = Array.isArray(data) ? data : (data.recalls || [])
          allRecalls.push(...recallsList)
        }
      }

      // Deduplicate by recall_number
      const uniqueRecalls = Array.from(
        new Map(allRecalls.map(r => [r.recall_number, r])).values()
      )

      // Sort by date (most recent first) and limit to 10
      setRecalls(
        uniqueRecalls
          .sort((a, b) => new Date(b.recall_date).getTime() - new Date(a.recall_date).getTime())
          .slice(0, 10)
      )
    } catch (err) {
      console.error('Error fetching recalls:', err)
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
        ) : (
          <>
            {/* Foods Section */}
            {foods.length > 0 ? (
              <div className="mb-12">
                <h2 className="text-2xl font-bold text-gray-900 mb-4">Foods in this Category</h2>
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
              </div>
            ) : (
              <div className="text-center py-8 bg-white rounded-lg border border-gray-200 mb-12">
                <p className="text-gray-600">No foods found in this category yet. Check recalls below.</p>
              </div>
            )}

            {/* Recalls Section */}
            {recalls.length > 0 && (
              <div>
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-2xl font-bold text-gray-900">Recent Recalls</h2>
                  <Link
                    href="/recalls"
                    className="text-sm text-primary-600 hover:text-primary-700 font-medium"
                  >
                    View all recalls →
                  </Link>
                </div>
                <div className="space-y-4">
                  {recalls.map((recall) => (
                    <div
                      key={recall.recall_number}
                      className="card p-6 border-l-4 border-red-500"
                    >
                      <div className="flex items-start justify-between mb-2">
                        <div className="flex items-start gap-3 flex-1">
                          <AlertTriangle className="w-5 h-5 text-red-600 mt-1 flex-shrink-0" />
                          <div className="flex-1">
                            <h3 className="font-semibold text-gray-900 mb-2">
                              {recall.product_description}
                            </h3>
                            {recall.reason_for_recall && (
                              <p className="text-sm text-gray-700 mb-2">
                                <span className="font-medium">Reason:</span> {recall.reason_for_recall}
                              </p>
                            )}
                            <div className="flex flex-wrap gap-3 text-sm text-gray-600">
                              <span>
                                <span className="font-medium">Company:</span> {recall.company_name}
                              </span>
                              <span>
                                <span className="font-medium">Date:</span>{' '}
                                {new Date(recall.recall_date).toLocaleDateString()}
                              </span>
                            </div>
                          </div>
                        </div>
                        <span
                          className={`px-3 py-1 rounded-full text-xs font-semibold whitespace-nowrap ml-4 ${
                            recall.classification === 'Class I'
                              ? 'bg-red-100 text-red-800'
                              : recall.classification === 'Class II'
                              ? 'bg-orange-100 text-orange-800'
                              : 'bg-yellow-100 text-yellow-800'
                          }`}
                        >
                          {recall.classification === 'Class I'
                            ? 'Critical'
                            : recall.classification === 'Class II'
                            ? 'High Risk'
                            : 'Moderate'}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </>
        )}
      </main>
    </div>
  )
}
