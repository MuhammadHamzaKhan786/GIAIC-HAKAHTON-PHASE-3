# Data Model: Todo CLI Homepage

**Feature**: Todo CLI – Modern Homepage
**Date**: 2026-01-30
**Branch**: 1-homepage

## Overview

The Todo CLI homepage contains static content that presents information about the product to visitors. Since this is a presentation-only page with no dynamic data from a backend, the data model consists of content structures that define what information is displayed on the page.

## Content Entities

### 1. Homepage Content

**Description**: Represents the static content displayed on the homepage including hero section text, feature card information, and footer content.

**Fields**:
- `heroTitle`: String - The main product name displayed prominently (e.g., "Todo CLI")
- `heroTagline`: String - Short tagline below the title (e.g., "CLI-Based Task Management")
- `heroDescription`: String - One-paragraph description explaining "CLI-based task management with web sync"
- `primaryCtaText`: String - Text for the primary CTA button (e.g., "Get Started")
- `secondaryCtaText`: String - Text for the secondary CTA button (e.g., "Sign In")
- `primaryCtaUrl`: String - Destination URL for the primary CTA
- `secondaryCtaUrl`: String - Destination URL for the secondary CTA

### 2. Feature Card

**Description**: Represents a single feature card in the feature section with icon, title, and description.

**Fields**:
- `id`: String/Number - Unique identifier for the card
- `icon`: String - SVG icon content or icon identifier
- `title`: String - Short, clear title for the feature
- `description`: String - 1-2 line description explaining the feature
- `order`: Number - Display order in the feature section

**Sample Features**:
1. Secure Authentication (JWT / user isolation)
2. Fast CLI Task Management
3. Real-time Sync (CLI ↔ Web)
4. Multi-user / Team Collaboration

### 3. Footer Content

**Description**: Represents the minimal footer content with essential links.

**Fields**:
- `links`: Array of objects containing `{ text: String, url: String }`
- `copyrightText`: String - Copyright information
- `companyInfo`: String - Company name or brand information

## Content Relationships

```
Homepage Content
    ├── Hero Section (1-to-1)
    ├── [Feature Card] (1-to-many, typically 3-4)
    └── Footer Content (1-to-1)
```

## Validation Rules

Based on functional requirements from the specification:

1. **FR-001**: Hero section must contain title, tagline, and description
2. **FR-002**: Must have two CTA buttons (primary and secondary)
3. **FR-003**: Must display 3-4 feature cards with icon, title, and description
4. **FR-007**: Must use light theme with appropriate styling attributes
5. **FR-008**: Must include minimal footer content

## State Transitions

Since this is a static homepage, there are no state transitions for the content itself. However, UI states exist for interactive elements:

- Feature Card: `normal` ↔ `hover` (for hover effects)
- CTA Button: `enabled` ↔ `disabled` (if needed for loading states)
- Page: `loading` → `loaded` (for entrance animations)

## Constraints

- Feature cards: Limited to 3-4 items as per design requirements
- Content length: Descriptions must be concise (1-2 lines max for feature cards)
- Responsive: Content must adapt to different screen sizes
- Accessibility: All content must meet WCAG 2.1 AA standards