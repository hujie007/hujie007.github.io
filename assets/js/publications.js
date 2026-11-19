const search = document.querySelector('#pub-search');
if (search) {
  let groupFilter = 'all';
  const topic = document.querySelector('#topic');
  const articles = [...document.querySelectorAll('.publication')];
  const buttons = [...document.querySelectorAll('.filter')];
  const reset = document.querySelector('#reset-filters');
  function applyFilters() {
    let count = 0;
    const query = search.value.toLowerCase().trim();
    for (const article of articles) {
      const groupMatches = groupFilter === 'all' || article.closest('.publication-group').dataset.group === groupFilter;
      const topicMatches = topic.value === 'all' || article.dataset.areas.split(' ').includes(topic.value);
      const visible = groupMatches && topicMatches && article.textContent.toLowerCase().includes(query);
      article.hidden = !visible;
      if (visible) count++;
    }
    document.querySelectorAll('.publication-group').forEach(group => {
      group.hidden = ![...group.querySelectorAll('.publication')].some(article => !article.hidden);
    });
    document.querySelector('#result-count').textContent = `${count} ${count === 1 ? 'paper' : 'papers'}`;
    document.querySelector('#empty-state').hidden = count > 0;
    reset.hidden = groupFilter === 'all' && topic.value === 'all' && !query;
  }
  function selectGroup(value) {
    groupFilter = value;
    buttons.forEach(button => {
      const active = button.dataset.filter === value;
      button.classList.toggle('active', active);
      button.setAttribute('aria-pressed', String(active));
    });
    applyFilters();
  }
  function clearFilters() {
    search.value = '';
    topic.value = 'all';
    selectGroup('all');
  }
  buttons.forEach(button => button.addEventListener('click', () => selectGroup(button.dataset.filter)));
  search.addEventListener('input', applyFilters);
  topic.addEventListener('change', applyFilters);
  reset.addEventListener('click', () => { clearFilters(); search.focus(); });
  document.addEventListener('keydown', event => {
    if (event.key === '/' && !['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName) && !document.querySelector('dialog[open]')) {
      event.preventDefault(); search.focus();
    }
  });
  function revealHash() {
    if (location.hash.startsWith('#paper-')) {
      clearFilters();
      requestAnimationFrame(() => document.getElementById(location.hash.slice(1))?.scrollIntoView({block: 'start'}));
    }
  }
  window.addEventListener('hashchange', revealHash);
  applyFilters();
  revealHash();
}

const citationDialog = document.querySelector('#citation-dialog');
if (citationDialog) {
  let records = null;
  let bibliographyUrl = null;
  const escapeBibTeX = text => text.replaceAll('&', '\\&').replaceAll('%', '\\%').replaceAll('_', '\\_').replaceAll('#', '\\#');
  document.querySelectorAll('.cite-button').forEach(button => button.addEventListener('click', async () => {
    try {
      records ??= await fetch(document.querySelector('#publication-list').dataset.source).then(response => {
        if (!response.ok) throw new Error('Citation records unavailable');
        return response.json();
      });
      const paper = records.find(record => record.id === Number(button.dataset.id));
      const authors = paper.authors.replace(/[†*]/g, '').replace(', et al.', ', others').split(', ').map(name => {
        if (name === 'others') return name;
        if (name.endsWith('La Cava')) return 'La Cava, ' + name.slice(0, -8).trim();
        const parts = name.split(' '); const last = parts.pop(); return `${last}, ${parts.join(' ')}`;
      }).join(' and ');
      const fields = [['title', escapeBibTeX(paper.title)], ['author', escapeBibTeX(authors)], ['year', paper.year]];
      if (paper.venue) fields.push(['journal', escapeBibTeX(paper.venue)]);
      if (paper.detail) fields.push(['note', escapeBibTeX(paper.detail)]);
      if (paper.url) fields.push(['url', paper.url]);
      const type = paper.status === 'Published & accepted' ? 'article' : 'unpublished';
      const citation = `@${type}{hu${paper.year}paper${paper.id},\n` + fields.map(([key, value]) => `  ${key} = {${value}}`).join(',\n') + '\n}';
      document.querySelector('#citation-text').textContent = citation;
      document.querySelector('#copy-status').textContent = '';
      if (bibliographyUrl) URL.revokeObjectURL(bibliographyUrl);
      bibliographyUrl = URL.createObjectURL(new Blob([citation], {type: 'application/x-bibtex'}));
      const download = document.querySelector('#download-citation');
      download.href = bibliographyUrl; download.download = `hu-${paper.year}-${paper.id}.bib`;
      citationDialog.showModal();
    } catch {
      document.querySelector('#citation-text').textContent = 'Citation could not be loaded. Please consult the downloadable CV.';
      citationDialog.showModal();
    }
  }));
  document.querySelector('#close-citation').addEventListener('click', () => citationDialog.close());
  citationDialog.addEventListener('click', event => {
    if (event.target !== citationDialog) return;
    const rectangle = citationDialog.getBoundingClientRect();
    if (event.clientX < rectangle.left || event.clientX > rectangle.right || event.clientY < rectangle.top || event.clientY > rectangle.bottom) citationDialog.close();
  });
  document.querySelector('#copy-citation').addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(document.querySelector('#citation-text').textContent);
      document.querySelector('#copy-status').textContent = 'Copied to clipboard.';
    } catch {
      document.querySelector('#copy-status').textContent = 'Use Download .bib, or select the citation text to copy it.';
    }
  });
}
