// Empty string = same origin — Flask serves both frontend and API
const API = '';

// ── Tabs ──────────────────────────────────────────────────────────────────────
document.querySelectorAll('.nav-link').forEach(link => {
  link.addEventListener('click', e => {
    e.preventDefault();
    const tab = link.dataset.tab;

    document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(s => s.classList.remove('active'));

    link.classList.add('active');
    document.getElementById('tab-' + tab).classList.add('active');

    if (tab === 'model') loadModelInfo();
  });
});

// ── API health check ──────────────────────────────────────────────────────────
async function checkHealth() {
  const badge = document.getElementById('api-status');
  try {
    const res = await fetch(API + '/health', { signal: AbortSignal.timeout(4000) });
    if (res.ok) {
      badge.textContent = '● API Online';
      badge.className = 'status-badge status-ok';
    } else {
      throw new Error();
    }
  } catch {
    badge.textContent = '● API Offline';
    badge.className = 'status-badge status-error';
  }
}

checkHealth();

// ── Set today as default date ────────────────────────────────────────────────
const dateInput = document.getElementById('date');
dateInput.value = new Date().toISOString().split('T')[0];

// ── Single prediction ─────────────────────────────────────────────────────────
const form = document.getElementById('predict-form');
const btn  = document.getElementById('predict-btn');

form.addEventListener('submit', async e => {
  e.preventDefault();

  hideEl('result-card');
  hideEl('error-card');

  // Collect form data
  const data = {
    Store:               parseInt(v('store')),
    DayOfWeek:           parseInt(v('day-of-week')),
    Date:                v('date'),
    Promo:               document.getElementById('promo').checked ? 1 : 0,
    Promo2:              document.getElementById('promo2').checked ? 1 : 0,
    SchoolHoliday:       document.getElementById('school-holiday').checked ? 1 : 0,
    StateHoliday:        v('state-holiday'),
    StoreType:           v('store-type'),
    Assortment:          v('assortment'),
    CompetitionDistance: parseFloat(v('competition-distance')) || 0,
  };

  setLoading(true);

  try {
    const res = await fetch(API + '/api/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });

    const json = await res.json();

    if (!res.ok || !json.success) {
      showError(json.error || 'Prediction failed. Check the backend is running.');
      return;
    }

    document.getElementById('result-value').textContent = formatNumber(json.prediction);
    document.getElementById('result-store').textContent = json.store;
    document.getElementById('result-date').textContent  = json.date;
    showEl('result-card');

  } catch (err) {
    showError('Could not reach the API. Make sure the Flask server is running on port 5000.');
  } finally {
    setLoading(false);
  }
});

form.addEventListener('reset', () => {
  hideEl('result-card');
  hideEl('error-card');
  setTimeout(() => { dateInput.value = new Date().toISOString().split('T')[0]; }, 0);
});

// ── Batch upload ──────────────────────────────────────────────────────────────
let selectedFile = null;

const uploadArea  = document.getElementById('upload-area');
const csvFileInput = document.getElementById('csv-file');
const uploadBtn   = document.getElementById('upload-btn');
const fileInfo    = document.getElementById('file-info');
const fileName    = document.getElementById('file-name');
const removeFile  = document.getElementById('remove-file');

// Drag & drop
uploadArea.addEventListener('dragover', e => { e.preventDefault(); uploadArea.classList.add('drag-over'); });
uploadArea.addEventListener('dragleave', () => uploadArea.classList.remove('drag-over'));
uploadArea.addEventListener('drop', e => {
  e.preventDefault();
  uploadArea.classList.remove('drag-over');
  handleFile(e.dataTransfer.files[0]);
});

csvFileInput.addEventListener('change', () => handleFile(csvFileInput.files[0]));

function handleFile(file) {
  if (!file) return;
  if (!file.name.endsWith('.csv')) {
    alert('Please select a CSV file.');
    return;
  }
  selectedFile = file;
  fileName.textContent = file.name + ' (' + (file.size / 1024).toFixed(1) + ' KB)';
  showEl('file-info');
  uploadBtn.disabled = false;
}

removeFile.addEventListener('click', () => {
  selectedFile = null;
  csvFileInput.value = '';
  hideEl('file-info');
  hideEl('batch-result');
  uploadBtn.disabled = true;
});

uploadBtn.addEventListener('click', async () => {
  if (!selectedFile) return;

  hideEl('batch-result');
  uploadBtn.disabled = true;
  uploadBtn.textContent = 'Uploading…';

  const formData = new FormData();
  formData.append('file', selectedFile);

  try {
    const res  = await fetch(API + '/api/upload/predict', { method: 'POST', body: formData });
    const json = await res.json();

    if (!res.ok || !json.success) {
      alert('Upload failed: ' + (json.error || 'Unknown error'));
      return;
    }

    renderBatchResults(json);
    showEl('batch-result');

  } catch {
    alert('Could not reach the API. Make sure the Flask server is running on port 5000.');
  } finally {
    uploadBtn.disabled = false;
    uploadBtn.textContent = 'Upload & Predict';
  }
});

function renderBatchResults(json) {
  const preds = json.predictions || [];
  const stats = document.getElementById('batch-stats');
  stats.innerHTML = `
    <div class="stat-box"><div class="stat-label">Total Rows</div><div class="stat-value">${json.count || preds.length}</div></div>
    <div class="stat-box"><div class="stat-label">Avg Sales</div><div class="stat-value">${formatNumber(json.avg || json.average)}</div></div>
    <div class="stat-box"><div class="stat-label">Min Sales</div><div class="stat-value">${formatNumber(json.min)}</div></div>
    <div class="stat-box"><div class="stat-label">Max Sales</div><div class="stat-value">${formatNumber(json.max)}</div></div>
  `;

  const tbody = document.getElementById('results-tbody');
  tbody.innerHTML = preds.map(p => `
    <tr>
      <td>${p.index + 1}</td>
      <td>${p.store}</td>
      <td>${p.date}</td>
      <td class="pred-cell">${formatNumber(p.prediction)}</td>
    </tr>
  `).join('');
}

// Download CSV template
document.getElementById('template-btn').addEventListener('click', async () => {
  try {
    const res  = await fetch(API + '/api/upload/template');
    const json = await res.json();
    if (!json.success) { alert('Could not fetch template.'); return; }

    const blob = new Blob([json.template], { type: 'text/csv' });
    const url  = URL.createObjectURL(blob);
    const a    = document.createElement('a');
    a.href     = url;
    a.download = 'template.csv';
    a.click();
    URL.revokeObjectURL(url);
  } catch {
    alert('Could not reach the API to download the template.');
  }
});

// ── Model info tab ────────────────────────────────────────────────────────────
let modelLoaded = false;

async function loadModelInfo() {
  if (modelLoaded) return;

  try {
    // Model info
    const res  = await fetch(API + '/api/insights/model-info');
    const json = await res.json();

    if (json.success) {
      const info = json.type ? json : (json.model || {});
      document.getElementById('model-info-body').innerHTML = `
        <div class="info-grid">
          <div class="info-box"><div class="info-box-label">Model Type</div><div class="info-box-value">${info.type || json.type || '—'}</div></div>
          <div class="info-box"><div class="info-box-label">Features</div><div class="info-box-value">${info.features || info.n_features || json.features || '—'}</div></div>
          <div class="info-box"><div class="info-box-label">Estimators</div><div class="info-box-value">${info.n_estimators || json.n_estimators || '—'}</div></div>
          <div class="info-box"><div class="info-box-label">Max Depth</div><div class="info-box-value">${info.max_depth || json.max_depth || '—'}</div></div>
        </div>
      `;
    } else {
      document.getElementById('model-info-body').innerHTML = '<p style="color:var(--red);font-size:14px">Could not load model info.</p>';
    }
  } catch {
    document.getElementById('model-info-body').innerHTML = '<p style="color:var(--gray-400);font-size:14px">API is offline.</p>';
  }

  try {
    // Features list
    const res2  = await fetch(API + '/api/insights/features');
    const json2 = await res2.json();

    if (json2.success && json2.features) {
      document.getElementById('features-body').innerHTML =
        '<div class="features-list">' +
        json2.features.map(f => `<span class="feature-tag">${f}</span>`).join('') +
        '</div>';
    } else {
      document.getElementById('features-body').innerHTML = '<p style="font-size:14px;color:var(--gray-400)">No feature data.</p>';
    }
  } catch {
    document.getElementById('features-body').innerHTML = '<p style="font-size:14px;color:var(--gray-400)">API is offline.</p>';
  }

  modelLoaded = true;
}

// ── Helpers ──────────────────────────────────────────────────────────────────
function v(id) { return document.getElementById(id).value; }

function showEl(id) { document.getElementById(id).classList.remove('hidden'); }
function hideEl(id) { document.getElementById(id).classList.add('hidden'); }

function setLoading(on) {
  btn.disabled = on;
  btn.querySelector('.btn-text').classList.toggle('hidden', on);
  btn.querySelector('.btn-spinner').classList.toggle('hidden', !on);
}

function showError(msg) {
  document.getElementById('error-msg').textContent = msg;
  showEl('error-card');
}

function formatNumber(n) {
  if (n == null || isNaN(n)) return '—';
  return Number(n).toLocaleString('en-DE', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}
