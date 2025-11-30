'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';

interface SidebarProps {
  role: 'student' | 'registrar' | 'cashier';
}

export function Sidebar({ role }: SidebarProps) {
  const pathname = usePathname();

  const studentLinks = [
    { href: '/student', label: 'Dashboard', icon: '📊' },
    { href: '/student/enrollment', label: 'Enrollment', icon: '📝' },
    { href: '/student/schedule', label: 'Schedule', icon: '📅' },
    { href: '/student/fees', label: 'Fees & Payments', icon: '💰' },
  ];

  const registrarLinks = [
    { href: '/registrar', label: 'Dashboard', icon: '📊' },
    { href: '/registrar/students', label: 'Students', icon: '👥' },
    { href: '/registrar/subjects', label: 'Subjects', icon: '📚' },
    { href: '/registrar/enrollments', label: 'Enrollments', icon: '📋' },
  ];

  const cashierLinks = [
    { href: '/cashier', label: 'Dashboard', icon: '📊' },
    { href: '/cashier/payments', label: 'Payments', icon: '💵' },
    { href: '/cashier/assessments', label: 'Assessments', icon: '📄' },
  ];

  const links = role === 'student' ? studentLinks : role === 'registrar' ? registrarLinks : cashierLinks;

  return (
    <div className="w-64 bg-gray-900 text-white min-h-screen p-6">
      <div className="mb-8">
        <div className="flex items-center space-x-2">
          <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-xl">T</span>
          </div>
          <span className="text-xl font-bold">Tandikan</span>
        </div>
      </div>

      <nav className="space-y-2">
        {links.map((link) => (
          <Link
            key={link.href}
            href={link.href}
            className={cn(
              'flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors',
              pathname === link.href
                ? 'bg-blue-600 text-white'
                : 'text-gray-300 hover:bg-gray-800'
            )}
          >
            <span className="text-xl">{link.icon}</span>
            <span>{link.label}</span>
          </Link>
        ))}
      </nav>

      <div className="mt-auto pt-6 border-t border-gray-700">
        <button className="w-full flex items-center space-x-3 px-4 py-3 text-gray-300 hover:bg-gray-800 rounded-lg transition-colors">
          <span className="text-xl">⚙️</span>
          <span>Settings</span>
        </button>
        <button className="w-full flex items-center space-x-3 px-4 py-3 text-gray-300 hover:bg-gray-800 rounded-lg transition-colors mt-2">
          <span className="text-xl">🚪</span>
          <span>Logout</span>
        </button>
      </div>
    </div>
  );
}
