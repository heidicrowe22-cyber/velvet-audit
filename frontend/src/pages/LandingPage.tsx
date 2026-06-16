import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Zap, Shield, BarChart3 } from 'lucide-react';
import { audits } from '../api/client';

const LandingPage = () => {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!url) return;
    
    setLoading(true);
    try {
      const result = await audits.start({ website_url: url });
      navigate(`/audit/${result.id}`);
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Failed to start audit');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-velvet-primary min-h-screen">
      {/* Hero Section */}
      <header className="relative py-24 px-4 sm:px-6 lg:px-8 flex flex-col items-center justify-center text-center overflow-hidden">
        {/* Subtle velvet texture background could go here */}
        <div className="relative z-10 max-w-4xl mx-auto">
          <h1 className="font-display text-5xl md:text-7xl text-gold-accent mb-6 leading-tight">
            Agency-level insights for small businesses, <br className="hidden md:block" />
            <span className="italic">in an hour.</span>
          </h1>
          <p className="text-ghost text-xl md:text-2xl mb-12 opacity-90 max-w-2xl mx-auto font-sans">
            Get a comprehensive 17-category audit of your website. 
            Identify critical issues, estimate business impact, and get professional fixes.
          </p>

          <form onSubmit={handleSubmit} className="flex flex-col md:flex-row gap-4 w-full max-w-2xl mx-auto bg-white/10 p-2 rounded-xl backdrop-blur-sm border border-white/20">
            <input
              type="url"
              placeholder="Enter your website URL (e.g., https://yourbusiness.com)"
              className="flex-grow bg-white text-slate-deep px-6 py-4 rounded-lg text-lg focus:outline-none focus:ring-2 focus:ring-gold-accent"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              required
            />
            <button
              type="submit"
              disabled={loading}
              className="btn-cta text-lg py-4 px-8 whitespace-nowrap flex items-center justify-center gap-2 disabled:opacity-50"
            >
              <Search className="w-5 h-5" />
              {loading ? 'Scanning...' : 'Get Free Audit'}
            </button>
          </form>
          
          <p className="mt-6 text-ghost/60 text-sm italic">
            No credit card required. Full report in under 60 seconds.
          </p>
        </div>
      </header>

      {/* Features Section */}
      <section className="bg-ghost py-24 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="font-display text-4xl text-velvet-primary mb-4">Why Velvet Hour?</h2>
            <p className="text-slate-deep/60 text-xl max-w-2xl mx-auto">
              We've automated the expertise of a high-end digital agency to give you the results you need at a fraction of the cost.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
            {[
              {
                icon: <Zap className="w-10 h-10 text-gold" />,
                title: "17-Category Scan",
                description: "From SEO and speed to accessibility and lead generation. We leave no stone unturned."
              },
              {
                icon: <BarChart3 className="w-10 h-10 text-gold" />,
                title: "Business Impact",
                description: "We don't just find bugs; we tell you how much they're costing your business in real revenue."
              },
              {
                icon: <Shield className="w-10 h-10 text-gold" />,
                title: "Done-For-You Fixes",
                description: "Stop guessing. Buy a fix package and our experts will implement the changes for you."
              }
            ].map((feature, i) => (
              <div key={i} className="card flex flex-col items-center text-center">
                <div className="mb-6 p-4 bg-velvet-primary/5 rounded-full">
                  {feature.icon}
                </div>
                <h3 className="text-2xl mb-4 text-velvet-primary">{feature.title}</h3>
                <p className="text-slate-deep/70">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Social Proof Placeholder */}
      <section className="bg-white py-16 border-y border-ghost">
        <div className="max-w-7xl mx-auto px-4 flex flex-wrap justify-center items-center gap-8 md:gap-16 opacity-30 grayscale">
          {/* Logo placeholders */}
          <span className="font-display text-2xl">RealtyPro</span>
          <span className="font-display text-2xl">BoutiqueHub</span>
          <span className="font-display text-2xl">DineBetter</span>
          <span className="font-display text-2xl">ServiceFlow</span>
          <span className="font-display text-2xl">LocalPulse</span>
        </div>
      </section>
    </div>
  );
};

export default LandingPage;
