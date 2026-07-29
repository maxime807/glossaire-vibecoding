import re
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GLOSSARY_PATH = os.path.join(BASE_DIR, 'glossaire_formation_vibe_coding.md')
OUTPUT_PATH = os.path.join(BASE_DIR, 'glossaire_interactive.html')
INDEX_PATH = os.path.join(BASE_DIR, 'index.html')

with open(GLOSSARY_PATH, 'r', encoding='utf-8') as f:
    lines = f.readlines()

table_lines = [l.strip() for l in lines if l.strip().startswith('|')]
data_rows = []
categories_set = set()
alphabet_set = set()

for line in table_lines[2:]:
    parts = [p.strip() for p in line.split('|')[1:-1]]
    if len(parts) >= 5:
        word_raw, statut, category, definition, ref = parts[0], parts[1], parts[2], parts[3], parts[4]
        word = re.sub(r'\*\*(.*?)\*\*', r'\1', word_raw)
        cat_clean = category.replace('`', '').strip()
        
        mod_match = re.search(r'(M[1-4])', ref)
        mod_code = mod_match.group(1) if mod_match else "Autre"
        
        categories_set.add(cat_clean)
        
        first_char = word.strip().lstrip('.').lstrip('(')[0].upper()
        if first_char.isalpha():
            alphabet_set.add(first_char)
        
        data_rows.append({
            'id': len(data_rows) + 1,
            'word': word,
            'statut': statut.replace('`', ''),
            'category': cat_clean,
            'definition': definition,
            'ref': ref,
            'module': mod_code
        })

categories_list = sorted(list(categories_set))
alphabet_list = sorted(list(alphabet_set))
terms_json = json.dumps(data_rows, ensure_ascii=False)

html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
  <title>Vibe Coding — Glossaire Interactif</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800;900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --color-brand-purple: #6634D9;
      --color-brand-fig: #18093B;
      --color-brand-sunny: #FFFF77;
      --color-brand-pink: #FFB2B2;
      --color-pink-20: #FCF1F0;
      --color-bg-light: #F8FAFC;
      --color-card-bg: #FFFFFF;
      --color-border: #E2E8F0;
      --color-text-dark: #18093B;
      --color-text-muted: #64748B;
      --font-main: 'Basic Sans Alt', 'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-tap-highlight-color: transparent;
    }}

    body {{
      font-family: var(--font-main);
      background-color: var(--color-bg-light);
      color: var(--color-text-dark);
      line-height: 1.5;
      padding: 0;
      margin: 0;
    }}

    .app-viewport {{
      width: 100%;
      max-width: 960px;
      margin: 0 auto;
      padding: 1rem 1rem 3rem 1rem;
    }}

    @media (min-width: 640px) {{
      .app-viewport {{
        padding: 2rem 1.5rem 4rem 1.5rem;
      }}
    }}

    header {{
      background: var(--color-brand-fig);
      color: #FFFFFF;
      padding: 1.5rem 1.25rem;
      border: 3px solid var(--color-brand-fig);
      box-shadow: 4px 4px 0px var(--color-brand-purple);
      margin-bottom: 1.25rem;
    }}

    .header-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.5rem;
    }}

    .brand-badge {{
      background: var(--color-brand-sunny);
      color: var(--color-brand-fig);
      font-weight: 900;
      font-size: 0.75rem;
      padding: 0.25rem 0.6rem;
      border: 1px solid var(--color-brand-fig);
      text-transform: uppercase;
    }}

    h1 {{
      font-size: clamp(1.5rem, 5vw, 2.2rem);
      font-weight: 900;
      line-height: 1.15;
      text-transform: uppercase;
      letter-spacing: -0.02em;
    }}

    .header-desc {{
      margin-top: 0.4rem;
      font-size: 0.95rem;
      font-weight: 600;
      color: var(--color-brand-sunny);
    }}

    .search-filter-section {{
      background: #FFFFFF;
      border: 2px solid var(--color-brand-fig);
      box-shadow: 4px 4px 0px var(--color-brand-fig);
      padding: 1.25rem;
      margin-bottom: 1.25rem;
      display: flex;
      flex-direction: column;
      gap: 0.85rem;
    }}

    .search-box {{
      position: relative;
      width: 100%;
    }}

    .search-input {{
      width: 100%;
      padding: 0.85rem 1rem 0.85rem 2.75rem;
      font-family: var(--font-main);
      font-size: 1rem;
      font-weight: 600;
      color: var(--color-brand-fig);
      background: #FFFFFF;
      border: 2px solid var(--color-brand-fig);
      outline: none;
      transition: border-color 0.2s, box-shadow 0.2s;
    }}

    .search-input:focus {{
      border-color: var(--color-brand-purple);
      box-shadow: 0 0 0 3px rgba(102, 52, 217, 0.2);
    }}

    .search-icon {{
      position: absolute;
      left: 0.9rem;
      top: 50%;
      transform: translateY(-50%);
      font-size: 1.1rem;
      color: var(--color-brand-fig);
      pointer-events: none;
    }}

    .clear-btn {{
      position: absolute;
      right: 0.75rem;
      top: 50%;
      transform: translateY(-50%);
      background: #E2E8F0;
      border: none;
      color: #475569;
      width: 24px;
      height: 24px;
      border-radius: 50%;
      cursor: pointer;
      font-weight: bold;
      display: none;
      align-items: center;
      justify-content: center;
      font-size: 0.8rem;
    }}

    /* Bouton Toggle pour replier les filtres */
    .toggle-filters-btn {{
      background: #F1F5F9;
      color: var(--color-brand-fig);
      border: 1px solid var(--color-brand-fig);
      padding: 0.6rem 1rem;
      font-family: var(--font-main);
      font-size: 0.88rem;
      font-weight: 800;
      cursor: pointer;
      display: flex;
      justify-content: space-between;
      align-items: center;
      width: 100%;
      text-transform: uppercase;
      letter-spacing: 0.02em;
      transition: background 0.15s ease;
    }}

    .toggle-filters-btn:hover {{
      background: #E2E8F0;
    }}

    .toggle-icon {{
      font-size: 0.75rem;
      transition: transform 0.2s ease;
    }}

    .toggle-icon.open {{
      transform: rotate(180deg);
    }}

    /* Panneau repliable */
    .filters-panel {{
      display: flex;
      flex-direction: column;
      gap: 1rem;
      padding-top: 0.5rem;
      border-top: 1px dashed var(--color-border);
    }}

    .filters-panel.collapsed {{
      display: none;
    }}

    .filter-group {{
      display: flex;
      flex-direction: column;
      gap: 0.4rem;
    }}

    .filter-label {{
      font-size: 0.8rem;
      font-weight: 800;
      text-transform: uppercase;
      color: var(--color-brand-fig);
      letter-spacing: 0.03em;
    }}

    .pills-row {{
      display: flex;
      gap: 0.4rem;
      overflow-x: auto;
      padding-bottom: 0.4rem;
      scrollbar-width: thin;
      -webkit-overflow-scrolling: touch;
    }}

    .pills-row::-webkit-scrollbar {{
      height: 4px;
    }}
    .pills-row::-webkit-scrollbar-thumb {{
      background: var(--color-brand-purple);
    }}

    .pill-btn {{
      background: #F1F5F9;
      color: var(--color-brand-fig);
      border: 1px solid var(--color-brand-fig);
      padding: 0.3rem 0.75rem;
      font-family: var(--font-main);
      font-size: 0.88rem;
      font-weight: 700;
      cursor: pointer;
      white-space: nowrap;
      transition: all 0.15s ease;
      flex-shrink: 0;
    }}

    .pill-btn:hover {{
      background: #E2E8F0;
    }}

    .pill-btn.active {{
      background: var(--color-brand-fig);
      color: var(--color-brand-sunny);
    }}

    .alpha-bar {{
      display: flex;
      gap: 0.3rem;
      overflow-x: auto;
      padding-bottom: 0.3rem;
    }}

    .alpha-btn {{
      min-width: 32px;
      height: 32px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      background: #F1F5F9;
      color: var(--color-brand-fig);
      border: 1px solid var(--color-brand-fig);
      font-family: var(--font-main);
      font-size: 0.85rem;
      font-weight: 800;
      cursor: pointer;
      flex-shrink: 0;
    }}

    .alpha-btn.active {{
      background: var(--color-brand-purple);
      color: #FFFFFF;
      border-color: var(--color-brand-fig);
    }}

    .results-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1rem;
      padding: 0 0.25rem;
      font-size: 0.85rem;
      font-weight: 700;
      color: var(--color-text-muted);
    }}

    .counter-tag {{
      background: var(--color-brand-purple);
      color: #FFFFFF;
      padding: 0.15rem 0.55rem;
      font-weight: 800;
    }}

    .cards-container {{
      display: flex;
      flex-direction: column;
      gap: 0.9rem;
    }}

    .card-item {{
      background: var(--color-card-bg);
      border: 1px solid var(--color-border);
      border-left: 4px solid var(--color-brand-purple);
      padding: 1.1rem 1.25rem;
      box-shadow: 0 2px 6px rgba(0,0,0,0.04);
      transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease;
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
    }}

    .card-item:hover {{
      transform: translateY(-2px);
      box-shadow: 0 6px 16px rgba(0,0,0,0.08);
      border-color: var(--color-brand-fig);
    }}

    .card-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 0.75rem;
      flex-wrap: wrap;
    }}

    .term-title {{
      font-size: 1.2rem;
      font-weight: 800;
      color: var(--color-brand-fig);
      letter-spacing: -0.01em;
      word-break: break-word;
    }}

    .type-badge {{
      background: var(--color-brand-fig);
      color: var(--color-brand-sunny);
      font-weight: 800;
      font-size: 0.72rem;
      padding: 0.2rem 0.6rem;
      border: 1px solid var(--color-brand-fig);
      text-transform: uppercase;
      white-space: nowrap;
    }}

    .term-def {{
      font-size: 0.95rem;
      font-weight: 500;
      color: var(--color-brand-fig);
      line-height: 1.5;
    }}

    .card-footer {{
      display: flex;
      align-items: center;
      gap: 0.5rem;
      margin-top: 0.25rem;
      padding-top: 0.5rem;
      border-top: 1px dashed var(--color-border);
      font-size: 0.8rem;
      font-weight: 700;
      flex-wrap: wrap;
    }}

    .ref-code {{
      background: var(--color-brand-purple);
      color: #FFFFFF;
      padding: 0.15rem 0.5rem;
      font-size: 0.75rem;
      font-weight: 900;
    }}

    .ref-title {{
      color: var(--color-text-muted);
      font-weight: 600;
    }}

    mark {{
      background: var(--color-brand-sunny);
      color: var(--color-brand-fig);
      padding: 0;
      margin: 0;
      font-weight: inherit;
      font-style: inherit;
    }}

    .empty-state {{
      background: #FFFFFF;
      border: 2px dashed var(--color-border);
      padding: 3rem 1.5rem;
      text-align: center;
      display: none;
    }}

    .empty-title {{
      font-size: 1.2rem;
      font-weight: 800;
      color: var(--color-brand-fig);
      margin-bottom: 0.5rem;
    }}

    .empty-desc {{
      font-size: 0.9rem;
      color: var(--color-text-muted);
      margin-bottom: 1rem;
    }}

    .reset-btn {{
      background: var(--color-brand-purple);
      color: var(--color-brand-sunny);
      border: 2px solid var(--color-brand-fig);
      padding: 0.6rem 1.2rem;
      font-family: var(--font-main);
      font-weight: 800;
      font-size: 0.85rem;
      cursor: pointer;
      text-transform: uppercase;
    }}

  </style>
</head>
<body>

  <div class="app-viewport">
    
    <header>
      <div class="header-top">
        <span class="brand-badge">Formation Vibe Coding</span>
        <span style="font-weight: 800; font-size: 0.85rem;">Modules 1 à 4</span>
      </div>
      <h1>Glossaire Interactif</h1>
      <div class="header-desc">57 notions clés pour le Vibe Coding</div>
    </header>

    <div class="search-filter-section">
      
      <!-- Champ de recherche principal -->
      <div class="search-box">
        <span class="search-icon">🔍</span>
        <input type="text" id="searchInput" class="search-input" placeholder="Rechercher par 1ère lettre (ex: B) ou mot-clé..." autocomplete="off">
        <button id="clearBtn" class="clear-btn" title="Effacer">✕</button>
      </div>

      <!-- Bouton pour ouvrir / replier les filtres -->
      <button id="toggleFiltersBtn" class="toggle-filters-btn" aria-expanded="false">
        <span>🎛️ Index A-Z & Filtres Avancés</span>
        <span id="toggleIcon" class="toggle-icon">▼</span>
      </button>

      <!-- Panneau de filtres repliable -->
      <div id="filtersPanel" class="filters-panel collapsed">
        
        <!-- Index Alphabétique A-Z -->
        <div class="filter-group">
          <div class="filter-label">Index Alphabétique :</div>
          <div class="alpha-bar" id="alphaBar">
            <button class="alpha-btn active" data-letter="ALL">TOUS</button>
"""

for letter in alphabet_list:
    html_content += f'            <button class="alpha-btn" data-letter="{letter}">{letter}</button>\n'

html_content += f"""          </div>
        </div>

        <!-- Filtres par Modules -->
        <div class="filter-group">
          <div class="filter-label">Filtrer par Module :</div>
          <div class="pills-row" id="modulePills">
            <button class="pill-btn active" data-module="ALL">Tous les modules</button>
            <button class="pill-btn" data-module="M1">Module 1 (Bases)</button>
            <button class="pill-btn" data-module="M2">Module 2 (Web)</button>
            <button class="pill-btn" data-module="M3">Module 3 (Mobile)</button>
            <button class="pill-btn" data-module="M4">Module 4 (Agents)</button>
          </div>
        </div>

        <!-- Filtres par Catégorie -->
        <div class="filter-group">
          <div class="filter-label">Filtrer par Thématique :</div>
          <div class="pills-row" id="categoryPills">
            <button class="pill-btn active" data-cat="ALL">Toutes les thématiques</button>
"""

for cat in categories_list:
    html_content += f'            <button class="pill-btn" data-cat="{cat}">{cat}</button>\n'

html_content += f"""          </div>
        </div>

      </div>

    </div>

    <div class="results-bar">
      <span>Résultats :</span>
      <span class="counter-tag" id="counterTag">57 termes</span>
    </div>

    <div class="cards-container" id="cardsContainer"></div>

    <div class="empty-state" id="emptyState">
      <div class="empty-title">Aucun terme ne correspond à la recherche</div>
      <div class="empty-desc">Essayez avec d'autres mots-clés ou cliquez sur un autre filtre.</div>
      <button class="reset-btn" id="resetBtn">Réinitialiser tous les filtres</button>
    </div>

  </div>

  <script>
    const TERMS_DATA = {terms_json};

    let activeModule = 'ALL';
    let activeCategory = 'ALL';
    let activeLetter = 'ALL';
    let searchQuery = '';

    const searchInput = document.getElementById('searchInput');
    const clearBtn = document.getElementById('clearBtn');
    const cardsContainer = document.getElementById('cardsContainer');
    const counterTag = document.getElementById('counterTag');
    const emptyState = document.getElementById('emptyState');
    const resetBtn = document.getElementById('resetBtn');

    const toggleFiltersBtn = document.getElementById('toggleFiltersBtn');
    const filtersPanel = document.getElementById('filtersPanel');
    const toggleIcon = document.getElementById('toggleIcon');

    // Gestion de la visibilite du panneau repliable
    toggleFiltersBtn.addEventListener('click', () => {{
      const isCollapsed = filtersPanel.classList.contains('collapsed');
      if (isCollapsed) {{
        filtersPanel.classList.remove('collapsed');
        toggleIcon.classList.add('open');
        toggleFiltersBtn.setAttribute('aria-expanded', 'true');
      }} else {{
        filtersPanel.classList.add('collapsed');
        toggleIcon.classList.remove('open');
        toggleFiltersBtn.setAttribute('aria-expanded', 'false');
      }}
    }});

    function matchWordStart(fullText, query) {{
      if (!query) return true;
      const q = escapeRegExp(query.trim().toLowerCase());
      const regex = new RegExp(`(?:^|[^a-zA-Z0-9à-ÿÀ-Ÿ])${{q}}`, 'i');
      return regex.test(fullText);
    }}

    function render() {{
      const query = searchQuery.trim().toLowerCase();
      
      const filtered = TERMS_DATA.filter(item => {{
        const matchMod = (activeModule === 'ALL' || item.module === activeModule);
        const matchCat = (activeCategory === 'ALL' || item.category === activeCategory);
        
        let matchAlpha = true;
        if (activeLetter !== 'ALL') {{
          const cleanWord = item.word.replace(/^[^a-zA-Z0-9]+/, '');
          matchAlpha = cleanWord.toUpperCase().startsWith(activeLetter);
        }}

        const textToSearch = item.word + ' ' + item.category + ' ' + item.definition + ' ' + item.ref;
        const matchSearch = matchWordStart(textToSearch, query);

        return matchMod && matchCat && matchAlpha && matchSearch;
      }});

      counterTag.textContent = `${{filtered.length}} terme${{filtered.length > 1 ? 's' : ''}}`;

      if (filtered.length === 0) {{
        cardsContainer.style.display = 'none';
        emptyState.style.display = 'block';
        return;
      }}

      cardsContainer.style.display = 'flex';
      emptyState.style.display = 'none';

      cardsContainer.innerHTML = filtered.map(item => {{
        let wordHtml = escapeHtml(item.word);
        let defHtml = escapeHtml(item.definition);

        if (query !== '') {{
          const qEscaped = escapeRegExp(query);
          const regex = new RegExp(`(^|[^a-zA-Z0-9à-ÿÀ-Ÿ])(${{qEscaped}})`, 'gi');
          wordHtml = wordHtml.replace(regex, '$1<mark>$2</mark>');
          defHtml = defHtml.replace(regex, '$1<mark>$2</mark>');
        }}

        const refParts = item.ref.split('—');
        const code = refParts[0] ? (refParts[0].trim ? refParts[0].trim() : refParts[0]) : item.ref;
        const title = refParts[1] ? refParts[1].trim() : '';

        return `
          <div class="card-item">
            <div class="card-header">
              <div class="term-title">${{wordHtml}}</div>
              <span class="type-badge">${{escapeHtml(item.category)}}</span>
            </div>
            <div class="term-def">${{defHtml}}</div>
            <div class="card-footer">
              <span class="ref-code">${{escapeHtml(code)}}</span>
              ${{title ? `<span class="ref-title">${{escapeHtml(title)}}</span>` : ''}}
            </div>
          </div>
        `;
      }}).join('');
    }}

    function escapeRegExp(string) {{
      return string.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&');
    }}

    function escapeHtml(str) {{
      return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");
    }}

    searchInput.addEventListener('input', (e) => {{
      searchQuery = e.target.value;
      clearBtn.style.display = searchQuery ? 'flex' : 'none';
      render();
    }});

    clearBtn.addEventListener('click', () => {{
      searchInput.value = '';
      searchQuery = '';
      clearBtn.style.display = 'none';
      searchInput.focus();
      render();
    }});

    document.getElementById('alphaBar').addEventListener('click', (e) => {{
      const btn = e.target.closest('.alpha-btn');
      if (!btn) return;
      document.querySelectorAll('.alpha-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      activeLetter = btn.getAttribute('data-letter');
      render();
    }});

    document.getElementById('modulePills').addEventListener('click', (e) => {{
      const btn = e.target.closest('.pill-btn');
      if (!btn) return;
      document.querySelectorAll('#modulePills .pill-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      activeModule = btn.getAttribute('data-module');
      render();
    }});

    document.getElementById('categoryPills').addEventListener('click', (e) => {{
      const btn = e.target.closest('.pill-btn');
      if (!btn) return;
      document.querySelectorAll('#categoryPills .pill-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      activeCategory = btn.getAttribute('data-cat');
      render();
    }});

    resetBtn.addEventListener('click', () => {{
      searchQuery = '';
      searchInput.value = '';
      clearBtn.style.display = 'none';
      activeModule = 'ALL';
      activeCategory = 'ALL';
      activeLetter = 'ALL';
      
      document.querySelectorAll('.pill-btn, .alpha-btn').forEach(b => b.classList.remove('active'));
      document.querySelector('#modulePills .pill-btn[data-module="ALL"]').classList.add('active');
      document.querySelector('#categoryPills .pill-btn[data-cat="ALL"]').classList.add('active');
      document.querySelector('#alphaBar .alpha-btn[data-letter="ALL"]').classList.add('active');
      
      render();
    }});

    render();
  </script>

</body>
</html>
"""

with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    f.write(html_content)

with open(INDEX_PATH, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Glossaire interactif avec panneau repliable mis a jour.")
