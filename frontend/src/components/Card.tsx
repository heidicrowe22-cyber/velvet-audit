import React from 'react';

interface CardProps {
  children: React.ReactNode;
  className?: string;
}

export const Card = ({ children, className = '' }: CardProps) => {
  return (
    <div className={`bg-white rounded-xl shadow-premium border border-gray-100 p-6 ${className}`}>
      {children}
    </div>
  );
};
