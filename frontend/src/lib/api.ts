const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!res.ok) throw new Error(`API error: ${res.status}`)
  return res.json()
}

export const api = {
  chat: (data: any) => apiFetch<any>('/api/v1/chat/', { method: 'POST', body: JSON.stringify(data) }),
  conversations: {
    list: () => apiFetch<any[]>('/api/v1/conversations/'),
    messages: (id: string) => apiFetch<any[]>(`/api/v1/conversations/${id}/messages`),
  },
  schemes: {
    list: () => apiFetch<any[]>('/api/v1/schemes/'),
    create: (data: any) => apiFetch<any>('/api/v1/schemes/', { method: 'POST', body: JSON.stringify(data) }),
  },
}
