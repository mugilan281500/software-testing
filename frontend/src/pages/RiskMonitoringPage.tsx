import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { TrendingUp, AlertTriangle, Activity, ShieldAlert } from 'lucide-react';
import { RiskBadge } from '../components/RiskBadge';

export const RiskMonitoringPage: React.FC = () => {
  const [anomalies, setAnomalies] = useState<any[]>([]);

  useEffect(() => {
    // Fetch live anomalies
    api.get('/dashboard/summary').then(res => setAnomalies(res.data.recent_alerts));
  }, []);

  return (
    <div className="p-6 space-y-6 max-w-7xl mx-auto">
      {/* Title */}
      <div className="flex items-center justify-between border-b border-dark-border pb-4">
        <div>
          <h1 className="text-xl font-extrabold text-white tracking-tight flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-brand-cyan" />
            RISK MONITORING & ANOMALY DETECTION ENGINE
          </h1>
          <p className="text-xs text-slate-400 mt-1">Continuous behavioral baseline profiling, velocity spike analysis, and anomalous transaction pattern flagging.</p>
        </div>
      </div>

      {/* Monitoring Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {anomalies.map((item) => (
          <div key={item.id} className="bg-dark-card border border-dark-border rounded-xl p-5 space-y-4 shadow-lg">
            <div className="flex items-center justify-between">
              <span className="font-mono text-xs font-bold text-brand-cyan">{item.id}</span>
              <RiskBadge level={item.severity} />
            </div>

            <div>
              <h2 className="text-sm font-extrabold text-white">{item.title}</h2>
              <div className="font-mono text-xs text-slate-400 mt-0.5">Endpoint: {item.endpoint}</div>
            </div>

            <p className="text-xs text-slate-300 leading-relaxed bg-[#0B0F17] p-3 rounded-lg border border-dark-border">
              {item.message}
            </p>

            <div className="grid grid-cols-2 gap-2 pt-2 border-t border-dark-border text-xs font-mono">
              <div className="bg-red-500/10 border border-red-500/20 p-2 rounded text-red-300">
                <div className="text-[10px] text-slate-400 uppercase">Observed Velocity</div>
                <div className="font-bold mt-0.5">{item.observed}</div>
              </div>
              <div className="bg-slate-800 p-2 rounded text-slate-300">
                <div className="text-[10px] text-slate-400 uppercase">Configured Baseline</div>
                <div className="font-bold mt-0.5">{item.baseline}</div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
