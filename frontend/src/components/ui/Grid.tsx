import React from 'react';

interface GridProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  cols?: {
    sm?: number;
    md?: number;
    lg?: number;
    xl?: number;
  };
  gap?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
}

const Grid = ({ children, cols = {}, gap = 'md', className = '', ...props }: GridProps) => {
  const gapClass = {
    xs: 'gap-2',
    sm: 'gap-3',
    md: 'gap-4',
    lg: 'gap-6',
    xl: 'gap-8',
  }[gap];

  // Construct grid template columns based on breakpoints
  let gridClass = 'grid ';

  if (cols.sm) gridClass += `grid-cols-${cols.sm} `;
  if (cols.md) gridClass += `md:grid-cols-${cols.md} `;
  if (cols.lg) gridClass += `lg:grid-cols-${cols.lg} `;
  if (cols.xl) gridClass += `xl:grid-cols-${cols.xl} `;

  gridClass += gapClass;

  return (
    <div className={`${gridClass} ${className}`} {...props}>
      {children}
    </div>
  );
};

export default Grid;