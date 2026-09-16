import React, { useEffect, useState } from 'react';
import { 
  AlertOctagon, 
  ShieldAlert, 
  CheckCircle2, 
  XCircle, 
  Clock, 
  FileText, 
  UserCheck, 
  UserX,
  MessageSquare
} from 'lucide-react';
import { getSecurityIncidents, updateIncidentStatus, markFalsePositive } from '../services/api';

export const IncidentsPage: React.FC = () => {
  const [incidents, setIncidents] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  // Modal State
  const [activeModalIncident, setActiveModalIncident] = useState<any>(null);
  const [isFalsePositive, setIsFalsePositive] = useState(true);
  const [testerName, setTesterName] = useState('Mukilan M (Security Analyst)');
  const [reason, setReason] = useState('');

  const loadIncidents = async () => {
    try {
      const data = await getSecurityIncidents();
      setIncidents(data);
      setLoading(false);
    } catch (err) {
      console.error(err);
      setLoading(false);
    }
  };

  useEffect(() => {
    loadIncidents();
  }, []);

  const handleStatusChange = async (code: string, newStatus: string) => {
    await updateIncidentStatus(code, newStatus, 'Status updated by analyst UI', 'Analyst');
    loadIncidents();
  };

  const handleFalsePositiveSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!activeModalIncident) return;

    await markFalsePositive(activeModalIncident.incident_code, isFalsePositive, testerName, reason);
    setActiveModalIncident(null);
    setReason('');
    loadIncidents();
  };

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
      <div className="border-b border-slate-800 pb-5">
        <h1 className="text-xl font-black tracking-tight text-slate-100 uppercase flex items-center gap-2">
          <AlertOctagon className="w-6 h-6 text-red-400" />
          CORRELATED SECURITY INCIDENTS & FALSE POSITIVE MANAGEMENT
        </h1>
        <p className="text-xs text-slate-400 mt-1">Multi-event correlation synthesizes related failed logins, device switches, IP metadata shifts, and rapid transfers into consolidated incidents</p>
      </div>

      {loading ? (
        <div className="p-12 text-center text-slate-400 font-mono">Loading security incidents...</div>
      ) : incidents.length === 0 ? (
        <div className="p-12 text-center text-slate-500 font-mono bg-[#0D131F] rounded-xl border border-slate-800">
          No security incidents recorded. Execute transactions or synthetic scenarios to generate correlated incidents.
        </div>
      ) : (
        <div className="space-y-6">
          {incidents.map((inc) => (
            <div key={inc.incident_code} className="bg-[#0D131F] p-6 rounded-xl border border-slate-800 shadow-xl space-y-4">
              {/* Top Header */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-4">
                <div>
                  <div className="flex items-center gap-3">
                    <span className="font-mono text-sm font-black text-cyan-400">{inc.incident_code}</span>
                    <span className={`px-2.5 py-0.5 text-xs font-black rounded border ${getSeverityBadge(inc.severity)}`}>
                      {inc.severity} ({inc.risk_score}/100)
                    </span>
                    <span className="px-2.5 py-0.5 text-xs font-bold rounded bg-slate-800 text-slate-300 border border-slate-700">
                      STATUS: {inc.status}
                    </span>
                  </div>
                  <h2 className="text-base font-extrabold text-slate-100 mt-2">{inc.title}</h2>
                </div>

                {/* Status Switcher Buttons */}
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => {
                      setActiveModalIncident(inc);
                      setIsFalsePositive(false);
                    }}
                    className="px-3 py-1.5 bg-emerald-500/15 hover:bg-emerald-500/25 border border-emerald-500/40 text-emerald-400 font-extrabold text-xs rounded-lg transition-all flex items-center gap-1.5"
                  >
                    <UserCheck className="w-3.5 h-3.5" />
                    Mark True Positive
                  </button>

                  <button
                    onClick={() => {
                      setActiveModalIncident(inc);
                      setIsFalsePositive(true);
                    }}
                    className="px-3 py-1.5 bg-purple-500/15 hover:bg-purple-500/25 border border-purple-500/40 text-purple-400 font-extrabold text-xs rounded-lg transition-all flex items-center gap-1.5"
                  >
                    <UserX className="w-3.5 h-3.5" />
                    Mark False Positive
                  </button>
                </div>
              </div>

              {/* Correlated Events Timeline */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-2 font-mono text-xs">
                  <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400">Correlated Event Sequence:</h3>
                  <div className="p-3 bg-slate-900 rounded-lg border border-slate-800 space-y-1.5">
                    {inc.events_json?.map((evt: string, idx: number) => (
                      <p key={idx} className="text-slate-200">• {evt}</p>
                    ))}
                  </div>
                </div>

                <div className="space-y-2 font-mono text-xs">
                  <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400">Recommended Action:</h3>
                  <div className="p-3 bg-cyan-500/10 border border-cyan-500/30 rounded-lg text-cyan-300">
                    {inc.recommended_action || 'Enforce MFA and freeze outbound transfer API.'}
                  </div>
                </div>
              </div>

              {/* Resolution Notes if present */}
              {inc.resolution_notes && (
                <div className="p-3 bg-slate-900/90 rounded-lg border border-slate-800 text-xs font-mono text-slate-300">
                  <span className="text-slate-400 font-bold">Analyst Feedback ({inc.marked_by}):</span> {inc.resolution_notes}
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Modal for True/False Positive Feedback */}
      {activeModalIncident && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-[#0D131F] border border-slate-800 rounded-xl w-full max-w-md p-6 space-y-4 shadow-2xl">
            <h3 className="text-sm font-black uppercase tracking-wider text-slate-100 flex items-center gap-2">
              <MessageSquare className="w-4 h-4 text-cyan-400" />
              {isFalsePositive ? 'Mark Incident as False Positive' : 'Confirm True Positive Incident'}
            </h3>
            <p className="text-xs text-slate-400">Incident Code: <span className="text-cyan-400 font-mono">{activeModalIncident.incident_code}</span></p>

            <form onSubmit={handleFalsePositiveSubmit} className="space-y-4 text-xs font-mono">
              <div>
                <label className="block text-slate-400 font-bold mb-1">Security Tester Name</label>
                <input
                  type="text"
                  value={testerName}
                  onChange={(e) => setTesterName(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-slate-100 focus:outline-none focus:border-cyan-500"
                  required
                />
              </div>

              <div>
                <label className="block text-slate-400 font-bold mb-1">Feedback Reason & Rule Tuning Notes</label>
                <textarea
                  rows={3}
                  value={reason}
                  onChange={(e) => setReason(e.target.value)}
                  placeholder="e.g. Legitimate user traveling with new IP; adjust location threshold."
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-slate-100 focus:outline-none focus:border-cyan-500"
                  required
                />
              </div>

              <div className="flex gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setActiveModalIncident(null)}
                  className="w-1/2 py-2 bg-slate-800 text-slate-300 font-bold rounded-lg hover:bg-slate-700"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="w-1/2 py-2 bg-cyan-500 text-slate-950 font-black rounded-lg hover:bg-cyan-400"
                >
                  Submit Feedback
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
