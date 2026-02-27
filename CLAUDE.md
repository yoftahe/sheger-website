# CLAUDE.md — Sheger International LLC Website

This file provides guidance for AI assistants (Claude and others) working on this codebase.

## Project Overview

**Sheger International LLC** is a premium vehicle export company based in Dubai, UAE. This repository contains their corporate website — a fully static HTML/CSS/JavaScript site with no build tools or external dependencies.

- **Business:** Vehicle import/export to Africa and Middle East markets
- **Contact:** info@shegerint.com | Dubai Free Zone, UAE
- **Stack:** Pure HTML5, CSS3, Vanilla JavaScript (ES6+)

---

## Repository Structure

```
sheger-website/
├── index.html          # Homepage — hero, featured vehicles, services overview
├── about.html          # Company overview, mission, history, key facts
├── services.html       # Detailed service descriptions (alternating grid layout)
├── inventory.html      # Vehicle listings with filterable cards
├── contact.html        # Contact form + info cards + WhatsApp integration
├── team.html           # Leadership profiles (placeholder photos)
├── market.html         # Target markets by region
├── marketing.html      # Marketing approach and strategy
├── css/
│   └── styles.css      # All styling (~1,454 lines), CSS variables, responsive breakpoints
├── js/
│   └── main.js         # All interactivity (~171 lines), vanilla JS
└── README.md           # Minimal project title only
```

---

## Technology Stack

| Layer | Technology |
|---|---|
| Markup | HTML5 (semantic) |
| Styling | CSS3 — custom properties, Grid, Flexbox |
| Scripting | Vanilla JavaScript (ES6+) |
| Fonts | Google Fonts: Inter (body), Playfair Display (headings) |
| Build tools | **None** — no npm, webpack, Vite, or bundler |
| Testing | **None** — no test framework |
| Backend | **None** — fully static, no server-side logic |

---

## Design System

### Color Palette (CSS Variables in `styles.css`)

```css
--primary-color: #c9a84c   /* Gold/champagne accent — brand color */
--dark-bg:       #1a1a1a   /* Primary dark background */
--darker-bg:     #0a0a0a   /* Deeper dark sections */
--text-gray:     #6b6b6b   /* Secondary text */
--white:         #ffffff
--whatsapp-green:#25d366   /* WhatsApp CTA elements */
```

### Typography

- **Body font:** Inter (sans-serif) — all body text and UI
- **Display font:** Playfair Display (serif) — page titles and hero headings
- Responsive sizing via `clamp()` throughout

### Layout

- Max container width: **1280px** (`max-w: 1280px, padding: 0 24px`)
- Grid columns: 3-col (desktop) → 2-col (tablet) → 1-col (mobile)
- Standard gap values: 16px, 24px, 32px, 48px, 64px, 80px

### Responsive Breakpoints

| Breakpoint | Layout Change |
|---|---|
| `< 480px` | Stacked single-column layouts, reduced padding |
| `< 768px` | Mobile navigation (hamburger), single-column sections |
| `768px – 1024px` | 2-column grids, tablet nav |
| `> 1024px` | Full desktop layout, 3-column grids |

---

## JavaScript Functionality (`js/main.js`)

All JavaScript is vanilla ES6+, wrapped in a single `DOMContentLoaded` listener.

### Modules / Features

1. **Mobile Navigation** — hamburger toggle, slide-in menu, overlay dismiss, auto-close on link click
2. **Sticky Header** — adds shadow at `scrollY > 50px`
3. **Scroll Animations** — Intersection Observer triggers `.fade-in` class on multiple element selectors; threshold `0.1`, rootMargin `'0px 0px -40px 0px'`
4. **Inventory Filtering** — filter buttons with `data-filter` attribute; vehicle cards have `data-category` attribute; `"All"` shows everything
5. **Contact Form** — client-side validation (required fields, red border feedback), simulated submit (no actual backend), button state changes, 3-second auto-reset
6. **Smooth Scroll** — handles internal anchor `#` links

### Data Attributes Used in HTML

```html
<!-- Inventory filter buttons -->
<button data-filter="suv">SUVs</button>

<!-- Vehicle cards -->
<div class="vehicle-card" data-category="suv">...</div>
```

---

## HTML Conventions

- **Semantic HTML5** throughout (`<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`)
- **Class naming:** BEM-inspired kebab-case — e.g., `.vehicle-card`, `.nav-menu`, `.hero-section`, `.service-grid`
- **Indentation:** 4 spaces
- **ARIA:** `aria-label` on interactive elements like nav toggle
- **Data attributes:** used for JavaScript hooks (not CSS styling)

---

## CSS Conventions

- **Organization:** Component-based sections separated by comments: `/* --- Component Name --- */`
- **Variables first:** All tokens defined at `:root` at the top of `styles.css`
- **No utility classes** — all styles are component-scoped
- **Hover/transition standard:** `transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1)`
- **Animations:** `.fade-in` class with `opacity` and `transform` transitions, triggered via JS

---

## Key Content & Business Logic

### Pages and Their Purpose

| Page | Key Purpose |
|---|---|
| `index.html` | First impression — hero, services teaser, vehicle highlights, trust signals |
| `about.html` | Company story, mission, compliance, location details |
| `services.html` | Full service breakdown in alternating grid rows |
| `inventory.html` | Filterable vehicle card grid (currently mock/static data) |
| `contact.html` | Simulated contact form + contact cards + WhatsApp button |
| `team.html` | Leadership team cards (photos and bios placeholder) |
| `market.html` | Regional target markets for vehicle exports |
| `marketing.html` | Numbered marketing approach cards |

### Image Source — Reference Site

**https://menamotors.com/ is the owner's other website.** All images on that site are owned by the same party and may be freely used on this site.

When adding real images to replace placeholders:

1. Download vehicle and site images directly from `https://menamotors.com/`
2. Save them into an `images/` directory at the project root (create it if absent)
3. Use descriptive filenames: `toyota-land-cruiser-300.jpg`, `nissan-patrol-v8.jpg`, etc.
4. Replace each `<div class="image-placeholder ...">` with a proper `<img>` tag:

```html
<!-- Before (placeholder) -->
<div class="vehicle-image">
    <div class="image-placeholder vehicle-img">
        <span>Toyota Land Cruiser 300</span>
    </div>
    <span class="vehicle-badge">Ready to Ship</span>
</div>

<!-- After (real image) -->
<div class="vehicle-image">
    <img src="images/toyota-land-cruiser-300.jpg"
         alt="Toyota Land Cruiser 300 — GCC Spec 2024"
         loading="lazy">
    <span class="vehicle-badge">Ready to Ship</span>
</div>
```

5. For team photos, replace the initials placeholder similarly:

```html
<!-- Before -->
<div class="team-photo">
    <div class="image-placeholder"><span>YF</span></div>
</div>

<!-- After -->
<div class="team-photo">
    <img src="images/team-yoftahe-fisseha.jpg" alt="Yoftahe Fisseha">
</div>
```

6. For the hero and intro section background/showcase images, replace `.intro-img-placeholder` divs with `<img>` tags styled to `width: 100%; height: 100%; object-fit: cover; border-radius: 8px;`

### Hardcoded Business Data (Needs Real Values)

The following values are placeholders and should be updated with real data:

- **Phone:** `+971 XX XXX XXXX` — appears in multiple pages
- **WhatsApp:** `https://wa.me/971000000000` — update with real number
- **Team photos:** Gray placeholder boxes — replace using process above
- **Vehicle images:** Gray placeholder boxes — replace using process above
- **Vehicle inventory:** Hardcoded mock cards — no CMS or database

---

## Known Limitations & Future Considerations

### What's Missing / Incomplete

1. **Contact form has no backend** — form `action="#"` is a simulation only; needs a real endpoint (e.g., Formspree, Netlify Forms, or a custom API)
2. **No real images** — team photos and vehicle images are placeholders
3. **Placeholder contact data** — phone and WhatsApp numbers need real values
4. **No CMS** — all content is in raw HTML, making updates manual
5. **No analytics** — no Google Analytics, Plausible, or similar tracking

### Potential Enhancements

- Connect contact form to a backend (Formspree is simplest for static sites)
- Add real vehicle images and team photos
- Integrate a headless CMS (Contentful, Sanity, or even a simple JSON file) for inventory
- Add Google Analytics or similar
- Optimize images with lazy loading (`loading="lazy"`)
- Add Open Graph / Twitter Card meta tags for social sharing

---

## Development Workflow

### No Build Step Required

Since this is a plain static site, you can:

1. Open any `.html` file directly in a browser
2. Use a simple local server for best results:
   ```bash
   # Python (built-in)
   python3 -m http.server 8080

   # Node.js (if available)
   npx serve .

   # VS Code: use Live Server extension
   ```

### Making Changes

- **HTML content:** Edit the relevant `.html` file directly
- **Styling:** All styles are in `css/styles.css` — look for the section comment matching the component
- **Behavior:** All JS is in `js/main.js` — sections are clearly commented

### No Linting or Formatting Tools

There is no configured linter or formatter. Follow the existing code style:
- 4-space HTML indentation
- Consistent CSS property ordering (layout → box model → typography → visual)
- Clear JS variable names, no minification

---

## Git Workflow

- **Main branch:** `main` (remote), `master` (local)
- **Feature branches:** `claude/<description>-<id>` pattern used for AI-assisted work
- **Commit style:** Descriptive imperative messages (e.g., `"Add complete Sheger International LLC vehicle export website"`)

### Branch for This Session

Development should occur on `claude/add-claude-documentation-WETyz`.

---

## Deployment

This site can be deployed to any static hosting platform:

| Platform | Method |
|---|---|
| GitHub Pages | Push to `gh-pages` branch or configure in repo settings |
| Netlify | Drag-and-drop or connect repo (no build command needed) |
| Vercel | `vercel --prod` with no framework preset |
| Traditional hosting | Upload all files via FTP/SFTP |
| AWS S3 | Static website hosting with CloudFront CDN |

No build command or output directory configuration is required — the root folder IS the deployable artifact.

---

## Quick Reference: Common Tasks

### Add a new page

1. Copy an existing page (e.g., `about.html`) as a starting template
2. Update the `<title>` and page-specific content
3. Add a link to it in the `<nav>` section of ALL pages (navigation is duplicated across pages)

### Add a vehicle to inventory

Find the vehicle grid in `inventory.html` and add a card following this pattern:

```html
<div class="vehicle-card" data-category="suv">
  <div class="vehicle-image">
    <img src="path/to/image.jpg" alt="Vehicle Name">
  </div>
  <div class="vehicle-info">
    <h3>Vehicle Name</h3>
    <div class="vehicle-specs">
      <span>Year</span>
      <span>Transmission</span>
      <span>Fuel Type</span>
    </div>
    <div class="vehicle-price">Contact for Price</div>
  </div>
</div>
```

Valid `data-category` values: `suv`, `truck`, `sedan`, `commercial` (or `all` to always show)

### Update contact information

Search across all HTML files for the placeholder values and replace:
- `+971 XX XXX XXXX` → actual phone number
- `wa.me/971000000000` → actual WhatsApp number
- `info@shegerint.com` → confirm this is correct

### Add a scroll animation to a new element

Add the appropriate selector to the `animatedElements` query in `js/main.js`:

```js
const animatedElements = document.querySelectorAll(
  '.your-new-class, .another-class, ...'
);
```

Then add initial CSS state in `styles.css`:

```css
.your-new-class {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}
.your-new-class.fade-in {
  opacity: 1;
  transform: translateY(0);
}
```
