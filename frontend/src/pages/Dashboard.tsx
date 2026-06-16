import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { 
  BarChart, 
  Clock, 
  History, 
  Globe, 
  Settings, 
  LogOut,
  TrendingUp,
  AlertTriangle,
  CheckCircle,
  FileText,
  Loader2
} from 'lucide-react';
import { audits as auditApi } from '../api/client';
import { Link } from 'react-router-dom';

const Dashboard = () => {
  const { data: audits, isLoading, error } = useQuery({
    queryKey: ['audits'],
    queryFn: auditApi.list
  });

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-ghost">
        <Loader2 className="w-12 h-12 text-velvet-primary animate-spin" />
      </div>
    );
  }

  const latestAudit = audits && audits.length > 0 ? audits[0] : null;

  return (
    <div className="flex min-h-screen bg-ghost">
      {/* Sidebar */}
      <aside className="w-64 bg-slate-deep text-white hidden lg:flex flex-col">
        <div className="p-8">
          <h2 className="font-display text-2xl text-gold-accent">Velvet Hour</h2>
        </div>
        <nav className="flex-grow px-4 space-y-2">
          <Link to="/dashboard" className="flex items-center gap-3 px-4 py-3 bg-white/10 rounded-lg border-l-4 border-gold-accent">
            <BarChart className="w-5 h-5 text-gold-accent" />
            <span className="font-heading text-sm text-white">Overview</span>
          </Link>
          <a href="#" className="flex items-center gap-3 px-4 py-3 hover:bg-white/5 rounded-lg transition-colors">
            <History className="w-5 h-5 opacity-60" />
            <span className="font-heading text-sm text-white/80">Audit History</span>
          </a>
          <a href="#" className="flex items-center gap-3 px-4 py-3 hover:bg-white/5 rounded-lg transition-colors">
            <FileText className="w-5 h-5 opacity-60" />
            <span className="font-heading text-sm text-white/80">My Fixes</span>
          </a>
          <a href="#" className="flex items-center gap-3 px-4 py-3 hover:bg-white/5 rounded-lg transition-colors">
            <Settings className="w-5 h-5 opacity-60" />
            <span className="font-heading text-sm text-white/80">Settings</span>
          </a>
        </nav>
        <div className="p-8 border-t border-white/10">
          <button className="flex items-center gap-3 text-white/60 hover:text-white transition-colors">
            <LogOut className="w-5 h-5" />
            <span className="font-heading text-sm font-bold uppercase tracking-widest text-white/80">Logout</span>
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-grow p-8">
        <header className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-12">
          <div>
            <h1 className="font-display text-4xl text-velvet-primary mb-2">My Dashboard</h1>
            <p className="text-slate-deep/60">Manage your website audits and fix implementations.</p>
          </div>
          <Link to="/" className="btn-cta">Start New Audit</Link>
        </header>

        {error ? (
          <div className="bg-alert/10 border border-alert/20 p-6 rounded-xl text-alert mb-12">
            <p className="font-bold">Failed to load audits</p>
            <p className="text-sm">Please make sure you are logged in or try again later.</p>
          </div>
        ) : (
          <>
            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
              <div className="card">
                <div className="flex justify-between items-center mb-4">
                  <span className="text-sm font-heading font-bold uppercase tracking-wider text-slate-deep/40">Latest Score</span>
                  <div className="p-2 bg-success/10 rounded-lg text-success"><TrendingUp className="w-5 h-5" /></div>
                </div>
                <div className="flex items-end gap-2">
                  <span className="text-5xl font-display text-velvet-primary">{latestAudit?.score || '--'}</span>
                  {latestAudit && <span className="text-success text-sm font-bold mb-2">Stable</span>}
                </div>
                <p className="mt-4 text-xs text-slate-deep/60">Last scan: {latestAudit ? new Date(latestAudit.created_at).toLocaleDateString() : 'Never'}</p>
              </div>

              <div className="card">
                <div className="flex justify-between items-center mb-4">
                  <span className="text-sm font-heading font-bold uppercase tracking-wider text-slate-deep/40">Pending Fixes</span>
                  <div className="p-2 bg-yellow-500/10 rounded-lg text-yellow-600"><Clock className="w-5 h-5" /></div>
                </div>
                <div className="flex items-end gap-2">
                  <span className="text-5xl font-display text-velvet-primary">0</span>
                  <span className="text-slate-deep/40 text-sm font-bold mb-2">All up to date</span>
                </div>
                <p className="mt-4 text-xs text-slate-deep/60">No active fix orders</p>
              </div>

              <div className="card">
                <div className="flex justify-between items-center mb-4">
                  <span className="text-sm font-heading font-bold uppercase tracking-wider text-slate-deep/40">Websites</span>
                  <div className="p-2 bg-velvet-primary/10 rounded-lg text-velvet-primary"><Globe className="w-5 h-5" /></div>
                </div>
                <div className="flex items-end gap-2">
                  <span className="text-5xl font-display text-velvet-primary">{Array.from(new Set(audits?.map(a => a.website_url) || [])).length}</span>
                </div>
                <p className="mt-4 text-xs text-slate-deep/60">Active domains</p>
              </div>
            </div>

            {/* Audit History Table */}
            <section className="card p-0 overflow-hidden">
              <div className="p-6 border-b border-ghost">
                <h2 className="text-xl font-display text-velvet-primary">Audit History</h2>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-left">
                  <thead className="bg-ghost/50 text-[10px] font-heading font-bold uppercase tracking-widest text-slate-deep/40">
                    <tr>
                      <th className="px-6 py-4">Website</th>
                      <th className="px-6 py-4">Score</th>
                      <th className="px-6 py-4">Date</th>
                      <th className="px-6 py-4">Status</th>
                      <th className="px-6 py-4 text-right">Action</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-ghost text-sm">
                    {audits?.map((audit: any) => (
                      <tr key={audit.id} className="hover:bg-ghost transition-colors">
                        <td className="px-6 py-4">
                          <div className="flex items-center gap-2">
                            <Globe className="w-4 h-4 text-slate-deep/20" />
                            <span className="font-bold">{audit.website_url}</span>
                          </div>
                        </td>
                        <td className="px-6 py-4">
                          <div className={`font-bold ${audit.score >= 80 ? 'text-success' : audit.score >= 50 ? 'text-yellow-600' : 'text-alert'}`}>
                            {audit.score}/100
                          </div>
                        </td>
                        <td className="px-6 py-4 text-slate-deep/60">{new Date(audit.created_at).toLocaleDateString()}</td>
                        <td className="px-6 py-4">
                          <span className={`px-2 py-1 rounded text-[10px] font-bold uppercase ${
                            audit.status === 'completed' ? 'bg-success/10 text-success' : 'bg-slate-deep/5 text-slate-deep/40'
                          }`}>
                            {audit.status}
                          </span>
                        </td>
                        <td className="px-6 py-4 text-right">
                          <Link to={`/audit/${audit.id}`} className="text-velvet-primary font-bold hover:text-gold-accent transition-colors">View Report</Link>
                        </td>
                      </tr>
                    ))}
                    {(!audits || audits.length === 0) && (
                      <tr>
                        <td colSpan={5} className="px-6 py-12 text-center text-slate-deep/40 font-heading italic">
                          No audits found. Start your first audit to see results.
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </section>
          </>
        )}
      </main>
    </div>
  );
};

export default Dashboard;
