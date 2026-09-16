import React from 'react';

interface RiskBadgeProps {
  level?: string;
  score?: number;
  showScore?: boolean;
  size?: 'sm' | 'md' | 'lg';
}

export const RiskBadge: React.FC<RiskBadgeProps> = ({ level, score, showScore = false, size = 'md' }) => {
  let badgeLevel = level || 'LOW';
  if (score !== undefined) {
    if (score >= 76) badgeLevel = 'CRITICAL';
    else if (score >= 51) badgeLevel = 'HIGH';
    else if (score >= 26) badgeLevel = 'MEDIUM';
    else badgeLevel = 'LOW';
  }

  const colors = {
    CRITICAL: 'bg-red-500/10 text-red-400 border-red-500/30 shadow-red-950/40',
    HIGH: 'bg-orange-500/10 text-orange-400 border-orange-500/30 shadow-orange-950/40',
    MEDIUM: 'bg-amber-500/10 text-amber-400 border-amber-500/30 shadow-amber-950/40',
    LOW: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30 shadow-emerald-950/40',
  };

  const sizes = {
    sm: 'px-2 py-0.5 text-xs font-semibold',
    md: 'px-2.5 py-1 text-xs font-bold',
    lg: 'px-3 py-1.5 text-sm font-extrabold',
  };

  const selectedColor = colors[badgeLevel as keyof typeof colors] || colors.LOW;

  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full border shadow-sm ${selectedColor} ${sizes[size]}`}
    >
      <span className="w-1.5 h-1.5 rounded-full bg-current animate-pulse" />
      {badgeLevel}
      {showScore && score !== undefined && <span className="opacity-75">({score})</span>}
    </span>
  );
};
