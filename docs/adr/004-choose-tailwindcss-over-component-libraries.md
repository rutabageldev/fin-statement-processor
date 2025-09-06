# ADR-004: Choose TailwindCSS Over Component Libraries

**Status:** ACCEPTED
**Date:** 2025-09-06
**Deciders:** Lead Developer

## Context

Ledgerly's frontend requires a styling approach for building financial dashboards with data visualizations, forms, tables, and responsive layouts. The choice affects development speed, design flexibility, learning value, and long-term maintainability.

Key considerations:

- This is a hobby project with focus on learning over speed
- Financial dashboards need precise control over data density and layout
- Future customization and unique design aesthetics are valued
- No business pressure for rapid MVP delivery
- Single developer with time to invest in CSS mastery

Two primary approaches considered:

1. **Component Library** (Chakra UI): Pre-built components with consistent design system
2. **Utility-First CSS** (TailwindCSS): Low-level utility classes for custom designs

## Decision

We will use **TailwindCSS** as the primary CSS framework with **Headless UI** for unstyled accessible components.

**Technology Stack:**

- **TailwindCSS**: Utility-first CSS framework
- **Headless UI**: Unstyled, accessible React components
- **Recharts**: Chart library with custom Tailwind styling
- **CSS Modules**: For complex component-specific styles when needed

## Rationale

**Learning and Skill Development:**

- **CSS Mastery**: Deepens understanding of flexbox, grid, responsive design, animations
- **Transferable Skills**: CSS knowledge applies to any future web project or framework
- **Problem Solving**: Builds capability to implement any design from scratch

**Design Flexibility:**

- **Custom Financial UI**: Build unique dashboard aesthetics, not "another generic admin panel"
- **Data Density Control**: Fine-tune spacing and layout for financial tables and charts
- **Responsive Precision**: Granular control over mobile/desktop layouts for data visualization
- **Brand Identity**: Create distinctive visual identity that stands out

**Technical Benefits:**

- **Performance**: Smaller bundle size (only includes used CSS)
- **No Framework Lock-in**: Pure CSS knowledge isn't tied to React ecosystem
- **Future-Proof**: CSS specifications evolve slowly and remain stable
- **Debugging**: Easier to debug styling issues with plain CSS classes

**Project Alignment:**

- **Hobby Timeline**: No business pressure allows time for learning-focused approach
- **Customization Priority**: Value unique design over development speed
- **Educational Goals**: Preference for mastering foundational technologies

## Consequences

### Positive

- **Deep CSS Understanding**: Master modern CSS techniques (Grid, Flexbox, animations)
- **Design Freedom**: Complete control over every pixel and interaction
- **Performance**: Minimal CSS bundle size with tree-shaking
- **Unique Aesthetics**: Build something that looks distinctly different from template-based apps
- **Long-term Value**: CSS skills remain relevant across all web technologies
- **Migration Flexibility**: Can add component libraries later without major refactoring

### Negative

- **Initial Development Time**: +20-30% development time for UI implementation
- **Learning Curve**: Need to master utility class patterns and responsive design principles
- **Accessibility Work**: Must implement WCAG compliance manually (mitigated by Headless UI)
- **Consistency Risk**: Requires discipline to maintain design system consistency
- **Debugging Time**: More CSS troubleshooting compared to pre-built components

### Neutral

- **Component Reusability**: Build custom component library over time
- **Documentation**: Need to document custom design system patterns
- **Team Onboarding**: Future contributors need Tailwind familiarity (less common than CSS)

## Alternatives Considered

### Option 1: Chakra UI Component Library

- **Description:** Pre-built React component library with theming system
- **Pros:**
  - Rapid MVP development (3x faster initial implementation)
  - Built-in accessibility (WCAG 2.1 AA compliant)
  - Consistent design system with theme switching
  - Rich ecosystem of financial dashboard components
  - Professional appearance out-of-the-box
- **Cons:**
  - Limited design flexibility - looks like other Chakra apps
  - Less CSS learning opportunity
  - Framework dependency and upgrade maintenance
  - Harder to customize for specific financial data presentation needs
  - Bundle size includes unused components
- **Rejected because:** Prioritizing learning and design uniqueness over development speed for hobby project

### Option 2: Styled Components (CSS-in-JS)

- **Description:** Write CSS directly in JavaScript components
- **Pros:**
  - Component-scoped styling
  - Dynamic styling based on props
  - Full CSS capabilities
  - Good TypeScript integration
- **Cons:**
  - Runtime performance overhead
  - Complex debugging with generated class names
  - Bundle size increases with styled components
  - Less design system consistency without discipline
- **Rejected because:** Runtime overhead and complexity don't provide clear benefits over utility-first approach

### Option 3: Material-UI (MUI)

- **Description:** React implementation of Google's Material Design
- **Pros:**
  - Comprehensive component ecosystem
  - Mature library with strong community
  - Built-in theming and customization
  - Good TypeScript support
- **Cons:**
  - Heavy Material Design aesthetics not ideal for financial dashboards
  - Large bundle size
  - Complex customization for non-Material designs
  - Over-engineered for simple hobby project needs
- **Rejected because:** Material Design aesthetic doesn't fit financial application requirements

## Implementation Notes

**Phase 1 Setup:**

- Install TailwindCSS with Vite integration
- Configure design system tokens (colors, spacing, typography)
- Set up Headless UI for accessible form components
- Create base component patterns (Button, Card, Input)

**Development Approach:**

- **Design System First**: Establish color palette, typography, spacing scale
- **Component Building**: Build reusable components with Tailwind classes
- **Responsive Strategy**: Mobile-first approach with Tailwind breakpoints
- **Dark Mode**: Use Tailwind's built-in dark mode utilities

**Learning Path:**

- Start with basic layouts and spacing
- Progress to complex responsive grid layouts
- Master Tailwind's animation and transition utilities
- Build custom chart styling to complement Recharts

**Future Migration Options:**

- Can add Chakra components for complex features (data tables)
- Easy to wrap Tailwind components in higher-level abstractions
- Utility classes can coexist with component libraries

## Related Decisions

- Builds on ADR-003 (Technology Stack) React frontend choice
- Supports custom financial dashboard requirements from product roadmap
- Enables unique brand identity development for Ledgerly
- Future decision needed on design system documentation approach

## References

- [TailwindCSS Documentation](https://tailwindcss.com/docs)
- [Headless UI Documentation](https://headlessui.com/)
- [Tailwind vs Component Libraries](https://tailwindcss.com/docs/reusing-styles)
- [Building Design Systems with Tailwind](https://tailwindcss.com/docs/adding-custom-styles)
- [Financial Dashboard Design Patterns](https://www.nngroup.com/articles/dashboard-design/)

---

_This document follows the [MADR template](https://adr.github.io/madr/)_
