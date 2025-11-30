"use client";
import React from 'react';
import { Button } from '../ui/button';

export const EnrollmentSummary: React.FC<{ subjectIds: number[]; onConfirm?: () => void }> = ({ subjectIds, onConfirm }) => (
  <div className="p-6 rounded-xl border border-slate-200 bg-white shadow-sm space-y-4">
    <h2 className="text-lg font-semibold text-slate-700">Enrollment Summary</h2>
    <div className="text-sm text-slate-600">Subjects Selected: {subjectIds.length}</div>
    <Button onClick={onConfirm} disabled={subjectIds.length === 0} className="w-full">Confirm Enrollment</Button>
  </div>
);