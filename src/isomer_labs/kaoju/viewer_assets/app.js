const escapeHtml = (value) => value.replace(/[&<>"']/g, (char) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
const renderMarkdown = (source) => {
  const safe = escapeHtml(source);
  return safe.split('\n').map((line) => {
    const heading = /^(#{1,6})\s+(.+)$/.exec(line);
    if (heading) return `<h${heading[1].length}>${heading[2]}</h${heading[1].length}>`;
    if (line.startsWith('```')) return '<hr>';
    return line ? `<p>${line.replace(/`([^`]+)`/g, '<code>$1</code>')}</p>` : '';
  }).join('\n');
};
const showPage = async (path) => {
  const response = await fetch(`data/${path}`);
  if (!response.ok) throw new Error(`Cannot load ${path}: ${response.status}`);
  document.querySelector('#content').innerHTML = renderMarkdown(await response.text());
};
const start = async () => {
  const response = await fetch('data/wiki.json');
  if (!response.ok) throw new Error(`Cannot load wiki manifest: ${response.status}`);
  const manifest = await response.json();
  const pages = manifest.sections.pages;
  document.querySelector('#status').textContent = `${pages.length} checked pages · ${manifest.source_fingerprint}`;
  const nav = document.querySelector('#pages');
  pages.forEach((page) => {
    const button = document.createElement('button');
    button.textContent = page.title || page.path;
    button.addEventListener('click', () => showPage(page.path).catch(fail));
    nav.appendChild(button);
  });
  if (pages.length) await showPage(pages[0].path);
};
const fail = (error) => { document.querySelector('#status').textContent = error.message; };
start().catch(fail);
