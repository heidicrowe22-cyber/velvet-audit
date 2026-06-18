import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
}

const Input = ({ label, className = '', ...props }: InputProps) => {
  return (
    <div className="space-y-3">
      {label && <label className="section-label block">{label}</label>}
      <input
        className={`input-field ${className}`}
        {...props}
      />
    </div>
  );
};

export default Input;
