import React, { useEffect, useState } from 'react';
import { 
  FlaskConical, 
  Play, 
  CheckCircle2, 
  ShieldAlert, 
  AlertTriangle, 
  RefreshCw,
  Cpu,
  Info
} from 'lucide-react';
import { getSimulationScenarios, runSimulationScenario } from '../services/api';

export const SimulationLabPage: React.FC = () => {
  const [scenarios, setScenarios] = useState<any[]>([]);
  const [runningKey, setRunningKey] = useState<string | null>(null);
  const [latestResult, setLatestResult] = useState<any>(null);

  useEffect(() => {
    getSimulationScenarios().then(setScenarios).catch(console.error);
  }, []);

  const handleRun = async (key: string) => {
    setRunningKey(key);
    setLatestResult(null);

    try {
      const res = await runSimulationScenario(key);
      setLatestResult(res);
      setRunningKey(null);
    } catch (err: any) {
      console.error(err);
      setRunningKey(null);
    }
  };

  return (
    <div className="p-6 space-y-6 bg-[#0B0F17] text-slate-100 min-h-screen">
      {/* Header */}
      <div className="border-b border-slate-800 pb-5">
        <h1 className="text-xl font-black tracking-tight text-slate-100 uppercase flex items-center gap-2">
          <FlaskConical className="w-6 h-6 text-cyan-400" />
          TRANSACTION SECURITY LAB — SYNTHETIC SCENARIOS
        </h1>
        <p className="text-xs text-slate-400 mt-1">Safely simulate synthetic attack vectors and observe real-time detection, explainable risk scoring, and auto security test triggering</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Scenario Selection Grid */}
        <div className="lg:col-span-2 space-y-4">
          <h2 className="text-xs font-black uppercase tracking-wider text-slate-300">Preset Synthetic Scenarios</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {scenarios.map((sc) => (
              <div key={sc.key} className="bg-[#0D131F] p-4 rounded-xl border border-slate-800 flex flex-col justify-between hover:border-cyan-500/40 transition-all">
                <div>
                  <div className="flex items-center justify-between">
                    <span className="font-mono text-[11px] font-bold text-cyan-400">{sc.key}</span>
                    <span className="text-[10px] font-extrabold px-2 py-0.5 rounded bg-slate-800 text-yellow-400 border border-slate-700">
                      {sc.expected_risk}
                    </span>
                  </div>
                  <h3 className="text-xs font-extrabold text-slate-100 mt-2">{sc.name}</h3>
                  <p className="text-[11px] text-slate-400 mt-1 leading-snug">{sc.description}</p>
                </div>

                <button
                  onClick={() => handleRun(sc.key)}
                  disabled={runningKey === sc.key}
                  className="mt-4 w-full py-2 bg-cyan-500/15 hover:bg-cyan-500/25 border border-cyan-500/40 text-cyan-400 font-extrabold rounded-lg text-xs transition-all flex items-center justify-center gap-1.5"
                >
                  {runningKey === sc.key ? (
                    <span className="flex items-center gap-2">
                      <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                      Simulating...
                    </span>
                  ) : (
                    <>
                      <Play className="w-3.5 h-3.5" />
                      Run Synthetic Scenario
                    </>
                  )}
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Live Simulation Output Card */}
        <div className="space-y-4">
          <h2 className="text-xs font-black uppercase tracking-wider text-slate-300 flex items-center gap-2">
            <Cpu className="w-4 h-4 text-cyan-400" />
            Live Security Monitor Response
          </h2>

          <div className="bg-[#0D131F] p-5 rounded-xl border border-slate-800 shadow-xl space-y-4">
            {!latestResult ? (
              <div className="p-12 text-center text-slate-500 text-xs italic font-mono space-y-2">
                <Info className="w-6 h-6 text-slate-600 mx-auto" />
                Select any synthetic scenario on the left to observe real-time engine evaluation live.
              </div>
            ) : (
              <div className="space-y-4 font-mono text-xs">
                <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                  <span className="font-bold text-slate-300">SCENARIO EXECUTION:</span>
                  <span className="font-black text-cyan-400">{latestResult.scenario}</span>
                </div>

                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-slate-400">Transaction ID:</span>
                    <span className="text-slate-100 font-bold">{latestResult.result?.transaction_id}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">Risk Score:</span>
                    <span className="text-cyan-400 font-black text-sm">{latestResult.result?.risk_score} / 100</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">Risk Level:</span>
                    <span className="text-yellow-400 font-bold">{latestResult.result?.risk_level}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">Decision:</span>
                    <span className="text-slate-100 font-bold uppercase">{latestResult.result?.decision}</span>
                  </div>
                </div>

                {/* Auto Triggered Security Tests */}
                {latestResult.result?.auto_triggered_tests?.triggered && (
                  <div className="p-3 bg-red-500/10 border border-red-500/30 rounded-lg space-y-1">
                    <p className="text-[11px] font-bold text-red-400 flex items-center gap-1.5">
                      <ShieldAlert className="w-3.5 h-3.5" />
                      AUTOMATIC SECURITY TESTS TRIGGERED
                    </p>
                    <p className="text-[10px] text-slate-300">Run Ref: {latestResult.result.auto_triggered_tests.run_number}</p>
                    <p className="text-[10px] text-slate-300">Total Security Tests: {latestResult.result.auto_triggered_tests.total_tests} | Passed: {latestResult.result.auto_triggered_tests.passed} | Failed: {latestResult.result.auto_triggered_tests.failed}</p>
                  </div>
                )}

                {/* Triggered Risk Indicators */}
                {latestResult.result?.indicators && (
                  <div className="space-y-2 pt-2 border-t border-slate-800">
                    <p className="text-[11px] font-bold text-slate-300 uppercase">Triggered Indicators:</p>
                    <div className="space-y-1">
                      {latestResult.result.indicators.map((ind: any, i: number) => (
                        <div key={i} className="p-2 bg-slate-900 rounded border border-slate-800 text-[11px]">
                          <div className="flex justify-between font-bold text-cyan-400">
                            <span>{ind.name}</span>
                            <span>+{ind.points}</span>
                          </div>
                          <p className="text-slate-400 text-[10px] mt-0.5 leading-snug">{ind.explanation}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
