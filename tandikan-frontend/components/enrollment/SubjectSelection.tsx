"use client";
import React, { useState } from 'react';
import { Button } from '../ui/button';

interface Subject { id: number; code: string; title: string; units: number; }
const sampleSubjects: Subject[] = [
  { id: 1, code: 'MATH101', title: 'Calculus I', units: 3 },
  { id: 2, code: 'COMP110', title: 'Intro to Programming', units: 3 },
  { id: 3, code: 'ENG101', title: 'Academic Writing', units: 3 },
];

export const SubjectSelection: React.FC<{ onChange?: (ids: number[]) => void }> = ({ onChange }) => {
  const [selected, setSelected] = useState<number[]>([]);
  const toggle = (id: number) => setSelected(s => { const next = s.includes(id) ? s.filter(x => x !== id) : [...s, id]; onChange?.(next); return next; });
  return (
    <div className="space-y-4 p-6 rounded-xl border border-slate-200 bg-white shadow-sm">
      <h2 className="text-lg font-semibold text-slate-700">Subject Selection</h2>
      <div className="space-y-2">
        {sampleSubjects.map(sub => (
          <button key={sub.id} onClick={() => toggle(sub.id)} className={`w-full text-left rounded-lg border px-4 py-3 transition ${selected.includes(sub.id) ? 'bg-slate-800 text-white border-slate-800' : 'bg-white hover:bg-slate-50'}`}>
            <div className="font-medium">{sub.code} — {sub.title}</div>
            <div className="text-xs text-slate-500">{sub.units} units</div>
          </button>
        ))}
      </div>
      <Button variant="outline" disabled={selected.length === 0}>Proceed</Button>
    </div>
  );
};