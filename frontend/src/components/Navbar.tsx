import { Link, useLocation } from 'react-router-dom';

const Navbar = () => {
  const location = useLocation();

  const navLinkClass = (path: string) => {
    const isActive = location.pathname === path;
    return `text-[0.7rem] uppercase tracking-[0.25em] transition-colors pb-1 ${
      isActive ? 'text-blush border-b border-gold' : 'text-text-muted hover:text-blush'
    }`;
  };

  return (
    <nav className="bg-background border-b border-border/60 sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-8 md:px-16">
        <div className="flex justify-between h-20 items-center">
          <div className="flex-shrink-0">
            <Link to="/" className="font-display text-2xl md:text-3xl text-blush tracking-tight lowercase">
              velvet hour audit
            </Link>
          </div>
          <div className="hidden md:block">
            <div className="ml-10 flex items-center space-x-8">
              <Link to="/dashboard" className={navLinkClass('/dashboard')}>dashboard</Link>
              <Link to="/login" className={navLinkClass('/login')}>login</Link>
              <Link to="/signup" className="btn-primary">get free audit</Link>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
