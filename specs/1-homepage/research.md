# Research: Todo CLI Homepage Implementation

**Feature**: Todo CLI – Modern Homepage
**Date**: 2026-01-30
**Branch**: 1-homepage

## Research Summary

This research addresses the key design and implementation decisions for the Todo CLI homepage, focusing on modern SaaS UI patterns, responsive design, and user experience best practices.

## Key Design Decisions

### 1. Light Gradient Background vs Solid Background

**Decision**: Light gradient background chosen for modern feel
**Rationale**: Based on analysis of successful SaaS homepages (Notion, Linear, Figma), light gradients with subtle blue/indigo tones create a premium, modern aesthetic that enhances visual appeal without overwhelming the content. This aligns with the requirement for a "modern SaaS UI" with "soft gradients".

**Alternatives considered**:
- Solid white background: Clean but potentially sterile and less engaging
- Plain light gray: More neutral but lacks the premium feel
- Image background: Could distract from core messaging

### 2. 3 vs 4 Feature Cards

**Decision**: 3 feature cards for clarity and balance
**Rationale**: Research on cognitive load suggests that 3 items provide optimal information density without overwhelming users. This creates better visual balance and allows for larger, more impactful cards. The requirement states "3-4 boxes" but 3 offers better spacing and readability.

**Alternatives considered**:
- 4 feature cards: More information but potentially cramped on smaller screens
- 2 feature cards: Too sparse and might not convey sufficient value

### 3. Centered Hero vs Split Layout

**Decision**: Centered hero layout for focus
**Rationale**: Analysis of high-converting SaaS homepages shows that centered layouts direct attention to the primary value proposition and CTA buttons. This supports the requirement for "center-aligned layout" and helps users understand the product within 5 seconds.

**Alternatives considered**:
- Split layout (text on left, image on right): More traditional but divides attention
- Left-aligned: Less visually balanced

### 4. Minimal Client-Side JavaScript

**Decision**: Minimal JavaScript for better performance
**Rationale**: Following web performance best practices, keeping JavaScript minimal improves load times and accessibility. Animations can be achieved primarily through CSS, meeting the requirement for "optimized for fast load" and "minimal JS on homepage".

**Implementation approach**:
- CSS animations for entrance effects (fade + slide)
- CSS transitions for hover effects (card lift, shadow, color changes)
- Progressive enhancement for any interactive elements

## Modern SaaS Homepage Patterns

### Common UX Patterns Identified

1. **Hero Section Structure**:
   - Centered layout with large, bold product name
   - Clear tagline below title
   - One-paragraph description explaining value proposition
   - Prominent CTA buttons

2. **Feature Presentation**:
   - 3-4 feature cards with consistent design
   - Icons at top for visual recognition
   - Clear titles and concise descriptions
   - Hover effects for interactivity

3. **CTA Button Design**:
   - Large, rounded buttons
   - High contrast colors
   - Clear differentiation between primary and secondary actions
   - Positioned prominently in hero section

## Color Palette Research

### Blue/Indigo Focused Palette

Based on research of successful SaaS products, the following palette supports the "calm blue/indigo accent colors" requirement:

- Primary Blue: Tailwind's `blue-600` (#2563eb) for primary CTAs
- Indigo Accent: Tailwind's `indigo-500` (#6366f1) for secondary elements
- Soft Background: `gray-50` (#f9fafb) or light gradient
- Card Background: White with soft shadows
- Text Colors: `gray-900` for headings, `gray-600` for body text

## Responsive Design Patterns

### Grid Layout Strategy

Research confirms the effectiveness of adaptive grids:
- Desktop: 3-4 column grid (using Tailwind's grid system)
- Tablet: 2 column grid (breakpoint at 768px)
- Mobile: 1 column grid (breakpoint at 640px)

This satisfies the requirement for "Desktop: 3 or 4 column grid, Tablet: 2 column grid, Mobile: 1 column".

## Animation and Micro-interaction Patterns

### Entrance Animation
- Fade-in combined with slight vertical slide (CSS opacity + transform)
- Duration: 300ms (within the 200-300ms range specified)
- Timing function: ease-out for smooth acceleration

### Hover Effects for Cards
- Transform: translateY(-4px) for upward movement
- Box-shadow: Increase shadow intensity for depth
- Border-color: Change to accent color for highlight
- Transition: 200-300ms for smooth response

## Accessibility Considerations

### Contrast Ratios
- Maintain WCAG 2.1 AA compliance (4.5:1 for normal text, 3:1 for large text)
- High contrast between text and backgrounds
- Sufficient contrast for interactive elements

### Touch Targets
- Minimum 44px touch targets for mobile devices
- Adequate spacing between interactive elements
- Visual feedback for touch interactions

## Technology Implementation Strategy

### Next.js 16 App Router
- Server Components by default for better performance
- Client Components only where interactivity is required
- Built-in image optimization
- Automatic code splitting

### Tailwind CSS
- Utility-first approach for rapid development
- Responsive design utilities built-in
- Dark mode support if needed in future
- Custom color palette configuration

### SVG Icons
- Inline SVG for icons to maintain crispness at all resolutions
- Customizable colors through Tailwind classes
- No external dependencies
- Accessible through proper labeling