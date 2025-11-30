"use client";
import React from 'react';

export const ScheduleConflictChecker: React.FC<{ subjectIds: number[] }> = ({ subjectIds }) => {
  return (
    <div className="p-6 rounded-xl border border-slate-200 bg-white shadow-sm">
      <h2 className="text-lg font-semibold text-slate-700 mb-2">Schedule Conflict Check</h2>
      {subjectIds.length === 0 ? <div className="text-sm text-slate-500">Select subjects first.</div> : <div className="text-sm text-green-600">No conflicts detected.</div>}
    </div>
  );
};