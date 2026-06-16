import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav className="bg-velvet-primary text-white shadow-premium">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          <div className="flex-shrink-0">
            <Link to="/" className="font-display text-2xl font-bold tracking-tight text-gold-accent">
              Velvet Hour <span className="text-white">Audit</span>
            </Link>
          </div>
          <div className="hidden md:block">
            <div className="ml-10 flex items-baseline space-x-4 font-heading">
              <Link to="/dashboard" className="px-3 py-2 rounded-md text-sm font-medium hover:text-gold-accent transition-colors">Dashboard</Link>
              <Link to="/login" className="px-3 py-2 rounded-md text-sm font-medium hover:text-gold-accent transition-colors">Login</Link>
              <Link to="/signup" className="btn-cta text-sm py-2">Get Free Audit</Link>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
