import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { auth } from '../api/client';
import { Mail, Lock, Loader2 } from 'lucide-react';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const result = await auth.login({ email, password });
      localStorage.setItem('velvet_token', result.access_token);
      navigate('/dashboard');
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-ghost flex items-center justify-center p-4">
      <div className="card max-w-md w-full">
        <div className="text-center mb-8">
          <h1 className="font-display text-3xl text-velvet-primary mb-2">Welcome Back</h1>
          <p className="text-slate-deep/60">Sign in to manage your audits</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-xs font-heading font-bold uppercase tracking-widest text-slate-deep/40 mb-2">Email Address</label>
            <div className="relative">
              <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-deep/20" />
              <input
                type="email"
                className="input-field pl-10"
                placeholder="name@company.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-heading font-bold uppercase tracking-widest text-slate-deep/40 mb-2">Password</label>
            <div className="relative">
              <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-deep/20" />
              <input
                type="password"
                className="input-field pl-10"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full btn-primary py-4 flex items-center justify-center gap-2"
          >
            {loading && <Loader2 className="w-5 h-5 animate-spin" />}
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        <div className="mt-8 pt-8 border-t border-ghost text-center">
          <p className="text-sm text-slate-deep/60">
            Don't have an account? <Link to="/signup" className="text-velvet-primary font-bold hover:text-gold-accent transition-colors">Get started</Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
