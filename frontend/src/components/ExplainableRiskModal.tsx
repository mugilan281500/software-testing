import React, { useEffect, useState } from 'react';
import { X, ShieldAlert, AlertTriangle, CheckCircle2, Info, ChevronRight, Cpu } from 'lucide-react';
import { getTransactionScorecard } from '../services/api';

interface ExplainableRiskModalProps {
  transactionId: string | null;
  onClose: () => void;
}

export const ExplainableRiskModal: React.FC<ExplainableRiskModalProps> = ({ transactionId, onClose }) => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [selectedFactor, setSelectedFactor] = useState<any>(null);

  useEffect(() => {
    if (transactionId) {
      setLoading(true);
      getTransactionScorecard(transactionId)
        .then((res) => {
          setData(res);
          if (res.explainable_risk_factors && res.explainable_risk_factors.length > 0) {
            setSelectedFactor(res.explainable_risk_factors[0]);
          }
          setLoading(false);
        })
        .catch(() => setLoading(false));
    }
  }, [transactionId]);

  if (!transactionId) return null;

  const getRiskBadgeColor = (level: string) => {
    switch (level) {
      case 'CRITICAL': return 'bg-red-500/20 text-red-400 border-red-500/50';
      case 'HIGH': return 'bg-orange-500/20 text-orange-400 border-orange-500/50';
      case 'MEDIUM': return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/50';
      default: return 'bg-emerald-500/20 text-emerald-400 border-emerald-500/50';
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-[#0D131F] border border-slate-800 rounded-xl w-full max-w-4xl max-h-[90vh] overflow-y-auto shadow-2xl">
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-800 flex items-center justify-between bg-[#111827]">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-cyan-500/10 rounded-lg border border-cyan-500/30 text-cyan-400">
              <Cpu className="w-5 h-5" />
            </div>
            <div>
              <h2 className="font-bold text-slate-100 text-lg">TRANSACTION RISK ANALYSIS & SCORECARD</h2>
              <p className="text-xs text-slate-400 font-mono">Transaction Ref: <span className="text-cyan-400">{transactionId}</span></p>
            </div>
          </div>
          <button onClick={onClose} className="p-1 text-slate-400 hover:text-slate-100 hover:bg-slate-800 rounded-lg">
            <X className="w-6 h-6" />
          </button>
        </div>

        {loading ? (
          <div className="p-12 text-center text-slate-400 font-mono flex items-center justify-center gap-3">
            <span className="w-4 h-4 border-2 border-cyan-400 border-t-transparent rounded-full animate-spin" />
            Analyzing real-time security indicators...
          </div>
        ) : !data ? (
          <div className="p-12 text-center text-red-400 font-mono">Failed to load risk analysis data.</div>
        ) : (
          <div className="p-6 space-y-6">
            {/* Top Overview Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="bg-slate-900/80 p-4 rounded-xl border border-slate-800">
                <p className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">Amount</p>
                <p className="text-2xl font-extrabold text-slate-100 mt-1">₹{data.amount?.toLocaleString('en-IN')}</p>
                <p className="text-xs text-slate-400 mt-0.5">{data.currency || 'INR'}</p>
              </div>

              <div className="bg-slate-900/80 p-4 rounded-xl border border-slate-800">
                <p className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">Transaction Risk</p>
                <div className="flex items-baseline gap-2 mt-1">
                  <span className="text-3xl font-black text-cyan-400">{data.risk_score}</span>
                  <span className="text-xs text-slate-400 font-mono">/ 100</span>
                </div>
              </div>

              <div className="bg-slate-900/80 p-4 rounded-xl border border-slate-800">
                <p className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">Risk Level</p>
                <span className={`inline-block mt-2 px-3 py-1 text-xs font-black rounded border ${getRiskBadgeColor(data.risk_level)}`}>
                  {data.risk_level}
                </span>
              </div>

              <div className="bg-slate-900/80 p-4 rounded-xl border border-slate-800">
                <p className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">Engine Decision</p>
                <p className="text-lg font-black text-slate-100 mt-1 tracking-wider uppercase text-cyan-400">{data.decision}</p>
              </div>
            </div>

            {/* Transaction Security Scorecard Grid */}
            <div className="bg-slate-900/60 p-5 rounded-xl border border-slate-800">
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300 mb-4 flex items-center gap-2">
                <ShieldAlert className="w-4 h-4 text-cyan-400" />
                Transaction Security Scorecard Breakdown
              </h3>
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
                {[
                  { label: 'Authentication', score: data.scorecard?.auth_score },
                  { label: 'Authorization', score: data.scorecard?.authz_score },
                  { label: 'Input Validation', score: data.scorecard?.validation_score },
                  { label: 'Business Rules', score: data.scorecard?.business_rules_score },
                  { label: 'Behavior Analysis', score: data.scorecard?.behavior_score },
                  { label: 'API Security', score: data.scorecard?.api_security_score }
                ].map((item) => (
                  <div key={item.label} className="bg-slate-950 p-3 rounded-lg border border-slate-800/80">
                    <div className="flex justify-between items-center text-xs text-slate-400 font-semibold mb-1">
                      <span>{item.label}</span>
                      <span className="text-slate-100 font-bold">{item.score}%</span>
                    </div>
                    <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
                      <div
                        className={`h-2 rounded-full ${item.score >= 80 ? 'bg-emerald-500' : item.score >= 50 ? 'bg-yellow-500' : 'bg-red-500'}`}
                        style={{ width: `${item.score}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Explainable Risk Factors Section */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Factors List */}
              <div className="space-y-3">
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2">
                  <AlertTriangle className="w-4 h-4 text-yellow-400" />
                  Detected Risk Factors & Score Contributions
                </h3>
                {data.explainable_risk_factors?.length === 0 ? (
                  <div className="p-4 bg-slate-900/60 rounded-xl border border-slate-800 text-xs text-emerald-400 flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4" />
                    No risk indicators detected for this transaction. Score is LOW.
                  </div>
                ) : (
                  <div className="space-y-2">
                    {data.explainable_risk_factors?.map((factor: any, idx: number) => (
                      <div
                        key={idx}
                        onClick={() => setSelectedFactor(factor)}
                        className={`p-3 rounded-xl border cursor-pointer transition-all flex items-center justify-between ${
                          selectedFactor?.code === factor.code
                            ? 'bg-cyan-500/15 border-cyan-500/50 text-slate-100'
                            : 'bg-slate-900/60 border-slate-800 text-slate-400 hover:border-slate-700'
                        }`}
                      >
                        <div className="flex items-center gap-3">
                          <span className="font-mono text-xs font-bold text-red-400">{factor.points}</span>
                          <span className="text-xs font-bold text-slate-200">{factor.factor}</span>
                        </div>
                        <ChevronRight className="w-4 h-4 text-slate-500" />
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Factor Explanation Box */}
              <div className="bg-slate-900/90 p-5 rounded-xl border border-slate-800 flex flex-col justify-between">
                <div>
                  <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-2 flex items-center gap-2">
                    <Info className="w-4 h-4 text-cyan-400" />
                    Factor Explanation Detail
                  </h4>
                  {selectedFactor ? (
                    <div className="space-y-3 mt-3">
                      <div className="flex items-center justify-between">
                        <span className="font-mono text-xs font-bold text-cyan-400">{selectedFactor.code}</span>
                        <span className="text-xs font-extrabold text-red-400 bg-red-500/10 px-2 py-0.5 rounded border border-red-500/30">
                          {selectedFactor.points} Score Impact
                        </span>
                      </div>
                      <p className="text-sm font-semibold text-slate-100">{selectedFactor.factor}</p>
                      <div className="p-3 bg-slate-950 rounded-lg border border-slate-800 text-xs text-slate-300 font-mono leading-relaxed">
                        {selectedFactor.explanation}
                      </div>
                    </div>
                  ) : (
                    <p className="text-xs text-slate-400 italic">Click any detected risk factor on the left to inspect its complete explanation.</p>
                  )}
                </div>

                <div className="mt-6 pt-4 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
                  <span>Sender Account: <strong className="text-slate-200">{data.sender}</strong></span>
                  <span>Receiver Account: <strong className="text-slate-200">{data.receiver}</strong></span>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
