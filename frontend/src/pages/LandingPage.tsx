import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Zap, BarChart3, ShieldCheck } from 'lucide-react';
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
    <div className="bg-background min-h-screen">
      {/* Hero Section */}
      <section className="py-24 md:py-32 px-8 md:px-16">
        <div className="max-w-6xl mx-auto text-center">
          <div className="inline-block mb-8">
            <span className="section-label px-4 py-1 border border-blush/20 rounded-full">
              the velvet hour collective
            </span>
          </div>
          <h1 className="text-4xl md:text-6xl lg:text-7xl mb-8 leading-tight max-w-5xl mx-auto">
            agency-level insights for small businesses, <br className="hidden md:block" />
            <em className="italic">in an hour.</em>
          </h1>
          <p className="text-text-muted text-lg md:text-xl mb-12 max-w-2xl mx-auto font-light">
            get a comprehensive 17-category audit of your website. 
            identify critical issues, estimate business impact, and get professional fixes.
          </p>

          <form onSubmit={handleSubmit} className="flex flex-col md:flex-row gap-8 w-full max-w-3xl mx-auto items-end">
            <div className="flex-grow w-full text-left">
              <label className="section-label block mb-3">website url</label>
              <input
                type="url"
                placeholder="https://yourbusiness.com"
                className="input-field"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                required
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="btn-primary whitespace-nowrap min-w-[200px]"
            >
              {loading ? 'scanning...' : 'get free audit'}
            </button>
          </form>
          
          <p className="mt-12 text-text-muted/60 text-[0.7rem] uppercase tracking-widest italic">
            no credit card required. full report in under 60 seconds.
          </p>
        </div>
      </section>

      <div className="hairline mx-auto max-w-6xl"></div>

      {/* Features Section */}
      <section className="py-24 md:py-32 px-8 md:px-16 bg-blush-light/10">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-20">
            <h2 className="text-4xl md:text-5xl mb-6">
              why <em className="italic">velvet hour?</em>
            </h2>
            <p className="text-text-muted text-lg max-w-2xl mx-auto font-light">
              we've automated the expertise of a high-end digital agency to give you the results you need at a fraction of the cost.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
            {[
              {
                icon: <Zap className="w-8 h-8 text-gold" />,
                title: "17-category scan",
                description: "from seo and speed to accessibility and lead generation. we leave no stone unturned."
              },
              {
                icon: <BarChart3 className="w-8 h-8 text-gold" />,
                title: "business impact",
                description: "we don't just find bugs; we tell you how much they're costing your business in real revenue."
              },
              {
                icon: <ShieldCheck className="w-8 h-8 text-gold" />,
                title: "done-for-you fixes",
                description: "stop guessing. buy a fix package and our experts will implement the changes for you."
              }
            ].map((feature, i) => (
              <div key={i} className="card group">
                <div className="mb-8 opacity-60 group-hover:opacity-100 transition-opacity">
                  {feature.icon}
                </div>
                <h3 className="text-2xl mb-4 lowercase">{feature.title}</h3>
                <p className="text-text-muted font-light leading-relaxed">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <div className="hairline mx-auto max-w-6xl"></div>

      {/* Pricing/CTA Section */}
      <section className="py-24 md:py-32 px-8 md:px-16 bg-background">
        <div className="max-w-6xl mx-auto text-center">
          <div className="h-px w-10 mx-auto mb-8 bg-gold/40"></div>
          <h2 className="text-4xl md:text-5xl mb-12">professional fixes, <em className="italic">flat fee.</em></h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            {[
              { name: 'quick fix', price: '$29', desc: 'single issue repair' },
              { name: 'standard fix', price: '$79', desc: 'full category optimization', popular: true },
              { name: 'category fix', price: '$149', desc: 'three categories deep-dive' },
              { name: 'bundle fix', price: '$299', desc: 'total site transformation' }
            ].map((plan, i) => (
              <div key={i} className="card relative text-center flex flex-col items-center">
                {plan.popular && (
                  <span className="absolute -top-3 left-1/2 -translate-x-1/2 bg-blush text-white text-[0.6rem] px-3 py-1 uppercase tracking-widest">
                    most popular
                  </span>
                )}
                <h4 className="section-label mb-2">{plan.name}</h4>
                <div className="text-3xl font-display mb-4">{plan.price}</div>
                <p className="text-text-muted text-xs mb-8 uppercase tracking-widest">{plan.desc}</p>
                <div className="mt-auto w-full">
                  <button className="btn-secondary w-full">select plan</button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <div className="hairline mx-auto max-w-6xl"></div>

      {/* Contact Form Section */}
      <section className="py-24 md:py-32 px-8 md:px-16 bg-blush-light/5">
        <div className="max-w-3xl mx-auto text-center">
          <h2 className="text-4xl mb-12">questions? <em className="italic">write to us.</em></h2>
          <form className="space-y-12">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-12 text-left">
              <div className="space-y-3">
                <label className="section-label">your name</label>
                <input type="text" placeholder="full name" className="input-field" />
              </div>
              <div className="space-y-3">
                <label className="section-label">your email</label>
                <input type="email" placeholder="hello@example.com" className="input-field" />
              </div>
            </div>
            <div className="text-left space-y-3">
              <label className="section-label">message</label>
              <textarea placeholder="how can we help?" rows={1} className="input-field resize-none" />
            </div>
            <button type="button" className="btn-primary px-12">send message</button>
          </form>
          <div className="mt-16 text-text-muted text-sm font-light">
            or write directly — <a href="mailto:hello@velvethour.co" className="text-blush hover:underline">hello@velvethour.co</a>
          </div>
        </div>
      </section>
    </div>
  );
};

export default LandingPage;
