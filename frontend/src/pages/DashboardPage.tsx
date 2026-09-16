import React, { useEffect, useState } from 'react';
import { 
  Activity, 
  ShieldAlert, 
  AlertTriangle, 
  CheckCircle2, 
  Clock, 
  ArrowUpRight, 
  Eye, 
  RefreshCw,
  Zap,
  TrendingUp,
  Cpu
} from 'lucide-react';
import { getLiveMonitoringFeed, getRiskTimeline } from '../services/api';
import { ExplainableRiskModal } from '../components/ExplainableRiskModal';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

export const DashboardPage: React.FC = () => {
  const [summary, setSummary] = useState({ total: 0, normal: 0, monitored: 0, flagged: 0, critical: 0 });
  const [transactions, setTransactions] = useState<any[]>([]);
  const [timeline, setTimeline] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedTxId, setSelectedTxId] = useState<string | null>(null);

  const fetchFeed = async () => {
    try {
      const feedData = await getLiveMonitoringFeed();
      setSummary(feedData.summary);
      setTransactions(feedData.transactions);

      const timelineData = await getRiskTimeline();
      setTimeline(timelineData);
      setLoading(false);
    } catch (err) {
      console.error(err);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFeed();
    const interval = setInterval(fetchFeed, 4000); // 4 second reliable real-time polling
    return () => clearInterval(interval);
  }, []);

  const getBadgeStyle = (level: string) => {
    switch (level) {
      case 'CRITICAL': return 'bg-red-500/20 text-red-400 border-red-500/50';
      case 'HIGH': return 'bg-orange-500/20 text-orange-400 border-orange-500/50';
      case 'MEDIUM': return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/50';
      default: return 'bg-emerald-500/20 text-emerald-400 border-emerald-500/50';
    }
  };

  return (
    <div className="p-6 space-y-6 bg-[#0B0F17] text-slate-100 min-h-screen">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-5">
        <div>
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-cyan-400 animate-ping" />
            <h1 className="text-xl font-black tracking-tight text-slate-100 uppercase">LIVE TRANSACTION SECURITY MONITOR</h1>
          </div>
          <p className="text-xs text-slate-400 mt-1">Automated Real-Time Transaction Security Engine & Multi-Factor Suspicious Activity Detection</p>
        </div>
        <button
          onClick={fetchFeed}
          className="flex items-center gap-2 px-3 py-2 bg-slate-900 border border-slate-800 rounded-lg text-xs font-bold text-slate-300 hover:text-cyan-400 hover:border-cyan-500/50 transition-all"
        >
          <RefreshCw className="w-4 h-4 animate-spin-slow" />
          Refresh Live Stream
        </button>
      </div>

      {/* Metrics Bar */}
      <div className="grid grid-cols-2 sm:grid-cols-5 gap-4">
        <div className="bg-[#0D131F] p-4 rounded-xl border border-slate-800 shadow-lg">
          <p className="text-[11px] font-extrabold text-slate-400 uppercase tracking-wider">Total Monitored</p>
          <p className="text-3xl font-black text-slate-100 mt-1">{summary.total}</p>
          <p className="text-[10px] text-cyan-400 font-mono mt-1">100% Auto-Monitored</p>
        </div>

        <div className="bg-[#0D131F] p-4 rounded-xl border border-slate-800 shadow-lg">
          <p className="text-[11px] font-extrabold text-slate-400 uppercase tracking-wider">Normal (0-29)</p>
          <p className="text-3xl font-black text-emerald-400 mt-1">{summary.normal}</p>
          <p className="text-[10px] text-emerald-500 font-mono mt-1">Allowed Transactions</p>
        </div>

        <div className="bg-[#0D131F] p-4 rounded-xl border border-slate-800 shadow-lg">
          <p className="text-[11px] font-extrabold text-slate-400 uppercase tracking-wider">Monitored (30-59)</p>
          <p className="text-3xl font-black text-yellow-400 mt-1">{summary.monitored}</p>
          <p className="text-[10px] text-yellow-500 font-mono mt-1">Under Surveillance</p>
        </div>

        <div className="bg-[#0D131F] p-4 rounded-xl border border-slate-800 shadow-lg">
          <p className="text-[11px] font-extrabold text-slate-400 uppercase tracking-wider">Flagged (60-79)</p>
          <p className="text-3xl font-black text-orange-400 mt-1">{summary.flagged}</p>
          <p className="text-[10px] text-orange-500 font-mono mt-1">Security Review</p>
        </div>

        <div className="bg-[#0D131F] p-4 rounded-xl border border-slate-800 shadow-lg">
          <p className="text-[11px] font-extrabold text-slate-400 uppercase tracking-wider">Critical (80-100)</p>
          <p className="text-3xl font-black text-red-400 mt-1">{summary.critical}</p>
          <p className="text-[10px] text-red-500 font-mono mt-1">Blocked & Auto-Tested</p>
        </div>
      </div>

      {/* Transaction Risk Timeline Graph */}
      <div className="bg-[#0D131F] p-5 rounded-xl border border-slate-800 shadow-xl space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="text-xs font-black uppercase tracking-wider text-slate-300 flex items-center gap-2">
            <TrendingUp className="w-4 h-4 text-cyan-400" />
            Transaction Risk Timeline & Escalation Graph
          </h2>
          <span className="text-[11px] text-slate-400 font-mono">Scores over consecutive transactions</span>
        </div>
        <div className="h-44 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={timeline}>
              <XAxis dataKey="tx_id" stroke="#475569" fontSize={10} />
              <YAxis domain={[0, 100]} stroke="#475569" fontSize={10} />
              <Tooltip
                contentStyle={{ backgroundColor: '#0F172A', borderColor: '#334155', borderRadius: '8px', color: '#F8FAFC' }}
              />
              <Line type="monotone" dataKey="risk_score" stroke="#38BDF8" strokeWidth={2.5} dot={{ r: 4, fill: '#38BDF8' }} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Live Transaction Feed Table */}
      <div className="bg-[#0D131F] rounded-xl border border-slate-800 shadow-xl overflow-hidden">
        <div className="px-6 py-4 border-b border-slate-800 flex items-center justify-between bg-[#111827]">
          <h2 className="text-sm font-black uppercase tracking-wider text-slate-200 flex items-center gap-2">
            <Activity className="w-4 h-4 text-cyan-400" />
            Live Transaction Stream & Risk Decisions
          </h2>
          <span className="text-xs text-slate-400 font-mono">{transactions.length} Transactions Recorded</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-[#0F172A] text-slate-400 border-b border-slate-800 uppercase tracking-wider">
              <tr>
                <th className="px-5 py-3">Transaction</th>
                <th className="px-5 py-3">Sender</th>
                <th className="px-5 py-3">Receiver</th>
                <th className="px-5 py-3">Amount</th>
                <th className="px-5 py-3">Risk Score</th>
                <th className="px-5 py-3">Level</th>
                <th className="px-5 py-3">Flags</th>
                <th className="px-5 py-3">Decision</th>
                <th className="px-5 py-3 text-right">Explainable Analysis</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {transactions.map((tx) => (
                <tr key={tx.transaction_id} className="hover:bg-slate-800/40 transition-colors">
                  <td className="px-5 py-3 font-bold text-cyan-400">{tx.transaction_id}</td>
                  <td className="px-5 py-3 text-slate-300">{tx.sender}</td>
                  <td className="px-5 py-3 text-slate-300">{tx.receiver}</td>
                  <td className="px-5 py-3 font-bold text-slate-100">₹{tx.amount?.toLocaleString('en-IN')}</td>
                  <td className="px-5 py-3 font-black text-sm text-slate-100">{tx.risk_score}</td>
                  <td className="px-5 py-3">
                    <span className={`px-2 py-0.5 rounded border text-[10px] font-extrabold ${getBadgeStyle(tx.risk_level)}`}>
                      {tx.risk_level}
                    </span>
                  </td>
                  <td className="px-5 py-3 font-bold text-slate-300">{tx.flags} Flags</td>
                  <td className="px-5 py-3 font-black tracking-wider text-slate-200">{tx.decision}</td>
                  <td className="px-5 py-3 text-right">
                    <button
                      onClick={() => setSelectedTxId(tx.transaction_id)}
                      className="px-2.5 py-1 bg-cyan-500/10 hover:bg-cyan-500/20 border border-cyan-500/30 text-cyan-400 font-bold rounded-lg transition-all flex items-center gap-1 ml-auto"
                    >
                      <Eye className="w-3.5 h-3.5" />
                      Scorecard
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Scorecard Modal */}
      <ExplainableRiskModal
        transactionId={selectedTxId}
        onClose={() => setSelectedTxId(null)}
      />
    </div>
  );
};
