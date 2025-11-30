"use client";
import React, { useMemo } from 'react';

export const FeeAssessment: React.FC<{ subjectIds: number[] }> = ({ subjectIds }) => {
  const assessment = useMemo(() => {
    const units = subjectIds.length * 3;
    const tuition = units * 500;
    const misc = tuition * 0.1;
    const total = tuition + misc;
    return { units, tuition, misc, total };
  }, [subjectIds]);
  return (
    <div className="p-6 rounded-xl border border-slate-200 bg-white shadow-sm space-y-3">
      <h2 className="text-lg font-semibold text-slate-700">Fee Assessment</h2>
      <div className="text-sm text-slate-600">Units: {assessment.units}</div>
      <div className="text-sm text-slate-600">Tuition: ₱{assessment.tuition.toLocaleString()}</div>
      <div className="text-sm text-slate-600">Misc: ₱{assessment.misc.toLocaleString()}</div>
      <div className="font-medium text-slate-800">Total: ₱{assessment.total.toLocaleString()}</div>
    </div>
  );
};