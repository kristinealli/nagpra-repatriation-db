# Deployment Guide: Supabase + GitHub Pages

This guide takes the repository from local files to a live portfolio demo.

## 1. Create the GitHub repository

On GitHub, create a repository named `nagpra-repatriation-db` (or another name you prefer). Do not add a README/license from GitHub if you are uploading this prepared package.

From Terminal, inside this project folder:

```bash
git init
git add .
git commit -m "Build NAGPRA repatriation database portfolio project"
git branch -M main
git remote add origin https://github.com/kristinealli/nagpra-repatriation-db.git
git push -u origin main
```

If you choose a different repository name, also update `repoUrl` in `docs/js/config.js`.

## 2. Create a Supabase project

1. Sign in to Supabase and create a new project.
2. Choose a project name such as `nagpra-repatriation-demo`.
3. Set a strong database password and store it in a password manager. Do **not** put it in this repository.
4. Wait for the project to finish provisioning.

## 3. Create the database

Open **SQL Editor** in the Supabase dashboard. Run these files, in this order:

1. `supabase/01_schema.sql` — creates the relational schema and the sanitized `portfolio_item` table.
2. `supabase/02_workflow_views.sql` — creates the eight workflow/reporting views.
3. `supabase/03_seed.sql` — loads the converted demonstration data from the original coursework seed.
4. `supabase/04_sync_portfolio.sql` — builds the public-safe `portfolio_item` dataset from the relational tables.
5. `supabase/05_security.sql` — enables RLS, locks down core tables, and grants public **SELECT-only** access to `portfolio_item`.

You can confirm the public projection in Table Editor by opening `portfolio_item`.

### Why there is a separate public table

The full schema contains fields that should not be exposed from a public portfolio site: contact data, exact/restricted site information, sensitive notes, storage locations, tracking numbers, and chain-of-custody paths. The web UI therefore reads only a sanitized projection.

## 4. Get the browser-safe Supabase credentials

In your Supabase project, open **Connect** or **Settings → API Keys** and copy:

- Project URL
- Publishable key (older projects may label this the `anon` key)

Do **not** use the `service_role` key or a secret key in GitHub Pages.

Edit `docs/js/config.js`:

```js
window.APP_CONFIG = {
  supabaseUrl: "https://YOUR_PROJECT.supabase.co",
  supabasePublishableKey: "YOUR_PUBLISHABLE_KEY",
  repoUrl: "https://github.com/kristinealli/nagpra-repatriation-db"
};
```

The publishable key is designed to be used in a browser; database permissions are enforced by RLS. The service-role/secret key bypasses RLS and must remain server-side.

## 5. Test locally

From the repository root:

```bash
./serve-local.sh
```

Then open `http://localhost:8000` in your browser.

Look at the small status badge above the table:

- **Live Supabase data** = the database connection is working.
- **Bundled demo snapshot** = config is blank or Supabase could not be reached; the page is using `docs/data/demo-items.json` instead.

Do not test by double-clicking `docs/index.html`; browsers often block local `fetch()` calls from `file://` pages.

## 6. Commit the Supabase configuration

Because a Supabase publishable/anon key is intended for browser clients, it can be present in the deployed JavaScript **only when RLS and least-privilege grants are correctly configured**.

```bash
git add docs/js/config.js
git commit -m "Connect portfolio UI to Supabase"
git push
```

Before pushing, confirm again that the value is a **publishable/anon** key, never `service_role` or a secret key.

## 7. Turn on GitHub Pages

In the GitHub repository:

1. Open **Settings**.
2. Select **Pages**.
3. Under **Build and deployment**, choose **Deploy from a branch**.
4. Choose branch **main**.
5. Choose folder **/docs**.
6. Save.

After deployment, the site will normally be available at:

```text
https://kristinealli.github.io/nagpra-repatriation-db/
```

If your GitHub username or repository name differs, GitHub shows the actual URL in the Pages settings.

## 8. Updating the demo data later

If you change records in the core demo schema through the Supabase SQL Editor, run:

```sql
-- Contents of supabase/04_sync_portfolio.sql
```

again to rebuild the safe public projection. The browser reads only `portfolio_item`.

## 9. Optional next phase: authenticated admin interface

Do not add anonymous browser writes to the operational tables. If you later want the web app to edit records, use Supabase Auth and create explicit RLS policies for authenticated users/roles. Keep the public portfolio view read-only.

## 10. Portfolio checklist

Before linking this from a resume:

- GitHub README renders cleanly.
- GitHub Pages loads on desktop and mobile.
- Status badge says **Live Supabase data**.
- Search and all filters work.
- No real restricted locations, cultural knowledge, personal contacts, credentials, or operational records are in the repo/database.
- Repository is pinned on your GitHub profile.
- Resume links to both the GitHub repo and live demo.
