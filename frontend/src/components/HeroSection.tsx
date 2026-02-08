'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';

export default function HeroSection() {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    // Trigger entrance animation after component mounts
    setIsVisible(true);
  }, []);

  return (
    <section className={`flex flex-col items-center justify-center text-center py-16 transition-all duration-500 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-4'}`}>
      <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-4">
        Todo CLI
      </h1>
      <p className="text-xl md:text-2xl text-gray-600 mb-6">
        CLI-Based Task Management
      </p>
      <p className="text-lg text-gray-500 max-w-2xl mb-10">
        CLI-based task management with web sync. Manage your tasks from anywhere,
        on any device, with seamless synchronization.
      </p>
      <div className="flex flex-col sm:flex-row gap-4 w-full max-w-md">
        <Link href="/signup" className="px-8 py-4 bg-blue-600 text-white font-semibold rounded-full hover:bg-blue-700 transition-colors shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-transform duration-200 text-center">
          Get Started
        </Link>
        <Link href="/signin" className="px-8 py-4 bg-white text-blue-600 font-semibold rounded-full border border-blue-200 hover:border-blue-300 hover:bg-blue-50 transition-colors shadow hover:shadow-md text-center">
          Sign In
        </Link>
      </div>
    </section>
  );
}