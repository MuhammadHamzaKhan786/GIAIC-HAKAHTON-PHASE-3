# Quickstart Guide: Todo CLI Homepage

**Feature**: Todo CLI – Modern Homepage
**Date**: 2026-01-30
**Branch**: 1-homepage

## Overview

This guide provides step-by-step instructions for implementing the Todo CLI homepage according to the specification and design plan. The homepage will be built using Next.js 16 with App Router, featuring a hero section, 3 feature cards with hover effects, and prominent CTA buttons.

## Prerequisites

- Node.js 18+ installed
- Next.js 16+ project set up
- Tailwind CSS configured in the project
- Basic knowledge of React and TypeScript/JavaScript

## Setup Instructions

### 1. Create the Homepage Route

Create the main page file:

```bash
# Create the page file if it doesn't exist
touch frontend/src/app/page.tsx
```

### 2. Install Required Dependencies

If not already installed:

```bash
npm install next react react-dom
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### 3. Configure Tailwind CSS

Update `tailwind.config.js` to include the necessary configurations:

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
        },
        indigo: {
          50: '#eef2ff',
          100: '#e0e7ff',
          200: '#c7d2fe',
          300: '#a5b4fc',
          400: '#818cf8',
          500: '#6366f1',
          600: '#4f46e5',
          700: '#4338ca',
          800: '#3730a3',
          900: '#312e81',
        },
      },
      borderRadius: {
        'xl': '0.75rem',
        '2xl': '1rem',
      },
    },
  },
  plugins: [],
}
```

## Implementation Steps

### Step 1: Create the Main Page Component

Create `frontend/src/app/page.tsx`:

```tsx
import HeroSection from '@/components/HeroSection';
import FeatureCards from '@/components/FeatureCards';
import Footer from '@/components/Footer';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
      <main className="container mx-auto px-4 py-8">
        <HeroSection />
        <FeatureCards />
      </main>
      <Footer />
    </div>
  );
}
```

### Step 2: Create the Hero Section Component

Create `frontend/src/components/HeroSection.tsx`:

```tsx
'use client';

import { useEffect, useState } from 'react';

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
        <button className="px-8 py-4 bg-blue-600 text-white font-semibold rounded-full hover:bg-blue-700 transition-colors shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-transform duration-200">
          Get Started
        </button>
        <button className="px-8 py-4 bg-white text-blue-600 font-semibold rounded-full border border-blue-200 hover:border-blue-300 hover:bg-blue-50 transition-colors shadow hover:shadow-md">
          Sign In
        </button>
      </div>
    </section>
  );
}
```

### Step 3: Create the Feature Cards Component

Create `frontend/src/components/FeatureCards.tsx`:

```tsx
import FeatureCard from './FeatureCard';

const features = [
  {
    id: 1,
    icon: (
      <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 text-indigo-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
      </svg>
    ),
    title: "Secure Authentication",
    description: "JWT-based authentication with user isolation and secure session management."
  },
  {
    id: 2,
    icon: (
      <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 text-indigo-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2m-2-4h.01M17 16h.01" />
      </svg>
    ),
    title: "Fast CLI Task Management",
    description: "Efficient command-line interface for managing tasks with keyboard shortcuts."
  },
  {
    id: 3,
    icon: (
      <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 text-indigo-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
      </svg>
    ),
    title: "Real-time Sync",
    description: "Seamless synchronization between CLI and web interface with instant updates."
  }
];

export default function FeatureCards() {
  return (
    <section className="py-16">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
        {features.map((feature) => (
          <FeatureCard
            key={feature.id}
            icon={feature.icon}
            title={feature.title}
            description={feature.description}
          />
        ))}
      </div>
    </section>
  );
}
```

### Step 4: Create the Individual Feature Card Component

Create `frontend/src/components/FeatureCard.tsx`:

```tsx
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
```

### Step 5: Create the Footer Component

Create `frontend/src/components/Footer.tsx`:

```tsx
export default function Footer() {
  return (
    <footer className="bg-white border-t border-gray-200 py-8">
      <div className="container mx-auto px-4 text-center">
        <p className="text-gray-500">
          © {new Date().getFullYear()} Todo CLI. All rights reserved.
        </p>
      </div>
    </footer>
  );
}
```

### Step 6: Update Global Styles

Add to `frontend/src/styles/globals.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
}

/* Additional custom styles if needed */
```

## Running the Application

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

4. Visit `http://localhost:3000` to see the homepage.

## Testing Checklist

- [ ] Hero section appears centered with product name, tagline, and description
- [ ] CTA buttons are large, rounded-full, high contrast, and clearly visible
- [ ] Feature cards display with icons, titles, and descriptions
- [ ] Hover effects work on feature cards (lift, shadow increase, color highlight)
- [ ] Entrance animation works on hero section (fade + slight slide)
- [ ] Page is responsive on mobile, tablet, and desktop
- [ ] Footer displays minimal content
- [ ] All interactive elements are touch-friendly
- [ ] Contrast ratios meet accessibility standards

## Troubleshooting

### Animation Issues
- Ensure the `useState` and `useEffect` hooks are properly imported in HeroSection
- Check that Tailwind classes for transitions are correctly applied

### Responsive Issues
- Verify Tailwind breakpoints are correctly configured
- Check that container widths adapt properly to different screen sizes

### Styling Issues
- Confirm Tailwind CSS is properly configured in your project
- Ensure all necessary Tailwind classes are included in the content files