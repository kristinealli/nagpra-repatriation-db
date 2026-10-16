// GitHub Pages client configuration.
// The Supabase publishable key is intended for browser use when RLS is configured.
// NEVER put a Supabase secret key or service_role key here.

const SUPABASE_URL = "https://lzkwtpudqbcdnlhrdegm.supabase.co";
const SUPABASE_PUBLISHABLE_KEY =
	"sb_publishable_VrZIqHtZjsI-GBEn45a0AA_qEy6H1xG";

window.APP_CONFIG = {
	supabaseUrl: SUPABASE_URL,
	supabasePublishableKey: SUPABASE_PUBLISHABLE_KEY,
	repoUrl: "https://github.com/kristinealli/nagpra-repatriation-db",
};