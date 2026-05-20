# LSC Creative · Project Estimate & Billing Application

A high-end internal operations tool built for **LSC Creative** — a motion and media production company. The application generates, archives, and exports pixel-perfect Letter-size project estimates and client invoices, featuring a native Base64 logo rendering engine, a typographic PDF print layout, and a client outreach link dashboard built for direct email deployment.

No frameworks. No dependencies. No build step. One file.

---

## Core Feature Stack

**PDF Print Engine**
Dual-mode document builder (`buildClientPDF` / `buildClientInvoicePDF`) that constructs a complete, self-contained HTML document string and opens it in a new browser tab for native print-to-PDF export. The layout uses a warm-white `#F0EDE8` primary canvas with a `#E8E2D9` accent block for the financial summary, a strict typographic scale (section headers at `1.4rem`, table data at `1rem`, eyebrow labels at `7.5pt`), and a single-row inline contact footer that never splits across page breaks.

**Base64 Logo Loader**
On page initialisation, a `fetch` + `FileReader` pipeline loads `uploads/logo.png` and converts it to a Base64 data URI stored in `LOGO_B64`. This approach is cross-origin safe and works correctly under both `file://` and `http://` schemes — no canvas taint errors.

**Estimate Archive & Card Dashboard**
All project estimates are persisted to `localStorage` and rendered as a grid of dark-surfaced project cards on the home screen. Each card displays the project UPID, client name, document type badge, and net invoice total. A **Copy Link** action on every card generates a shareable `#UPID` hash URL and copies it to clipboard.

**Client Outreach Share Panel**
When viewing an estimate, a sticky bottom bar appears with a live-populated URL input, a **Copy Link** button, and a **Copy Email Template** button that pre-fills a professional outreach email with the client name and estimate link — ready to drop directly into any email client.

**Hash-Based URL Navigation**
Estimates are directly linkable. Opening `index.html#EST-001` auto-navigates to that estimate on load. The browser hash is set and cleared as the user navigates between views.

**Pricing Engine**
Internal cost inputs (labour rates, equipment hire, travel, crew) are stored separately from the client-facing output. A 35% internal tax is applied strictly to labour categories. Expenses are tax-exempt. The client PDF shows only the net invoice total — no internal margins, markups, or line-item costs are ever exposed.

---

## File Structure

```
/
├── index.html           — Full application (UI, logic, PDF builders, data layer)
├── uploads/
│   ├── logo.png         — Brand logo asset (loaded via fetch on init)
│   ├── Delight-VF.ttf   — Primary display typeface (variable font)
│   └── FunnelSans-Light.ttf  — UI body typeface
├── .gitignore
└── README.md
```

> All asset paths in `index.html` are relative (`uploads/logo.png`, `uploads/Delight-VF.ttf`). The application is fully portable — clone the repo and it runs immediately with no path configuration.

---

## Running Locally

The application requires a local HTTP server to enable the `fetch`-based logo loader and clipboard API. Do **not** open `index.html` directly via `file://` in Chrome — the fetch call will be blocked.

**Python (recommended — zero setup):**

```bash
cd "LSC Billing App"
python3 -m http.server 8080
```

Then open [http://localhost:8080](http://localhost:8080) in Chrome.

**Hard-refresh after every update:**
```
⌘ Shift R
```

---

## Deploying to GitHub Pages

Once the repository is on GitHub, enable Pages under **Settings → Pages → Source: main branch / root**. The app will be live at:

```
https://<your-username>.github.io/<repo-name>/
```

No build pipeline required.

---

## Git Initialisation

Run these commands from inside the project folder:

```bash
# 1. Initialise the repository
git init

# 2. Stage all files (respects .gitignore)
git add .

# 3. Initial commit
git commit -m "feat: initial commit — LSC Billing App v1"

# 4. Rename default branch to main
git branch -M main

# 5. Link to your GitHub remote (replace with your actual repo URL)
git remote add origin https://github.com/<your-username>/<repo-name>.git

# 6. Push
git push -u origin main
```

**Subsequent updates:**

```bash
git add index.html
git commit -m "fix: <describe what changed>"
git push
```

---

## Tech Stack

| Layer | Implementation |
|---|---|
| UI & Layout | Vanilla JS · CSS Grid · CSS Custom Properties |
| Data Persistence | `localStorage` (no backend, no database) |
| PDF Export | `window.open` + `document.write` + `window.print` |
| Logo Loading | `fetch` + `FileReader` → Base64 data URI |
| Fonts | `@font-face` with local `.ttf` files via relative path |
| Deployment | Static HTML — GitHub Pages, Netlify, or any web server |

---

## Brand Tokens

| Token | Value | Usage |
|---|---|---|
| `--bg` | `#0E0E0E` | App background |
| `--surface` | `#1C1F24` | Card & panel surfaces |
| `--accent` | `#C0603C` | Terracotta — CTAs, eyebrows, totals |
| `--text` | `#F0EDE8` | Warm white — primary type |
| `--muted` | `rgba(240,237,232,0.42)` | Secondary labels |
| PDF canvas | `#F0EDE8` | Document background |
| PDF accent block | `#E8E2D9` | Estimate / invoice summary block |
| PDF body text | `#252930` | Charcoal — all PDF typography |

---

*Built by LSC Creative · Internal tooling · Not for public distribution.*
