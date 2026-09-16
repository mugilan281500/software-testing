import React, { useEffect, useState } from 'react';
import { 
  Unplug, 
  Upload, 
  Grid, 
  ShieldAlert, 
  CheckCircle2, 
  AlertTriangle, 
  Layers, 
  Code,
  FileCode
} from 'lucide-react';
import { getApiInventory, importOpenApiSpec } from '../services/api';

export const ApiInventoryPage: React.FC = () => {
  const [apis, setApis] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'catalog' | 'heatmap' | 'import'>('catalog');

  // Import Modal State
  const [openApiTitle, setOpenApiTitle] = useState('Core Banking OpenAPI Spec');
  const [openApiVersion, setOpenApiVersion] = useState('v2.1.0');
  const [importResult, setImportResult] = useState<any>(null);

  const loadApis = async () => {
    try {
      const data = await getApiInventory();
      setApis(data);
      setLoading(false);
    } catch (err) {
      console.error(err);
      setLoading(false);
    }
  };

  useEffect(() => {
    loadApis();
  }, []);

  const handleOpenApiImport = async (e: React.FormEvent) => {
    e.preventDefault();
    const sampleEndpoints = [
      { endpoint: "/mock-bank/transfer", method: "POST", name: "Fund Transfer API", description: "Processes transfers" },
      { endpoint: "/mock-bank/accounts", method: "GET", name: "Account Balance API", description: "Fetch account balance" },
      { endpoint: "/mock-bank/loan-application", method: "POST", name: "Instant Loan API [NEW]", description: "Applies for quick credit loan" },
      { endpoint: "/mock-bank/crypto-wallet", method: "POST", name: "Crypto Transfer API [NEW]", description: "Digital asset transfers" }
    ];

    const res = await importOpenApiSpec(openApiTitle, openApiVersion, sampleEndpoints);
    setImportResult(res);
    loadApis();
  };

  const getHeatmapColor = (level: string) => {
    switch (level) {
      case 'CRITICAL': return 'bg-red-500/20 text-red-400 border-red-500/60';
      case 'HIGH': return 'bg-orange-500/20 text-orange-400 border-orange-500/60';
      case 'MEDIUM': return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/60';
      default: return 'bg-emerald-500/20 text-emerald-400 border-emerald-500/60';
    }
  };

  return (
    <div className="p-6 space-y-6 bg-[#0B0F17] text-slate-100 min-h-screen">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-5">
        <div>
          <h1 className="text-xl font-black tracking-tight text-slate-100 uppercase flex items-center gap-2">
            <Unplug className="w-6 h-6 text-cyan-400" />
            API INVENTORY, RISK HEATMAP & CHANGE DETECTION
          </h1>
          <p className="text-xs text-slate-400 mt-1">API security scores calculated independently from transaction risk; OpenAPI change detector automatically tags regression priorities</p>
        </div>

        {/* Tab Switcher */}
        <div className="flex bg-[#0D131F] p-1 rounded-xl border border-slate-800 text-xs font-bold">
          <button
            onClick={() => setActiveTab('catalog')}
            className={`px-3.5 py-1.5 rounded-lg transition-all ${
              activeTab === 'catalog' ? 'bg-cyan-500 text-slate-950 font-black' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            API Catalog
          </button>
          <button
            onClick={() => setActiveTab('heatmap')}
            className={`px-3.5 py-1.5 rounded-lg transition-all ${
              activeTab === 'heatmap' ? 'bg-cyan-500 text-slate-950 font-black' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Risk Heatmap Matrix
          </button>
          <button
            onClick={() => setActiveTab('import')}
            className={`px-3.5 py-1.5 rounded-lg transition-all ${
              activeTab === 'import' ? 'bg-cyan-500 text-slate-950 font-black' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            OpenAPI Spec Import
          </button>
        </div>
      </div>

      {activeTab === 'catalog' && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {apis.map((api) => (
            <div key={api.id} className="bg-[#0D131F] p-5 rounded-xl border border-slate-800 space-y-3 shadow-lg hover:border-cyan-500/40 transition-all">
              <div className="flex items-center justify-between">
                <span className="font-mono text-xs font-black text-cyan-400">{api.method} {api.endpoint}</span>
                <span className={`px-2 py-0.5 text-[10px] font-extrabold rounded border ${getHeatmapColor(api.risk_level)}`}>
                  {api.risk_level} ({api.risk_score})
                </span>
              </div>

              <h3 className="text-sm font-extrabold text-slate-100">{api.name}</h3>
              <p className="text-xs text-slate-400 leading-snug">{api.description}</p>

              <div className="pt-3 border-t border-slate-800 grid grid-cols-2 gap-2 text-xs font-mono">
                <div className="p-2 bg-slate-900 rounded border border-slate-800">
                  <span className="text-[10px] text-slate-400 block">API Sec Score</span>
                  <span className="font-black text-emerald-400 text-sm">{api.security_score || 90.0}/100</span>
                </div>
                <div className="p-2 bg-slate-900 rounded border border-slate-800">
                  <span className="text-[10px] text-slate-400 block">Regression Priority</span>
                  <span className="font-black text-cyan-400 text-sm">{api.regression_priority || 'NORMAL'}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {activeTab === 'heatmap' && (
        <div className="bg-[#0D131F] p-6 rounded-xl border border-slate-800 space-y-6">
          <h2 className="text-sm font-black uppercase tracking-wider text-slate-200 flex items-center gap-2">
            <Grid className="w-4 h-4 text-cyan-400" />
            Visual API Risk Heatmap Matrix
          </h2>

          <div className="grid grid-cols-1 sm:grid-cols-4 gap-4 text-center font-mono">
            {['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'].map((level) => {
              const count = apis.filter((a) => a.risk_level === level).length;
              return (
                <div key={level} className={`p-5 rounded-xl border ${getHeatmapColor(level)}`}>
                  <p className="text-xs font-extrabold uppercase">{level} RISK ENDPOINTS</p>
                  <p className="text-3xl font-black mt-2">{count}</p>
                </div>
              );
            })}
          </div>

          {/* Matrix Grid */}
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs font-mono">
              <thead className="bg-[#0F172A] text-slate-400 border-b border-slate-800 uppercase">
                <tr>
                  <th className="p-3">Endpoint</th>
                  <th className="p-3">Method</th>
                  <th className="p-3">API Risk Level</th>
                  <th className="p-3">API Sec Score</th>
                  <th className="p-3">Regression Priority</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {apis.map((api) => (
                  <tr key={api.id} className="hover:bg-slate-800/40">
                    <td className="p-3 font-bold text-cyan-400">{api.endpoint}</td>
                    <td className="p-3 font-bold text-slate-300">{api.method}</td>
                    <td className="p-3">
                      <span className={`px-2 py-0.5 rounded border font-bold text-[10px] ${getHeatmapColor(api.risk_level)}`}>
                        {api.risk_level} ({api.risk_score})
                      </span>
                    </td>
                    <td className="p-3 font-black text-emerald-400">{api.security_score || 90.0}/100</td>
                    <td className="p-3 font-bold text-cyan-300">{api.regression_priority || 'NORMAL'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {activeTab === 'import' && (
        <div className="bg-[#0D131F] p-6 rounded-xl border border-slate-800 space-y-6 max-w-2xl">
          <div>
            <h2 className="text-sm font-black uppercase tracking-wider text-slate-200 flex items-center gap-2">
              <FileCode className="w-4 h-4 text-cyan-400" />
              OpenAPI / Swagger Spec Import & Change Detector
            </h2>
            <p className="text-xs text-slate-400 mt-1">Upload or import OpenAPI JSON. Detects new/removed endpoints, schema changes, and automatically assigns CRITICAL regression priorities to endpoints with past security failures.</p>
          </div>

          <form onSubmit={handleOpenApiImport} className="space-y-4 text-xs font-mono">
            <div>
              <label className="block text-slate-400 font-bold mb-1">Specification Title</label>
              <input
                type="text"
                value={openApiTitle}
                onChange={(e) => setOpenApiTitle(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-slate-100 focus:outline-none focus:border-cyan-500"
                required
              />
            </div>

            <div>
              <label className="block text-slate-400 font-bold mb-1">Spec Version</label>
              <input
                type="text"
                value={openApiVersion}
                onChange={(e) => setOpenApiVersion(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-slate-100 focus:outline-none focus:border-cyan-500"
                required
              />
            </div>

            <button
              type="submit"
              className="w-full py-2.5 bg-cyan-500 text-slate-950 font-black rounded-lg hover:bg-cyan-400 uppercase tracking-wider flex items-center justify-center gap-2"
            >
              <Upload className="w-4 h-4" />
              Import OpenAPI Spec & Run Diff Analysis
            </button>
          </form>

          {importResult && (
            <div className="p-4 bg-slate-900 rounded-xl border border-cyan-500/40 space-y-2 text-xs font-mono">
              <p className="text-cyan-400 font-bold">Import & Diff Analysis Completed:</p>
              <p className="text-slate-300">• New Endpoints Added: {importResult.new_endpoints_count}</p>
              <p className="text-slate-300">• Modified Endpoints: {importResult.modified_endpoints_count}</p>
              <p className="text-slate-300">• Affected Test Cases Tagged: {importResult.affected_test_cases?.length || 0}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
