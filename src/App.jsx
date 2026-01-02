import { useState } from 'react'
import FishTable from './components/FishTable'
import fishData from './data/fish.json'

function App() {
  return (
    <div className="min-h-screen bg-ocean-dark text-white font-sans selection:bg-accent-teal selection:text-white">

      {/* Hero Section */}
      <header className="relative pt-20 pb-16 px-6 text-center overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-accent-teal/10 to-transparent pointer-events-none" />
        <div className="relative z-10 max-w-3xl mx-auto">
          <div className="inline-flex items-center justify-center p-1.5 mb-6 bg-white/5 rounded-full border border-white/10 backdrop-blur-sm animate-fade-in">
            <span className="px-3 py-1 text-xs font-medium tracking-wide text-accent-teal uppercase">Updated Database</span>
          </div>
          <h1 className="text-5xl md:text-6xl font-extrabold tracking-tight mb-6 bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400 animate-slide-up">
            Seafood Safety Ranker
          </h1>
          <p className="text-lg text-slate-400 max-w-2xl mx-auto leading-relaxed animate-slide-up" style={{ animationDelay: '0.1s' }}>
            Make informed decisions about your seafood consumption. Browse our comprehensive database of FDA mercury levels to find the healthiest options for you and your family.
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="px-4 pb-20 animate-slide-up" style={{ animationDelay: '0.2s' }}>
        <FishTable data={fishData} />
      </main>

    </div>
  )
}

export default App
