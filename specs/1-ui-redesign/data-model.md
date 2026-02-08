# Data Model: UI Redesign — Todo Web Application (Auth + Dashboard)

**Feature**: 1-ui-redesign
**Created**: 2026-01-28
**Status**: Design

## Overview

This data model describes the UI state and data structures needed for the redesigned Todo application interface. The focus is on UI/UX elements and visual presentation rather than backend data storage.

## UI State Objects

### User Interface Configuration
- **themeSettings**
  - themeType: String (light/dark/auto)
  - primaryColor: HexColor
  - secondaryColor: HexColor
  - fontFamily: String
  - fontSize: String (small/medium/large)

### Authentication Page States
- **signInState**
  - email: String
  - password: String
  - isLoading: Boolean
  - errorMessage: String
  - isValid: Boolean

- **signUpState**
  - email: String
  - password: String
  - confirmPassword: String
  - isLoading: Boolean
  - errorMessage: String
  - isValid: Boolean
  - termsAccepted: Boolean

### Dashboard Page States
- **dashboardState**
  - activeTab: String (all/completed/pending)
  - tasks: Array of TaskSummary
  - searchQuery: String
  - sortBy: String (date/alpha/status)
  - filterBy: String (all/completed/pending)

### Task Presentation Objects
- **TaskSummary**
  - taskId: String
  - title: String
  - description: String
  - status: String (pending/completed)
  - createdAt: DateTime
  - updatedAt: DateTime
  - priority: String (low/medium/high)
  - category: String

- **TaskDetail**
  - extends TaskSummary
  - notes: String
  - dueDate: DateTime
  - assignedTo: String
  - tags: Array of String

## UI Component States

### Form Elements
- **inputFieldState**
  - value: String
  - isValid: Boolean
  - errorMessage: String
  - isFocused: Boolean
  - isDirty: Boolean

### Navigation Elements
- **navigationBarState**
  - currentPage: String
  - breadcrumbs: Array of String
  - userMenuOpen: Boolean
  - notificationsCount: Integer

### Layout Elements
- **layoutConfiguration**
  - sidebarCollapsed: Boolean
  - contentWidth: String (full/narrow/wide)
  - responsiveBreakpoint: String (mobile/tablet/desktop)
  - animationEnabled: Boolean

## Visual Design Tokens

### Color Palette
- **primaryColors**
  - primary50: HexColor
  - primary100: HexColor
  - primary200: HexColor
  - primary300: HexColor
  - primary400: HexColor
  - primary500: HexColor (main)
  - primary600: HexColor
  - primary700: HexColor
  - primary800: HexColor
  - primary900: HexColor

- **secondaryColors**
  - secondary50: HexColor
  - secondary100: HexColor
  - secondary200: HexColor
  - secondary300: HexColor
  - secondary400: HexColor
  - secondary500: HexColor (main)
  - secondary600: HexColor
  - secondary700: HexColor
  - secondary800: HexColor
  - secondary900: HexColor

- **semanticColors**
  - success: HexColor
  - warning: HexColor
  - error: HexColor
  - info: HexColor

### Typography Scale
- **typographyScale**
  - xs: String (font-size)
  - sm: String (font-size)
  - md: String (font-size)
  - lg: String (font-size)
  - xl: String (font-size)
  - '2xl': String (font-size)
  - '3xl': String (font-size)
  - '4xl': String (font-size)

### Spacing Scale
- **spacingScale**
  - 0: String (0px)
  - 1: String (4px)
  - 2: String (8px)
  - 3: String (12px)
  - 4: String (16px)
  - 5: String (20px)
  - 6: String (24px)
  - 8: String (32px)
  - 10: String (40px)
  - 12: String (48px)
  - 16: String (64px)
  - 20: String (80px)
  - 24: String (96px)
  - 32: String (128px)

## Responsive Breakpoints

- **breakpoints**
  - mobile: String (max-width: 640px)
  - tablet: String (min-width: 641px) and (max-width: 1024px)
  - desktop: String (min-width: 1025px) and (max-width: 1280px)
  - desktopLarge: String (min-width: 1281px)

## Animation Specifications

- **animationPresets**
  - fadeIn: Object (duration, easing)
  - slideIn: Object (direction, duration, easing)
  - scaleIn: Object (scale factor, duration, easing)
  - transitionDuration: String (fast/normal/slow)
  - easingFunctions: Array (ease-in, ease-out, ease-in-out, linear)

## Accessibility Attributes

- **accessibilityConfig**
  - highContrastMode: Boolean
  - reducedMotion: Boolean
  - screenReaderOptimized: Boolean
  - keyboardNavigation: Boolean
  - focusIndicatorStyle: String