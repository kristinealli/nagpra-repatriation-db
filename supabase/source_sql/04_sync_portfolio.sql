-- Build the sanitized portfolio table from the relational data.
-- Run after 03_seed.sql, and re-run after you intentionally change demo data.
-- Sensitive fields are not copied into portfolio_item.

begin;
truncate table portfolio_item;

insert into portfolio_item (item_id, item_title, category, institution_name, communities, holding_since)
select
  ci.item_id,
  ci.item_title,
  ci.item_category,
  i.institution_name,
  coalesce(string_agg(distinct c.community_name, '; ' order by c.community_name), 'Unaffiliated') as communities,
  h.holding_start_date
from cultural_item ci
join holding h
  on h.item_id = ci.item_id
 and h.holding_current = 1
join institution i
  on i.institution_id = h.institution_id
left join affiliation a
  on a.item_id = ci.item_id
left join community c
  on c.community_id = a.community_id
group by ci.item_id, ci.item_title, ci.item_category, i.institution_name, h.holding_start_date
order by ci.item_id;

commit;
