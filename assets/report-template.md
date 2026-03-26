# Report Template — Academic HTML Report Generation

## Purpose

Generate self-contained, single-file HTML reports for academic research workflows. Reports should feel like opening a well-typeset journal article — quiet confidence, generous whitespace, and zero visual noise.

## Design Philosophy

> "Perfection is achieved, not when there is nothing more to add, but when there is nothing left to take away." — Antoine de Saint-Exupéry

The template follows three principles:

1. **Content-first** — typography, spacing, and hierarchy serve readability above all else.
2. **Restrained elegance** — color is used sparingly and with purpose; decoration is structural, never ornamental.
3. **Academic gravity** — the visual language should feel like a respected peer-reviewed journal, not a startup landing page.

---

## Typography System

Use Google Fonts. Load exactly two families:

- **Headings**: `Cormorant Garamond` (weights 400, 600) — a refined serif with editorial authority.
- **Body**: `Source Sans 3` (weights 300, 400, 600) — a humanist sans-serif with excellent reading comfort at long-form lengths.
- **Monospace** (code/data): `JetBrains Mono` (weight 400) — only if the report contains code or raw identifiers.

Fallback stack: `Georgia, 'Times New Roman', serif` for headings; `'Segoe UI', Helvetica, Arial, sans-serif` for body.

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600&family=Source+Sans+3:wght@300;400;600&display=swap" rel="stylesheet">
```

### Chinese (中文) Typography

When the report language is Chinese, swap to CJK-optimized families:

- **Headings**: `Noto Serif SC` (weights 400, 600, 700) — the open-source 思源宋体, editorial and authoritative.
- **Body**: `Noto Sans SC` (weights 300, 400, 500, 700) — the open-source 思源黑体, clean and comfortable for long-form reading.
- **Data / numbers**: `Source Sans 3` (weights 300, 400, 600) — keep Latin numerals in a proportional sans for metric cards and tables.
- **Monospace**: `JetBrains Mono` (weight 400) — only if the report contains code.

Fallback stack: `'Songti SC', 'SimSun', serif` for headings; `'PingFang SC', 'Microsoft YaHei', sans-serif` for body.

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&family=Noto+Sans+SC:wght@300;400;500;700&family=Source+Sans+3:wght@300;400;600&display=swap" rel="stylesheet">
```

Use CSS custom properties to switch font stacks cleanly:

```css
:root {
  --font-heading: 'Noto Serif SC', '思源宋体', 'Songti SC', 'SimSun', serif;
  --font-body:    'Noto Sans SC', '思源黑体', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  --font-data:    'Source Sans 3', 'Helvetica Neue', Arial, sans-serif;
  --font-mono:    'JetBrains Mono', 'Menlo', 'Consolas', monospace;
}
```

### CJK-specific adjustments

Chinese text requires wider line-height and adjusted spacing compared to Latin:

| Token | English value | Chinese value | Reason |
|---|---|---|---|
| `body line-height` | 1.75 | 1.9 | CJK glyphs are taller and denser |
| `h1 line-height` | 1.25 | 1.4 | Prevent clipping on multi-line titles |
| `h2 line-height` | 1.3 | 1.4 | Same reason |
| `callout line-height` | 1.7 | 1.85 | Reading comfort in callout blocks |
| `blockquote font-style` | italic | normal | Most CJK fonts lack true italics; faux-italic distorts glyphs |
| `table header text-transform` | uppercase | none | Uppercase has no meaning in CJK |
| `table header letter-spacing` | 0.06em | 0.04em | CJK characters need less tracking |
| `metric-label text-transform` | uppercase | none | Same as above |

### Scale

| Element | Font | Size | Weight | Color |
|---|---|---|---|---|
| Report title | Cormorant Garamond | 2.25rem | 600 | `--ink` |
| Subtitle / date | Source Sans 3 | 0.95rem | 300 | `--muted` |
| Section heading (H2) | Cormorant Garamond | 1.5rem | 600 | `--ink` |
| Sub-section (H3) | Source Sans 3 | 1.1rem | 600 | `--ink` |
| Body paragraph | Source Sans 3 | 1.0rem / 1.75 line-height | 400 | `--text` |
| Caption / footnote | Source Sans 3 | 0.85rem | 400 | `--muted` |
| Table header | Source Sans 3 | 0.85rem | 600 | `--muted` (uppercase, letter-spacing 0.06em) |
| Table cell | Source Sans 3 | 0.9rem | 400 | `--text` |

---

## Color Palette

A muted, paper-toned palette. No saturated primaries. No gradients.

```css
:root {
  /* Surface */
  --bg:        #FAFAF7;       /* warm off-white, like fine paper */
  --surface:   #FFFFFF;       /* card / table background */
  --border:    #E8E6E1;       /* subtle warm grey dividers */

  /* Text */
  --ink:       #1A1A1A;       /* titles, headings — near-black */
  --text:      #374151;       /* body text — dark grey, easy on eyes */
  --muted:     #8C8C8C;       /* captions, dates, secondary info */

  /* Accent — one single accent, used very sparingly */
  --accent:    #4A6741;       /* muted sage green — scholarly, calm */
  --accent-bg: #F0F4EE;       /* tinted background for highlights */

  /* Semantic */
  --positive:  #5B8C5A;
  --caution:   #C9A84C;
  --negative:  #B85C5C;
}
```

### Dark-mode variant (optional)

If the report should support `prefers-color-scheme: dark`:

```css
@media (prefers-color-scheme: dark) {
  :root {
    --bg:        #1C1C1E;
    --surface:   #2C2C2E;
    --border:    #3A3A3C;
    --ink:       #F2F2F2;
    --text:      #D1D1D6;
    --muted:     #8E8E93;
    --accent:    #7DA876;
    --accent-bg: #2A3328;
  }
}
```

---

## Page Layout

```css
body {
  background: var(--bg);
  color: var(--text);
  font-family: 'Source Sans 3', 'Segoe UI', Helvetica, sans-serif;
  font-weight: 400;
  font-size: 1rem;
  line-height: 1.75;
  margin: 0;
  padding: 0;
  -webkit-font-smoothing: antialiased;
}

.report {
  max-width: 820px;
  margin: 0 auto;
  padding: 4rem 2rem 6rem;
}

@media (max-width: 640px) {
  .report { padding: 2rem 1.25rem 4rem; }
}
```

---

## Component Catalog

### 1. Report Header

A quiet header. Title, optional subtitle, author line, date. No background blocks, no hero banners.

```html
<header class="report-header">
  <p class="report-tag">Research Report</p>
  <h1 class="report-title">{{TITLE}}</h1>
  <p class="report-subtitle">{{SUBTITLE}}</p>
  <div class="report-meta">
    <span>{{AUTHOR}}</span>
    <span class="meta-sep">·</span>
    <span>{{DATE}}</span>
  </div>
</header>
```

```css
.report-header {
  text-align: center;
  margin-bottom: 3.5rem;
  padding-bottom: 2.5rem;
  border-bottom: 1px solid var(--border);
}

.report-tag {
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--accent);
  margin-bottom: 1rem;
}

.report-title {
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-size: 2.25rem;
  font-weight: 600;
  color: var(--ink);
  line-height: 1.25;
  margin: 0 0 0.5rem;
}

.report-subtitle {
  font-size: 1.1rem;
  font-weight: 300;
  color: var(--muted);
  margin: 0 0 1.25rem;
}

.report-meta {
  font-size: 0.85rem;
  color: var(--muted);
}

.meta-sep {
  margin: 0 0.5em;
}
```

### 2. Section Headings

H2 sections have a thin left accent bar. H3 sub-sections are plain and compact.

```css
h2 {
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--ink);
  margin: 3rem 0 1rem;
  padding-left: 0.85rem;
  border-left: 3px solid var(--accent);
  line-height: 1.3;
}

h3 {
  font-family: 'Source Sans 3', sans-serif;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--ink);
  margin: 2rem 0 0.75rem;
}
```

### 3. Tables

Clean, minimal. Horizontal lines only. Uppercase compact headers.

```css
table {
  width: 100%;
  border-collapse: collapse;
  margin: 1.5rem 0;
  font-size: 0.9rem;
}

thead th {
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--muted);
  text-align: left;
  padding: 0.6rem 0.75rem;
  border-bottom: 2px solid var(--border);
}

tbody td {
  padding: 0.65rem 0.75rem;
  border-bottom: 1px solid var(--border);
  vertical-align: top;
}

tbody tr:last-child td {
  border-bottom: none;
}

/* Optional: subtle hover for long data tables */
tbody tr:hover { background: var(--accent-bg); }
```

### 4. Highlight / Callout Boxes

Used for key findings, abstracts, or important notes. No icons, no colored borders on all sides — just a quiet left bar and tinted background.

```css
.callout {
  background: var(--accent-bg);
  border-left: 3px solid var(--accent);
  padding: 1.25rem 1.5rem;
  margin: 1.5rem 0;
  border-radius: 2px;
  font-size: 0.95rem;
  line-height: 1.7;
}

.callout strong {
  color: var(--ink);
}
```

### 5. Metric Cards

For summary statistics (e.g., "42 papers found", "3 research gaps identified"). Use a simple horizontal row.

```css
.metrics {
  display: flex;
  gap: 1.5rem;
  margin: 2rem 0;
  flex-wrap: wrap;
}

.metric-card {
  flex: 1;
  min-width: 140px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 1.25rem 1.5rem;
  text-align: center;
}

.metric-value {
  font-family: 'Source Sans 3', 'Segoe UI', Helvetica, sans-serif;
  font-size: 1.75rem;
  font-weight: 600;
  color: var(--ink);
  line-height: 1;
}

.metric-label {
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--muted);
  margin-top: 0.5rem;
}
```

### 6. Tags / Badges

For keywords, methods, journal names.

```css
.tag {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.2em 0.65em;
  border-radius: 3px;
  background: var(--accent-bg);
  color: var(--accent);
  margin: 0.15em 0.25em;
  letter-spacing: 0.02em;
}
```

### 7. Ordered / Unordered Lists

```css
ul, ol {
  padding-left: 1.25rem;
  margin: 1rem 0;
}

li {
  margin-bottom: 0.4rem;
}

li::marker {
  color: var(--accent);
}
```

### 8. Blockquotes

For direct quotations from papers.

```css
blockquote {
  margin: 1.5rem 0;
  padding: 0.75rem 1.5rem;
  border-left: 2px solid var(--border);
  color: var(--muted);
  font-style: italic;
  font-size: 0.95rem;
}
```

### 9. Footer

```css
.report-footer {
  margin-top: 4rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border);
  font-size: 0.8rem;
  color: var(--muted);
  text-align: center;
}
```

---

## Structural Template (Full Skeleton)

When generating a report, follow this HTML skeleton. Populate sections as needed — omit any section that has no content.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{TITLE}}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600&family=Source+Sans+3:wght@300;400;600&display=swap" rel="stylesheet">
  <style>
    /* — Paste all CSS from sections above — */
  </style>
</head>
<body>
  <div class="report">

    <!-- Header -->
    <header class="report-header">
      <p class="report-tag">{{REPORT_TYPE}}</p>
      <h1 class="report-title">{{TITLE}}</h1>
      <p class="report-subtitle">{{SUBTITLE}}</p>
      <div class="report-meta">
        <span>{{AUTHOR}}</span>
        <span class="meta-sep">·</span>
        <span>{{DATE}}</span>
      </div>
    </header>

    <!-- Optional: Summary Metrics -->
    <div class="metrics">
      <div class="metric-card">
        <div class="metric-value">{{N}}</div>
        <div class="metric-label">{{LABEL}}</div>
      </div>
      <!-- repeat as needed -->
    </div>

    <!-- Optional: Abstract / Key Findings callout -->
    <div class="callout">
      <strong>Key Findings</strong> — {{SUMMARY}}
    </div>

    <!-- Sections -->
    <h2>{{SECTION TITLE}}</h2>
    <p>{{CONTENT}}</p>

    <!-- Tables, lists, tags as needed -->

    <!-- Footer -->
    <footer class="report-footer">
      Generated by PaperSkills · {{DATE}}
    </footer>

  </div>
</body>
</html>
```

---

## Usage Rules

1. **Always self-contained** — all CSS inlined in `<style>`. No external stylesheets beyond Google Fonts.
2. **Never overload** — if a section is empty, omit it entirely. A shorter report is better than a padded one.
3. **Tables over bullet-lists** for structured data (papers, citations, comparisons). Use lists only for narrative enumeration.
4. **One accent color** — do not introduce additional colors unless semantically necessary (positive/caution/negative indicators in gap analysis or review scores).
5. **Responsive** — the layout must read comfortably on screens from 375px to 1440px.
6. **Print-friendly** — add a `@media print` block that hides non-essential UI and forces white background:

```css
@media print {
  body { background: #fff; }
  .report { padding: 0; max-width: 100%; }
  .metrics { break-inside: avoid; }
  table { break-inside: avoid; }
  h2 { break-after: avoid; }
}
```

7. **No JavaScript** — reports are static documents. No interactivity, no animations, no scripted behavior.
8. **Minimal decoration** — no box-shadows, no rounded-corner cards with colored headers, no emoji, no icon libraries. The only decorative elements allowed are the left accent bars on H2 and callouts.
