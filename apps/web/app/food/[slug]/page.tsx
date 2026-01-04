'use client'

import { useState, useEffect } from 'react'
import { useParams, useRouter, notFound } from 'next/navigation'
import { ArrowLeft, ExternalLink, AlertTriangle, CheckCircle, Info } from 'lucide-react'
import Link from 'next/link'

interface Contaminant {
  id: number
  name: string
  health_effects: string
  unit: string
}

interface Source {
  id: number
  name: string
  url: string
  source_type: string
}

interface ContaminantLevel {
  id: string
  level_value: number | null
  level_unit: string
  risk_score: number
  risk_category: string
  notes: string
  contaminant: Contaminant
  source: Source | null
}

interface Nutrient {
  id: string
  nutrient_name: string
  amount: number
  unit: string
  per_serving_size: string
}

interface FoodDetail {
  id: string
  name: string
  description: string
  slug: string
  contaminant_levels: ContaminantLevel[]
  nutrients: Nutrient[]
}

export default function FoodDetailPage() {
  const params = useParams()
  const router = useRouter()
  const slug = params.slug as string

  const [food, setFood] = useState<FoodDetail | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetch(`/api/v1/foods/slug/${params.slug}`)
      .then(res => res.json())
      .then(data => {
        setFood(data)
        setLoading(false)
      })
      .catch(() => setLoading(false))
  }, [params.slug])

  if (loading) return <div>Loading...</div>
  if (!food) return notFound()

  const fetchFood = async () => {
    setLoading(true)
    setError('')

    try {
      const response = await fetch(`/api/v1/foods/slug/${slug}`)

      if (!response.ok) {
        throw new Error('Food not found')
      }

      const data = await response.json()
      setFood(data)
    } catch (err) {
      setError('Failed to load food details. Please try again.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const getRiskColor = (category: string) => {
    switch (category) {
      case 'low':
        return 'bg-green-100 text-green-800 border-green-300'
      case 'high':
        return 'bg-red-100 text-red-800 border-red-300'
      default:
        return 'bg-yellow-100 text-yellow-800 border-yellow-300'
    }
  }

  const getRiskIcon = (category: string) => {
    switch (category) {
      case 'low':
        return <CheckCircle className="w-5 h-5" />
      case 'high':
        return <AlertTriangle className="w-5 h-5" />
      default:
        return <Info className="w-5 h-5" />
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500"></div>
      </div>
    )
  }

  if (error || !food) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Food Not Found</h1>
          <p className="text-gray-600 mb-4">{error}</p>
          <Link href="/" className="text-primary-600 hover:text-primary-700">
            ← Back to Home
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <button onClick={() => router.back()} className="flex items-center text-gray-600 hover:text-gray-900">
            <ArrowLeft className="w-5 h-5 mr-2" />
            Back
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Title */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">{food.name}</h1>
          <p className="text-lg text-gray-600">{food.description}</p>
        </div>

        {/* Overall Safety Score */}
        {food.contaminant_levels.length > 0 && (
          <div className="card p-6 mb-8">
            <h2 className="text-xl font-semibold mb-4">Safety Overview</h2>
            <div className="flex items-center space-x-3">
              {getRiskIcon(food.contaminant_levels[0].risk_category)}
              <span
                className={`px-4 py-2 rounded-full text-lg font-medium border ${getRiskColor(
                  food.contaminant_levels[0].risk_category
                )}`}
              >
                {food.contaminant_levels[0].risk_category.charAt(0).toUpperCase() +
                  food.contaminant_levels[0].risk_category.slice(1)}{' '}
                Risk
              </span>
              <span className="text-gray-600">
                Score: {food.contaminant_levels[0].risk_score}/100
              </span>
            </div>
          </div>
        )}

        {/* Contaminants */}
        {food.contaminant_levels.length > 0 && (
          <div className="card p-6 mb-8">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <AlertTriangle className="w-5 h-5 mr-2 text-orange-500" />
              Contaminants & Risks
            </h2>
            <div className="space-y-4">
              {food.contaminant_levels.map((level) => (
                <div key={level.id} className="border-l-4 border-gray-300 pl-4">
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="font-semibold text-gray-900">
                      {level.contaminant.name}
                    </h3>
                    {level.level_value !== null && (
                      <span className="text-sm text-gray-600">
                        {level.level_value} {level.level_unit}
                      </span>
                    )}
                  </div>
                  {level.contaminant.health_effects && (
                    <p className="text-sm text-gray-600 mb-2">
                      <strong>Health Effects:</strong> {level.contaminant.health_effects}
                    </p>
                  )}
                  {level.notes && (
                    <p className="text-sm bg-blue-50 border border-blue-200 rounded p-3 text-blue-900">
                      <strong>Recommendation:</strong> {level.notes}
                    </p>
                  )}
                  {level.source && (
                    <div className="mt-2">
                      <a
                        href={level.source.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-xs text-primary-600 hover:text-primary-700 flex items-center"
                      >
                        Source: {level.source.name}
                        <ExternalLink className="w-3 h-3 ml-1" />
                      </a>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Nutrients (if available) */}
        {food.nutrients.length > 0 && (
          <div className="card p-6 mb-8">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <CheckCircle className="w-5 h-5 mr-2 text-green-500" />
              Nutritional Benefits
            </h2>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              {food.nutrients.map((nutrient) => (
                <div key={nutrient.id} className="text-center p-4 bg-gray-50 rounded-lg">
                  <p className="text-sm text-gray-600">{nutrient.nutrient_name}</p>
                  <p className="text-lg font-semibold text-gray-900">
                    {nutrient.amount} {nutrient.unit}
                  </p>
                  {nutrient.per_serving_size && (
                    <p className="text-xs text-gray-500">per {nutrient.per_serving_size}</p>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Disclaimer */}
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 text-sm text-yellow-900">
          <p className="font-semibold mb-1">Disclaimer</p>
          <p>
            This information is for educational purposes only and does not constitute medical
            advice. Always consult with a healthcare professional for personalized dietary
            guidance.
          </p>
        </div>
      </main>
    </div>
  )
}
