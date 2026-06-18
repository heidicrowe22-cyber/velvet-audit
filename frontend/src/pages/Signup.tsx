import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { auth } from '../api/client';
import { Loader2 } from 'lucide-react';

const Signup = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await auth.signup({ email, password, full_name: fullName });
      const loginResult = await auth.login({ email, password });
      localStorage.setItem('velvet_token', loginResult.access_token);
      navigate('/dashboard');
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Signup failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-8 font-sans">
      <div className="max-w-md w-full">
        <div className="text-center mb-16">
          <Link to="/" className="font-display text-3xl text-blush lowercase mb-8 inline-block">velvet hour</Link>
          <h1 className="text-4xl mb-4">create <em className="italic">account.</em></h1>
          <p className="text-text-muted font-light">start your free website audit today.</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-12">
          <div className="space-y-3">
            <label className="section-label">full name</label>
            <input
              type="text"
              className="input-field"
              placeholder="sarah johnson"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              required
            />
          </div>

          <div className="space-y-3">
            <label className="section-label">email address</label>
            <input
              type="email"
              className="input-field"
              placeholder="name@company.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="space-y-3">
            <label className="section-label">password</label>
            <input
              type="password"
              className="input-field"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full btn-primary py-4 flex items-center justify-center gap-3"
          >
            {loading && <Loader2 className="w-4 h-4 animate-spin" />}
            {loading ? 'creating account...' : 'get free audit'}
          </button>
        </form>

        <div className="mt-16 text-center">
          <p className="text-sm text-text-muted font-light">
            already have an account? <Link to="/login" className="text-blush hover:underline">sign in</Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Signup;
