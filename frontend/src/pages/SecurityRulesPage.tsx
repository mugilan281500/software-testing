import React, { useEffect, useState } from 'react';
import { Sliders, ShieldCheck, CheckCircle2, Save, RefreshCw } from 'lucide-react';
import { getSecurityRules, updateSecurityRule, getBankingRules, updateBankingRule } from '../services/api';

export const SecurityRulesPage: React.FC = () => {
  const [securityRules, setSecurityRules] = useState<any[]>([]);
  const [bankingRules, setBankingRules] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [savedMsg, setSavedMsg] = useState('');

  const loadRules = async () => {
    try {
      const sec = await getSecurityRules();
      setSecurityRules(sec);
      const bank = await getBankingRules();
      setBankingRules(bank);
      setLoading(false);
    } catch (err) {
      console.error(err);
      setLoading(false);
    }
  };

  useEffect(() => {
    loadRules();
  }, []);

  const toggleSecRule = async (key: string, isEnabled: boolean) => {
    await updateSecurityRule(key, !isEnabled);
    setSavedMsg(`Rule ${key} updated successfully.`);
    setTimeout(() => setSavedMsg(''), 3000);
    loadRules();
  };

  const toggleBankRule = async (code: string, isEnabled: boolean) => {
    await updateBankingRule(code, !isEnabled);
    setSavedMsg(`Banking Rule ${code} updated successfully.`);
    setTimeout(() => setSavedMsg(''), 3000);
    loadRules();
  };

  return (
    <div className="p-6 space-y-6 bg-[#0B0F17] text-slate-100 min-h-screen">
      {/* Header */}
      <div className="border-b border-slate-800 pb-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-black tracking-tight text-slate-100 uppercase flex items-center gap-2">
            <Sliders className="w-6 h-6 text-cyan-400" />
            ADMIN SECURITY & BANKING RULE CONFIGURATION
          </h1>
          <p className="text-xs text-slate-400 mt-1">Configure threshold multipliers, time windows, penalty weights, and ENABLE/DISABLE toggles stored in database</p>
        </div>

        {savedMsg && (
          <div className="px-3 py-1.5 bg-emerald-500/20 text-emerald-400 border border-emerald-500/50 rounded-lg text-xs font-mono font-bold flex items-center gap-1.5">
            <CheckCircle2 className="w-4 h-4" />
            {savedMsg}
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Security Risk Rules */}
        <div className="bg-[#0D131F] p-6 rounded-xl border border-slate-800 space-y-4 shadow-xl">
          <h2 className="text-sm font-black uppercase tracking-wider text-slate-200 flex items-center gap-2 border-b border-slate-800 pb-3">
            <ShieldCheck className="w-4 h-4 text-cyan-400" />
            Security Risk Rules & Threshold Configuration
          </h2>

          <div className="space-y-3 font-mono text-xs">
            {securityRules.map((rule) => (
              <div key={rule.rule_key} className="p-3.5 bg-slate-900 rounded-xl border border-slate-800 flex items-center justify-between">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-bold text-cyan-400">{rule.rule_key}</span>
                    <span className="text-[10px] px-1.5 py-0.5 rounded bg-slate-800 text-slate-400 border border-slate-700">{rule.category}</span>
                  </div>
                  <p className="text-xs font-bold text-slate-100 mt-1">{rule.name}</p>
                  <p className="text-[11px] text-slate-400 leading-snug mt-0.5">{rule.description}</p>
                </div>

                <button
                  onClick={() => toggleSecRule(rule.rule_key, rule.is_enabled)}
                  className={`px-3 py-1.5 text-xs font-black rounded-lg transition-all border ${
                    rule.is_enabled
                      ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/50'
                      : 'bg-slate-800 text-slate-400 border-slate-700'
                  }`}
                >
                  {rule.is_enabled ? 'ENABLED' : 'DISABLED'}
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Banking Business Rules */}
        <div className="bg-[#0D131F] p-6 rounded-xl border border-slate-800 space-y-4 shadow-xl">
          <h2 className="text-sm font-black uppercase tracking-wider text-slate-200 flex items-center gap-2 border-b border-slate-800 pb-3">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            Banking Business Rules Engine
          </h2>

          <div className="space-y-3 font-mono text-xs">
            {bankingRules.map((rule) => (
              <div key={rule.rule_code} className="p-3.5 bg-slate-900 rounded-xl border border-slate-800 flex items-center justify-between">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-bold text-emerald-400">{rule.rule_code}</span>
                    <span className="text-[10px] px-1.5 py-0.5 rounded bg-slate-800 text-slate-400 border border-slate-700">{rule.rule_type}</span>
                  </div>
                  <p className="text-xs font-bold text-slate-100 mt-1">{rule.name}</p>
                  <p className="text-[11px] text-slate-400 leading-snug mt-0.5">{rule.description}</p>
                </div>

                <button
                  onClick={() => toggleBankRule(rule.rule_code, rule.is_enabled)}
                  className={`px-3 py-1.5 text-xs font-black rounded-lg transition-all border ${
                    rule.is_enabled
                      ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/50'
                      : 'bg-slate-800 text-slate-400 border-slate-700'
                  }`}
                >
                  {rule.is_enabled ? 'ENABLED' : 'DISABLED'}
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
