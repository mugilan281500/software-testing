import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { Flag, ShieldAlert, CheckCircle, MessageSquare } from 'lucide-react';
import { RiskBadge } from '../components/RiskBadge';

export const FlagsPage: React.FC = () => {
  const [flags, setFlags] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchFlags = async () => {
    try {
      const res = await api.get('/flags');
      setFlags(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFlags();
  }, []);

  const handleUpdateStatus = async (id: number, newStatus: string) => {
    try {
      await api.put(`/flags/${id}`, { status: newStatus });
      fetchFlags();
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) return <div className="p-8 text-center text-slate-400">Loading Threat Flags...</div>;

  return (
    <div className="p-6 space-y-6 max-w-7xl mx-auto">
      {/* Title */}
      <div className="flex items-center justify-between border-b border-dark-border pb-4">
        <div>
          <h1 className="text-xl font-extrabold text-white tracking-tight flex items-center gap-2">
            <Flag className="w-5 h-5 text-orange-400" />
            AUTOMATED THREAT FLAGS & INCIDENTS
          </h1>
          <p className="text-xs text-slate-400 mt-1">Real-time automatically generated security flags demanding analyst triage and remediation tracking.</p>
        </div>
      </div>

      {/* Grid of Threat Flags */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {flags.map((item) => (
          <div key={item.id} className="bg-dark-card border border-dark-border rounded-xl p-5 space-y-4 shadow-lg flex flex-col justify-between">
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="font-mono text-xs font-bold text-brand-cyan">{item.flag_code}</span>
                <RiskBadge level={item.severity} showScore score={item.risk_score} />
              </div>

              <div>
                <h2 className="text-sm font-extrabold text-white leading-snug">{item.title}</h2>
                <div className="font-mono text-[11px] text-slate-400 mt-1">Target: {item.api_endpoint}</div>
              </div>

              <p className="text-xs text-slate-300 leading-relaxed bg-[#0B0F17] p-3 rounded-lg border border-dark-border">
                {item.evidence_summary}
              </p>
            </div>

            <div className="pt-3 border-t border-dark-border space-y-2">
              <div className="flex items-center justify-between text-xs">
                <span className="text-slate-400 font-bold">Status:</span>
                <select
                  value={item.status}
                  onChange={(e) => handleUpdateStatus(item.id, e.target.value)}
                  className="bg-[#0B0F17] border border-dark-border rounded px-2.5 py-1 text-xs text-white font-bold"
                >
                  <option value="OPEN">🔴 OPEN</option>
                  <option value="INVESTIGATING">🟠 INVESTIGATING</option>
                  <option value="RESOLVED">🟢 RESOLVED</option>
                  <option value="ACCEPTED_RISK">🟡 ACCEPTED RISK</option>
                </select>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
