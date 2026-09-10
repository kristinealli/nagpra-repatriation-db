-- Supabase/PostgreSQL adaptation of the original workflow views.

-- NAGPRA Workflow Database Views

-- 1) Human Remains Inventory
-- Shows all human remains items with their current holding information
CREATE
OR REPLACE VIEW vw_hr_inventory_scope AS
SELECT
    ci.item_id                    AS "Item ID",
    ci.item_title                 AS "Item Title",
    ci.item_category              AS "Category",
    i.institution_id              AS "Institution ID",
    i.institution_name            AS "Institution Name",
    h.holding_type                AS "Holding Type",
    h.holding_owns_title          AS "Owns Title?",
    h.holding_rop                 AS "ROP?",
    ci.item_created_at            AS "Date Created",
    h.holding_start_date          AS "Holding Since Date",
    h.holding_storage_location    AS "Storage Location"
FROM
    cultural_item ci
    JOIN holding h
        ON h.item_id = ci.item_id
        AND h.holding_current = 1
    JOIN institution i
        ON i.institution_id = h.institution_id
WHERE
    ci.item_category = 'human_remains';

-- 2) Inventory of Hazardous Items
-- Shows items that are hazardous or have hazard notes
CREATE OR REPLACE VIEW vw_hr_hazards AS
SELECT
    ci.item_id                    AS "Item ID",
    ci.item_title                 AS "Item Title",
    ci.item_category              AS "Category",
    ci.item_haz_treated           AS "Hazardous?",
    ci.item_haz_notes             AS "Hazard Notes",
    i.institution_name            AS "Institution Name",
    h.holding_storage_location    AS "Storage Location"
FROM
    cultural_item ci
    JOIN holding h
        ON h.item_id = ci.item_id
        AND h.holding_current = 1
    JOIN institution i
        ON i.institution_id = h.institution_id
WHERE
    (ci.item_haz_treated = 1 OR ci.item_haz_notes IS NOT NULL)
    AND ci.item_category IN (
        'human_remains',
        'associated_funerary_object',
        'unassociated_funerary_object'
    );

-- 3) Open Consultations for Human Remains
-- Shows all consultations for human remains that are not complete
CREATE OR REPLACE VIEW vw_hr_open_consultations AS
SELECT
    c.consult_id                  AS "Consultation ID",
    ci.item_id                    AS "Item ID",
    ci.item_title                 AS "Item Title",
    c.consult_status              AS "Status",
    c.consult_started_on          AS "Started On",
    c.consult_last_meeting        AS "Last Meeting",
    comm.community_name           AS "Community",
    inst.institution_name         AS "Institution",
    c.consult_notes               AS "Notes"
FROM
    consultation c
    JOIN cultural_item ci 
        ON ci.item_id = c.item_id
    JOIN community comm 
        ON comm.community_id = c.community_id
    JOIN institution inst 
        ON inst.institution_id = c.institution_id
WHERE
    ci.item_category = 'human_remains'
    AND c.consult_status <> 'complete';

-- 4) Community Affiliations for Human Remains
-- Shows all community affiliations for human remains items
CREATE OR REPLACE VIEW vw_hr_affiliations AS
SELECT
    a.affiliation_id              AS "Affiliation ID",
    ci.item_id                    AS "Item ID",
    ci.item_title                 AS "Item Title",
    a.affiliation_type            AS "Affiliation Type",
    a.affiliation_basis           AS "Basis",
    a.affiliation_determined      AS "Date Determined",
    comm.community_name           AS "Community"
FROM
    affiliation a
    JOIN cultural_item ci
        ON ci.item_id = a.item_id
    JOIN community comm
        ON comm.community_id = a.community_id
WHERE
    ci.item_category = 'human_remains';

-- 5) Unaffiliated Human Remains Backlog
-- Shows human remains items that have no community affiliations
CREATE OR REPLACE VIEW vw_hr_unaffiliated_backlog AS
SELECT
    ci.item_id                    AS "Item ID",
    ci.item_title                 AS "Item Title",
    i.institution_name            AS "Institution Name",
    h.holding_storage_location    AS "Storage Location",
    ci.item_created_at            AS "Date Created"
FROM
    cultural_item ci
    JOIN holding h
        ON h.item_id = ci.item_id
        AND h.holding_current = 1
    JOIN institution i
        ON i.institution_id = h.institution_id
    LEFT JOIN affiliation a
        ON a.item_id = ci.item_id
WHERE
    ci.item_category = 'human_remains'
    AND a.item_id IS NULL;

-- 6) Pending Repatriation Requests
-- Shows all repatriation requests that are still pending
CREATE OR REPLACE VIEW vw_pending_requests AS
SELECT
    rr.request_id                 AS "Request ID",
    ci.item_id                    AS "Item ID",
    ci.item_title                 AS "Item Title",
    rr.request_received_on        AS "Received On",
    rr.request_acknowledged_on    AS "Acknowledged On",
    rr.request_decision           AS "Decision",
    comm.community_name           AS "Requesting Community",
    inst.institution_name         AS "Institution",
    h.holding_type                AS "Holding Type",
    h.holding_owns_title          AS "Owns Title?",
    h.holding_rop                 AS "Right of Possession?"
FROM
    repatriation_request rr
    JOIN cultural_item ci
        ON ci.item_id = rr.item_id
    JOIN community comm
        ON comm.community_id = rr.requesting_community_id
    JOIN holding h
        ON h.item_id = rr.item_id
        AND h.holding_current = 1
    JOIN institution inst
        ON inst.institution_id = h.institution_id
WHERE
    rr.request_decision = 'pending';

-- 7) Pending Transfers
-- Shows approved repatriation requests that haven't been transferred yet
CREATE OR REPLACE VIEW vw_pending_transfers AS
SELECT
    rr.request_id                 AS "Request ID",
    ci.item_id                    AS "Item ID",
    ci.item_title                 AS "Item Title",
    rr.request_decision_on        AS "Approval Date",
    req_comm.community_name       AS "To Community",
    inst.institution_name         AS "From institution",
    t.transfer_scheduled_on       AS "Scheduled Transfer"
FROM
    repatriation_request rr
    JOIN cultural_item ci
        ON ci.item_id = rr.item_id
    JOIN community req_comm
        ON req_comm.community_id = rr.requesting_community_id
    JOIN holding h
        ON h.item_id = rr.item_id
        AND h.holding_current = 1
    JOIN institution inst
        ON inst.institution_id = h.institution_id
    LEFT JOIN transfer t
        ON t.item_id = rr.item_id
        AND t.transfer_completed_on IS NULL
WHERE
    rr.request_decision = 'approved'
    AND NOT EXISTS (
        SELECT 1
        FROM transfer tx
        WHERE tx.item_id = rr.item_id
        AND tx.transfer_completed_on IS NOT NULL
    );

-- 8) Completed Transfers
-- Shows all transfers that have been completed
CREATE OR REPLACE VIEW vw_completed_transfers AS
SELECT
    t.transfer_id                 AS "Transfer ID",
    ci.item_id                    AS "Item ID",
    ci.item_title                 AS "Item Title",
    fi.institution_name           AS "From institution",
    cto.community_name            AS "To Community",
    t.transfer_scheduled_on       AS "Scheduled On",
    t.transfer_completed_on       AS "Completed On",
    t.transfer_transport          AS "Transport Method",
    t.transfer_location           AS "Location",
    t.transfer_tracking_number    AS "Tracking Number"
FROM
    transfer t
    JOIN cultural_item ci
        ON ci.item_id = t.item_id
    JOIN institution fi
        ON fi.institution_id = t.from_institution_id
    JOIN community cto
        ON cto.community_id = t.to_community_id
WHERE
    t.transfer_completed_on IS NOT NULL;
