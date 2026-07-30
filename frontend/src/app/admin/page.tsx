'use client'
import { useEffect, useState } from 'react'
import { api } from '@/lib/api'
import Link from 'next/link'

export default function AdminPage() {
  const [conversations, setConversations] = useState<any[]>([])
  const [schemes, setSchemes] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([api.conversations.list(), api.schemes.list()])
      .then(([c, s]) => { setConversations(c); setSchemes(s) })
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Admin Dashboard</h1>
      <div className="grid grid-cols-3 gap-4">
        {[
          { label: 'Total Conversations', value: conversations.length, href: '/admin/conversations' },
          { label: 'Active Schemes', value: schemes.filter(s => s.is_active).length, href: '/admin/schemes' },
          { label: 'Channels', value: 'Web, WhatsApp', href: '#' },
        ].map(card => (
          <Link key={card.label} href={card.href} className="bg-white rounded-lg shadow p-5 hover:shadow-md transition-shadow">
            <div className="text-3xl font-bold text-green-700 mb-1">{card.value}</div>
            <p className="text-sm text-gray-600">{card.label}</p>
          </Link>
        ))}
      </div>
    </div>
  )
}
