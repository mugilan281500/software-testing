import React, { useEffect, useState } from 'react';
import { 
  Play, 
  FlaskConical, 
  CheckCircle2, 
  XCircle, 
  AlertTriangle, 
  Clock, 
  RefreshCw, 
  Layers, 
  SlidersHorizontal,
  ChevronRight,
  Eye,
  FileCheck
} from 'lucide-react';
import { 
  getAdaptiveTestQueue, 
  runFullAutomatedTest, 
  runSelectedTests, 
  getTestRunsHistory, 
  getTestRunDetails 
} from '../services/api';

export const TestExecutionPage: React.FC = () => {
  const [queue, setQueue] = useState<any[]>([]);
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [executing, setExecuting] = useState(false);
  const [progress, setProgress] = useState(0);

  // Selected Modules
  const availableModules = [
    'Authentication',
    'Authorization',
    'Functional',
    'Negative',
    'Security',
    'Banking Rules',
    'Transaction Monitoring',
    'Performance'
  ];
  const [selectedModules, setSelectedModules] = useState<string[]>(availableModules);

  // Details Modal
  const [selectedRunDetails, setSelectedRunDetails] = useState<any>(null);

  const loadData = async () => {
    try {
      const q = await getAdaptiveTestQueue();
      setQueue(q);
      const h = await getTestRunsHistory();
      setHistory(h);
      setLoading(false);
    } catch (err) {
      console.error(err);
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleModuleToggle = (mod: string) => {
    if (selectedModules.includes(mod)) {
      setSelectedModules(selectedModules.filter((m) => m !== mod));
    } else {
      setSelectedModules([...selectedModules, mod]);
    }
  };

  const executeFullSuite = async () => {
    setExecuting(true);
    setProgress(15);
    try {
      setTimeout(() => setProgress(45), 300);
      setTimeout(() => setProgress(75), 700);
      const res = await runFullAutomatedTest();
      setProgress(100);
      setTimeout(() => {
        setExecuting(false);
        setProgress(0);
        loadData();
      }, 400);
    } catch (err) {
      console.error(err);
      setExecuting(false);
      setProgress(0);
    }
  };

  const executeSelectedSuite = async () => {
    if (selectedModules.length === 0) return;
    setExecuting(true);
    setProgress(20);
    try {
      setTimeout(() => setProgress(65), 400);
      const res = await runSelectedTests(selectedModules);
      setProgress(100);
      setTimeout(() => {
        setExecuting(false);
        setProgress(0);
        loadData();
      }, 400);
    } catch (err) {
      console.error(err);
      setExecuting(false);
      setProgress(0);
    }
  };

  const viewRunDetails = async (runId: number) => {
    const details = await getTestRunDetails(runId);
    setSelectedRunDetails(details);
  };

  return (
    <div className="p-6 space-y-6 bg-[#0B0F17] text-slate-100 min-h-screen">
      {/* Header */}
      <div className="border-b border-slate-800 pb-5 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-black tracking-tight text-slate-100 uppercase flex items-center gap-2">
            <FlaskConical className="w-6 h-6 text-cyan-400" />
            AUTOMATED TEST EXECUTION ORCHESTRATOR
          </h1>
          <p className="text-xs text-slate-400 mt-1">Executes functional, security, negative, banking-rules, and performance testing independently from real-time transaction monitoring</p>
        </div>

        {/* Central Execution Buttons */}
        <div className="flex flex-wrap items-center gap-2">
          <button
            onClick={executeSelectedSuite}
            disabled={executing || selectedModules.length === 0}
            className="px-4 py-2.5 bg-slate-800 hover:bg-slate-700 text-cyan-400 font-extrabold text-xs rounded-xl border border-cyan-500/30 transition-all flex items-center gap-2 shadow-md"
          >
            <Play className="w-4 h-4" />
            RUN SELECTED TESTS ({selectedModules.length})
          </button>

          <button
            onClick={executeFullSuite}
            disabled={executing}
            className="px-5 py-2.5 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-black text-xs rounded-xl uppercase tracking-wider transition-all flex items-center gap-2 shadow-lg shadow-cyan-500/20"
          >
            <Play className="w-4 h-4" />
            RUN FULL AUTOMATED TEST
          </button>
        </div>
      </div>

      {/* Progress Bar during Execution */}
      {executing && (
        <div className="bg-[#0D131F] p-4 rounded-xl border border-cyan-500/40 space-y-2 shadow-xl">
          <div className="flex justify-between text-xs font-mono font-bold text-cyan-400">
            <span>Executing 11-Step Pipeline (Auth &rarr; Authz &rarr; Functional &rarr; Negative &rarr; Security &rarr; Rules &rarr; Performance)...</span>
            <span>{progress}%</span>
          </div>
          <div className="w-full bg-slate-900 rounded-full h-3 overflow-hidden border border-slate-800">
            <div className="bg-cyan-400 h-3 rounded-full transition-all duration-300" style={{ width: `${progress}%` }} />
          </div>
        </div>
      )}

      {/* User-Controlled Module Selection Bar */}
      <div className="bg-[#0D131F] p-5 rounded-xl border border-slate-800 space-y-3">
        <h2 className="text-xs font-black uppercase tracking-wider text-slate-300 flex items-center gap-2">
          <SlidersHorizontal className="w-4 h-4 text-cyan-400" />
          User-Controlled Test Module Selection
        </h2>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {availableModules.map((mod) => (
            <label
              key={mod}
              onClick={() => handleModuleToggle(mod)}
              className={`p-2.5 rounded-lg border text-xs font-mono font-bold cursor-pointer transition-all flex items-center gap-2 select-none ${
                selectedModules.includes(mod)
                  ? 'bg-cyan-500/15 border-cyan-500/50 text-cyan-300'
                  : 'bg-slate-900 border-slate-800 text-slate-400 hover:border-slate-700'
              }`}
            >
              <input
                type="checkbox"
                checked={selectedModules.includes(mod)}
                onChange={() => {}}
                className="rounded accent-cyan-400 cursor-pointer"
              />
              <span>{mod}</span>
            </label>
          ))}
        </div>
      </div>

      {/* Adaptive Test Queue */}
      <div className="bg-[#0D131F] rounded-xl border border-slate-800 shadow-xl overflow-hidden">
        <div className="px-6 py-4 border-b border-slate-800 flex items-center justify-between bg-[#111827]">
          <h2 className="text-xs font-black uppercase tracking-wider text-slate-200 flex items-center gap-2">
            <Layers className="w-4 h-4 text-cyan-400" />
            Adaptive Test Queue (Prioritized by Risk & Regression Status)
          </h2>
          <span className="text-xs text-slate-400 font-mono">{queue.length} APIs in Queue</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-[#0F172A] text-slate-400 border-b border-slate-800 uppercase">
              <tr>
                <th className="p-3">Rank</th>
                <th className="p-3">API Name</th>
                <th className="p-3">Endpoint</th>
                <th className="p-3">Method</th>
                <th className="p-3">API Risk Level</th>
                <th className="p-3">Regression Priority</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {queue.map((item, idx) => (
                <tr key={item.id} className="hover:bg-slate-800/40">
                  <td className="p-3 font-bold text-slate-400">#{idx + 1}</td>
                  <td className="p-3 font-bold text-slate-100">{item.name}</td>
                  <td className="p-3 font-bold text-cyan-400">{item.endpoint}</td>
                  <td className="p-3 text-slate-300">{item.method}</td>
                  <td className="p-3">
                    <span className={`px-2 py-0.5 rounded border text-[10px] font-extrabold ${
                      item.risk_level === 'CRITICAL' ? 'bg-red-500/20 text-red-400 border-red-500/50' :
                      item.risk_level === 'HIGH' ? 'bg-orange-500/20 text-orange-400 border-orange-500/50' : 'bg-emerald-500/20 text-emerald-400 border-emerald-500/50'
                    }`}>
                      {item.risk_level} ({item.risk_score})
                    </span>
                  </td>
                  <td className="p-3 font-bold text-cyan-400">{item.regression_priority}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Execution History Table */}
      <div className="bg-[#0D131F] rounded-xl border border-slate-800 shadow-xl overflow-hidden">
        <div className="px-6 py-4 border-b border-slate-800 flex items-center justify-between bg-[#111827]">
          <h2 className="text-xs font-black uppercase tracking-wider text-slate-200 flex items-center gap-2">
            <Clock className="w-4 h-4 text-cyan-400" />
            Execution History Logs
          </h2>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-[#0F172A] text-slate-400 border-b border-slate-800 uppercase">
              <tr>
                <th className="p-3">Run Ref</th>
                <th className="p-3">Execution Type</th>
                <th className="p-3">Total</th>
                <th className="p-3">Passed</th>
                <th className="p-3">Failed</th>
                <th className="p-3">Security Score</th>
                <th className="p-3">Status</th>
                <th className="p-3 text-right">Details</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {history.map((h) => (
                <tr key={h.id} className="hover:bg-slate-800/40">
                  <td className="p-3 font-bold text-cyan-400">{h.run_number}</td>
                  <td className="p-3 text-slate-300">{h.execution_type}</td>
                  <td className="p-3 text-slate-100 font-bold">{h.total_tests}</td>
                  <td className="p-3 text-emerald-400 font-bold">{h.passed}</td>
                  <td className="p-3 text-red-400 font-bold">{h.failed}</td>
                  <td className="p-3 text-cyan-300 font-black">{h.security_score}%</td>
                  <td className="p-3 font-bold text-slate-200">{h.status}</td>
                  <td className="p-3 text-right">
                    <button
                      onClick={() => viewRunDetails(h.id)}
                      className="px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-cyan-400 font-bold rounded-lg border border-slate-700 ml-auto flex items-center gap-1"
                    >
                      <Eye className="w-3.5 h-3.5" />
                      View Results
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Response Validation Details Modal */}
      {selectedRunDetails && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-[#0D131F] border border-slate-800 rounded-xl w-full max-w-4xl max-h-[85vh] overflow-y-auto p-6 space-y-4 shadow-2xl">
            <div className="flex justify-between items-center border-b border-slate-800 pb-3">
              <div>
                <h3 className="text-sm font-black uppercase text-slate-100 flex items-center gap-2">
                  <FileCheck className="w-4 h-4 text-cyan-400" />
                  Test Run Response Validation Details [{selectedRunDetails.run_number}]
                </h3>
                <p className="text-xs text-slate-400 font-mono">Executed: {selectedRunDetails.started_at}</p>
              </div>
              <button onClick={() => setSelectedRunDetails(null)} className="text-slate-400 hover:text-slate-100 font-bold">Close</button>
            </div>

            <div className="space-y-3 font-mono text-xs">
              {selectedRunDetails.results?.map((res: any) => (
                <div key={res.id} className="p-3 bg-slate-900 rounded-lg border border-slate-800 flex justify-between items-start gap-4">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-bold text-cyan-400">{res.test_case_id}</span>
                      <span className="text-slate-200 font-bold">{res.test_name}</span>
                      <span className="text-[10px] px-1.5 py-0.5 rounded bg-slate-800 text-slate-400 border border-slate-700">{res.category}</span>
                    </div>
                    <p className="text-slate-400 text-[11px] mt-1">Endpoint: {res.api_endpoint}</p>
                    <p className="text-slate-300 text-[11px] mt-0.5">{res.recommendation}</p>
                  </div>
                  <div className="text-right whitespace-nowrap">
                    <span className={`px-2.5 py-1 rounded text-xs font-black border ${res.status === 'PASS' ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/50' : 'bg-red-500/20 text-red-400 border-red-500/50'}`}>
                      {res.status}
                    </span>
                    <p className="text-[10px] text-slate-400 mt-1">{res.response_time_ms} ms</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
