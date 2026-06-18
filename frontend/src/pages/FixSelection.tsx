import { useParams, Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { ArrowLeft, Loader2, CreditCard } from 'lucide-react';
import { reports as reportApi, fixes as fixApi } from '../api/client';

const FixSelection = () => {
  const { auditId } = useParams();

  const { data: report, isLoading: isLoadingReport } = useQuery({
    queryKey: ['report', auditId],
    queryFn: () => reportApi.get(auditId!),
    enabled: !!auditId
  });

  const { data: packages, isLoading: isLoadingPackages } = useQuery({
    queryKey: ['fix-packages'],
    queryFn: fixApi.listPackages
  });

  if (isLoadingReport || isLoadingPackages) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <Loader2 className="w-8 h-8 text-blush animate-spin" />
      </div>
    );
  }

  return (
    <div className="bg-background min-h-screen pb-32 font-sans">
      <div className="bg-blush-light/10 py-16 px-8 md:px-16 border-b border-border">
        <div className="max-w-6xl mx-auto">
          <Link to={`/audit/${auditId}`} className="nav-link flex items-center gap-2 mb-6">
            <ArrowLeft className="w-3 h-3" /> back to report
          </Link>
          <h1 className="text-4xl md:text-5xl mb-4">select your <em className="italic">fixes.</em></h1>
          <p className="text-text-muted font-light uppercase text-xs tracking-widest">choose the issues you want us to implement for you.</p>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-8 md:px-16 mt-20">
        <div className="grid grid-cols-1 gap-20">
          {/* Fix Packages */}
          <div className="space-y-12">
            <div className="flex items-center gap-4">
              <h2 className="text-3xl font-normal">available <em className="italic">packages.</em></h2>
              <div className="hairline flex-grow"></div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              {packages?.map((pkg: any) => (
                <div key={pkg.id} className="card group flex flex-col p-10 md:p-12 transition-all cursor-pointer">
                   <h3 className="text-xl mb-4 lowercase">{pkg.name}</h3>
                   <p className="text-text-muted text-sm font-light mb-12 flex-grow leading-relaxed">{pkg.description}</p>
                   <div className="flex justify-between items-center mt-auto border-t border-border/40 pt-8">
                      <span className="text-3xl font-display text-blush">${pkg.price}</span>
                      <button className="btn-secondary">select</button>
                   </div>
                </div>
              ))}
            </div>
          </div>

          {/* Individual Issues */}
          <div className="space-y-12">
             <div className="flex items-center gap-4">
               <h2 className="text-3xl font-normal">individual <em className="italic">issues.</em></h2>
               <div className="hairline flex-grow"></div>
             </div>
             <div className="space-y-4">
                {report?.issues?.map((issue: any, i: number) => (
                  <div key={i} className="card flex justify-between items-center gap-8 p-8">
                     <div>
                        <p className="text-lg lowercase mb-1">{issue.title}</p>
                        <p className="section-label">{issue.category}</p>
                     </div>
                     <div className="flex items-center gap-8">
                        <span className="text-xl font-display text-text-primary">$29</span>
                        <input type="checkbox" className="w-5 h-5 border-gold/30 rounded-none text-blush focus:ring-blush" />
                     </div>
                  </div>
                ))}
             </div>
          </div>

          {/* Checkout Summary */}
          <div className="bg-blush text-white p-12 md:p-16">
             <div className="flex flex-col md:flex-row justify-between items-center gap-12">
                <div>
                   <p className="text-[0.6rem] uppercase tracking-widest text-white/60 mb-2">total implementation cost</p>
                   <p className="text-5xl font-display">$0.00</p>
                </div>
                <button className="w-full md:w-auto bg-white text-blush px-12 py-5 text-[0.7rem] uppercase tracking-widest hover:bg-blush-light transition-colors flex items-center justify-center gap-3">
                   <CreditCard className="w-4 h-4" /> proceed to checkout
                </button>
             </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FixSelection;
