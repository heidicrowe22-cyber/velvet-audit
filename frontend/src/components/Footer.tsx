const Footer = () => {
  return (
    <footer className="bg-slate-deep text-ghost py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <p className="font-display text-xl mb-4">Velvet Hour Audit</p>
        <p className="text-sm opacity-60">
          &copy; {new Date().getFullYear()} Velvet Hour Audit. Agency-level insights for small businesses.
        </p>
      </div>
    </footer>
  );
};

export default Footer;
