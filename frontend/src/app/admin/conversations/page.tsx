'use client'
import { useEffect, useState } from 'react'
import { api } from '@/lib/api'

export default function ConversationsPage() {
  const [conversations, setConversations] = useState<any[]>([])
  const [selected, setSelected] = useState<any>(null)
  const [messages, setMessages] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.conversations.list().then(setConversations).catch(console.error).finally(() => setLoading(false))
  }, [])

  const viewMessages = async (conv: any) => {
    setSelected(conv)
    const msgs = await api.conversations.messages(conv.id).catch(() => [])
    setMessages(msgs)
  }

  return (
    <div className="max-w-7xl mx-auto grid grid-cols-2 gap-6">
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <h2 className="text-lg font-semibold px-5 py-4 border-b">Conversations</h2>
        {loading ? <div className="text-center py-12 text-gray-500">Loading...</div> : (
          <div className="divide-y">
            {conversations.map(conv => (
              <button key={conv.id} onClick={() => viewMessages(conv)}
                className={`w-full text-left px-5 py-3 hover:bg-gray-50 ${selected?.id === conv.id ? 'bg-green-50' : ''}`}>
                <div className="text-sm font-medium text-gray-900">{conv.channel} — {conv.language}</div>
                <div className="text-xs text-gray-500">{new Date(conv.created_at).toLocaleString()}</div>
              </button>
            ))}
            {conversations.length === 0 && <div className="text-center py-12 text-gray-500">No conversations yet</div>}
          </div>
        )}
      </div>
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <h2 className="text-lg font-semibold px-5 py-4 border-b">Messages {selected ? `(${selected.channel})` : ''}</h2>
        <div className="p-4 space-y-3 max-h-96 overflow-y-auto">
          {messages.map(msg => (
            <div key={msg.id} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-xs px-3 py-2 rounded-lg text-sm ${msg.role === 'user' ? 'bg-green-100 text-gray-900' : 'bg-gray-100 text-gray-900'}`}>
                <div className="font-medium text-xs text-gray-500 mb-1">{msg.role}</div>
                {msg.content}
              </div>
            </div>
          ))}
          {!selected && <div className="text-center py-8 text-gray-500">Select a conversation to view messages</div>}
        </div>
      </div>
    </div>
  )
}
