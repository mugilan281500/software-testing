import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { Activity } from 'lucide-react';
import { RiskBadge } from '../components/RiskBadge';

export const TestCasesPage: React.FC = () => {
  const [cases, setCases] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('/tests/cases')
      .then(res => setCases(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="p-8 text-center text-slate-400">Loading Modular Security Test Cases...</div>;

  return (
    <div className="p-6 space-y-6 max-w-7xl mx-auto">
      <div className="flex items-center justify-between border-b border-dark-border pb-4">
        <div>
          <h1 className="text-xl font-extrabold text-white tracking-tight flex items-center gap-2">
            <Activity className="w-5 h-5 text-brand-cyan" />
            MODULAR SECURITY TEST CASE REPOSITORY
          </h1>
          <p className="text-xs text-slate-400 mt-1">Pre-packaged banking security test vectors covering Auth, IDOR, Payload, Logic, and Header controls.</p>
        </div>
      </div>

      <div className="bg-dark-card border border-dark-border rounded-xl overflow-hidden shadow-lg">
        <table className="w-full text-left text-xs">
          <thead className="bg-[#0B0F17] border-b border-dark-border text-slate-400 uppercase font-mono text-[10px] tracking-wider">
            <tr>
              <th className="px-4 py-3">Test ID</th>
              <th className="px-4 py-3">Test Assertion Name</th>
              <th className="px-4 py-3">Category</th>
              <th className="px-4 py-3">Target Endpoint</th>
              <th className="px-4 py-3">Expected Status</th>
              <th className="px-4 py-3">Severity</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-dark-border">
            {cases.map((item) => (
              <tr key={item.id} className="hover:bg-dark-hover/50 transition-colors">
                <td className="px-4 py-3 font-mono font-bold text-brand-cyan">{item.test_id}</td>
                <td className="px-4 py-3 font-bold text-slate-200">{item.name}</td>
                <td className="px-4 py-3 font-semibold text-slate-300">{item.category}</td>
                <td className="px-4 py-3 font-mono text-slate-400">{item.endpoint}</td>
                <td className="px-4 py-3 font-mono font-bold text-emerald-400">HTTP {item.expected_status}</td>
                <td className="px-4 py-3">
                  <RiskBadge level={item.severity} size="sm" />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
