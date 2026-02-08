---
name: frontend-skill
description: Build frontend interfaces including pages, reusable components, layouts, and styling.
---

# Frontend Skill

## Instructions

1. **Page construction**
   - Build pages using a clear folder structure
   - Separate page-level and reusable components
   - Handle routing and navigation
   - Manage page-level state and data fetching

2. **Component design**
   - Create reusable and composable components
   - Use props and state effectively
   - Keep components small and focused
   - Follow consistent naming conventions

3. **Layout structure**
   - Design responsive layouts using flexbox or grid
   - Implement common layouts (header, footer, sidebar)
   - Ensure proper spacing and alignment
   - Support multiple screen sizes

4. **Styling**
   - Apply consistent design tokens (colors, spacing, typography)
   - Use CSS modules, utility classes, or styled components
   - Handle hover, focus, and active states
   - Ensure accessibility in styling

## Best Practices
- Mobile-first responsive design
- Reuse components instead of duplicating UI
- Keep styling predictable and scalable
- Avoid deeply nested components
- Use semantic HTML
- Test UI on multiple screen sizes
- Optimize for performance and accessibility

## Example Structure
```tsx
export function Card({ title, description }) {
  return (
    <div className="card">
      <h2>{title}</h2>
      <p>{description}</p>
    </div>
  );
}
