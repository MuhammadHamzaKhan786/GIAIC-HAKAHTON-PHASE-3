import React from 'react';

interface ContainerProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  maxWidth?: 'sm' | 'md' | 'lg' | 'xl' | '2xl';
}

const Container = ({ children, maxWidth = '2xl', className = '', ...props }: ContainerProps) => {
  const maxWidthClass = {
    sm: 'max-w-screen-sm',
    md: 'max-w-screen-md',
    lg: 'max-w-screen-lg',
    xl: 'max-w-screen-xl',
    '2xl': 'max-w-screen-2xl',
  }[maxWidth];

  return (
    <div className={`mx-auto w-full ${maxWidthClass} ${className}`} {...props}>
      {children}
    </div>
  );
};

export default Container;