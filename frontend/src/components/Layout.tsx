import React from 'react';
import { Card, CardContent } from './ui/Card';

interface LayoutProps {
  children: React.ReactNode;
  title?: string;
  description?: string;
  centered?: boolean;
}

const Layout: React.FC<LayoutProps> = ({ children, title, description, centered = true }) => {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Main Content */}
      <main className="flex-grow flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div className="w-full max-w-md space-y-8">
          {(title || description) && (
            <div className="text-center">
              {title && (
                <h2 className="mt-6 text-3xl font-bold tracking-tight text-gray-900">
                  {title}
                </h2>
              )}
              {description && (
                <p className="mt-2 text-sm text-gray-600">
                  {description}
                </p>
              )}
            </div>
          )}
          <Card className="shadow-lg">
            <CardContent className="p-6">
              {children}
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
};

export default Layout;