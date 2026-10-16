# NAGPRA Repatriation Database & Workflow Explorer

The Native American Graves Protection and Repatriation Act (NAGPRA) provides a framework for the protection and return of Native American ancestors and cultural items to their descendants and communities. For many Native communities, these ancestors and belongings are not simply collection records; they are connected to relatives, places, cultural continuity, and living responsibilities. Repatriation is also connected to Tribal sovereignty and institutional responsibility. California has a related state law, the California Native American Graves Protection and Repatriation Act (CalNAGPRA).

This project began with research into NAGPRA and the information relationships involved in repatriation, then explored how database design and software could help organize that information. Its workflow concepts are educational models, not a complete account of the requirements under NAGPRA or CalNAGPRA.

The repository brings together the original coursework database, a Python desktop application, a PostgreSQL/Supabase implementation, and a GitHub Pages demonstration. It illustrates ways to structure and navigate workflow information; it does not make cultural or repatriation decisions.

> **Educational demonstration only.** This is not an operational NAGPRA management system and has not been used for actual repatriation cases. The public interface uses synthetic demonstration data and a limited data projection. It is not affiliated with or endorsed by a Tribe, the National Park Service, the Bureau of Indian Affairs, or another government or cultural organization.

## Why This Project Matters

Repatriation involves more than an inventory of items. NAGPRA applies to federal agencies and museums that meet the law's criteria, and establishes a process that includes dialogue with Native communities; California's CalNAGPRA provides a related state framework. The coursework report also describes the Bureau of Indian Affairs' work with Tribal communities in identifying holdings, consultation, and repatriation. It situates this recordkeeping work in an ongoing context: as of 2024, the report notes that thousands of ancestors and tens of thousands of funerary objects had been returned, while many more remained in institutional collections.

Records may connect ancestors and cultural items, institutional holdings, communities, affiliations, consultations, requests, and transfers. Understanding those relationships was the starting point for this project—not a generic database with a cultural theme added afterward.

The software explores how a relational model, workflow-oriented SQL views, searchable records, and summary reports can help organize information in a complex process. These tools can support information management, but they cannot replace consultation, cultural knowledge, or the decision-making authority of Native communities. For an authoritative overview of the federal program, see the [National Park Service NAGPRA program](https://www.nps.gov/subjects/nagpra/index.htm).

## Workflow Context and Database Views

The National Park Service describes an eight-step process for museums and federal agencies handling Native American human remains and associated funerary objects. In brief: (1) compile an itemized list; (2) initiate consultation and invite consulting parties; (3) consult on identifications and document responses; (4) complete and submit an inventory by the applicable deadline; (5) submit a notice of inventory completion for Federal Register publication, no later than six months after completing the inventory; (6) receive and consider eligible repatriation requests after publication; (7) provide written responses within 90 days; and (8) issue a written repatriation statement within 90 days. Requirements and deadlines depend on the applicable regulations and circumstances. See the [National Park Service’s current human-remains process](https://www.nps.gov/subjects/nagpra/repatriation-of-human-remains.htm) and [43 CFR Part 10](https://www.ecfr.gov/current/title-43/subtitle-A/part-10) for authoritative details.

The project’s SQL views organize selected records that may inform workflow review; they do not perform the steps, calculate legal deadlines, establish eligibility, or make determinations. Several views are specifically scoped to human remains.

| SQL view                     | Information organized                                                                                    |
| ---------------------------- | -------------------------------------------------------------------------------------------------------- |
| `vw_hr_inventory_scope`      | Human-remains records with current holding and selected institutional, legal-status, and storage fields. |
| `vw_hr_hazards`              | Items with known or noted potential hazards for handling review.                                         |
| `vw_hr_open_consultations`   | Open human-remains consultations, including status, meeting dates, and involved parties.                 |
| `vw_hr_affiliations`         | Recorded human-remains affiliation determinations, including type, basis, date, and community.           |
| `vw_hr_unaffiliated_backlog` | Human-remains records without a recorded affiliation, for follow-up review.                              |
| `vw_pending_requests`        | Pending repatriation requests, requesting community, current holding institution, and decision status.   |
| `vw_pending_transfers`       | Approved requests with no completed transfer recorded and available scheduling information.              |
| `vw_completed_transfers`     | Completed transfer records, including parties, dates, and selected logistics.                            |

These workflow views can include operational information and are not the public demo dataset. Public access is limited to the separate `portfolio_item` projection.

## Research-Informed Design

The initial work was developed for a Database Management course after researching NAGPRA and the associated information-management needs. The accompanying project report documented the data dictionary and the rationale for organizing connected records rather than treating each catalog item in isolation. The relational SQL model represents connections among Indigenous communities, institutions, cultural items, human remains records, institutional holdings, affiliations, consultations, requests, and transfers.

The model groups related information into four areas:

- **People and organizations:** Community records represent Tribes and Native Hawaiian organizations; Institution records represent museums, universities, and agencies; Contact records can link people and roles to either.
- **Catalog and provenance:** CulturalItem represents the record category, including human remains, funerary objects, sacred objects, and objects of cultural patrimony. RemainsProfile stores additional human-remains details in a one-to-one relationship. DiscoverySite and the ItemSite bridge support links between items and findspots or reported and probable origins, including many-to-many relationships.
- **Holdings and affiliation:** Holding records track possession, control, or custody over time, along with acquisition and selected title or right-of-possession fields. Affiliation records store a lineal or cultural determination, its basis, date, and associated community.
- **Consultation and repatriation workflow:** Consultation records connect a community, institution, and item; RepatriationRequest records a community's formal request; Transfer records selected details when an approved return is carried out.

Hazard indicators and sensitive-site fields support careful information management, while workflow views organize selected inventory, hazard, consultation, affiliation, request, and transfer records for review. These structures organize information; they do not make determinations or carry out repatriation.

The coursework report drew on National Park Service NAGPRA program and database materials, 43 CFR Part 10, the 2023 NAGPRA Final Rule, and institutional collections-safety references. See the [National Park Service NAGPRA program](https://www.nps.gov/subjects/nagpra/index.htm), [43 CFR Part 10](https://www.ecfr.gov/current/title-43/subtitle-A/part-10), and the [2023 Final Rule](https://www.federalregister.gov/documents/2023/12/13/2023-27040/native-american-graves-protection-and-repatriation-act-systematic-processes-for-disposition-or) for federal reference material.

### References cited in the coursework report

- “Chapter 24: Collections-Based Hazards.” _Smithsonian Institution Safety Manual_, Office of Safety, Health, and Environmental Management (OSHEM), Smithsonian Institution, 9 June 2011. PDF. Accessed 19 Aug. 2025.
- “Compliance.” [Native American Graves Protection and Repatriation Act](https://www.nps.gov/subjects/nagpra/compliance.htm), National NAGPRA Program, National Park Service, U.S. Department of the Interior, updated 4 Oct. 2024. Web. Accessed 19 Aug. 2025.
- “Consultation.” _Consultation + Repatriation Process_, UC Santa Barbara NAGPRA, University of California, Santa Barbara, updated 2025. Web. Accessed 19 Aug. 2025.
- “Databases.” [Native American Graves Protection and Repatriation Act](https://www.nps.gov/subjects/nagpra/databases.htm), National NAGPRA Program, National Park Service, U.S. Department of the Interior, updated 3 June 2024. Web. Accessed 20 Aug. 2025.
- “Glossary.” [Native American Graves Protection and Repatriation Act](https://www.nps.gov/subjects/nagpra/glossary.htm), National NAGPRA Program, National Park Service, U.S. Department of the Interior, updated 12 Jan. 2024. Web. Accessed 19 Aug. 2025.
- “Native American Graves Protection and Repatriation Act Systematic Processes for Disposition or Repatriation of Native American Human Remains, Funerary Objects, Sacred Objects, and Objects of Cultural Patrimony.” [_Federal Register_](https://www.federalregister.gov/documents/2023/12/13/2023-27040/native-american-graves-protection-and-repatriation-act-systematic-processes-for-disposition-or), vol. 88, no. 238, 13 Dec. 2023, pp. 86452–86540. Web. Accessed 18 Aug. 2025.
- “Part 10 — Native American Graves Protection and Repatriation Regulations.” [e-CFR](https://www.ecfr.gov/current/title-43/subtitle-A/part-10), Title 43, Subtitle A, Part 10, updated as of 15 Aug. 2025, Office of the Secretary of the Interior, U.S. Government Publishing Office. Web. Accessed 19 Aug. 2025.
- “Repatriation of Human Remains.” [Native American Graves Protection and Repatriation Act](https://www.nps.gov/subjects/nagpra/repatriation-of-human-remains.htm), National NAGPRA Program, National Park Service, U.S. Department of the Interior, updated 2025. Web. Accessed 20 Aug. 2025.
- “Repatriation Policy.” _National Museum of the American Indian Repatriation Policy_, adopted 19 June 2020; revised June 2022, National Museum of the American Indian, Smithsonian Institution. PDF. Accessed 19 Aug. 2025.

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
- **8 SQL workflow views** for human-remains inventory scope, hazard flags, open consultations, affiliations, unaffiliated backlog, pending requests, pending transfers, and completed transfers.
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
