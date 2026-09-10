# Supabase deployment files

This directory is ready for the Supabase GitHub integration.

- `config.toml` is committed configuration for the Supabase CLI/integration.
- `migrations/` contains production migrations. Supabase applies new files in timestamp order.
- `source_sql/` preserves the human-readable numbered SQL files used to build the migrations. These files are reference material only and are not auto-executed by the GitHub integration.

For this portfolio project, demonstration data is intentionally included in a production migration because the deployed site is itself a public demo. It contains synthetic/demo records only.
