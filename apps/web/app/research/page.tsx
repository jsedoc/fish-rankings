'use client'

export const dynamic = 'force-dynamic'

import { useState, useEffect } from 'react'
import { ArrowLeft, FileText, ExternalLink } from 'lucide-react'
import { useRouter } from 'next/navigation'

interface ResearchPaper {
    id: string
    title: string
    authors: string[]
    journal: string | null
    publication_date: string | null
    url: string | null
    abstract: string | null
}

export default function ResearchPage() {
    const router = useRouter()
    const [papers, setPapers] = useState<ResearchPaper[]>([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        fetch('/api/v1/research')
            .then(res => res.json())
            .then(data => {
                setPapers(data)
                setLoading(false)
            })
            .catch(err => {
                console.error(err)
                setLoading(false)
            })
    }, [])

    return (
        <div className="min-h-screen bg-gray-50">
            <header className="bg-white border-b border-gray-200">
                <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
                    <button onClick={() => router.push('/')} className="flex items-center text-gray-600 hover:text-gray-900">
                        <ArrowLeft className="w-5 h-5 mr-2" />
                        Back to Home
                    </button>
                </div>
            </header>

            <main className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <h1 className="text-3xl font-bold text-gray-900 mb-6">Research & Scientific References</h1>
                <p className="text-gray-600 mb-8">
                    A collection of peer-reviewed studies and authoritative reports supporting our data.
                </p>

                {loading ? (
                    <div className="text-center py-12">
                        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 mx-auto"></div>
                    </div>
                ) : (
                    <div className="space-y-6">
                        {papers.map((paper) => (
                            <div key={paper.id} className="card p-6">
                                <div className="flex items-start">
                                    <FileText className="w-6 h-6 text-gray-400 mt-1 mr-4 flex-shrink-0" />
                                    <div className="flex-1">
                                        <h2 className="text-xl font-semibold text-gray-900 hover:text-primary-600 transition-colors">
                                            {paper.url ? (
                                                <a href={paper.url} target="_blank" rel="noopener noreferrer" className="flex items-center">
                                                    {paper.title}
                                                    <ExternalLink className="w-4 h-4 ml-2 opacity-50" />
                                                </a>
                                            ) : (
                                                paper.title
                                            )}
                                        </h2>
                                        <p className="text-sm text-gray-600 mt-1">
                                            {paper.authors.length > 0 ? paper.authors.join(', ') : 'Unknown Authors'}
                                            {paper.journal && ` • ${paper.journal}`}
                                            {paper.publication_date && ` • ${new Date(paper.publication_date).getFullYear()}`}
                                        </p>
                                        {paper.abstract && (
                                            <p className="text-gray-700 mt-3 text-sm line-clamp-3">
                                                {paper.abstract}
                                            </p>
                                        )}
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
