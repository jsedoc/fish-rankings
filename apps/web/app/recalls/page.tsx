'use client'

export const dynamic = 'force-dynamic'

import { useState, useEffect } from 'react'
import { ArrowLeft, Search, AlertTriangle, ExternalLink } from 'lucide-react'
import { useRouter } from 'next/navigation'

interface Recall {
    id: string
    recall_number: string
    product_description: string
    reason_for_recall: string
    recall_date: string
    company_name: string
    status: string
    classification: string
    product_quantity: string
    city: string | null
    state: string | null
    distribution_pattern: string | null
}

interface RecallResponse {
    recalls: Recall[]
    total: number
    skip: number
    limit: number
}

export default function RecallsPage() {
    const router = useRouter()
    const [recalls, setRecalls] = useState<Recall[]>([])
    const [loading, setLoading] = useState(true)
    const [searchQuery, setSearchQuery] = useState('')
    const [debouncedQuery, setDebouncedQuery] = useState('')

    useEffect(() => {
        const timer = setTimeout(() => {
            setDebouncedQuery(searchQuery)
        }, 500)
        return () => clearTimeout(timer)
    }, [searchQuery])

    useEffect(() => {
        setLoading(true)
        const url = debouncedQuery
            ? `/api/v1/recalls?search=${encodeURIComponent(debouncedQuery)}`
            : `/api/v1/recalls/recent?limit=50`

        fetch(url)
            .then(res => res.json())
            .then((data: RecallResponse | Recall[]) => {
                // '/recent' returns array, '/recalls' returns object with list
                const list = Array.isArray(data) ? data : data.recalls
                setRecalls(list || [])
                setLoading(false)
            })
            .catch(err => {
                console.error(err)
                setLoading(false)
            })
    }, [debouncedQuery])

    const getSeverityColor = (classification: string) => {
        if (classification?.includes('Class I')) return 'bg-red-100 text-red-800 border-red-200'
        if (classification?.includes('Class II')) return 'bg-orange-100 text-orange-800 border-orange-200'
        return 'bg-yellow-100 text-yellow-800 border-yellow-200'
    }

    const getSeverityLabel = (classification: string) => {
        if (classification?.includes('Class I')) return 'Critical (Class I)'
        if (classification?.includes('Class II')) return 'High (Class II)'
        return 'Moderate (Class III)'
    }

    return (
        <div className="min-h-screen bg-gray-50">
            <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
                <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
                    <div className="flex items-center justify-between mb-4">
                        <button onClick={() => router.push('/')} className="flex items-center text-gray-600 hover:text-gray-900">
                            <ArrowLeft className="w-5 h-5 mr-2" />
                            Back to Home
                        </button>
                        <h1 className="text-2xl font-bold text-gray-900">FDA Food Recalls</h1>
                    </div>

                    <div className="relative">
                        <input
                            type="text"
                            placeholder="Search recalls by product (e.g., 'cheese', 'salad')..."
                            className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                        />
                        <Search className="w-5 h-5 text-gray-400 absolute left-3 top-3.5" />
                    </div>
                </div>
            </header>

            <main className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {loading ? (
                    <div className="text-center py-12">
                        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 mx-auto mb-4"></div>
                        <p className="text-gray-500">Loading recalls...</p>
                    </div>
                ) : recalls.length === 0 ? (
                    <div className="text-center py-12 bg-white rounded-lg border border-gray-200">
                        <AlertTriangle className="w-12 h-12 text-gray-300 mx-auto mb-3" />
                        <h3 className="text-lg font-medium text-gray-900">No recalls found</h3>
                        <p className="text-gray-500 mt-1">Try adjusting your search terms.</p>
                    </div>
                ) : (
                    <div className="space-y-4">
                        <p className="text-sm text-gray-500 mb-2">Showing {recalls.length} recent recalls</p>
                        {recalls.map((recall) => (
                            <div key={recall.id || recall.recall_number} className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow">
                                <div className="p-6">
                                    <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
                                        <div className="flex-1">
                                            <div className="flex items-center gap-2 mb-2">
                                                <span className={`px-2.5 py-0.5 rounded-full text-xs font-semibold border ${getSeverityColor(recall.classification)}`}>
                                                    {getSeverityLabel(recall.classification)}
                                                </span>
                                                <span className="text-xs text-gray-500">
                                                    {new Date(recall.recall_date).toLocaleDateString()}
                                                </span>
                                            </div>
                                            <h3 className="text-lg font-semibold text-gray-900 mb-2">
                                                {recall.product_description}
                                            </h3>
                                            <p className="text-gray-600 text-sm mb-3">
                                                <span className="font-medium">Reason:</span> {recall.reason_for_recall}
                                            </p>

                                            <div className="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-2 text-xs text-gray-500">
                                                <p><span className="font-medium text-gray-700">Company:</span> {recall.company_name}</p>
                                                <p><span className="font-medium text-gray-700">Distribution:</span> {recall.distribution_pattern || 'Not specified'}</p>
                                                <p><span className="font-medium text-gray-700">Quantity:</span> {recall.product_quantity || 'Unknown'}</p>
                                                <p><span className="font-medium text-gray-700">Location:</span> {recall.city}, {recall.state}</p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </main>
        </div>
    )
}
