-- Public portfolio security for Supabase.
-- Run after schema/seed/sync.
-- Core relational tables stay private; only sanitized portfolio_item is readable by the website.

begin;

-- Enable RLS everywhere in the exposed public schema.
alter table community enable row level security;
alter table institution enable row level security;
alter table contact enable row level security;
alter table cultural_item enable row level security;
alter table remains_profile enable row level security;
alter table discovery_site enable row level security;
alter table item_site enable row level security;
alter table holding enable row level security;
alter table affiliation enable row level security;
alter table consultation enable row level security;
alter table repatriation_request enable row level security;
alter table transfer enable row level security;
alter table portfolio_item enable row level security;

-- Remove client access to operational tables. No client policies are created on them.
revoke all on table community, institution, contact, cultural_item, remains_profile,
  discovery_site, item_site, holding, affiliation, consultation,
  repatriation_request, transfer from anon, authenticated;

-- The browser gets SELECT-only access to the sanitized projection table.
revoke all on table portfolio_item from anon, authenticated;
grant select on table portfolio_item to anon, authenticated;

drop policy if exists "Portfolio demo is publicly readable" on portfolio_item;
create policy "Portfolio demo is publicly readable"
  on portfolio_item
  for select
  to anon, authenticated
  using (true);

-- Workflow views are useful in the SQL editor, but should not be exposed to browser roles.
revoke all on table vw_hr_inventory_scope, vw_hr_hazards, vw_hr_open_consultations,
  vw_hr_affiliations, vw_hr_unaffiliated_backlog, vw_pending_requests,
  vw_pending_transfers, vw_completed_transfers from anon, authenticated;

commit;
