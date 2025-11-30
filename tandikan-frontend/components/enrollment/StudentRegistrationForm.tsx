"use client";
import React, { useState } from 'react';
import { Button } from '../ui/button';
import { Input } from '../ui/input';

interface RegistrationData { firstName: string; lastName: string; email: string; }

export const StudentRegistrationForm: React.FC<{ onRegistered?: (id: string) => void }> = ({ onRegistered }) => {
  const [data, setData] = useState<RegistrationData>({ firstName: '', lastName: '', email: '' });
  const [loading, setLoading] = useState(false);
  const [studentId, setStudentId] = useState<string | null>(null);

  const submit = async () => {
    setLoading(true);
    await new Promise(r => setTimeout(r, 600));
    const generated = `TEMP-${Date.now().toString().slice(-6)}`;
    setStudentId(generated);
    onRegistered?.(generated);
    setLoading(false);
  };

  return (
    <div className="space-y-4 p-6 rounded-xl border border-slate-200 bg-white shadow-sm">
      <h2 className="text-lg font-semibold text-slate-700">Student Registration</h2>
      <div className="grid gap-3 sm:grid-cols-2">
        <Input placeholder="First Name" value={data.firstName} onChange={e => setData({ ...data, firstName: e.target.value })} />
        <Input placeholder="Last Name" value={data.lastName} onChange={e => setData({ ...data, lastName: e.target.value })} />
        <Input className="sm:col-span-2" placeholder="Email" value={data.email} onChange={e => setData({ ...data, email: e.target.value })} />
      </div>
      <Button disabled={loading} onClick={submit} className="w-full">{loading ? 'Registering...' : 'Register'}</Button>
      {studentId && <div className="text-sm text-green-600">Student ID: {studentId}</div>}
    </div>
  );
};