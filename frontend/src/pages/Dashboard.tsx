import { useQuery } from '@tanstack/react-query';
import { 
  BarChart, 
  History, 
  Settings, 
  LogOut,
  FileText,
  Loader2,
  ArrowRight
} from 'lucide-react';
import { audits as auditApi } from '../api/client';
import { Link, useNavigate } from 'react-router-dom';

const Dashboard = () => {
  const navigate = useNavigate();
  const { data: audits, isLoading, error } = useQuery({
    queryKey: ['audits'],
    queryFn: auditApi.list
  });

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <Loader2 className="w-8 h-8 text-blush animate-spin" />
      </div>
    );
  }

  const latestAudit = audits && audits.length > 0 ? audits[0] : null;

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <div className="flex min-h-screen bg-background">
      {/* Sidebar */}
      <aside className="w-72 border-r border-border hidden lg:flex flex-col">
        <div className="p-12">
          <Link to="/" className="font-display text-2xl text-blush lowercase">velvet hour</Link>
        </div>
        <nav className="flex-grow px-8 space-y-4">
          <Link to="/dashboard" className="text-[0.7rem] uppercase tracking-widest transition-colors flex items-center gap-3 text-blush">
            <BarChart className="w-4 h-4" />
            <span>overview</span>
          </Link>
          <a href="#" className="text-[0.7rem] uppercase tracking-widest transition-colors flex items-center gap-3 text-text-muted opacity-60 hover:opacity-100">
            <History className="w-4 h-4" />
            <span>audit history</span>
          </a>
          <a href="#" className="text-[0.7rem] uppercase tracking-widest transition-colors flex items-center gap-3 text-text-muted opacity-60 hover:opacity-100">
            <FileText className="w-4 h-4" />
            <span>my fixes</span>
          </a>
          <a href="#" className="text-[0.7rem] uppercase tracking-widest transition-colors flex items-center gap-3 text-text-muted opacity-60 hover:opacity-100">
            <Settings className="w-4 h-4" />
            <span>settings</span>
          </a>
        </nav>
        <div className="p-12">
          <button 
            onClick={handleLogout}
            className="text-[0.7rem] uppercase tracking-widest transition-colors flex items-center gap-3 text-text-muted opacity-40 hover:opacity-100 hover:text-alert"
          >
            <LogOut className="w-4 h-4" />
            <span>logout</span>
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-grow p-12 md:p-16 lg:p-24 overflow-y-auto font-sans">
        <header className="flex flex-col md:flex-row justify-between items-start md:items-end gap-8 mb-20">
          <div>
            <h1 className="text-4xl md:text-5xl mb-4 font-normal">my <em className="italic">dashboard.</em></h1>
            <p className="text-text-muted font-light">manage your website audits and fix implementations.</p>
          </div>
          <Link to="/" className="btn-primary">start new audit</Link>
        </header>

        <div className="hairline mb-20"></div>

        {error ? (
          <div className="bg-alert/5 border border-alert/20 p-8 text-alert mb-20">
            <p className="section-label mb-2">error loading data</p>
            <p className="text-sm font-light">please make sure you are logged in or try again later.</p>
          </div>
        ) : (
          <>
            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-16 mb-32">
              <div className="space-y-6">
                <span className="section-label">latest score</span>
                <div className="flex items-baseline gap-4">
                  <span className="text-6xl font-display text-blush">{latestAudit?.score || '--'}</span>
                  <span className="text-success text-[0.6rem] uppercase tracking-widest font-bold">stable</span>
                </div>
                <div className="h-px w-10 bg-gold/40"></div>
                <p className="text-text-muted text-[0.65rem] uppercase tracking-widest font-light">last scan: {latestAudit ? new Date(latestAudit.created_at).toLocaleDateString() : 'never'}</p>
              </div>

              <div className="space-y-6">
                <span className="section-label">pending fixes</span>
                <div className="flex items-baseline gap-4">
                  <span className="text-6xl font-display text-text-primary">0</span>
                  <span className="text-text-muted text-[0.6rem] uppercase tracking-widest font-bold">optimized</span>
                </div>
                <div className="h-px w-10 bg-gold/40"></div>
                <p className="text-text-muted text-[0.65rem] uppercase tracking-widest font-light">no active fix orders</p>
              </div>

              <div className="space-y-6">
                <span className="section-label">active domains</span>
                <div className="flex items-baseline gap-4">
                  <span className="text-6xl font-display text-text-primary">{Array.from(new Set(audits?.map(a => a.website_url) || [])).length}</span>
                </div>
                <div className="h-px w-10 bg-gold/40"></div>
                <p className="text-text-muted text-[0.65rem] uppercase tracking-widest font-light">monitored websites</p>
              </div>
            </div>

            {/* Audit History */}
            <section className="space-y-12">
              <div className="flex items-center gap-4">
                <h2 className="text-3xl font-normal">audit <em className="italic">history.</em></h2>
                <div className="hairline flex-grow"></div>
              </div>
              
              <div className="overflow-x-auto">
                <table className="w-full text-left">
                  <thead>
                    <tr className="border-b border-border">
                      <th className="section-label pb-6">website</th>
                      <th className="section-label pb-6">score</th>
                      <th className="section-label pb-6">date</th>
                      <th className="section-label pb-6">status</th>
                      <th className="section-label pb-6 text-right">report</th>
                    </tr>
                  </thead>
                  <tbody className="font-light">
                    {audits?.map((audit: any) => (
                      <tr key={audit.id} className="border-b border-border/40 group">
                        <td className="py-8 font-normal text-text-primary">{audit.website_url}</td>
                        <td className="py-8">
                          <span className={`font-bold ${audit.score >= 80 ? 'text-success' : audit.score >= 50 ? 'text-gold' : 'text-alert'}`}>
                            {audit.score}%
                          </span>
                        </td>
                        <td className="py-8 text-text-muted">{new Date(audit.created_at).toLocaleDateString()}</td>
                        <td className="py-8">
                          <span className={`text-[0.6rem] uppercase tracking-widest px-2 py-1 ${
                            audit.status === 'completed' ? 'bg-success/10 text-success' : 'bg-border text-text-muted'
                          }`}>
                            {audit.status}
                          </span>
                        </td>
                        <td className="py-8 text-right">
                          <Link to={`/audit/${audit.id}`} className="text-blush hover:text-blush-dark transition-colors inline-flex items-center gap-2 text-sm">
                            view <ArrowRight className="w-3 h-3" />
                          </Link>
                        </td>
                      </tr>
                    ))}
                    {(!audits || audits.length === 0) && (
                      <tr>
                        <td colSpan={5} className="py-24 text-center text-text-muted italic font-light">
                          no audits found. start your first audit to see results.
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
