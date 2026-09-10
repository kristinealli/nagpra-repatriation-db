(() => {
  const state = { all: [], filtered: [], source: 'demo' };
  const els = {
    body: document.querySelector('#records-body'),
    search: document.querySelector('#search'),
    category: document.querySelector('#category-filter'),
    institution: document.querySelector('#institution-filter'),
    affiliation: document.querySelector('#affiliation-filter'),
    count: document.querySelector('#result-count'),
    clear: document.querySelector('#clear-filters'),
    empty: document.querySelector('#empty-state'),
    status: document.querySelector('#connection-status'),
    total: document.querySelector('#metric-total'),
    human: document.querySelector('#metric-human'),
    affiliated: document.querySelector('#metric-affiliated'),
    repo: document.querySelector('#repo-link')
  };

  const categoryLabel = (value) => ({
    human_remains: 'Human remains',
    associated_funerary_object: 'Associated funerary object',
    unassociated_funerary_object: 'Unassociated funerary object',
    sacred_object: 'Sacred object',
    object_of_cultural_patrimony: 'Object of cultural patrimony'
  }[value] || value || 'Unknown');

  const formatDate = (value) => {
    if (!value) return '—';
    const d = new Date(`${value}T00:00:00`);
    return Number.isNaN(d.getTime()) ? value : new Intl.DateTimeFormat('en-US', {year:'numeric', month:'short', day:'numeric'}).format(d);
  };

  const isAffiliated = (item) => (item.communities || '').trim().toLowerCase() !== 'unaffiliated';
  const escapeHtml = (value) => String(value ?? '').replace(/[&<>'"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#039;','"':'&quot;'}[c]));

  async function loadSupabaseLibrary() {
    if (window.supabase?.createClient) return;
    await new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2';
      script.async = true;
      const timeout = setTimeout(() => reject(new Error('Supabase library timed out')), 7000);
      script.onload = () => { clearTimeout(timeout); resolve(); };
      script.onerror = () => { clearTimeout(timeout); reject(new Error('Supabase library failed to load')); };
      document.head.appendChild(script);
    });
  }

  async function loadData() {
    const cfg = window.APP_CONFIG || {};
    if (cfg.repoUrl) els.repo.href = cfg.repoUrl;

    if (cfg.supabaseUrl && cfg.supabasePublishableKey) {
      try {
        await loadSupabaseLibrary();
        const client = window.supabase.createClient(cfg.supabaseUrl, cfg.supabasePublishableKey);
        const { data, error } = await client.from('portfolio_item').select('*').order('item_id');
        if (error) throw error;
        state.all = data || [];
        state.source = 'live';
        setStatus('Live Supabase data', 'live');
        initialize();
        return;
      } catch (err) {
        console.warn('Supabase unavailable; using bundled demo snapshot.', err);
      }
    }

    const response = await fetch('data/demo-items.json');
    if (!response.ok) throw new Error('Could not load bundled demo data.');
    state.all = await response.json();
    state.source = 'demo';
    setStatus('Bundled demo snapshot', 'demo');
    initialize();
  }

  function setStatus(text, mode) {
    els.status.classList.remove('live', 'demo');
    if (mode) els.status.classList.add(mode);
    els.status.querySelector('span:last-child').textContent = text;
  }

  function initialize() {
    populateFilters();
    updateMetrics();
    applyFilters();
  }

  function populateFilters() {
    const categories = [...new Set(state.all.map(i => i.category).filter(Boolean))].sort((a,b)=>categoryLabel(a).localeCompare(categoryLabel(b)));
    const institutions = [...new Set(state.all.map(i => i.institution_name).filter(Boolean))].sort();
    categories.forEach(v => els.category.insertAdjacentHTML('beforeend', `<option value="${escapeHtml(v)}">${escapeHtml(categoryLabel(v))}</option>`));
    institutions.forEach(v => els.institution.insertAdjacentHTML('beforeend', `<option value="${escapeHtml(v)}">${escapeHtml(v)}</option>`));
  }

  function updateMetrics() {
    els.total.textContent = state.all.length;
    els.human.textContent = state.all.filter(i => i.category === 'human_remains').length;
    els.affiliated.textContent = state.all.filter(isAffiliated).length;
  }

  function applyFilters() {
    const q = els.search.value.trim().toLowerCase();
    const category = els.category.value;
    const institution = els.institution.value;
    const affiliation = els.affiliation.value;

    state.filtered = state.all.filter(item => {
      const haystack = [item.item_id, item.item_title, item.category, item.institution_name, item.communities].join(' ').toLowerCase();
      if (q && !haystack.includes(q)) return false;
      if (category && item.category !== category) return false;
      if (institution && item.institution_name !== institution) return false;
      if (affiliation === 'affiliated' && !isAffiliated(item)) return false;
      if (affiliation === 'unaffiliated' && isAffiliated(item)) return false;
      return true;
    });
    render();
  }

  function render() {
    els.body.innerHTML = state.filtered.map(item => {
      const affiliated = isAffiliated(item);
      return `<tr>
        <td><span class="item-title">${escapeHtml(item.item_title || 'Untitled record')}</span><span class="item-id">ID ${escapeHtml(item.item_id)}</span></td>
        <td>${escapeHtml(categoryLabel(item.category))}</td>
        <td>${escapeHtml(item.institution_name)}</td>
        <td><span class="pill ${affiliated ? '' : 'unaffiliated'}">${escapeHtml(item.communities || 'Unaffiliated')}</span></td>
        <td>${escapeHtml(formatDate(item.holding_since))}</td>
      </tr>`;
    }).join('');
    els.count.textContent = `${state.filtered.length} ${state.filtered.length === 1 ? 'record' : 'records'}`;
    els.empty.hidden = state.filtered.length !== 0;
  }

  ['input','change'].forEach(eventName => {
    els.search.addEventListener(eventName, applyFilters);
    els.category.addEventListener(eventName, applyFilters);
    els.institution.addEventListener(eventName, applyFilters);
    els.affiliation.addEventListener(eventName, applyFilters);
  });
  els.clear.addEventListener('click', () => {
    els.search.value = '';
    els.category.value = '';
    els.institution.value = '';
    els.affiliation.value = '';
    applyFilters();
    els.search.focus();
  });

  loadData().catch(err => {
    console.error(err);
    setStatus('Data failed to load', 'demo');
    els.empty.hidden = false;
    els.empty.textContent = 'The demo data could not be loaded. Serve this folder through a local web server rather than opening index.html directly.';
  });
})();
