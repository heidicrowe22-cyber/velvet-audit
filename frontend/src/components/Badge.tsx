import React from 'react';

interface BadgeProps {
  children: React.ReactNode;
  variant?: 'good' | 'needs-work' | 'critical' | 'info';
  className?: string;
}

export const Badge = ({ children, variant = 'info', className = '' }: BadgeProps) => {
  const styles = {
    good: 'bg-success/10 text-success',
    'needs-work': 'bg-gold/10 text-gold',
    critical: 'bg-alert/10 text-alert',
    info: 'bg-border text-text-muted',
  };

  return (
    <span className={`text-[0.65rem] font-bold px-3 py-1 uppercase tracking-widest ${styles[variant]} ${className}`}>
      {children}
    </span>
  );
};

export default Badge;
