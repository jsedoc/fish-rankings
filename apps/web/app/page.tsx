'use client'

import { useState } from 'react'
import { Search, Fish, Leaf, Beef, Milk, Scan, AlertTriangle, Shield, Waves } from 'lucide-react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'

export default function HomePage() {
  const [searchQuery, setSearchQuery] = useState('')
  const router = useRouter()

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    if (searchQuery.trim()) {
      router.push(`/search?q=${encodeURIComponent(searchQuery)}`)
    }
  }

  const categories = [
    { name: 'Seafood', slug: 'seafood', icon: Fish, color: 'from-blue-500 to-cyan-500', count: '60+', recalls: '150+' },
    { name: 'Produce', slug: 'produce', icon: Leaf, color: 'from-green-500 to-emerald-500', count: '40+', recalls: '50+' },
    { name: 'Meat & Poultry', slug: 'meat-poultry', icon: Beef, color: 'from-red-500 to-orange-500', count: '25+', recalls: '300+' },
    { name: 'Dairy', slug: 'dairy', icon: Milk, color: 'from-purple-500 to-pink-500', count: '20+', recalls: '150+' },
  ]

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-primary-700 rounded-lg flex items-center justify-center">
                <Leaf className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">Food Safety Platform</h1>
                <p className="text-xs text-gray-500">Evidence-based food safety insights</p>
              </div>
            </div>
            <nav className="hidden md:flex space-x-6">
              <Link href="/barcode" className="text-gray-600 hover:text-gray-900 text-sm font-medium">
                Barcode Scanner
              </Link>
              <Link href="/recalls" className="text-gray-600 hover:text-gray-900 text-sm font-medium">
                Recalls
              </Link>
              <Link href="/about" className="text-gray-600 hover:text-gray-900 text-sm font-medium">
                About
              </Link>
              <Link href="/sources" className="text-gray-600 hover:text-gray-900 text-sm font-medium">
                Data Sources
              </Link>
            </nav>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-primary-500 via-primary-600 to-primary-700 text-white py-20 px-4">
        <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-10"></div>
        <div className="relative max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center px-4 py-2 bg-white/10 rounded-full border border-white/20 backdrop-blur-sm mb-6">
            <span className="text-sm font-medium">✨ New: 2.3M+ Products • FDA Recalls • Barcode Scanner</span>
          </div>

          <h2 className="text-5xl md:text-6xl font-extrabold mb-6 leading-tight">
            Make Informed<br />Food Choices
          </h2>

          <p className="text-xl md:text-2xl text-primary-100 max-w-2xl mx-auto mb-10 leading-relaxed">
            Research food safety, contaminants, and health impacts backed by FDA, EPA, and academic research
          </p>

          {/* Search Bar */}
          <form onSubmit={handleSearch} className="max-w-2xl mx-auto">
            <div className="relative">
              <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search for any food... (e.g., salmon, strawberries, chicken)"
                className="w-full pl-12 pr-4 py-4 text-lg rounded-xl border-0 shadow-2xl text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-4 focus:ring-accent-500/50"
              />
            </div>
          </form>

          <p className="mt-4 text-sm text-primary-200">
            Popular searches: <button onClick={() => router.push('/search?q=salmon')} className="underline hover:text-white">Salmon</button> • <button onClick={() => router.push('/search?q=strawberries')} className="underline hover:text-white">Strawberries</button> • <button onClick={() => router.push('/search?q=tuna')} className="underline hover:text-white">Tuna</button>
          </p>
        </div>
      </section>

      {/* Categories */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <h3 className="text-2xl font-bold text-gray-900 mb-8">Browse by Category</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {categories.map((category) => {
            const Icon = category.icon
            return (
              <Link
                key={category.slug}
                href={`/category/${category.slug}`}
                className="card p-6 hover:scale-105 transition-transform"
              >
                <div className={`w-12 h-12 rounded-lg bg-gradient-to-br ${category.color} flex items-center justify-center mb-4`}>
                  <Icon className="w-6 h-6 text-white" />
                </div>
                <h4 className="text-lg font-semibold text-gray-900 mb-1">{category.name}</h4>
                <p className="text-sm text-gray-600 mb-1">{category.count} foods</p>
                <p className="text-xs text-red-600 font-medium">{category.recalls} recalls</p>
              </Link>
            )
          })}
        </div>
      </section>

      {/* New Features - Milestone 2 */}
      <section className="bg-gradient-to-br from-blue-50 to-cyan-50 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <span className="inline-block px-4 py-2 bg-blue-600 text-white text-sm font-semibold rounded-full mb-4">
              NEW FEATURES
            </span>
            <h3 className="text-3xl font-bold text-gray-900 mb-4">Milestone 2: Advanced Food Safety Tools</h3>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Access 2.3M+ products, real-time recalls, and comprehensive safety data
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <Link href="/barcode" className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-all transform hover:-translate-y-1">
              <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-lg flex items-center justify-center mb-4">
                <Scan className="w-6 h-6 text-white" />
              </div>
              <h4 className="text-lg font-semibold text-gray-900 mb-2">Barcode Scanner</h4>
              <p className="text-sm text-gray-600 mb-3">Scan any product to check nutrition, ingredients, and recalls</p>
              <div className="text-blue-600 text-sm font-medium">2.3M+ products →</div>
            </Link>

            <Link href="/recalls" className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-all transform hover:-translate-y-1">
              <div className="w-12 h-12 bg-gradient-to-br from-red-500 to-orange-500 rounded-lg flex items-center justify-center mb-4">
                <AlertTriangle className="w-6 h-6 text-white" />
              </div>
              <h4 className="text-lg font-semibold text-gray-900 mb-2">FDA Recalls</h4>
              <p className="text-sm text-gray-600 mb-3">Stay updated on food safety recalls and product alerts</p>
              <div className="text-red-600 text-sm font-medium">700+ recalls →</div>
            </Link>

            <Link href="/advisories" className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-all transform hover:-translate-y-1">
              <div className="w-12 h-12 bg-gradient-to-br from-green-500 to-emerald-500 rounded-lg flex items-center justify-center mb-4">
                <Shield className="w-6 h-6 text-white" />
              </div>
              <h4 className="text-lg font-semibold text-gray-900 mb-2">EPA Advisories</h4>
              <p className="text-sm text-gray-600 mb-3">Fish consumption warnings by state and waterbody</p>
              <div className="text-green-600 text-sm font-medium">100+ advisories →</div>
            </Link>

            <Link href="/sustainability" className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-all transform hover:-translate-y-1">
              <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-lg flex items-center justify-center mb-4">
                <Waves className="w-6 h-6 text-white" />
              </div>
              <h4 className="text-lg font-semibold text-gray-900 mb-2">Sustainability</h4>
              <p className="text-sm text-gray-600 mb-3">NOAA ratings for sustainable seafood choices</p>
              <div className="text-blue-600 text-sm font-medium">14+ ratings →</div>
            </Link>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="bg-white border-y border-gray-200 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h3 className="text-2xl font-bold text-gray-900 mb-8 text-center">Why Use Our Platform?</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-3xl">📊</span>
              </div>
              <h4 className="text-lg font-semibold mb-2">Evidence-Based</h4>
              <p className="text-gray-600">All data from FDA, EPA, EWG, and peer-reviewed research</p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-accent-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-3xl">🔍</span>
              </div>
              <h4 className="text-lg font-semibold mb-2">Transparent</h4>
              <p className="text-gray-600">Every claim cited with sources and last updated dates</p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-3xl">✅</span>
              </div>
              <h4 className="text-lg font-semibold mb-2">Actionable</h4>
              <p className="text-gray-600">Clear guidance on safe consumption and alternatives</p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-300 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div>
              <h5 className="text-white font-semibold mb-4">Food Safety Platform</h5>
              <p className="text-sm">
                Empowering consumers with transparent, data-driven food safety insights.
              </p>
            </div>
            <div>
              <h5 className="text-white font-semibold mb-4">Resources</h5>
              <ul className="space-y-2 text-sm">
                <li><Link href="/about" className="hover:text-white">About Us</Link></li>
                <li><Link href="/sources" className="hover:text-white">Data Sources</Link></li>
                <li><Link href="/research" className="hover:text-white">Research Papers</Link></li>
              </ul>
            </div>
            <div>
              <h5 className="text-white font-semibold mb-4">Disclaimer</h5>
              <p className="text-xs">
                This platform provides educational information only. Always consult healthcare professionals for medical advice.
              </p>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-sm">
            <p>© 2025 Food Safety Platform. Data from FDA, EPA, EWG, USDA, and PubMed.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
