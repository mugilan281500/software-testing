import React, { useEffect, useState } from 'react';
import { Bell, ShieldAlert, AlertTriangle, CheckCircle2, Clock, Filter } from 'lucide-react';
import { getSecurityAlerts } from '../services/api';

export const AlertsPage: React.FC = () => {
  const [alerts, setAlerts] = useState<any[]>([]);
  const [filterSeverity, setFilterSeverity] = useState('ALL');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getSecurityAlerts()
      .then((data) => {
        setAlerts(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  const filteredAlerts = alerts.filter(
    (a) => filterSeverity === 'ALL' || a.severity === filterSeverity
  );

  const getSeverityBadge = (sev: string) => {
    switch (sev) {
      case 'CRITICAL': return 'bg-red-500/20 text-red-400 border-red-500/50';
      case 'HIGH': return 'bg-orange-500/20 text-orange-400 border-orange-500/50';
      default: return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/50';
    }
  };

  return (
    <div className="p-6 space-y-6 bg-[#0B0F17] text-slate-100 min-h-screen">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-5">
        <div>
          <h1 className="text-xl font-black tracking-tight text-slate-100 uppercase flex items-center gap-2">
            <Bell className="w-6 h-6 text-yellow-400" />
            SECURITY ALERT CENTER
          </h1>
          <p className="text-xs text-slate-400 mt-1">Automated security alerts generated for suspicious transactions, authorization failures, and risk escalation</p>
        </div>

        {/* Filter */}
        <div className="flex items-center gap-2 bg-[#0D131F] p-1.5 rounded-xl border border-slate-800 text-xs font-mono">
          <Filter className="w-4 h-4 text-slate-400 ml-2" />
          <select
            value={filterSeverity}
            onChange={(e) => setFilterSeverity(e.target.value)}
            className="bg-transparent text-slate-200 font-bold focus:outline-none pr-2 cursor-pointer"
          >
            <option value="ALL" className="bg-slate-900">All Severities</option>
            <option value="CRITICAL" className="bg-slate-900">CRITICAL Only</option>
            <option value="HIGH" className="bg-slate-900">HIGH Only</option>
            <option value="MEDIUM" className="bg-slate-900">MEDIUM Only</option>
          </select>
        </div>
      </div>

      {loading ? (
        <div className="p-12 text-center text-slate-400 font-mono">Loading active security alerts...</div>
      ) : filteredAlerts.length === 0 ? (
        <div className="p-12 text-center text-slate-500 font-mono bg-[#0D131F] rounded-xl border border-slate-800">
          No security alerts matching current criteria.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {filteredAlerts.map((alt) => (
            <div key={alt.id} className="bg-[#0D131F] p-5 rounded-xl border border-slate-800 space-y-3 shadow-lg hover:border-slate-700 transition-all">
              <div className="flex items-center justify-between">
                <span className="font-mono text-xs font-bold text-cyan-400">{alt.flag_code || alt.alert_code || `ALT-${alt.id}`}</span>
                <span className={`px-2.5 py-0.5 text-xs font-black rounded border ${getSeverityBadge(alt.severity)}`}>
                  {alt.severity} ({alt.risk_score}/100)
                </span>
              </div>

              <h3 className="text-sm font-extrabold text-slate-100">{alt.title}</h3>
              <p className="text-xs text-slate-400 font-mono leading-relaxed">{alt.message || alt.evidence_summary}</p>

              <div className="pt-2 border-t border-slate-800/80 flex items-center justify-between text-[11px] font-mono text-slate-400">
                <span>Endpoint: <strong className="text-slate-200">{alt.api_endpoint || alt.endpoint}</strong></span>
                <span className="text-emerald-400 font-bold">STATUS: {alt.status}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
