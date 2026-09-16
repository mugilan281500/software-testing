import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { History, ShieldCheck, User } from 'lucide-react';

export const AuditLogsPage: React.FC = () => {
  const [logs, setLogs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('/reports/audit-logs')
      .then(res => setLogs(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="p-8 text-center text-slate-400">Loading Structured Audit Trail...</div>;

  return (
    <div className="p-6 space-y-6 max-w-7xl mx-auto">
      {/* Title */}
      <div className="flex items-center justify-between border-b border-dark-border pb-4">
        <div>
          <h1 className="text-xl font-extrabold text-white tracking-tight flex items-center gap-2">
            <History className="w-5 h-5 text-brand-cyan" />
            STRUCTURED SECURITY AUDIT LOGS
          </h1>
          <p className="text-xs text-slate-400 mt-1">Immutable audit records tracking user actions, risk score calculations, and system test executions.</p>
        </div>
      </div>

      {/* Audit Log Table */}
      <div className="bg-dark-card border border-dark-border rounded-xl overflow-hidden shadow-lg">
        <table className="w-full text-left text-xs font-mono">
          <thead className="bg-[#0B0F17] border-b border-dark-border text-slate-400 uppercase text-[10px] tracking-wider">
            <tr>
              <th className="px-4 py-3">Timestamp</th>
              <th className="px-4 py-3">User Email</th>
              <th className="px-4 py-3">Action Executed</th>
              <th className="px-4 py-3">Resource Target</th>
              <th className="px-4 py-3">Risk Impact</th>
              <th className="px-4 py-3">IP Address</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-dark-border">
            {logs.map((item) => (
              <tr key={item.id} className="hover:bg-dark-hover/50 transition-colors">
                <td className="px-4 py-3 text-slate-400">{new Date(item.timestamp).toLocaleString()}</td>
                <td className="px-4 py-3 text-slate-200 font-bold">{item.user_email}</td>
                <td className="px-4 py-3 text-brand-cyan font-bold">{item.action}</td>
                <td className="px-4 py-3 text-slate-300">{item.resource}</td>
                <td className="px-4 py-3 text-red-400 font-bold">{item.risk_score} / 100</td>
                <td className="px-4 py-3 text-slate-500">{item.ip_address}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
