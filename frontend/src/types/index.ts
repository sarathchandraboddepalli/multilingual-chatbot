export interface Conversation {
  id: string
  channel: string
  language: string
  status: string
  created_at: string
}

export interface Message {
  id: string
  role: string
  content: string
  language: string
  created_at: string
}

export interface Scheme {
  id: string
  scheme_id: string
  name: string
  description: string
  category: string | null
  is_active: boolean
}
