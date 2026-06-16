import React from 'react';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'cta' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
}

export const Button = ({ 
  className, 
  variant = 'primary', 
  size = 'md', 
  loading, 
  children, 
  ...props 
}: ButtonProps) => {
  const variants = {
    primary: 'btn-primary',
    secondary: 'btn-secondary',
    cta: 'btn-cta',
    ghost: 'hover:bg-ghost transition-colors text-slate-deep'
  };

  const sizes = {
    sm: 'px-4 py-2 text-sm',
    md: 'px-6 py-3 text-base',
    lg: 'px-8 py-4 text-lg'
  };

  return (
    <button
      className={cn(variants[variant], sizes[size], className)}
      disabled={loading || props.disabled}
      {...props}
    >
      {loading ? 'Loading...' : children}
    </button>
  );
};
