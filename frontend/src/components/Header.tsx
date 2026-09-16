import React from 'react';
import { Bell, Search, UserCheck, ShieldCheck } from 'lucide-react';

interface HeaderProps {
  userRole?: string;
  username?: string;
}

export const Header: React.FC<HeaderProps> = ({ userRole = "ADMIN", username = "Security Analyst" }) => {
  return (
    <header className="h-16 bg-[#0D131F] border-b border-dark-border px-6 flex items-center justify-between sticky top-0 z-30">
      {/* Search Input */}
      <div className="flex items-center gap-3 w-96">
        <div className="relative w-full">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
          <input
            type="text"
            placeholder="Search API endpoints, test IDs, threat flags..."
            className="w-full bg-[#0B0F17] border border-dark-border rounded-lg pl-9 pr-4 py-1.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-brand-cyan/50 transition-colors"
          />
        </div>
      </div>

      {/* Header Actions */}
      <div className="flex items-center gap-4">
        {/* Quick System Badge */}
        <div className="hidden md:flex items-center gap-2 px-3 py-1 bg-emerald-500/10 border border-emerald-500/20 rounded-full text-[11px] font-medium text-emerald-400">
          <ShieldCheck className="w-3.5 h-3.5" />
          <span>Banking Gateway Isolated</span>
        </div>

        {/* Notifications */}
        <button className="relative p-2 rounded-lg bg-dark-card border border-dark-border text-slate-400 hover:text-white transition-colors">
          <Bell className="w-4 h-4" />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-red-500 ring-2 ring-[#0D131F]" />
        </button>

        {/* User Profile */}
        <div className="flex items-center gap-3 pl-2 border-l border-dark-border">
          <div className="w-8 h-8 rounded-lg bg-brand-cyan/20 border border-brand-cyan/40 flex items-center justify-center text-brand-cyan font-bold text-xs">
            {userRole.substring(0, 2)}
          </div>
          <div className="hidden sm:block text-left">
            <div className="text-xs font-bold text-slate-200">{username}</div>
            <div className="text-[10px] font-bold text-brand-cyan uppercase tracking-wider">{userRole}</div>
          </div>
        </div>
      </div>
    </header>
  );
};
