const statusEl = document.getElementById('status');
const resultsEl = document.getElementById('results');
const alternativesEl = document.getElementById('alternatives');

const organIcons = {
  liver: '🧪',
  lungs: '🫁',
  kidneys: '🫘',
  brain: '🧠',
  hormones: '🧬',
  'cancer risk': '⚠️',
  heart: '❤️',
  gut: '🦠',
  'immune system': '🛡️',
  'nervous system': '🔌',
  skin: '🧴',
  blood: '🩸',
  bones: '🦴'
};

function setStatus(message, isError = false) {
  statusEl.textContent = message;
  statusEl.style.color = isError ? 'var(--high)' : 'var(--green-mid)';
}

function renderResults(items, title = 'Flagged Toxins') {
  resultsEl.innerHTML = '';
  alternativesEl.innerHTML = '';
  alternativesEl.style.display = 'none';
  const wrapper = document.getElementById('results-wrapper');
  if (wrapper) wrapper.style.display = 'block';

  if (!items.length) {
    setStatus('No known toxins found in the current Raíz database.');
    return;
  }

  setStatus(`${title}: ${items.length} match(es) found.`);

  items.forEach((item) => {
    const card = document.createElement('article');
    card.className = `result-card ${item.risk_level}`;
    card.innerHTML = `
      <h3>${item.name}</h3>
      <span class="badge ${item.risk_level}">${item.risk_level} risk</span>
      <p>${item.description}</p>
      <p><strong>Safe threshold:</strong> ${item.safe_threshold}</p>
      <div class="organs">
        ${item.organs_affected.map((organ) => `<span>${organIcons[organ] || '•'} ${organ}</span>`).join('')}
      </div>
      <p><strong>Natural alternatives:</strong></p>
      <ul>${item.natural_alternatives.map((alt) => `<li>${alt}</li>`).join('')}</ul>
    `;
    resultsEl.appendChild(card);
  });

  const allAlternatives = [...new Set(items.flatMap((item) => item.natural_alternatives))];
  alternativesEl.style.display = 'block';
  alternativesEl.innerHTML = `
    <h3>Natural Alternatives</h3>
    <p style="font-size:0.88rem;color:var(--text-mid);margin-bottom:12px;">Whole-food and herbal replacements you can use instead:</p>
    <ul style="padding-left:1.2rem;">${allAlternatives.map((alt) => `<li style="font-size:0.88rem;color:var(--text-mid);margin-bottom:4px;">${alt}</li>`).join('')}</ul>
  `;
}

async function handleBarcode() {
  const barcode = document.getElementById('barcodeInput').value.trim();
  if (!barcode) return setStatus('Please enter a barcode.', true);

  setStatus('Fetching product from Open Food Facts...');
  try {
    const productRes = await fetch(`/api/product/${barcode}`);
    if (!productRes.ok) throw new Error((await productRes.json()).detail || 'Barcode lookup failed');
    const product = await productRes.json();

    setStatus(`Loaded ${product.product_name}. Analyzing ingredients...`);
    const analysisRes = await fetch('/api/analyze-ingredients', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ingredients: product.ingredients })
    });
    const analysis = await analysisRes.json();
    renderResults(analysis.flagged_toxins, `Results for ${product.product_name}`);
  } catch (err) {
    setStatus(err.message, true);
  }
}

async function handleAnalyze() {
  const ingredients = document.getElementById('ingredientsInput').value.trim();
  if (!ingredients) return setStatus('Please add an ingredient list first.', true);

  setStatus('Analyzing ingredient list...');
  try {
    const res = await fetch('/api/analyze-ingredients', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ingredients })
    });
    const data = await res.json();
    renderResults(data.flagged_toxins);
  } catch (err) {
    setStatus('Could not analyze ingredients.', true);
  }
}

async function handleSingleSearch() {
  const query = document.getElementById('singleInput').value.trim();
  if (!query) return setStatus('Please enter an ingredient name.', true);

  setStatus('Searching toxin database...');
  try {
    const res = await fetch(`/api/search?query=${encodeURIComponent(query)}`);
    const data = await res.json();
    renderResults(data.results, `Search for "${query}"`);
  } catch (err) {
    setStatus('Could not run search.', true);
  }
}

document.getElementById('barcodeBtn').addEventListener('click', handleBarcode);
document.getElementById('analyzeBtn').addEventListener('click', handleAnalyze);
document.getElementById('singleBtn').addEventListener('click', handleSingleSearch);
