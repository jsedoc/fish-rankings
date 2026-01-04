'use client'

import { useState } from 'react'
import { Search, Scan, AlertTriangle, CheckCircle, Info, ArrowLeft } from 'lucide-react'
import Link from 'next/link'

interface ProductData {
  found: boolean
  source: string
  product?: {
    name: string
    barcode: string
    brands?: string
    categories?: string[]
    ingredients?: string
    allergens?: string[]
    nutriscore_grade?: string
    nova_group?: number
    ecoscore_grade?: string
    image_url?: string
    nutrients?: {
      energy_kcal?: number
      fat?: number
      saturated_fat?: number
      carbohydrates?: number
      sugars?: number
      proteins?: number
      salt?: number
    }
  }
  recalls?: any[]
  recall_count: number
  has_active_recalls: boolean
  message?: string
}

export default function BarcodePage() {
  const [barcode, setBarcode] = useState('')
  const [loading, setLoading] = useState(false)
  const [productData, setProductData] = useState<ProductData | null>(null)
  const [error, setError] = useState('')

  const handleLookup = async (e: React.FormEvent) => {
    e.preventDefault()
    const cleanedBarcode = barcode.trim()

    if (!cleanedBarcode) {
      setError('Please enter a barcode.')
      setProductData(null)
      return
    }

    const isNumeric = /^\d+$/.test(cleanedBarcode)
    const validLengths = [8, 12, 13, 14]
    const hasValidLength = validLengths.includes(cleanedBarcode.length)

    if (!isNumeric || !hasValidLength) {
      setError('Please enter a valid barcode (8, 12, 13, or 14 digits).')
      setProductData(null)
      return
    }

    setLoading(true)
    setError('')
    setProductData(null)

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/barcode/lookup/${cleanedBarcode}`)

      if (!response.ok) {
        throw new Error('Failed to lookup barcode')
      }

      const data = await response.json()
      setProductData(data)
    } catch (err) {
      setError('Failed to lookup product. Please check the barcode and try again.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const getNutriscoreColor = (grade?: string) => {
    const colors: Record<string, string> = {
      A: 'bg-green-500',
      B: 'bg-lime-500',
      C: 'bg-yellow-500',
      D: 'bg-orange-500',
      E: 'bg-red-500',
    }
    return grade ? colors[grade.toUpperCase()] || 'bg-gray-500' : 'bg-gray-500'
  }

  const getNovaColor = (group?: number) => {
    const colors: Record<number, string> = {
      1: 'text-green-600',
      2: 'text-yellow-600',
      3: 'text-orange-600',
      4: 'text-red-600',
    }
    return group ? colors[group] || 'text-gray-600' : 'text-gray-600'
  }

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
            <h1 className="text-xl font-bold text-gray-900">Barcode Scanner</h1>
            <div className="w-24"></div> {/* Spacer for centering */}
          </div>
        </div>
      </header>

      <div className="max-w-4xl mx-auto px-4 py-12">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-2xl flex items-center justify-center mx-auto mb-6">
            <Scan className="w-10 h-10 text-white" />
          </div>
          <h2 className="text-4xl font-bold text-gray-900 mb-4">Scan Any Product</h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Access 2.3M+ products from Open Food Facts. Check nutrition, ingredients, and recalls instantly.
          </p>
        </div>

        {/* Search Form */}
        <form onSubmit={handleLookup} className="mb-8">
          <div className="relative">
            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              value={barcode}
              onChange={(e) => setBarcode(e.target.value)}
              placeholder="Enter barcode (e.g., 5449000000996 for Coca-Cola)"
              className="w-full pl-12 pr-4 py-4 text-lg rounded-xl border border-gray-300 shadow-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <button
            type="submit"
            disabled={loading || !barcode.trim()}
            className="w-full mt-4 bg-gradient-to-r from-blue-500 to-cyan-500 text-white font-semibold py-4 px-6 rounded-xl hover:from-blue-600 hover:to-cyan-600 transition-all shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Looking up...' : 'Lookup Product'}
          </button>
        </form>

        {/* Example Barcodes */}
        <div className="text-center mb-8">
          <p className="text-sm text-gray-600 mb-2">Try these examples:</p>
          <div className="flex flex-wrap justify-center gap-2">
            {['5449000000996', '3017620422003', '737628064502'].map((code) => (
              <button
                key={code}
                onClick={() => setBarcode(code)}
                className="px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded-lg text-sm text-gray-700 transition-colors"
              >
                {code}
              </button>
            ))}
          </div>
        </div>

        {/* Error */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-xl p-4 mb-8">
            <div className="flex items-start">
              <AlertTriangle className="w-5 h-5 text-red-600 mt-0.5 mr-3 flex-shrink-0" />
              <p className="text-red-800">{error}</p>
            </div>
          </div>
        )}

        {/* Results */}
        {productData && (
          <div className="space-y-6">
            {/* Not Found */}
            {!productData.found && (
              <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-6 text-center">
                <Info className="w-12 h-12 text-yellow-600 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Product Not Found</h3>
                <p className="text-gray-600">This barcode isn't in our database yet. Try another one!</p>
              </div>
            )}

            {/* Product Found */}
            {productData.found && productData.product && (
              <>
                {/* Recall Alert */}
                {productData.has_active_recalls && (
                  <div className="bg-red-50 border-2 border-red-500 rounded-xl p-6">
                    <div className="flex items-start">
                      <AlertTriangle className="w-6 h-6 text-red-600 mt-1 mr-4 flex-shrink-0" />
                      <div>
                        <h3 className="text-lg font-bold text-red-900 mb-2">⚠️ Active Recall Alert</h3>
                        <p className="text-red-800 mb-4">
                          This product has {productData.recall_count} active recall(s). Please check the details below.
                        </p>
                        {productData.recalls && productData.recalls.map((recall, idx) => (
                          <div key={idx} className="bg-white rounded-lg p-4 mb-2">
                            <p className="font-semibold text-gray-900">{recall.reason_for_recall}</p>
                            <p className="text-sm text-gray-600 mt-1">Classification: {recall.classification}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                )}

                {/* Safe Badge */}
                {!productData.has_active_recalls && (
                  <div className="bg-green-50 border border-green-200 rounded-xl p-4">
                    <div className="flex items-center">
                      <CheckCircle className="w-5 h-5 text-green-600 mr-3" />
                      <p className="text-green-800 font-medium">No active recalls for this product</p>
                    </div>
                  </div>
                )}

                {/* Product Info Card */}
                <div className="bg-white rounded-xl shadow-lg overflow-hidden">
                  <div className="md:flex">
                    {/* Product Image */}
                    {productData.product.image_url && (
                      <div className="md:w-1/3 bg-gray-100 flex items-center justify-center p-6">
                        <img
                          src={productData.product.image_url}
                          alt={productData.product.name}
                          className="max-h-64 object-contain"
                        />
                      </div>
                    )}

                    {/* Product Details */}
                    <div className={`p-6 ${productData.product.image_url ? 'md:w-2/3' : 'w-full'}`}>
                      <div className="mb-4">
                        <h3 className="text-2xl font-bold text-gray-900 mb-2">{productData.product.name}</h3>
                        {productData.product.brands && (
                          <p className="text-gray-600">Brand: {productData.product.brands}</p>
                        )}
                        <p className="text-sm text-gray-500 mt-1">Barcode: {productData.product.barcode}</p>
                      </div>

                      {/* Scores */}
                      <div className="flex flex-wrap gap-3 mb-6">
                        {productData.product.nutriscore_grade && (
                          <div className="flex items-center space-x-2">
                            <span className="text-sm text-gray-600">Nutri-Score:</span>
                            <span className={`${getNutriscoreColor(productData.product.nutriscore_grade)} text-white font-bold px-3 py-1 rounded`}>
                              {productData.product.nutriscore_grade.toUpperCase()}
                            </span>
                          </div>
                        )}
                        {productData.product.nova_group && (
                          <div className="flex items-center space-x-2">
                            <span className="text-sm text-gray-600">NOVA Group:</span>
                            <span className={`${getNovaColor(productData.product.nova_group)} font-bold`}>
                              {productData.product.nova_group}
                            </span>
                          </div>
                        )}
                      </div>

                      {/* Categories */}
                      {productData.product.categories && productData.product.categories.length > 0 && (
                        <div className="mb-4">
                          <h4 className="text-sm font-semibold text-gray-700 mb-2">Categories</h4>
                          <div className="flex flex-wrap gap-2">
                            {productData.product.categories.slice(0, 5).map((cat, idx) => (
                              <span key={idx} className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">
                                {cat}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* Nutrition */}
                      {productData.product.nutrients && (
                        <div className="mb-4">
                          <h4 className="text-sm font-semibold text-gray-700 mb-2">Nutrition (per 100g)</h4>
                          <div className="grid grid-cols-2 gap-2 text-sm">
                            {productData.product.nutrients.energy_kcal && (
                              <div><span className="text-gray-600">Energy:</span> <span className="font-medium">{productData.product.nutrients.energy_kcal} kcal</span></div>
                            )}
                            {productData.product.nutrients.fat !== undefined && (
                              <div><span className="text-gray-600">Fat:</span> <span className="font-medium">{productData.product.nutrients.fat}g</span></div>
                            )}
                            {productData.product.nutrients.carbohydrates !== undefined && (
                              <div><span className="text-gray-600">Carbs:</span> <span className="font-medium">{productData.product.nutrients.carbohydrates}g</span></div>
                            )}
                            {productData.product.nutrients.proteins !== undefined && (
                              <div><span className="text-gray-600">Protein:</span> <span className="font-medium">{productData.product.nutrients.proteins}g</span></div>
                            )}
                            {productData.product.nutrients.sugars !== undefined && (
                              <div><span className="text-gray-600">Sugars:</span> <span className="font-medium">{productData.product.nutrients.sugars}g</span></div>
                            )}
                            {productData.product.nutrients.salt !== undefined && (
                              <div><span className="text-gray-600">Salt:</span> <span className="font-medium">{productData.product.nutrients.salt}g</span></div>
                            )}
                          </div>
                        </div>
                      )}

                      {/* Ingredients */}
                      {productData.product.ingredients && (
                        <div className="mb-4">
                          <h4 className="text-sm font-semibold text-gray-700 mb-2">Ingredients</h4>
                          <p className="text-sm text-gray-600">{productData.product.ingredients}</p>
                        </div>
                      )}

                      {/* Allergens */}
                      {productData.product.allergens && productData.product.allergens.length > 0 && (
                        <div>
                          <h4 className="text-sm font-semibold text-gray-700 mb-2">Allergens</h4>
                          <div className="flex flex-wrap gap-2">
                            {productData.product.allergens.map((allergen, idx) => (
                              <span key={idx} className="px-2 py-1 bg-red-100 text-red-800 text-xs rounded font-medium">
                                {allergen}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* Source */}
                      <div className="mt-4 pt-4 border-t border-gray-200">
                        <p className="text-xs text-gray-500">
                          Data source: {productData.source === 'openfoodfacts' ? 'Open Food Facts' : 'Local Database'}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
