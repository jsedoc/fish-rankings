'use client'

import { ArrowLeft } from 'lucide-react'
import { useRouter } from 'next/navigation'

export default function AboutPage() {
    const router = useRouter()

    return (
        <div className="min-h-screen bg-gray-50">
            <header className="bg-white border-b border-gray-200">
                <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
                    <button onClick={() => router.push('/')} className="flex items-center text-gray-600 hover:text-gray-900">
                        <ArrowLeft className="w-5 h-5 mr-2" />
                        Back to Home
                    </button>
                </div>
            </header>

            <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <div className="card p-8">
                    <h1 className="text-3xl font-bold text-gray-900 mb-6">About the Food Safety Platform</h1>

                    <div className="prose max-w-none text-gray-600 space-y-4">
                        <p>
                            The Food Safety Platform is a comprehensive database designed to help consumers make informed decisions about the food they eat.
                            By aggregating data from trusted government and scientific sources, we provide transparent information about contaminants and nutritional benefits in common foods.
                        </p>

                        <h2 className="text-xl font-semibold text-gray-900 mt-6">Our Mission</h2>
                        <p>
                            Information about food safety is often scattered across various agency websites and scientific journals, making it difficult for the average consumer to access and understand.
                            Our mission is to centralize this data and present it in a clear, easy-to-understand format.
                        </p>

                        <h2 className="text-xl font-semibold text-gray-900 mt-6">How It Works</h2>
                        <p>
                            We collect data from sources like the FDA, USDA, and independent research studies. This data is processed to normalize units and calculate safety scores based on established risk levels.
                        </p>
                        <ul className="list-disc pl-5 space-y-2">
                            <li><strong>Mercury in Fish:</strong> Based on FDA data from 1990-2012.</li>
                            <li><strong>Pesticides in Produce:</strong> Based on USDA and EWG data.</li>
                        </ul>

                        <h2 className="text-xl font-semibold text-gray-900 mt-6">Disclaimer</h2>
                        <p className="bg-yellow-50 p-4 rounded-lg border border-yellow-200 text-yellow-900">
                            This website is for educational purposes only. While we strive for accuracy, recommendations should not replace professional medical advice.
                            Data sources may specific to certain regions or time periods.
                        </p>
                    </div>
                </div>
            </main>
        </div>
    )
}
