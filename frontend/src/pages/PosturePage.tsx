import React, { useEffect, useState } from 'react';
import { Award, ShieldCheck, TrendingDown, TrendingUp, CheckCircle2, ArrowRight } from 'lucide-react';
import { getSecurityPosture, getBeforeAfterComparison } from '../services/api';

export const PosturePage: React.FC = () => {
  const [posture, setPosture] = useState<any>(null);
  const [comparison, setComparison] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([getSecurityPosture(), getBeforeAfterComparison()])
      .then(([p, c]) => {
        setPosture(p);
        setComparison(c);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="p-6 space-y-6 bg-[#0B0F17] text-slate-100 min-h-screen">
      {/* Header */}
      <div className="border-b border-slate-800 pb-5">
        <h1 className="text-xl font-black tracking-tight text-slate-100 uppercase flex items-center gap-2">
          <Award className="w-6 h-6 text-cyan-400" />
          OVERALL SECURITY POSTURE & BEFORE/AFTER COMPARISON
        </h1>
        <p className="text-xs text-slate-400 mt-1">Calculated project security posture score and visual security improvement delta metrics</p>
      </div>

      {loading ? (
        <div className="p-12 text-center text-slate-400 font-mono">Calculating security posture score...</div>
      ) : (
        <div className="space-y-6">
          {/* Posture Score Banner */}
          <div className="bg-gradient-to-r from-[#0D131F] via-[#111827] to-[#0F172A] p-6 rounded-2xl border border-slate-800 shadow-2xl flex flex-col md:flex-row items-center justify-between gap-6">
            <div className="space-y-2">
              <span className="text-xs text-cyan-400 font-bold uppercase tracking-wider">PROJECT SECURITY POSTURE SCORE</span>
              <div className="flex items-baseline gap-3">
                <span className="text-5xl font-black text-slate-100">{posture?.overall_posture_score}</span>
                <span className="text-sm text-slate-400 font-mono">/ 100</span>
                <span className="px-3 py-1 bg-emerald-500/20 text-emerald-400 border border-emerald-500/50 rounded-lg text-xs font-black tracking-wider uppercase">
                  {posture?.status_label}
                </span>
              </div>
              <p className="text-xs text-slate-400">Combines API Security + Functional Reliability + Transaction Security + Business Compliance</p>
            </div>

            {/* Scorecard Breakdown */}
            <div className="grid grid-cols-2 gap-3 font-mono text-xs w-full md:w-auto">
              <div className="p-3 bg-slate-900 rounded-xl border border-slate-800">
                <span className="text-slate-400 block text-[10px]">API Security</span>
                <span className="text-emerald-400 font-bold text-sm">{posture?.breakdown?.api_security}%</span>
              </div>
              <div className="p-3 bg-slate-900 rounded-xl border border-slate-800">
                <span className="text-slate-400 block text-[10px]">Functional Reliability</span>
                <span className="text-cyan-400 font-bold text-sm">{posture?.breakdown?.functional_reliability}%</span>
              </div>
              <div className="p-3 bg-slate-900 rounded-xl border border-slate-800">
                <span className="text-slate-400 block text-[10px]">Transaction Security</span>
                <span className="text-emerald-400 font-bold text-sm">{posture?.breakdown?.transaction_security}%</span>
              </div>
              <div className="p-3 bg-slate-900 rounded-xl border border-slate-800">
                <span className="text-slate-400 block text-[10px]">Business Compliance</span>
                <span className="text-cyan-400 font-bold text-sm">{posture?.breakdown?.business_rule_compliance}%</span>
              </div>
            </div>
          </div>

          {/* Before vs After Security Comparison */}
          <div className="bg-[#0D131F] p-6 rounded-xl border border-slate-800 shadow-xl space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h2 className="text-sm font-black uppercase tracking-wider text-slate-200 flex items-center gap-2">
                <ShieldCheck className="w-4 h-4 text-cyan-400" />
                Before vs After Security Fix Comparison
              </h2>
              <span className="text-xs font-mono text-emerald-400 font-bold">{comparison?.delta}</span>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs font-mono">
                <thead className="bg-[#0F172A] text-slate-400 border-b border-slate-800 uppercase">
                  <tr>
                    <th className="p-3">Vulnerability Category</th>
                    <th className="p-3">Before Patch (Risk)</th>
                    <th className="p-3">After Patch (Risk)</th>
                    <th className="p-3">Security Delta</th>
                    <th className="p-3">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800">
                  {comparison?.metrics?.map((m: any, idx: number) => (
                    <tr key={idx} className="hover:bg-slate-800/40">
                      <td className="p-3 font-bold text-slate-100">{m.category}</td>
                      <td className="p-3 font-bold text-red-400">{m.before}</td>
                      <td className="p-3 font-bold text-emerald-400">{m.after}</td>
                      <td className="p-3 font-bold text-cyan-400">{m.improvement}</td>
                      <td className="p-3">
                        <span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/50 text-[10px] font-bold">
                          {m.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
