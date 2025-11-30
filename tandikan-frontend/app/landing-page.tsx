import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { motion } from 'framer-motion'

const roles = [
  { key: 'student', label: 'Student' },
  { key: 'registrar', label: 'Registrar' },
  { key: 'cashier', label: 'Cashier' },
  { key: 'faculty', label: 'Faculty' },
  { key: 'admin', label: 'Admin' },
]

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-slate-50 via-white to-slate-100">
      <nav className="border-b bg-white/70 backdrop-blur-sm sticky top-0 z-40">
        <div className="mx-auto max-w-6xl px-6 py-3 flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <div className="w-10 h-10 bg-slate-800 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-xl">T</span>
            </div>
            <span className="text-xl font-semibold text-slate-800">Tandikan Enrollment</span>
          </div>
          <div className="flex gap-3">
            <Link href="/auth/role-select"><Button variant="outline">Choose Role</Button></Link>
            <Link href="/auth/login"><Button>Login</Button></Link>
          </div>
        </div>
      </nav>

      <section className="relative isolate py-20 sm:py-28">
        <div className="mx-auto max-w-5xl px-6 text-center">
          <motion.h1 initial={{opacity:0,y:20}} animate={{opacity:1,y:0}} transition={{duration:0.6}} className="text-4xl sm:text-5xl font-bold tracking-tight text-slate-800">
            University Computerized Enrollment System
          </motion.h1>
          <motion.p initial={{opacity:0,y:20}} animate={{opacity:1,y:0}} transition={{duration:0.8}} className="mt-6 text-lg leading-8 text-slate-600 max-w-2xl mx-auto">
            Seamless subject selection, conflict-free scheduling, transparent fee assessment, and secure payment integration.
          </motion.p>
          <motion.div initial={{opacity:0}} animate={{opacity:1}} transition={{delay:0.9}} className="mt-10 flex flex-wrap justify-center gap-4">
            {roles.map(r => (
              <Link key={r.key} href={`/auth/login?role=${r.key}`}>
                <Button variant="outline" className="rounded-full border-slate-300 hover:bg-slate-800 hover:text-white transition">
                  {r.label} Portal
                </Button>
              </Link>
            ))}
          </motion.div>
        </div>
        <div className="pointer-events-none absolute inset-0 -z-10 bg-[radial-gradient(circle_at_center,rgba(15,23,42,0.08),transparent_60%)]" />
      </section>

      <section className="py-14 bg-white/70 backdrop-blur">
        <div className="mx-auto max-w-6xl px-6">
          <h2 className="text-xl font-semibold text-slate-700 mb-6">Quick Access</h2>
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
              {[
                { title: 'Enrollment Portal', href: '/dashboard/student' },
                { title: 'Subject Catalog', href: '/subjects' },
                { title: 'Academic Calendar', href: '/calendar' },
                { title: 'Payments Center', href: '/payments' },
              ].map(link => (
                <Link key={link.title} href={link.href} className="group rounded-xl border border-slate-200 p-5 bg-white shadow-sm hover:shadow-md transition">
                  <div className="font-medium text-slate-800 group-hover:text-slate-900">{link.title}</div>
                  <div className="mt-2 text-xs text-slate-500">Open {link.title}</div>
                </Link>
              ))}
            </div>
        </div>
      </section>

      <footer className="mt-auto py-6 text-center text-sm text-slate-500">© {new Date().getFullYear()} Tandikan University Enrollment System</footer>
    </div>
  )
}
