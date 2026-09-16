import React from 'react';
import { Settings, ShieldCheck, Code, Cpu } from 'lucide-react';

export const SettingsPage: React.FC = () => {
  const sampleYaml = `name: BankSecure API Guard Security Gate

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  security-gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Run BankSecure API Gate Assertion
        run: |
          pip install httpx
          python -c "
          import httpx
          res = httpx.post('http://localhost:8000/tests/run-suite', json={'execution_type': 'REGRESSION'})
          data = res.json()
          print(f'Gate Status: {data[\"status\"]} | Critical Flaws: {data[\"critical_count\"]}')
          if data['critical_count'] > 0 or data['overall_risk_score'] > 50.0:
              print('SECURITY GATE FAILED: High-risk vulnerabilities detected!')
              exit(1)
          print('SECURITY GATE PASSED!')
          "`;

  return (
    <div className="p-6 space-y-6 max-w-7xl mx-auto">
      {/* Title */}
      <div className="flex items-center justify-between border-b border-dark-border pb-4">
        <div>
          <h1 className="text-xl font-extrabold text-white tracking-tight flex items-center gap-2">
            <Settings className="w-5 h-5 text-brand-cyan" />
            SYSTEM SETTINGS & CI/CD SECURITY GATE CONFIGURATION
          </h1>
          <p className="text-xs text-slate-400 mt-1">Manage risk thresholds, API timeout bounds, and GitHub Actions CI/CD Security Gate pipeline workflow.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Settings Box */}
        <div className="bg-dark-card border border-dark-border rounded-xl p-5 space-y-4 shadow-lg">
          <h2 className="text-xs font-extrabold uppercase tracking-wider text-slate-300 border-b border-dark-border pb-3">
            RISK ENGINE THRESHOLDS & POLICY
          </h2>

          <div className="space-y-4 text-xs">
            <div>
              <label className="block text-slate-400 font-bold mb-1">Critical Risk Cutoff (0-100)</label>
              <input type="number" defaultValue={76} className="w-full bg-[#0B0F17] border border-dark-border rounded-lg px-3 py-2 text-white font-mono" />
            </div>

            <div>
              <label className="block text-slate-400 font-bold mb-1">High Risk Cutoff (0-100)</label>
              <input type="number" defaultValue={51} className="w-full bg-[#0B0F17] border border-dark-border rounded-lg px-3 py-2 text-white font-mono" />
            </div>

            <div>
              <label className="block text-slate-400 font-bold mb-1">CI/CD Build Failure Condition</label>
              <select className="w-full bg-[#0B0F17] border border-dark-border rounded-lg px-3 py-2 text-white font-bold">
                <option value="ANY_CRITICAL">Fail build if ANY Critical finding exists (Recommended)</option>
                <option value="SCORE_ABOVE_50">Fail build if Dynamic Risk Score &gt; 50</option>
                <option value="STRICT_ZERO">Strict Zero Vulnerability Tolerance</option>
              </select>
            </div>

            <button className="w-full py-2.5 bg-brand-cyan hover:bg-cyan-400 text-black font-extrabold rounded-lg transition-all shadow">
              UPDATE SECURITY POLICY
            </button>
          </div>
        </div>

        {/* GitHub Actions Snippet Box */}
        <div className="bg-dark-card border border-dark-border rounded-xl p-5 space-y-3 shadow-lg">
          <h2 className="text-xs font-extrabold uppercase tracking-wider text-slate-300 flex items-center gap-2 border-b border-dark-border pb-3">
            <Code className="w-4 h-4 text-brand-cyan" />
            GITHUB ACTIONS SECURITY GATE WORKFLOW (.github/workflows/security-gate.yml)
          </h2>
          <pre className="p-3 bg-[#080B11] border border-slate-900 rounded-lg text-[10px] font-mono text-slate-300 overflow-x-auto h-72">
            {sampleYaml}
          </pre>
        </div>
      </div>
    </div>
  );
};
