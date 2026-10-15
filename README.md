# NAGPRA Repatriation Database & Workflow Explorer

The Native American Graves Protection and Repatriation Act (NAGPRA) provides a framework for the protection and return of Native American ancestors and cultural items to their descendants and communities. For many Native communities, these ancestors and belongings are not simply collection records; they are connected to relatives, places, cultural continuity, and living responsibilities. Repatriation is also connected to Tribal sovereignty and institutional responsibility. California has a related state law, the California Native American Graves Protection and Repatriation Act (CalNAGPRA).

This project began with research into NAGPRA and the information relationships involved in repatriation, then explored how database design and software could help organize that information. Its workflow concepts are educational models, not a complete account of the requirements under NAGPRA or CalNAGPRA.

The repository brings together the original coursework database, a Python desktop application, a PostgreSQL/Supabase implementation, and a GitHub Pages demonstration. It illustrates ways to structure and navigate workflow information; it does not make cultural or repatriation decisions.

> **Educational demonstration only.** This is not an operational NAGPRA management system and has not been used for actual repatriation cases. The public interface uses synthetic demonstration data and a limited data projection. It is not affiliated with or endorsed by a Tribe, the National Park Service, the Bureau of Indian Affairs, or another government or cultural organization.

## Why This Project Matters

Repatriation involves more than an inventory of items. NAGPRA establishes a process that includes dialogue between covered museums and federal agencies and Native communities; California's CalNAGPRA provides a related state framework. Records may connect ancestors and cultural items, institutional holdings, communities, affiliations, consultations, requests, and transfers. Understanding those relationships was the starting point for this project—not a generic database with a cultural theme added afterward.

The software explores how a relational model, workflow-oriented SQL views, searchable records, and summary reports can help organize information in a complex process. These tools can support information management, but they cannot replace consultation, cultural knowledge, or the decision-making authority of Native communities. For an authoritative overview of the federal program, see the [National Park Service NAGPRA program](https://www.nps.gov/subjects/nagpra/index.htm).

## Research-Informed Design

The initial work was developed for a Database Management course after researching NAGPRA and the associated information-management needs. The relational SQL model represents connections among Indigenous communities, institutions, cultural items, human remains records, institutional holdings, affiliations, consultations, requests, and transfers. Constraints and workflow views provide structure for records and status checkpoints.

The Python Programming final project extended that work into a desktop application using Flet. It imports CSV data exported from a relational database view, organizes records in an in-memory dictionary keyed by Item ID, and supports browsing and multi-field searching. It validates user input when updating community information in the working dataset and generates summary reports counting items by community and category. The application also uses event handlers, conditional logic, loops, file operations, functions, and string manipulation. Flet was selected to explore a GUI framework beyond Tkinter.

The design represents selected information relationships and workflow concepts; it is not a complete model of NAGPRA or CalNAGPRA requirements. It does not determine affiliation, settle questions of cultural authority, or stand in for consultation or community decisions.

## Project Evolution

1. **Database Management coursework — MySQL:** Researched NAGPRA and developed the original relational database, including its records, relationships, and workflow views.
2. **Python Programming final project — Flet:** Built a desktop application around exported database-view data, with browsing, search, validated community updates, and summary reporting. An earlier Tkinter application is also retained in the repository.
3. **Subsequent development — PostgreSQL/Supabase and GitHub Pages:** Extended the database implementation with PostgreSQL/Supabase, SQL workflow views, and a static web demonstration backed by a deliberately limited synthetic-data projection.

## Ethical Considerations & Project Scope

The public demonstration is for learning and presentation, not for managing operational records. It uses synthetic demonstration data and omits sensitive fields from the public-facing projection. Do not add confidential records, sensitive cultural knowledge, real contact details, restricted locations, or other non-public information to the demonstration.

Technical controls such as restricted projections, access policies, and least-privilege permissions can reduce exposure; they do not by themselves establish culturally appropriate data governance. This project does not replace consultation, community authority or decision-making, cultural protocols, or institutional responsibilities. It has not been developed for or endorsed by a Tribe or government organization.

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
│   ├── migrations/            # timestamped Supabase migrations
│   └── source_sql/            # numbered SQL source files
├── desktop/
│   ├── flet/                  # Python/Flet application
│   └── tkinter/               # earlier Tkinter application
├── sample-data/
├── documentation/
├── legacy/mysql/              # original MySQL coursework files
└── SETUP.md                   # step-by-step Supabase + GitHub Pages deployment
```

## Technical highlights

- **12-table relational model** for communities, institutions, contacts, cultural items, remains profiles, sites, holdings, affiliations, consultations, repatriation requests, and transfers.
- **8 SQL workflow views** for inventory scope, hazards, open consultations, affiliations, unaffiliated backlog, pending requests, pending transfers, and completed transfers.
- **Python/Flet desktop interface** with multi-field search, input validation, CSV-based data handling, community information updates, and summary generation.
- **Supabase/PostgreSQL implementation** with Row Level Security and least-privilege browser access.
- **GitHub Pages UI** built with plain HTML, CSS, and JavaScript; no frontend build step is required.
- **Limited public projection**: the website queries only `portfolio_item`, not the operational schema.

## Quick start

Read **[SETUP.md](SETUP.md)** for the complete deployment sequence. In short:

1. Create a Supabase project.
2. Follow the SQL setup steps in `SETUP.md`.
3. Put the Supabase Project URL and **publishable key** in `docs/js/config.js`.
4. Push the repository to GitHub.
5. Enable GitHub Pages from the `main` branch and `/docs` folder.

The page also works before Supabase is configured: it falls back to the safe static snapshot in `docs/data/demo-items.json`.

## Security note

The original `users.sql` contained hard-coded local MySQL passwords. That file is **not** included in this public package. A redacted role summary is preserved under `legacy/mysql/users_REDACTED.sql`. The Supabase version uses RLS and grants instead.

Do not commit a Supabase `service_role` key or secret key. The browser configuration should use only the project's publishable key (or legacy anon key) with RLS enabled.
