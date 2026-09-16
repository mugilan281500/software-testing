import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { RiskBadge } from '../components/RiskBadge';
import { AlertTriangle, ShieldAlert, CheckCircle2, MessageSquare, Filter } from 'lucide-react';

export const FindingsPage: React.FC = () => {
  const [findings, setFindings] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedFinding, setSelectedFinding] = useState<any>(null);

  const fetchFindings = async () => {
    try {
      const res = await api.get('/findings');
      setFindings(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFindings();
  }, []);

  const handleStatusUpdate = async (id: number, newStatus: string) => {
    try {
      await api.put(`/findings/${id}`, { status: newStatus });
      fetchFindings();
      if (selectedFinding && selectedFinding.id === id) {
        setSelectedFinding({ ...selectedFinding, status: newStatus });
      }
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) return <div className="p-8 text-center text-slate-400">Loading Vulnerability Findings...</div>;

  return (
    <div className="p-6 space-y-6 max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-dark-border pb-4">
        <div>
          <h1 className="text-xl font-extrabold text-white tracking-tight flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-red-500" />
            SECURITY VULNERABILITY FINDINGS
          </h1>
          <p className="text-xs text-slate-400 mt-1">Detailed repository of identified banking API flaws, CVSS vector scores, evidence, and remediation advice.</p>
        </div>
      </div>

      {/* Grid: Findings List + Detail View */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Table / List Column */}
        <div className="lg:col-span-2 bg-dark-card border border-dark-border rounded-xl overflow-hidden shadow-lg">
          <table className="w-full text-left text-xs">
            <thead className="bg-[#0B0F17] border-b border-dark-border text-slate-400 uppercase font-mono text-[10px] tracking-wider">
              <tr>
                <th className="px-4 py-3">Finding Code</th>
                <th className="px-4 py-3">Vulnerability Title</th>
                <th className="px-4 py-3">Category</th>
                <th className="px-4 py-3">Severity</th>
                <th className="px-4 py-3">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-dark-border">
              {findings.map((item) => (
                <tr
                  key={item.id}
                  onClick={() => setSelectedFinding(item)}
                  className={`cursor-pointer transition-colors ${
                    selectedFinding?.id === item.id ? 'bg-brand-cyan/10 border-l-4 border-l-brand-cyan' : 'hover:bg-dark-hover/50'
                  }`}
                >
                  <td className="px-4 py-3 font-mono font-bold text-brand-cyan">{item.finding_code}</td>
                  <td className="px-4 py-3 font-bold text-slate-200">{item.title}</td>
                  <td className="px-4 py-3 text-slate-400">{item.category}</td>
                  <td className="px-4 py-3">
                    <RiskBadge level={item.severity} size="sm" />
                  </td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-0.5 text-[10px] font-bold rounded ${
                      item.status === 'OPEN' ? 'bg-red-500/10 text-red-400 border border-red-500/30' :
                      item.status === 'RESOLVED' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30' :
                      'bg-amber-500/10 text-amber-400 border border-amber-500/30'
                    }`}>
                      {item.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Selected Finding Detail Column */}
        <div className="lg:col-span-1 bg-dark-card border border-dark-border rounded-xl p-5 space-y-4 shadow-lg">
          {selectedFinding ? (
            <div className="space-y-4">
              <div className="flex items-center justify-between border-b border-dark-border pb-3">
                <span className="font-mono text-xs font-bold text-brand-cyan">{selectedFinding.finding_code}</span>
                <RiskBadge level={selectedFinding.severity} showScore score={selectedFinding.risk_score} />
              </div>

              <div>
                <h2 className="text-sm font-extrabold text-white">{selectedFinding.title}</h2>
                <div className="font-mono text-xs text-slate-400 mt-1">Endpoint: {selectedFinding.api_endpoint}</div>
              </div>

              <div className="space-y-1.5 pt-2 border-t border-dark-border">
                <div className="text-[11px] font-bold uppercase text-slate-400">CVSS v3.1 Score</div>
                <div className="text-lg font-black text-red-400 font-mono">{selectedFinding.cvss_score} / 10.0</div>
              </div>

              {/* Status Selector */}
              <div className="space-y-1.5">
                <label className="text-[11px] font-bold uppercase text-slate-400 block">Workflow Status</label>
                <select
                  value={selectedFinding.status}
                  onChange={(e) => handleStatusUpdate(selectedFinding.id, e.target.value)}
                  className="w-full bg-[#0B0F17] border border-dark-border rounded-lg px-3 py-1.5 text-xs text-white font-bold"
                >
                  <option value="OPEN">🔴 OPEN</option>
                  <option value="INVESTIGATING">🟠 INVESTIGATING</option>
                  <option value="RESOLVED">🟢 RESOLVED</option>
                  <option value="FALSE_POSITIVE">⚪ FALSE POSITIVE</option>
                  <option value="ACCEPTED_RISK">🟡 ACCEPTED RISK</option>
                </select>
              </div>

              {/* Remediation Advice */}
              <div className="space-y-1.5 p-3 bg-[#0B0F17] rounded-lg border border-dark-border">
                <div className="text-[11px] font-bold text-brand-cyan uppercase tracking-wider flex items-center gap-1">
                  <ShieldAlert className="w-3.5 h-3.5" /> Remediation Guidance
                </div>
                <p className="text-xs text-slate-300 leading-relaxed">{selectedFinding.recommendation}</p>
              </div>

              {/* Evidence JSON view */}
              <div className="space-y-1.5">
                <div className="text-[11px] font-bold uppercase text-slate-400">Evidence Log</div>
                <pre className="p-3 bg-[#080B11] border border-slate-900 rounded-lg text-[10px] font-mono text-slate-300 overflow-x-auto">
                  {JSON.stringify(selectedFinding.evidence, null, 2)}
                </pre>
              </div>
            </div>
          ) : (
            <div className="text-center py-16 text-slate-500 text-xs">
              Select a vulnerability finding from the list to inspect CVSS details, evidence payload, and remediation guidance.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
