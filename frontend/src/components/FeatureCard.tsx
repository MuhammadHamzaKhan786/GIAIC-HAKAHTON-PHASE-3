import { ReactNode } from 'react';

interface FeatureCardProps {
  icon: ReactNode;
  title: string;
  description: string;
}

export default function FeatureCard({ icon, title, description }: FeatureCardProps) {
  return (
    <div className="bg-white rounded-2xl shadow-sm hover:shadow-md p-6 transition-all duration-300 hover:-translate-y-1 border border-gray-100 hover:border-indigo-200 group">
      <div className="flex flex-col items-center text-center">
        <div className="mb-4 group-hover:text-indigo-600 transition-colors">
          {icon}
        </div>
        <h3 className="text-xl font-semibold text-gray-900 mb-2">{title}</h3>
        <p className="text-gray-600">{description}</p>
      </div>
    </div>
  );
}