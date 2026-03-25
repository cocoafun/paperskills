This is the design system for all HTML reports. When any skill writes an HTML report, follow these rules EXACTLY.

## File Convention
- Location: `reports/` subdirectory in working directory
- Naming: `{YYYY-MM-DD}-{skill-name}-{topic-kebab}.html`
- Single self-contained HTML file, no external dependencies except CDN fonts

## Design Philosophy
Academic book aesthetic — Crimson Pro serif for body, JetBrains Mono for labels/codes. Cream background, dark burgundy accents. Minimal, typographic, print-worthy.

## CSS Variables (use these exactly)
```css
:root {
  --bg: #f4f0e8;
  --text: #1a1a1a;
  --text-muted: #555;
  --text-light: #888;
  --accent: #7b2d26;
  --border: #c8bfa8;
  --border-light: #ddd5c4;
  --success: #2d5f2d;
  --warn: #8a6914;
}
```

## Fonts (Google Fonts import)
```css
@import url('https://fonts.googleapis.com/css2?family=Crimson+Pro:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400;1,500&family=JetBrains+Mono:wght@400&family=Noto+Serif+SC:wght@300;400;500;600;700&display=swap');
```
- Body: `'Crimson Pro', Georgia, serif` — 17px, line-height 1.7
- Mono labels: `'JetBrains Mono', monospace` — 10-12px, uppercase, letter-spacing 0.08-0.12em

## Multilingual Support

Default language is English (`<html lang="en">`). For Chinese reports, set `<html lang="zh">`.

```css
html[lang="zh"] body {
  font-family: 'Noto Serif SC', 'Crimson Pro', Georgia, serif;
  font-size: 16px;
  line-height: 1.8;
}
```

- **Chinese font stack**: `'Noto Serif SC', 'Crimson Pro', Georgia, serif` — Noto Serif SC handles CJK glyphs, Crimson Pro handles embedded Latin characters (common in academic citations)
- **JetBrains Mono** remains unchanged for labels/codes (ASCII-only labels work in both languages)
- The `lang` attribute enables proper CJK line-breaking and text-spacing in browsers
- Chinese reports use slightly smaller font-size (16px) and taller line-height (1.8) for CJK readability

## Page Layout
```css
.page { max-width: 1080px; margin: 0 auto; padding: 48px 40px 80px; }
body { background: var(--bg); color: var(--text); }
```

## Header Pattern
Every report starts with:
```html
<div class="header">
  <div class="header-meta">REPORT TYPE · DATE</div>
  <div class="header-body">
    <div class="header-title-block">
      <h1>Report Title</h1>
      <div class="header-subtitle">Subtitle or description</div>
    </div>
    <div class="header-score-block">
      <div class="score-big">3.8<span class="score-denom">/5</span></div>
      <div class="score-label">Overall Score</div>
      <span class="badge badge--accept">Minor Revisions</span>
    </div>
  </div>
</div>
```
- `header-meta`: JetBrains Mono, 11px, uppercase, light gray
- `h1`: 22px, weight 600, letter-spacing -0.02em
- `score-big`: 48px, weight 300, accent color
- Header bottom: `border-bottom: 2px solid var(--text)`

## Stats Bar (summary numbers)
```html
<div class="stats">
  <div class="stat"><div class="stat-value">42</div><div class="stat-label">References</div></div>
  <div class="stat"><div class="stat-value">8</div><div class="stat-label">Sections</div></div>
  <!-- ... -->
</div>
```
- Grid: `grid-template-columns: repeat(4, 1fr)`
- Borders top/bottom: 1.5px solid var(--border)
- stat-value: 26px, weight 300, accent color
- stat-label: JetBrains Mono, 10px, uppercase

## Section Headers
```css
h2 {
  font-size: 13px; text-transform: uppercase; letter-spacing: 0.12em;
  color: var(--accent); border-bottom: 1.5px solid var(--accent);
  padding-bottom: 6px; margin-bottom: 20px; margin-top: 40px; font-weight: 600;
}
```

## Badges and Flags
```css
.badge { font-size: 11px; font-family: mono; text-transform: uppercase; letter-spacing: 0.08em; padding: 3px 10px; border: 1.5px solid; }
.badge--accept { border-color: var(--success); color: var(--success); }
.badge--warn { border-color: var(--warn); color: var(--warn); }
.badge--accent { border-color: var(--accent); color: var(--accent); }
```

## Data Tables
```css
thead th { font-size: 11px; font-family: mono; uppercase; letter-spacing: 0.08em; color: var(--text-muted); border-bottom: 1.5px solid var(--text); }
tbody td { padding: 10px; border-bottom: 0.5px solid var(--border-light); }
tbody tr:last-child td { border-bottom: 1.5px solid var(--border); }
```

## Score Bars (inline progress)
```html
<span class="score-bar" style="width:80px;background:var(--success)"></span>
<span class="score-num">4/5</span>
```
- Height 5px, border-radius 1px
- Color by score: >=4 success, 3 warn, <=2 accent

## Accordion Sections (details/summary)
```html
<details>
  <summary>
    <span class="summary-left">
      <span class="summary-kode">K1</span>
      <span class="summary-title">Originality</span>
    </span>
    <span class="summary-score">4/5</span>
    <span class="summary-arrow">▸</span>
  </summary>
  <div class="acc-body">
    <p>Evaluation text...</p>
    <div class="rec-box">Recommendation: ...</div>
  </div>
</details>
```
- No list-style markers on summary
- Arrow rotates 90deg when open
- acc-body: padded left 44px
- rec-box: left border 2px accent, light accent background, italic

## Charts (Chart.js)
```html
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
```
- Radar chart for multi-criteria scoring
- Colors: `rgba(123, 45, 38, 0.2)` fill, `rgb(123, 45, 38)` border
- Point: `rgb(123, 45, 38)`, radius 4
- Grid: `color: '#c8bfa8'`
- Scale 0-5, font: Crimson Pro

## Grid Layouts
```css
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; }
.grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 24px; }
```

## Recommendation Box
```css
.rec-box { padding: 10px 14px; border-left: 2px solid var(--accent); background: rgba(123,45,38,0.04); font-style: italic; color: var(--text-muted); }
```

## Footer
```html
<div class="footer">Generated by PaperSkills · {date}</div>
```
```css
.footer { margin-top: 60px; padding-top: 16px; border-top: 1px solid var(--border); font-family: mono; font-size: 11px; color: var(--text-light); text-align: center; }
```

## Color Coding Semantics
- **Success/Good**: `var(--success)` #2d5f2d — verified, high score, accepted
- **Warning/Attention**: `var(--warn)` #8a6914 — partial match, medium score, needs revision
- **Error/Critical**: `var(--accent)` #7b2d26 — not found, low score, rejected
- **Neutral**: `var(--border)` #c8bfa8 — unchecked, N/A

## DO NOT
- Do not use Tailwind CDN — use the custom CSS above
- Do not use bright/saturated colors — keep everything muted and academic
- Do not use sans-serif for body text — always Crimson Pro serif
- Do not use rounded corners larger than 2px
- Do not add shadows — use borders only
