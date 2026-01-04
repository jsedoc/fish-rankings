'use client'

export const dynamic = 'force-dynamic'

import { useState, useEffect } from 'react'
import { useParams, useRouter, notFound } from 'next/navigation'
import { ArrowLeft, ExternalLink, AlertTriangle, CheckCircle, Info, Leaf, MapPin } from 'lucide-react'
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

interface StateAdvisory {
  id: string
  state_name: string
  state_code: string
  waterbody_name: string
  advisory_type: string
  advisory_level: string
  consumption_limit: string
  fish_species: string
  effective_date: string
}

interface SustainabilityRating {
  id: string
  rating: string
  source: string
  rating_score: number
  fishing_method: string
  sustainability_notes: string
}

interface FoodDetail {
  id: string
  name: string
  description: string
  slug: string
  contaminant_levels: ContaminantLevel[]
  nutrients: Nutrient[]
  advisories: StateAdvisory[]
  sustainability_ratings: SustainabilityRating[]
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
      .catch((err) => {
        console.error(err)
        setError('Failed to load food details')
        setLoading(false)
      })
  }, [params.slug])

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

  const getSustColor = (rating: string) => {
    const r = rating?.toLowerCase() || ''
    if (r.includes('best choice') || r.includes('certified')) return 'bg-green-100 text-green-800 border-green-300'
    if (r.includes('avoid')) return 'bg-red-100 text-red-800 border-red-300'
    return 'bg-yellow-100 text-yellow-800 border-yellow-300'
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
          <p className="text-gray-600 mb-4">{error || 'Could not retrieve data'}</p>
          <Link href="/" className="text-primary-600 hover:text-primary-700">
            ← Back to Home
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <button onClick={() => router.back()} className="flex items-center text-gray-600 hover:text-gray-900">
            <ArrowLeft className="w-5 h-5 mr-2" />
            Back
          </button>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">{food.name}</h1>
          <p className="text-lg text-gray-600">{food.description}</p>
        </div>

        {/* --- Sustainability Section --- */}
        {food.sustainability_ratings && food.sustainability_ratings.length > 0 && (
          <div className="card p-6 mb-8 bg-blue-50 border border-blue-100">
            <h2 className="text-xl font-semibold mb-4 flex items-center text-blue-900">
              <Leaf className="w-5 h-5 mr-2 text-green-600" />
              Sustainability Rating
            </h2>
            <div className="flex flex-wrap gap-4">
              {food.sustainability_ratings.map((rating, idx) => (
                <div key={idx} className={`p-4 rounded-lg border ${getSustColor(rating.rating)} bg-white shadow-sm flex-1 min-w-[200px]`}>
                  <div className="font-bold text-lg mb-1">{rating.rating}</div>
                  <div className="text-xs text-gray-500 uppercase tracking-wide mb-2">Source: {rating.source}</div>
                  <p className="text-sm text-gray-700">{rating.sustainability_notes || rating.fishing_method}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* --- Safety / Mercury Section --- */}
        {food.contaminant_levels?.length > 0 && (
          <div className="card p-6 mb-8">
            <h2 className="text-xl font-semibold mb-4">Mercury & Health Risks</h2>
            <div className="flex items-center space-x-3 mb-6">
              {getRiskIcon(food.contaminant_levels[0].risk_category || 'unknown')}
              <span
                className={`px-4 py-2 rounded-full text-lg font-medium border ${getRiskColor(
                  food.contaminant_levels[0].risk_category || 'unknown'
                )}`}
              >
                {(food.contaminant_levels[0].risk_category || 'Unknown').charAt(0).toUpperCase() +
                  (food.contaminant_levels[0].risk_category || 'Unknown').slice(1)}{' '}
                Risk
              </span>
              <span className="text-gray-600">
                Score: {food.contaminant_levels[0].risk_score ?? 'N/A'}/100
              </span>
            </div>

            {/* State Advisories Warning */}
            {food.advisories && food.advisories.length > 0 && (
              <div className="mb-6 bg-orange-50 border border-orange-200 rounded-lg p-4">
                <h3 className="text-md font-bold text-orange-900 mb-2 flex items-center">
                  <MapPin className="w-4 h-4 mr-2" />
                  Active State Advisories ({food.advisories.length})
                </h3>
                <p className="text-sm text-orange-800 mb-3">
                  Specific waterbodies in these states have issued consumption warnings for this species:
                </p>
                <div className="max-h-40 overflow-y-auto space-y-2 pr-2">
                  {food.advisories.map((adv, idx) => (
                    <div key={idx} className="text-xs bg-white p-2 rounded border border-orange-100 shadow-sm">
                      <span className="font-bold">{adv.state_name}:</span> {adv.waterbody_name} — <span className="text-red-600 font-medium">{adv.advisory_level || 'Consumption Limit'}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Contaminant Details */}
            <div className="space-y-4">
              {food.contaminant_levels.map((level) => (
                <div key={level.id} className="border-l-4 border-gray-300 pl-4">
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="font-semibold text-gray-900">{level.contaminant.name}</h3>
                    {level.level_value !== null && (
                      <span className="text-sm text-gray-600">
                        {level.level_value} {level.level_unit}
                      </span>
                    )}
                  </div>
                  {level.notes && (
                    <p className="text-sm bg-gray-50 border border-gray-200 rounded p-3 text-gray-700">
                      {level.notes}
                    </p>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Nutrients */}
        {food.nutrients && food.nutrients.length > 0 && (
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
