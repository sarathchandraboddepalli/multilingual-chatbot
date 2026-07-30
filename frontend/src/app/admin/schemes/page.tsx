'use client'
import { useEffect, useState } from 'react'
import { api } from '@/lib/api'

export default function SchemesPage() {
  const [schemes, setSchemes] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [form, setForm] = useState({ scheme_id: '', name: '', description: '', category: '' })

  const loadSchemes = () => {
    api.schemes.list().then(setSchemes).catch(console.error).finally(() => setLoading(false))
  }
  useEffect(() => { loadSchemes() }, [])

  const addScheme = async () => {
    if (!form.scheme_id || !form.name || !form.description) return
    await api.schemes.create(form).catch(console.error)
    setForm({ scheme_id: '', name: '', description: '', category: '' })
    loadSchemes()
  }

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Knowledge Base — Government Schemes</h1>
      <div className="bg-white rounded-lg shadow p-5">
        <h2 className="text-lg font-semibold mb-4">Add Scheme</h2>
        <div className="grid grid-cols-2 gap-3">
          <input className="border rounded px-3 py-2 text-sm" placeholder="Scheme ID (e.g. YSR-PENSION)" value={form.scheme_id} onChange={e => setForm(f => ({...f, scheme_id: e.target.value}))} />
          <input className="border rounded px-3 py-2 text-sm" placeholder="Scheme Name" value={form.name} onChange={e => setForm(f => ({...f, name: e.target.value}))} />
          <input className="border rounded px-3 py-2 text-sm" placeholder="Category" value={form.category} onChange={e => setForm(f => ({...f, category: e.target.value}))} />
          <textarea className="border rounded px-3 py-2 text-sm col-span-2" rows={3} placeholder="Description" value={form.description} onChange={e => setForm(f => ({...f, description: e.target.value}))} />
          <button onClick={addScheme} className="bg-green-600 text-white px-4 py-2 rounded text-sm hover:bg-green-700">Add Scheme</button>
        </div>
      </div>
      {loading ? <div className="text-center py-12 text-gray-500">Loading...</div> : (
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                {['ID', 'Name', 'Category', 'Status'].map(h => (
                  <th key={h} className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {schemes.map(s => (
                <tr key={s.id} className="hover:bg-gray-50">
                  <td className="px-4 py-3 text-sm font-mono text-gray-700">{s.scheme_id}</td>
                  <td className="px-4 py-3 text-sm font-medium text-gray-900">{s.name}</td>
                  <td className="px-4 py-3 text-sm text-gray-500">{s.category || '—'}</td>
                  <td className="px-4 py-3 text-sm">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${s.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`}>
                      {s.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {schemes.length === 0 && <div className="text-center py-12 text-gray-500">No schemes added yet</div>}
        </div>
      )}
    </div>
  )
}
