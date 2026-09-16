import React, { useEffect, useState } from 'react';
import { 
  CreditCard, 
  Send, 
  ShieldCheck, 
  AlertTriangle, 
  CheckCircle2, 
  XCircle, 
  Sliders, 
  RefreshCw,
  User,
  Smartphone,
  Globe
} from 'lucide-react';
import { 
  executeManualTransfer, 
  getMockAccounts, 
  getBeneficiaries, 
  getSandboxToggles, 
  updateSandboxToggle 
} from '../services/api';

export const MockBankSandboxPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'portal' | 'sandbox'>('portal');

  // Portal State
  const [accounts, setAccounts] = useState<any[]>([]);
  const [senderAccount, setSenderAccount] = useState('ACC-1001');
  const [beneficiaries, setBeneficiaries] = useState<any[]>([]);
  const [receiverAccount, setReceiverAccount] = useState('ACC-1002');
  const [amount, setAmount] = useState<string>('5000');
  const [currency, setCurrency] = useState('INR');
  const [deviceId, setDeviceId] = useState('DEVICE-001');
  const [ipAddress, setIpAddress] = useState('192.168.1.50');

  const [transferResult, setTransferResult] = useState<any>(null);
  const [errorResult, setErrorResult] = useState<any>(null);
  const [submitting, setSubmitting] = useState(false);

  // Sandbox State
  const [toggles, setToggles] = useState<any[]>([]);

  const loadData = async () => {
    try {
      const accs = await getMockAccounts();
      setAccounts(accs);

      const bens = await getBeneficiaries(senderAccount);
      setBeneficiaries(bens);

      const togs = await getSandboxToggles();
      setToggles(togs);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    loadData();
  }, [senderAccount]);

  const handleTransfer = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setTransferResult(null);
    setErrorResult(null);

    try {
      const res = await executeManualTransfer({
        sender_account: senderAccount,
        receiver_account: receiverAccount,
        amount: parseFloat(amount) || 0,
        currency,
        device_id: deviceId,
        ip_address: ipAddress
      });

      setTransferResult(res);
      loadData(); // Refresh balance
      setSubmitting(false);
    } catch (err: any) {
      const detail = err.response?.data?.detail;
      setErrorResult(detail || { message: err.message || 'Transaction rejected by security engine' });
      setSubmitting(false);
    }
  };

  const handleToggle = async (key: string, isEnabled: boolean) => {
    await updateSandboxToggle(key, !isEnabled);
    const togs = await getSandboxToggles();
    setToggles(togs);
  };

  const selectedAccObj = accounts.find((a) => a.account_number === senderAccount) || accounts[0];

  return (
    <div className="p-6 space-y-6 bg-[#0B0F17] text-slate-100 min-h-screen">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-5">
        <div>
          <h1 className="text-xl font-black tracking-tight text-slate-100 uppercase">CUSTOMER BANKING PORTAL & SANDBOX</h1>
          <p className="text-xs text-slate-400 mt-1">Manual transfers automatically pass through the Real-Time Security Monitoring & Risk Engine</p>
        </div>

        {/* Tab Switcher */}
        <div className="flex bg-[#0D131F] p-1 rounded-xl border border-slate-800">
          <button
            onClick={() => setActiveTab('portal')}
            className={`px-4 py-1.5 rounded-lg text-xs font-bold transition-all ${
              activeTab === 'portal' ? 'bg-cyan-500 text-slate-950 font-black shadow-md' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Manual Transfer Portal
          </button>
          <button
            onClick={() => setActiveTab('sandbox')}
            className={`px-4 py-1.5 rounded-lg text-xs font-bold transition-all ${
              activeTab === 'sandbox' ? 'bg-cyan-500 text-slate-950 font-black shadow-md' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Security Sandbox Toggles
          </button>
        </div>
      </div>

      {activeTab === 'portal' ? (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Account Details & Balance Card */}
          <div className="space-y-6">
            <div className="bg-gradient-to-br from-[#1E293B] to-[#0F172A] p-6 rounded-2xl border border-slate-700 shadow-xl relative overflow-hidden">
              <div className="absolute -right-6 -bottom-6 w-32 h-32 bg-cyan-500/10 rounded-full blur-2xl" />
              <div className="flex justify-between items-start mb-6">
                <div>
                  <p className="text-xs text-cyan-400 font-bold uppercase tracking-widest">BankSecure Digital Account</p>
                  <p className="text-lg font-black text-slate-100 mt-1">{selectedAccObj?.owner_name || 'Customer'}</p>
                </div>
                <CreditCard className="w-8 h-8 text-cyan-400 opacity-80" />
              </div>

              <div className="space-y-1">
                <p className="text-[11px] text-slate-400 font-mono">Available Account Balance</p>
                <p className="text-3xl font-black text-emerald-400">
                  ₹{selectedAccObj?.balance?.toLocaleString('en-IN') || '75,000.00'}
                </p>
              </div>

              <div className="mt-6 pt-4 border-t border-slate-700/80 flex items-center justify-between text-xs font-mono text-slate-300">
                <span>Acc: **** **** {selectedAccObj?.account_number?.slice(-4)}</span>
                <span className="text-emerald-400 font-bold">STATUS: ACTIVE</span>
              </div>
            </div>

            {/* Account Quick Select */}
            <div className="bg-[#0D131F] p-5 rounded-xl border border-slate-800 space-y-3">
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2">
                <User className="w-4 h-4 text-cyan-400" />
                Select Customer Account
              </h3>
              <select
                value={senderAccount}
                onChange={(e) => setSenderAccount(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-xs text-slate-100 focus:outline-none focus:border-cyan-500 font-mono"
              >
                {accounts.map((acc) => (
                  <option key={acc.account_number} value={acc.account_number}>
                    {acc.owner_name} ({acc.account_number}) — Bal: ₹{acc.balance.toLocaleString('en-IN')}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Transfer Execution Form */}
          <div className="lg:col-span-2 space-y-6">
            <div className="bg-[#0D131F] p-6 rounded-xl border border-slate-800 shadow-xl space-y-5">
              <h2 className="text-sm font-black uppercase tracking-wider text-slate-200 flex items-center gap-2">
                <Send className="w-4 h-4 text-cyan-400" />
                Execute Manual Fund Transfer
              </h2>

              <form onSubmit={handleTransfer} className="space-y-4 text-xs font-mono">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-slate-400 font-bold mb-1.5">Recipient Beneficiary Account</label>
                    <input
                      type="text"
                      value={receiverAccount}
                      onChange={(e) => setReceiverAccount(e.target.value)}
                      placeholder="e.g. ACC-1002"
                      className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-slate-100 focus:outline-none focus:border-cyan-500"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-slate-400 font-bold mb-1.5">Transfer Amount (INR)</label>
                    <input
                      type="number"
                      value={amount}
                      onChange={(e) => setAmount(e.target.value)}
                      placeholder="e.g. 5000"
                      className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-slate-100 focus:outline-none focus:border-cyan-500 font-black text-sm"
                      required
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
                  <div>
                    <label className="block text-slate-400 font-bold mb-1.5 flex items-center gap-1.5">
                      <Smartphone className="w-3.5 h-3.5 text-cyan-400" />
                      Client Device ID (Synthetic)
                    </label>
                    <input
                      type="text"
                      value={deviceId}
                      onChange={(e) => setDeviceId(e.target.value)}
                      className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-slate-100 focus:outline-none focus:border-cyan-500"
                    />
                  </div>

                  <div>
                    <label className="block text-slate-400 font-bold mb-1.5 flex items-center gap-1.5">
                      <Globe className="w-3.5 h-3.5 text-cyan-400" />
                      Client IP Metadata (Synthetic)
                    </label>
                    <input
                      type="text"
                      value={ipAddress}
                      onChange={(e) => setIpAddress(e.target.value)}
                      className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-slate-100 focus:outline-none focus:border-cyan-500"
                    />
                  </div>
                </div>

                <button
                  type="submit"
                  disabled={submitting}
                  className="w-full py-3 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-black uppercase tracking-wider rounded-lg transition-all flex items-center justify-center gap-2 text-sm shadow-lg shadow-cyan-500/20"
                >
                  {submitting ? (
                    <span className="flex items-center gap-2">
                      <RefreshCw className="w-4 h-4 animate-spin" />
                      Security Monitoring Engine Analyzing...
                    </span>
                  ) : (
                    <>
                      <Send className="w-4 h-4" />
                      Submit Manual Banking Transfer
                    </>
                  )}
                </button>
              </form>
            </div>

            {/* Real-Time Security Feedback Modal Card */}
            {transferResult && (
              <div className="bg-slate-900/90 p-5 rounded-xl border border-emerald-500/50 shadow-xl space-y-3">
                <div className="flex items-center justify-between border-b border-slate-800 pb-2">
                  <div className="flex items-center gap-2 text-emerald-400 font-black text-sm">
                    <CheckCircle2 className="w-5 h-5" />
                    SECURITY ENGINE MONITORING FEEDBACK — ALLOWED
                  </div>
                  <span className="text-xs font-mono text-cyan-400">{transferResult.transaction_id}</span>
                </div>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs font-mono">
                  <div><span className="text-slate-400">Risk Score:</span> <strong className="text-slate-100 font-bold">{transferResult.risk_score}/100</strong></div>
                  <div><span className="text-slate-400">Risk Level:</span> <strong className="text-emerald-400 font-bold">{transferResult.risk_level}</strong></div>
                  <div><span className="text-slate-400">Decision:</span> <strong className="text-cyan-400 font-bold">{transferResult.decision}</strong></div>
                  <div><span className="text-slate-400">Flags:</span> <strong className="text-slate-100 font-bold">{transferResult.flags_count}</strong></div>
                </div>
              </div>
            )}

            {errorResult && (
              <div className="bg-slate-900/90 p-5 rounded-xl border border-red-500/50 shadow-xl space-y-3">
                <div className="flex items-center justify-between border-b border-slate-800 pb-2">
                  <div className="flex items-center gap-2 text-red-400 font-black text-sm">
                    <XCircle className="w-5 h-5" />
                    SECURITY ENGINE MONITORING FEEDBACK — REJECTED / BLOCKED
                  </div>
                  <span className="text-xs font-mono text-red-400">{errorResult.decision || 'BLOCKED'}</span>
                </div>
                <p className="text-xs text-slate-200 font-semibold">{errorResult.message || JSON.stringify(errorResult)}</p>
                {errorResult.indicators && (
                  <div className="space-y-1">
                    <p className="text-[11px] font-bold text-slate-400 uppercase">Triggered Indicators:</p>
                    {errorResult.indicators.map((ind: any, i: number) => (
                      <p key={i} className="text-xs text-red-300 font-mono">• {ind.name} (+{ind.points}) — {ind.explanation}</p>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      ) : (
        /* Sandbox Vulnerability Toggles Tab */
        <div className="bg-[#0D131F] p-6 rounded-xl border border-slate-800 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <div>
              <h2 className="text-sm font-black uppercase tracking-wider text-slate-200 flex items-center gap-2">
                <Sliders className="w-4 h-4 text-cyan-400" />
                Simulated Sandbox Vulnerability Toggles
              </h2>
              <p className="text-xs text-slate-400">Enable vulnerabilities in mock banking APIs to test automated security test triggering</p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {toggles.map((tog) => (
              <div key={tog.key} className="p-4 bg-slate-900/80 rounded-xl border border-slate-800 flex items-center justify-between">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-xs font-bold text-cyan-400">{tog.key}</span>
                    <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-slate-800 text-slate-400 border border-slate-700">{tog.category}</span>
                  </div>
                  <p className="text-xs font-bold text-slate-100 mt-1">{tog.name}</p>
                  <p className="text-[11px] text-slate-400 mt-0.5 leading-snug">{tog.description}</p>
                </div>

                <button
                  onClick={() => handleToggle(tog.key, tog.is_enabled)}
                  className={`px-3 py-1.5 text-xs font-black rounded-lg transition-all border ${
                    tog.is_enabled
                      ? 'bg-red-500/20 text-red-400 border-red-500/50 shadow-sm'
                      : 'bg-slate-800 text-slate-400 border-slate-700 hover:text-slate-200'
                  }`}
                >
                  {tog.is_enabled ? 'VULN LIVE' : 'SECURE'}
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
