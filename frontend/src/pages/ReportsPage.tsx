import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { FileText, Download, Plus, FileSpreadsheet, FileCode, History } from 'lucide-react';

export const ReportsPage: React.FC = () => {
  const [reports, setReports] = useState<any[]>([]);
  const [logs, setLogs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [reportTitle, setReportTitle] = useState('Executive Banking API Security Audit');
  const [reportFormat, setReportFormat] = useState('PDF');
  const [activeSubTab, setActiveSubTab] = useState<'reports' | 'audit'>('reports');

  const fetchReports = async () => {
    try {
      const res = await api.get('/reports');
      setReports(res.data);
      const auditRes = await api.get('/reports/audit-logs');
      setLogs(auditRes.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReports();
  }, []);

  const handleGenerateReport = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.post('/reports/generate', {
        title: reportTitle,
        format: reportFormat
      });
      fetchReports();
    } catch (err) {
      console.error(err);
    }
  };

  const handleDownload = (id: number) => {
    window.open(`http://localhost:8000/reports/download/${id}`, '_blank');
  };

  if (loading) return <div className="p-8 text-center text-slate-400 font-mono">Loading Security Reports & Audit Trail...</div>;

  return (
    <div className="p-6 space-y-6 bg-[#0B0F17] text-slate-100 min-h-screen">
      {/* Title */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-5">
        <div>
          <h1 className="text-xl font-black tracking-tight text-slate-100 uppercase flex items-center gap-2">
            <FileText className="w-6 h-6 text-cyan-400" />
            EXECUTIVE SECURITY REPORTS & IMMUTABLE AUDIT LOGS
          </h1>
          <p className="text-xs text-slate-400 mt-1">Generate and download comprehensive PDF, HTML, CSV, and JSON security assessment documents</p>
        </div>

        <div className="flex bg-[#0D131F] p-1 rounded-xl border border-slate-800 text-xs font-bold font-mono">
          <button
            onClick={() => setActiveSubTab('reports')}
            className={`px-3 py-1.5 rounded-lg transition-all ${activeSubTab === 'reports' ? 'bg-cyan-500 text-slate-950 font-black' : 'text-slate-400 hover:text-slate-200'}`}
          >
            Generated Reports
          </button>
          <button
            onClick={() => setActiveSubTab('audit')}
            className={`px-3 py-1.5 rounded-lg transition-all ${activeSubTab === 'audit' ? 'bg-cyan-500 text-slate-950 font-black' : 'text-slate-400 hover:text-slate-200'}`}
          >
            System Audit Trail
          </button>
        </div>
      </div>

      {activeSubTab === 'reports' ? (
        <div className="space-y-6">
          {/* Generator Form */}
          <div className="bg-[#0D131F] border border-slate-800 p-5 rounded-xl space-y-3 shadow-lg">
            <h2 className="text-xs font-black uppercase tracking-wider text-slate-300">GENERATE NEW EXECUTIVE REPORT</h2>
            <form onSubmit={handleGenerateReport} className="flex flex-col sm:flex-row items-center gap-3 text-xs font-mono">
              <input
                type="text"
                required
                value={reportTitle}
                onChange={(e) => setReportTitle(e.target.value)}
                placeholder="Report Document Title"
                className="flex-1 w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2.5 text-slate-100 focus:outline-none focus:border-cyan-500"
              />
              <select
                value={reportFormat}
                onChange={(e) => setReportFormat(e.target.value)}
                className="bg-slate-900 border border-slate-700 rounded-lg px-3 py-2.5 text-slate-100 font-bold"
              >
                <option value="PDF">PDF Report Document</option>
                <option value="HTML">HTML Interactive Report</option>
                <option value="CSV">CSV Data Export</option>
                <option value="JSON">JSON Data Structure</option>
              </select>
              <button
                type="submit"
                className="w-full sm:w-auto px-5 py-2.5 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-black rounded-lg transition-all uppercase tracking-wider shadow"
              >
                GENERATE & EXPORT
              </button>
            </form>
          </div>

          {/* Reports Table */}
          <div className="bg-[#0D131F] border border-slate-800 rounded-xl overflow-hidden shadow-lg">
            <table className="w-full text-left text-xs font-mono">
              <thead className="bg-[#0F172A] border-b border-slate-800 text-slate-400 uppercase tracking-wider">
                <tr>
                  <th className="px-4 py-3">Report Code</th>
                  <th className="px-4 py-3">Document Title</th>
                  <th className="px-4 py-3">Format</th>
                  <th className="px-4 py-3">Risk Index</th>
                  <th className="px-4 py-3">Security Score</th>
                  <th className="px-4 py-3">Generated At</th>
                  <th className="px-4 py-3 text-right">Download</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {reports.map((item) => (
                  <tr key={item.id} className="hover:bg-slate-800/40 transition-colors">
                    <td className="px-4 py-3 font-bold text-cyan-400">{item.report_code}</td>
                    <td className="px-4 py-3 font-bold text-slate-200">{item.title}</td>
                    <td className="px-4 py-3 font-bold">
                      <span className={`px-2 py-0.5 rounded text-[10px] ${
                        item.format === 'PDF' ? 'bg-red-500/10 text-red-400 border border-red-500/30' :
                        item.format === 'HTML' ? 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/30' :
                        item.format === 'CSV' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30' :
                        'bg-blue-500/10 text-blue-400 border border-blue-500/30'
                      }`}>
                        {item.format}
                      </span>
                    </td>
                    <td className="px-4 py-3 font-extrabold text-red-400">{item.risk_score} / 100</td>
                    <td className="px-4 py-3 font-extrabold text-emerald-400">{item.security_score} / 100</td>
                    <td className="px-4 py-3 text-slate-400">{new Date(item.created_at).toLocaleString()}</td>
                    <td className="px-4 py-3 text-right">
                      <button
                        onClick={() => handleDownload(item.id)}
                        className="inline-flex items-center gap-1 px-3 py-1 bg-slate-800 hover:bg-slate-700 text-cyan-400 border border-slate-700 rounded text-xs font-bold transition-all"
                      >
                        <Download className="w-3.5 h-3.5" /> Download
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ) : (
        /* Audit Trail Table */
        <div className="bg-[#0D131F] border border-slate-800 rounded-xl overflow-hidden shadow-lg">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-[#0F172A] border-b border-slate-800 text-slate-400 uppercase tracking-wider">
              <tr>
                <th className="px-4 py-3">Timestamp</th>
                <th className="px-4 py-3">User Email</th>
                <th className="px-4 py-3">Action Executed</th>
                <th className="px-4 py-3">Resource Target</th>
                <th className="px-4 py-3">Risk Impact</th>
                <th className="px-4 py-3">IP Address</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {logs.map((item) => (
                <tr key={item.id} className="hover:bg-slate-800/40 transition-colors">
                  <td className="px-4 py-3 text-slate-400">{new Date(item.timestamp).toLocaleString()}</td>
                  <td className="px-4 py-3 text-slate-200 font-bold">{item.user_email}</td>
                  <td className="px-4 py-3 text-cyan-400 font-bold">{item.action}</td>
                  <td className="px-4 py-3 text-slate-300">{item.resource}</td>
                  <td className="px-4 py-3 text-red-400 font-bold">{item.risk_score} / 100</td>
                  <td className="px-4 py-3 text-slate-400">{item.ip_address}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

