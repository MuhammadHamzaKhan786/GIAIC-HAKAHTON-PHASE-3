'use client';

import React, { createContext, useContext, ReactNode } from 'react';

interface ThemeContextType {
  theme: 'light';
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export const ThemeProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  // We're using a consistent light theme throughout the app
  const theme: 'light' = 'light';

  return (
    <ThemeContext.Provider value={{ theme }}>
      <div className="bg-gray-50 min-h-screen">
        {children}
      </div>
    </ThemeContext.Provider>
  );
};

export const useTheme = (): ThemeContextType => {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};