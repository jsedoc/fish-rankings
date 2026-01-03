'use client'

import { useState, useEffect } from 'react'
import { notFound } from 'next/navigation'

export default function FoodDetailPage({ params }: { params: { slug: string } }) {
  const [food, setFood] = useState<any>(null)
  const [loading, setLoading] = useState(true)

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

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold mb-4">{food.name}</h1>
      <div className="prose max-w-none">
        <p>{food.description}</p>
      </div>
    </div>
  )
}