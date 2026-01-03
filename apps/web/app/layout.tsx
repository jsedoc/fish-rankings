import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Food Safety Platform - Make Informed Food Choices',
  description: 'Research food safety, contaminants, and health impacts across thousands of foods. Evidence-based guidance from FDA, EPA, and academic research.',
  keywords: ['food safety', 'mercury', 'pesticides', 'contaminants', 'nutrition', 'health'],
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="min-h-screen bg-gray-50">
          {children}
        </div>
      </body>
    </html>
  )
}
