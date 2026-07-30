import type { Metadata } from 'next'
import './globals.css'
import Link from 'next/link'

export const metadata: Metadata = {
  title: 'Mana Mitra | Government Chatbot',
  description: 'Multilingual Government Services Chatbot for Andhra Pradesh',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-gray-50 min-h-screen">
        <nav className="bg-green-800 text-white px-6 py-4 flex items-center gap-8">
          <span className="font-bold text-lg">Mana Mitra</span>
          <Link href="/chat" className="hover:text-green-200 text-sm">Chat</Link>
          <Link href="/admin" className="hover:text-green-200 text-sm">Admin</Link>
          <Link href="/admin/conversations" className="hover:text-green-200 text-sm">Conversations</Link>
          <Link href="/admin/schemes" className="hover:text-green-200 text-sm">Schemes</Link>
        </nav>
        <main className="p-6">{children}</main>
      </body>
    </html>
  )
}
