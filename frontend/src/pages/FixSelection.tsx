import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { ArrowLeft, CheckCircle2, Loader2, CreditCard } from 'lucide-react';
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
      <div className="min-h-screen flex items-center justify-center bg-ghost">
        <Loader2 className="w-12 h-12 text-velvet-primary animate-spin" />
      </div>
    );
  }

  return (
    <div className="bg-ghost min-h-screen pb-24">
      <div className="bg-velvet-primary py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto">
          <Link to={`/audit/${auditId}`} className="flex items-center gap-2 text-ghost/60 hover:text-gold-accent mb-4 transition-colors text-sm uppercase tracking-widest font-heading font-bold">
            <ArrowLeft className="w-4 h-4" /> Back to Report
          </Link>
          <h1 className="font-display text-4xl text-white mb-2">Select Your Fixes</h1>
          <p className="text-ghost/60">Choose the issues you want us to implement for you.</p>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 -mt-8">
        <div className="grid grid-cols-1 gap-8">
          {/* Fix Packages */}
          <div className="space-y-6">
            <h2 className="text-xl font-display text-velvet-primary mt-4">Available Packages</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {packages?.map((pkg: any) => (
                <div key={pkg.id} className="card flex flex-col hover:border-gold-accent border-2 border-transparent transition-all cursor-pointer group">
                   <h3 className="text-xl font-bold text-slate-deep mb-2">{pkg.name}</h3>
                   <p className="text-sm text-slate-deep/60 mb-6 flex-grow">{pkg.description}</p>
                   <div className="flex justify-between items-center mt-auto">
                      <span className="text-2xl font-display text-velvet-primary">${pkg.price}</span>
                      <button className="btn-primary py-2 px-4 text-sm">Select</button>
                   </div>
                </div>
              ))}
            </div>
          </div>

          {/* Individual Issues */}
          <div className="card">
             <h2 className="text-xl font-display text-velvet-primary mb-6">Individual Issues</h2>
             <div className="divide-y divide-ghost">
                {report?.issues?.map((issue: any, i: number) => (
                  <div key={i} className="py-4 flex justify-between items-center gap-4">
                     <div>
                        <p className="font-bold text-slate-deep">{issue.title}</p>
                        <p className="text-xs text-slate-deep/60">{issue.category}</p>
                     </div>
                     <div className="flex items-center gap-4">
                        <span className="text-sm font-bold text-velvet-primary">$29</span>
                        <input type="checkbox" className="w-5 h-5 rounded border-gray-300 text-velvet-primary focus:ring-velvet-500" />
                     </div>
                  </div>
                ))}
             </div>
          </div>

          {/* Checkout Summary */}
          <div className="card bg-slate-deep text-white border-none">
             <div className="flex flex-col md:flex-row justify-between items-center gap-8">
                <div>
                   <p className="text-xs font-heading font-bold uppercase tracking-widest text-white/40 mb-1">Total Implementation Cost</p>
                   <p className="text-4xl font-display text-gold-accent">$0.00</p>
                </div>
                <button className="w-full md:w-auto btn-cta py-4 px-12 text-lg flex items-center justify-center gap-3">
                   <CreditCard className="w-6 h-6" /> Proceed to Checkout
                </button>
             </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FixSelection;
