import React, { useState, useEffect } from 'react';
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

const AuditReport = () => {
  const { auditId } = useParams();
  const [searchParams] = useSearchParams();
  const urlParam = searchParams.get('url');
  
  const { data: audit, isLoading: isLoadingAudit, refetch: refetchStatus } = useQuery({
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
    const progress = audit?.status === 'running' ? 50 : 10;
    return (
      <div className="min-h-screen bg-velvet-primary flex flex-col items-center justify-center p-4 text-center">
        <div className="max-w-md w-full">
          <Loader2 className="w-12 h-12 text-gold-accent animate-spin mx-auto mb-8" />
          <h2 className="font-display text-4xl text-gold-accent mb-8">Scanning {audit?.website_url || urlParam}...</h2>
          <div className="w-full bg-white/10 rounded-full h-4 mb-4 overflow-hidden border border-white/20">
            <div 
              className={`bg-gold-accent h-full transition-all duration-1000 ease-out ${audit?.status === 'running' ? 'w-2/3' : 'w-1/4'}`}
            ></div>
          </div>
          <p className="text-ghost opacity-60 font-sans italic">
            {audit?.status === 'running' ? 'Almost there! Finalizing results...' : 'Connecting to site and initializing 17-category scan...'}
          </p>
        </div>
      </div>
    );
  }

  if (audit?.status === 'failed') {
     return (
        <div className="min-h-screen bg-ghost flex flex-col items-center justify-center p-4 text-center">
           <AlertCircle className="w-16 h-16 text-alert mb-4" />
           <h2 className="text-2xl font-display text-velvet-primary mb-2">Audit Failed</h2>
           <p className="text-slate-deep/60 mb-8 max-w-md">We encountered an error while scanning {audit.website_url}. This can happen if the site blocks bots or is temporarily down.</p>
           <Link to="/" className="btn-primary">Try Another Website</Link>
        </div>
     );
  }

  return (
    <div className="bg-ghost min-h-screen pb-24">
      {/* Report Header */}
      <div className="bg-velvet-primary py-12 px-4 sm:px-6 lg:px-8 shadow-premium">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-8">
          <div>
            <Link to="/dashboard" className="flex items-center gap-2 text-ghost/60 hover:text-gold-accent mb-4 transition-colors text-sm uppercase tracking-widest font-heading font-bold">
              <ArrowLeft className="w-4 h-4" /> Back to Dashboard
            </Link>
            <h1 className="font-display text-4xl md:text-5xl text-white mb-2">
              Audit Report for <span className="text-gold-accent italic font-normal">{audit.website_url}</span>
            </h1>
            <p className="text-ghost/60 font-sans">Audit ID: {auditId} • Generated on {new Date(audit.created_at).toLocaleDateString()}</p>
          </div>
          
          <div className="relative group">
            <div className="absolute -inset-1 bg-gold-accent rounded-full opacity-20 blur group-hover:opacity-40 transition-opacity"></div>
            <div className="relative bg-white rounded-full w-40 h-40 flex flex-col items-center justify-center border-4 border-gold-accent shadow-premium">
              <span className="text-slate-deep text-xs font-heading font-bold uppercase tracking-wider mb-1">Velvet Score</span>
              <span className="text-velvet-primary text-5xl font-display font-bold">{audit.score}</span>
              <span className="text-slate-deep/40 text-xs font-heading font-bold uppercase mt-1">/ 100</span>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 -mt-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Main Categories */}
          <div className="lg:col-span-2 space-y-6">
            <h2 className="text-2xl font-display text-velvet-primary mt-4">Audit Results</h2>
            {isLoadingReport ? (
               <div className="card flex items-center justify-center py-20">
                  <Loader2 className="w-8 h-8 text-velvet-primary animate-spin" />
               </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {report?.categories?.map((cat: any) => (
                  <div key={cat.name} className="card hover:border-gold-accent border border-transparent transition-all cursor-pointer group">
                    <div className="flex justify-between items-start mb-4">
                      <div className="p-2 bg-velvet-primary/5 rounded-lg text-velvet-primary group-hover:bg-gold-accent/10 group-hover:text-gold-accent transition-colors">
                        {categoryIcons[cat.name] || <CheckCircle2 className="w-5 h-5" />}
                      </div>
                      <div className={`px-3 py-1 rounded-full text-xs font-bold ${
                        cat.score >= 90 ? 'bg-success/10 text-success' : 
                        cat.score >= 70 ? 'bg-yellow-500/10 text-yellow-600' : 'bg-alert/10 text-alert'
                      }`}>
                        {cat.score}/100
                      </div>
                    </div>
                    <h3 className="font-heading font-bold text-slate-deep mb-2">{cat.name}</h3>
                    <div className="flex items-center gap-2">
                      <span className={`text-xs flex items-center gap-1 font-medium ${cat.issue_count === 0 ? 'text-success' : 'text-alert'}`}>
                        {cat.issue_count === 0 ? <CheckCircle2 className="w-3 h-3" /> : <AlertCircle className="w-3 h-3" />}
                        {cat.issue_count === 0 ? 'No critical issues' : `${cat.issue_count} issues found`}
                      </span>
                      <ChevronRight className="w-4 h-4 ml-auto text-slate-deep/20 group-hover:text-gold-accent transition-colors" />
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Side Bar: Fix Selection & Business Impact */}
          <div className="space-y-6">
             <div className="card sticky top-24">
                <h2 className="text-xl font-display text-velvet-primary mb-6">Actionable Fixes</h2>
                
                {report?.top_fixes?.length > 0 ? (
                  <div className="space-y-4 mb-8">
                    {report.top_fixes.map((fix: any, i: number) => (
                      <div key={i} className={`p-4 rounded-lg border ${fix.severity === 'critical' ? 'bg-alert/5 border-alert/10' : 'bg-yellow-500/5 border-yellow-500/10'}`}>
                        <div className={`flex items-center gap-2 mb-2 font-bold text-xs uppercase tracking-wider ${fix.severity === 'critical' ? 'text-alert' : 'text-yellow-600'}`}>
                          <AlertCircle className="w-4 h-4" /> {fix.severity === 'critical' ? 'Urgent — Fix Now' : 'Important — Revenue Impact'}
                        </div>
                        <p className="text-sm font-bold text-slate-deep mb-1">{fix.title}</p>
                        <p className="text-xs text-slate-deep/60 mb-3">{fix.impact_description}</p>
                        <button className="w-full btn-cta py-2 text-sm">Add to Fixes — ${fix.price || 29}</button>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="py-8 text-center text-slate-deep/40 italic text-sm">
                    {isLoadingReport ? 'Loading fixes...' : 'No urgent fixes recommended at this time.'}
                  </div>
                )}
                
                <div className="pt-6 border-t border-ghost">
                  <div className="flex justify-between items-center mb-6">
                    <span className="font-heading font-bold text-slate-deep uppercase text-xs tracking-wider">Total Selected</span>
                    <span className="text-2xl font-display text-velvet-primary">$0</span>
                  </div>
                  <button className="w-full btn-cta py-4 text-lg opacity-50 cursor-not-allowed">
                    Purchase & Fix All
                  </button>
                  <p className="mt-4 text-[10px] text-center text-slate-deep/40 uppercase tracking-widest font-bold">
                    100% Satisfaction Guaranteed
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
