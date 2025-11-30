import React from 'react'
import Link from 'next/link'
import { Button } from '@/components/ui/button'

const roles = [
  { key: 'student', desc: 'Access enrollment, schedules & fees.' },
  { key: 'registrar', desc: 'Approve enrollments & manage curriculum.' },
  { key: 'cashier', desc: 'Process & confirm student payments.' },
  { key: 'faculty', desc: 'View assigned classes & schedules.' },
  { key: 'admin', desc: 'System oversight & configuration.' },
]

export default function RoleSelectPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-white to-slate-100 p-6">
      <div className="max-w-xl w-full space-y-8">
        <h1 className="text-3xl font-semibold text-slate-800 text-center">Select Role</h1>
        <div className="grid gap-4">
          {roles.map(r => (
            <div key={r.key} className="rounded-xl border border-slate-200 bg-white p-5 flex items-center justify-between hover:shadow-sm transition">
              <div>
                <div className="font-medium capitalize text-slate-700">{r.key}</div>
                <div className="text-xs text-slate-500">{r.desc}</div>
              </div>
              <Link href={`/auth/login?role=${r.key}`}>
                <Button variant="outline">Login</Button>
              </Link>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}