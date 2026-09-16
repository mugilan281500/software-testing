import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  ShieldAlert,
  Activity, 
  CreditCard, 
  FlaskConical, 
  AlertOctagon, 
  Bell, 
  Unplug, 
  Play, 
  Sliders, 
  Award, 
  FileText, 
  History 
} from 'lucide-react';

export const Sidebar: React.FC = () => {
  const navItems = [
    { to: '/', label: 'Live Security Monitor', icon: Activity, badge: 'LIVE' },
    { to: '/banking', label: 'Customer Banking Portal', icon: CreditCard, badge: 'MANUAL' },
    { to: '/simulation', label: 'Transaction Security Lab', icon: FlaskConical, badge: 'LAB' },
    { to: '/incidents', label: 'Suspicious Incidents', icon: AlertOctagon, badge: 'CORRELATED' },
    { to: '/alerts', label: 'Security Alert Center', icon: Bell },
    { to: '/apis', label: 'API Inventory & Heatmap', icon: Unplug },
    { to: '/tests', label: 'Test Orchestrator', icon: Play },
    { to: '/rules', label: 'Admin Rule Config', icon: Sliders },
    { to: '/posture', label: 'Posture & Comparison', icon: Award },
    { to: '/reports', label: 'Reports & Audit Logs', icon: FileText },
  ];

  return (
    <aside className="w-64 bg-[#0B0F17] border-r border-slate-800 min-h-screen flex flex-col justify-between select-none">
      <div>
        {/* Brand Header */}
        <div className="h-16 flex items-center gap-3 px-5 border-b border-slate-800 bg-[#0D131F]">
          <div className="p-2 bg-cyan-500/10 rounded-lg border border-cyan-500/30 text-cyan-400 shadow-sm shadow-cyan-500/20">
            <ShieldAlert className="w-6 h-6" />
          </div>
          <div>
            <h1 className="font-extrabold text-slate-100 tracking-tight text-sm leading-tight">BANK<span className="text-cyan-400">SECURE</span></h1>
            <p className="text-[10px] font-bold tracking-wider text-slate-400 uppercase">API GUARD PLATFORM v2</p>
          </div>
        </div>

        {/* Navigation Menu */}
        <nav className="p-3 space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  `flex items-center justify-between px-3 py-2.5 rounded-lg text-xs font-semibold transition-all duration-150 ${
                    isActive
                      ? 'bg-cyan-500/15 text-cyan-400 border border-cyan-500/30 shadow-sm shadow-cyan-500/10'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                  }`
                }
              >
                <div className="flex items-center gap-2.5">
                  <Icon className="w-4 h-4" />
                  <span>{item.label}</span>
                </div>
                {item.badge && (
                  <span className="px-1.5 py-0.5 text-[9px] font-extrabold rounded bg-slate-800 text-cyan-400 border border-cyan-500/30">
                    {item.badge}
                  </span>
                )}
              </NavLink>
            );
          })}
        </nav>
      </div>

      {/* Footer Status */}
      <div className="p-4 border-t border-slate-800 bg-[#0D131F]/60">
        <div className="flex items-center justify-between text-[11px] text-slate-400 font-mono">
          <span>MONITORING ENGINE</span>
          <span className="inline-flex items-center gap-1.5 text-emerald-400 font-bold">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping" />
            ACTIVE
          </span>
        </div>
      </div>
    </aside>
  );
};
