'use client'

export const dynamic = 'force-dynamic'

import { useState } from 'react'
import { ArrowLeft, Search, ScanBarcode, AlertTriangle, CheckCircle, Info } from 'lucide-react'
import { useRouter } from 'next/navigation'
import Image from 'next/image'

interface ProductInfo {
    name: string
    brands: string
    image_url: string
    nutriscore_grade: string
    nova_group: number
    ecoscore_grade: string
    ingredients: string
    nutrients: any
}

interface RecallInfo {
    recall_number: string
    reason: string
    classification: string
    date: string
}

interface ScanResult {
    source: string
    found: boolean
    message?: string
    product: ProductInfo
    recalls: RecallInfo[]
    has_active_recalls: boolean
    can_import: boolean
}

export default function ScanPage() {
    const router = useRouter()
    const [barcode, setBarcode] = useState('')
    const [loading, setLoading] = useState(false)
    const [result, setResult] = useState<ScanResult | null>(null)
    const [error, setError] = useState('')

    const handleScan = async (e: React.FormEvent) => {
        e.preventDefault()
        if (!barcode) return

        setLoading(true)
        setError('')
        setResult(null)

        try {
            const res = await fetch(`/api/v1/barcode/lookup/${barcode}`)
            if (!res.ok) throw new Error('Failed to lookup product')
            const data = await res.json()

            if (!data.found) {
                setError(data.message || 'Product not found')
            } else {
                setResult(data)
            }
        } catch (err) {
            setError('Error connecting to scanner service')
            console.error(err)
        } finally {
            setLoading(false)
        }
    }

    const getNutriscoreColor = (grade: string) => {
        switch (grade?.toLowerCase()) {
            case 'a': return 'bg-green-600'
            case 'b': return 'bg-green-400'
            case 'c': return 'bg-yellow-400'
            case 'd': return 'bg-orange-400'
            case 'e': return 'bg-red-500'
            default: return 'bg-gray-400'
        }
    }

    return (
        <div className="min-h-screen bg-gray-50">
            <header className="bg-white border-b border-gray-200">
                <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
                    <button onClick={() => router.push('/')} className="flex items-center text-gray-600 hover:text-gray-900">
                        <ArrowLeft className="w-5 h-5 mr-2" />
                        Back to Home
                    </button>
                </div>
            </header>

            <main className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <div className="text-center mb-8">
                    <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-100 rounded-full mb-4">
                        <ScanBarcode className="w-8 h-8 text-blue-600" />
                    </div>
                    <h1 className="text-3xl font-bold text-gray-900">Product Scanner</h1>
                    <p className="text-gray-600 mt-2">Enter a barcode to check for safety and recalls</p>
                </div>

                <div className="card p-6 mb-8">
                    <form onSubmit={handleScan} className="flex gap-2">
                        <input
                            type="text"
                            placeholder="Enter barcode (e.g. 5449000000996)"
                            className="flex-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none"
                            value={barcode}
                            onChange={(e) => setBarcode(e.target.value)}
                        />
                        <button
                            type="submit"
                            disabled={loading || !barcode}
                            className="btn btn-primary px-6"
                        >
                            {loading ? 'Scanning...' : 'Check'}
                        </button>
                    </form>
                    <div className="mt-3 text-xs text-center text-gray-500">
                        Example barcodes: 0049000006346 (Coke), 3017620422003 (Nutella)
                    </div>
                </div>

                {error && (
                    <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-center text-red-700 mb-8">
                        <AlertTriangle className="w-6 h-6 mx-auto mb-2" />
                        {error}
                    </div>
                )}

                {result && (
                    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
                        {/* Main Product Card */}
                        <div className="card overflow-hidden">
                            <div className="p-6">
                                <div className="flex flex-col md:flex-row gap-6">
                                    {result.product.image_url && (
                                        <div className="w-32 h-32 relative flex-shrink-0 bg-white rounded-lg border border-gray-100 mx-auto md:mx-0">
                                            <Image
                                                src={result.product.image_url}
                                                alt={result.product.name}
                                                fill
                                                className="object-contain p-2"
                                            />
                                        </div>
                                    )}
                                    <div className="flex-1 text-center md:text-left">
                                        <h2 className="text-2xl font-bold text-gray-900 mb-1">{result.product.name}</h2>
                                        <p className="text-gray-600 mb-4">{result.product.brands}</p>

                                        {/* Badges */}
                                        <div className="flex flex-wrap justify-center md:justify-start gap-3">
                                            {result.product.nutriscore_grade && (
                                                <span className={`px-3 py-1 rounded-full text-white font-bold uppercase text-sm ${getNutriscoreColor(result.product.nutriscore_grade)}`}>
                                                    Nutri-Score {result.product.nutriscore_grade}
                                                </span>
                                            )}
                                            {result.product.nova_group && (
                                                <span className="px-3 py-1 rounded-full bg-gray-100 text-gray-700 border border-gray-200 text-sm">
                                                    NOVA {result.product.nova_group}
                                                </span>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            </div>

                            {/* Product Details Section */}
                            <div className="bg-gray-50 px-6 py-4 border-t border-gray-200">
                                {result.product.ingredients && (
                                    <div className="mb-4">
                                        <h4 className="text-sm font-semibold text-gray-900 uppercase tracking-wider mb-2">Ingredients</h4>
                                        <p className="text-sm text-gray-600">{result.product.ingredients}</p>
                                    </div>
                                )}
                            </div>
                        </div>

                        {/* Safety Status */}
                        {result.has_active_recalls ? (
                            <div className="bg-red-50 border border-red-200 rounded-lg p-6">
                                <div className="flex items-start">
                                    <AlertTriangle className="w-6 h-6 text-red-600 mr-3 flex-shrink-0 mt-0.5" />
                                    <div>
                                        <h3 className="text-lg font-bold text-red-900 mb-2">Active Recalls Found!</h3>
                                        <p className="text-red-700 mb-4">
                                            This product matches {result.recalls.length} active recall alert(s).
                                        </p>
                                        <div className="space-y-3">
                                            {result.recalls.map((recall, idx) => (
                                                <div key={idx} className="bg-white p-3 rounded border border-red-100 shadow-sm">
                                                    <div className="flex justify-between text-xs text-gray-500 mb-1">
                                                        <span>{recall.recall_number}</span>
                                                        <span>{new Date(recall.date).toLocaleDateString()}</span>
                                                    </div>
                                                    <p className="text-sm font-medium text-gray-900">{recall.reason}</p>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ) : (
                            <div className="bg-green-50 border border-green-200 rounded-lg p-6 flex items-center">
                                <CheckCircle className="w-8 h-8 text-green-500 mr-4" />
                                <div>
                                    <h3 className="text-lg font-bold text-green-900">No Active Recalls</h3>
                                    <p className="text-green-700">
                                        No FDA recall alerts were found matching this product name.
                                    </p>
                                </div>
                            </div>
                        )}
                    </div>
                )}
            </main>
        </div>
    )
}
