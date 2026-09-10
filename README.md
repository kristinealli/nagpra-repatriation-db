# NAGPRA Repatriation Database & Workflow Explorer

A portfolio-ready version of a database/programming coursework project that models a NAGPRA repatriation workflow and demonstrates relational data modeling, SQL views, Python desktop UI work, secure data exposure, and a static web client.

> **Portfolio / educational use only.** This repository is not an official NAGPRA system. The public GitHub Pages interface is intentionally limited to synthetic/demo data and excludes sensitive operational fields such as contact details, exact site coordinates, sensitive notes, storage locations, tracking information, and chain-of-custody documents.

## What is in this repository

```text
nagpra-repatriation-db/
├── docs/                       # GitHub Pages frontend
│   ├── index.html
│   ├── css/styles.css
│   ├── js/config.js
│   ├── js/app.js
│   └── data/demo-items.json   # safe fallback snapshot
├── supabase/                  # PostgreSQL/Supabase deployment scripts
│   ├── 01_schema.sql
│   ├── 02_workflow_views.sql
│   ├── 03_seed.sql
│   ├── 04_sync_portfolio.sql
│   └── 05_security.sql
├── desktop/
│   ├── flet/                  # later Python/Flet application
│   └── tkinter/               # earlier Tkinter application
├── sample-data/
├── documentation/
├── legacy/mysql/              # original MySQL coursework files
└── SETUP.md                   # step-by-step Supabase + GitHub Pages deployment
```

## Technical highlights

- **12-table relational model** for communities, institutions, contacts, cultural items, remains profiles, sites, holdings, affiliations, consultations, repatriation requests, and transfers.
- **8 SQL workflow views** for inventory scope, hazards, open consultations, affiliations, unaffiliated backlog, pending requests, pending transfers, and completed transfers.
- **Python/Flet desktop interface** with multi-field search, validation, CSV persistence, and summary generation.
- **Supabase/PostgreSQL deployment layer** with Row Level Security and least-privilege browser access.
- **GitHub Pages UI** built with plain HTML, CSS, and JavaScript; no frontend build step is required.
- **Safe public projection**: the website queries only `portfolio_item`, not the operational schema.

## Quick start

Read **[SETUP.md](SETUP.md)** for the complete deployment sequence. In short:

1. Create a Supabase project.
2. Run the five SQL files in `supabase/` in numeric order.
3. Put the Supabase Project URL and **publishable key** in `docs/js/config.js`.
4. Push the repository to GitHub.
5. Enable GitHub Pages from the `main` branch and `/docs` folder.

The page also works before Supabase is configured: it falls back to the safe static snapshot in `docs/data/demo-items.json`.

## Security note

The original `users.sql` contained hard-coded local MySQL passwords. That file is **not** included in this public package. A redacted role summary is preserved under `legacy/mysql/users_REDACTED.sql`. The Supabase version uses RLS and grants instead.

Do not commit a Supabase `service_role` key or secret key. The browser configuration should use only the project's publishable key (or legacy anon key) with RLS enabled.

## Original project lineage

The database project was later extended into a Python UI that reads exported database data into an in-memory dictionary, supports multi-field search and record updates, and writes summary output. The GitHub Pages version adds a public portfolio presentation layer without exposing the sensitive fields in the original schema.
