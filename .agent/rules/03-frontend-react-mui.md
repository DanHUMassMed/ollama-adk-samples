---
trigger: always_on
description: Frontend Standards (React, MUI, Vite)
---

# Frontend: React, MUI, Vite

- **Component Library:** Use Material UI (MUI) components exclusively. Do not write raw CSS files or use Tailwind unless explicitly required. Use `sx` props or `styled` utility for custom styling.
- **State Management:** Use React Hooks (`useState`, `useEffect`) for local component state. Use Context, Redux, or Zustand only for global Agent session data.
- **Vite Configuration:** Ensure asset paths are compatible with Vite's bundling logic. Always use `import.meta.env` for accessing environment variables instead of `process.env`.
- **Responsive Layout:** Use MUI's `<Grid2>` (or `<Grid>`), `<Stack>`, and `theme.breakpoints` consistently to ensure responsive layouts. Avoid manual CSS flexbox/grid.
