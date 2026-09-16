import React from 'react';

interface ScoreGaugeProps {
  score: number;
  label?: string;
}

export const ScoreGauge: React.FC<ScoreGaugeProps> = ({ score, label = "Security Score" }) => {
  let color = "#10B981"; // Emerald
  let textLevel = "EXCELLENT";
  
  if (score < 50) {
    color = "#EF4444"; // Red
    textLevel = "CRITICAL RISK";
  } else if (score < 75) {
    color = "#F97316"; // Orange
    textLevel = "NEEDS ATTENTION";
  } else if (score < 90) {
    color = "#F59E0B"; // Amber
    textLevel = "GOOD";
  }

  const radius = 42;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  return (
    <div className="flex flex-col items-center justify-center p-4 bg-dark-card border border-dark-border rounded-xl shadow-lg">
      <div className="relative w-36 h-36 flex items-center justify-center">
        <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
          <circle
            cx="50"
            cy="50"
            r={radius}
            className="text-slate-800"
            strokeWidth="10"
            stroke="currentColor"
            fill="transparent"
          />
          <circle
            cx="50"
            cy="50"
            r={radius}
            stroke={color}
            strokeWidth="10"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            fill="transparent"
            className="transition-all duration-1000 ease-out"
          />
        </svg>
        <div className="absolute flex flex-col items-center justify-center text-center">
          <span className="text-3xl font-black text-white tracking-tight">{Math.round(score)}</span>
          <span className="text-[10px] font-bold uppercase tracking-widest text-slate-400">/ 100</span>
        </div>
      </div>
      <div className="mt-2 text-center">
        <div className="text-xs font-semibold uppercase tracking-wider text-slate-400">{label}</div>
        <div className="text-sm font-extrabold mt-0.5" style={{ color }}>{textLevel}</div>
      </div>
    </div>
  );
};
