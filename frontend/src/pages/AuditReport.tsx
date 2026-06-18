import { useParams, useSearchParams, Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { 
  CheckCircle2, 
  AlertCircle, 
  ChevronRight, 
  ArrowLeft,
  Smartphone,
  Zap,
  Search,
  MapPin,
  Accessibility,
  Layout,
  Menu,
  MousePointer2,
  Phone,
  ShieldCheck,
  Star,
  FileText,
  Image as ImageIcon,
  Lock,
  Terminal,
  UserPlus,
  Loader2
} from 'lucide-react';
import { audits as auditApi, reports as reportApi } from '../api/client';

const categoryIcons: Record<string, React.ReactNode> = {
  'Mobile Responsiveness': <Smartphone className="w-5 h-5" />,
  'Page Speed': <Zap className="w-5 h-5" />,
  'SEO Fundamentals': <Search className="w-5 h-5" />,
  'Local SEO': <MapPin className="w-5 h-5" />,
  'Accessibility': <Accessibility className="w-5 h-5" />,
  'User Experience': <Layout className="w-5 h-5" />,
  'Navigation': <Menu className="w-5 h-5" />,
  'Conversion Optimization': <MousePointer2 className="w-5 h-5" />,
  'Calls to Action': <CheckCircle2 className="w-5 h-5" />,
  'Contact Visibility': <Phone className="w-5 h-5" />,
  'Trust Signals': <ShieldCheck className="w-5 h-5" />,
  'Reviews & Reputation': <Star className="w-5 h-5" />,
  'Content Quality': <FileText className="w-5 h-5" />,
  'Image Optimization': <ImageIcon className="w-5 h-5" />,
  'Security Basics': <Lock className="w-5 h-5" />,
  'Technical Issues': <Terminal className="w-5 h-5" />,
  'Lead Generation': <UserPlus className="w-5 h-5" />,
};

const SeverityTag = ({ severity }: { severity: string }) => {
  const styles: Record<string, string> = {
    critical: 'bg-alert text-white',
    high: 'bg-blush text-white',
    medium: 'bg-gold/20 text-text-primary',
    low: 'bg-text-muted/20 text-text-muted',
    info: 'bg-border text-text-muted',
  };

  const labels: Record<string, string> = {
    critical: 'Urgent — fix now',
    high: 'Important — impacts revenue',
    medium: 'Should fix',
    low: 'Nice to have',
    info: 'FYI',
  };

  return (
    <span className={`text-[0.6rem] uppercase tracking-widest px-3 py-1 font-bold ${styles[severity] || styles.info}`}>
      {labels[severity] || severity}
    </span>
  );
};

const AuditReport = () => {
  const { auditId } = useParams();
  const [searchParams] = useSearchParams();
  const urlParam = searchParams.get('url');
  
  const { data: audit, isLoading: isLoadingAudit } = useQuery({
    queryKey: ['audit', auditId],
    queryFn: () => auditApi.get(auditId!),
    enabled: !!auditId,
    refetchInterval: (query) => {
      const data = query.state.data as any;
      return data?.status === 'pending' || data?.status === 'running' ? 2000 : false;
    }
  });

  const { data: report, isLoading: isLoadingReport } = useQuery({
    queryKey: ['report', auditId],
    queryFn: () => reportApi.get(auditId!),
    enabled: audit?.status === 'completed'
  });

  if (isLoadingAudit || (audit?.status !== 'completed' && audit?.status !== 'failed')) {
    return (
      <div className="min-h-screen bg-background flex flex-col items-center justify-center p-8 text-center">
        <div className="max-w-md w-full">
          <div className="mb-12">
            <span className="section-label px-4 py-1 border border-blush/20 rounded-full">
              scanning engine active
            </span>
          </div>
          <h2 className="text-4xl md:text-5xl mb-8">scanning <em className="italic">{audit?.website_url || urlParam}</em></h2>
          <div className="w-full bg-border h-px mb-8 overflow-hidden">
            <div 
              className="bg-gold h-full transition-all duration-1000 ease-out animate-pulse"
              style={{ width: audit?.status === 'running' ? '66%' : '33%' }}
            ></div>
          </div>
          <p className="text-text-muted text-xs uppercase tracking-widest italic font-light">
            {audit?.status === 'running' ? 'almost there. finalizing results...' : 'connecting to site and initializing 17-category scan...'}
          </p>
        </div>
      </div>
    );
  }

  if (audit?.status === 'failed') {
     return (
        <div className="min-h-screen bg-background flex flex-col items-center justify-center p-8 text-center">
           <AlertCircle className="w-12 h-12 text-alert mb-6" />
           <h2 className="text-4xl mb-4">audit <em className="italic">failed.</em></h2>
           <p className="text-text-muted mb-12 max-w-md font-light">we encountered an error while scanning {audit.website_url}. this can happen if the site blocks bots or is temporarily down.</p>
           <Link to="/" className="btn-primary">try another website</Link>
        </div>
     );
  }

  return (
    <div className="bg-background min-h-screen pb-32">
      {/* Report Header */}
      <div className="bg-blush-light/10 py-16 px-8 md:px-16 border-b border-border">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row justify-between items-center gap-12">
          <div className="text-center md:text-left">
            <Link to="/dashboard" className="nav-link flex items-center gap-2 mb-6">
              <ArrowLeft className="w-3 h-3" /> back to dashboard
            </Link>
            <h1 className="text-4xl md:text-5xl mb-4">
              audit report for <em className="italic">{audit.website_url}</em>
            </h1>
            <p className="text-text-muted text-xs uppercase tracking-widest font-light">
              audit id: {auditId} • generated on {new Date(audit.created_at).toLocaleDateString()}
            </p>
          </div>
          
          <div className="flex flex-col items-center">
            <div className="text-[0.6rem] uppercase tracking-widest text-text-muted mb-2">velvet score</div>
            <div className="relative w-40 h-40 flex items-center justify-center rounded-full border-2 border-gold/40">
              <span className="text-blush text-6xl font-display">{audit.score}</span>
              <div className="absolute -bottom-3 bg-background px-4 text-[0.6rem] uppercase tracking-widest text-text-muted">/ 100</div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-8 md:px-16 mt-20">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-16">
          
          {/* Main Categories */}
          <div className="lg:col-span-2 space-y-12">
            <div className="flex items-center gap-4">
               <h2 className="text-3xl">audit <em className="italic">results.</em></h2>
               <div className="hairline flex-grow"></div>
            </div>

            {isLoadingReport ? (
               <div className="py-20 text-center">
                  <Loader2 className="w-8 h-8 text-blush animate-spin mx-auto" />
               </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {report?.categories?.map((cat: any) => (
                  <div key={cat.name} className="card group cursor-pointer flex flex-col p-8 md:p-10">
                    <div className="flex justify-between items-start mb-8">
                      <div className="text-text-muted group-hover:text-blush transition-colors">
                        {categoryIcons[cat.name] || <CheckCircle2 className="w-5 h-5" />}
                      </div>
                      <div className={`text-xs font-bold px-3 py-1 ${
                        cat.score >= 90 ? 'bg-success/10 text-success' : 
                        cat.score >= 70 ? 'bg-gold/10 text-gold' : 'bg-alert/10 text-alert'
                      }`}>
                        {cat.score}%
                      </div>
                    </div>
                    <h3 className="text-xl mb-4 lowercase">{cat.name}</h3>
                    <div className="mt-auto flex items-center gap-2">
                      <span className={`text-[0.65rem] uppercase tracking-widest flex items-center gap-2 font-medium ${cat.issue_count === 0 ? 'text-success' : 'text-alert'}`}>
                        {cat.issue_count === 0 ? 'no critical issues' : `${cat.issue_count} issues found`}
                      </span>
                      <ChevronRight className="w-3 h-3 ml-auto text-border group-hover:text-gold transition-colors" />
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Side Bar: Fix Selection & Business Impact */}
          <div className="space-y-12">
             <div className="sticky top-32">
                <div className="flex items-center gap-4 mb-8">
                  <h2 className="text-3xl">actionable <em className="italic">fixes.</em></h2>
                </div>
                
                {report?.top_fixes?.length > 0 ? (
                  <div className="space-y-8 mb-12">
                    {report.top_fixes.map((fix: any, i: number) => (
                      <div key={i} className="space-y-4">
                        <SeverityTag severity={fix.severity} />
                        <h4 className="text-lg lowercase">{fix.title}</h4>
                        <p className="text-text-muted text-sm font-light leading-relaxed">{fix.impact_description}</p>
                        <button className="btn-secondary w-full py-2">add to fixes — ${fix.price || 29}</button>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="py-12 text-center text-text-muted/40 italic text-sm font-light">
                    {isLoadingReport ? 'loading fixes...' : 'no urgent fixes recommended at this time.'}
                  </div>
                )}
                
                <div className="pt-8 border-t border-border">
                  <div className="flex justify-between items-center mb-8">
                    <span className="section-label">total selected</span>
                    <span className="text-3xl font-display text-blush">$0</span>
                  </div>
                  <button className="w-full btn-primary py-4 text-sm opacity-50 cursor-not-allowed">
                    purchase & fix all
                  </button>
                  <p className="mt-6 text-[0.6rem] text-center text-text-muted uppercase tracking-[0.3em] font-light">
                    100% satisfaction guaranteed
                  </p>
                </div>
             </div>
          </div>

        </div>
      </div>
    </div>
  );
};

export default AuditReport;
