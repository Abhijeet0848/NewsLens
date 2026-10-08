/**
 * NewsSense – Frontend Application Logic
 * Academic MCA ML Project UI Controller
 */

// Global State
const state = {
  activeView: 'dashboard',
  theme: 'light',
  datasetStats: null,
  evaluationMetrics: null,
  charts: {},
  samplePresets: [
    {
      category: 'Politics',
      title: 'Parliament Voting',
      text: 'Parliament passes historic election reform bill after extensive parliamentary debate on constitutional safeguards and democratic electoral integrity. Opposition lawmakers challenged several amendments during the voting session.'
    },
    {
      category: 'Sports',
      title: 'Cricket Final Victory',
      text: 'National cricket team clinches thrilling final victory in international championship match with a sensational boundary on the penultimate delivery. The captain praised the team\'s discipline under pressure.'
    },
    {
      category: 'Business',
      title: 'Central Bank Rates',
      text: 'Central bank keeps benchmark interest rates steady to tame consumer inflation while monitoring corporate bond yields and international exchange rate fluctuations amid global monetary policy shifts.'
    },
    {
      category: 'Technology',
      title: '2nm Microchip Architecture',
      text: 'Semiconductor engineers unveil next-generation 2nm microchip architecture featuring billions of ultra-dense transistors, slashing power consumption and accelerating neural network inference tasks.'
    },
    {
      category: 'Entertainment',
      title: 'Film Festival Honors',
      text: 'Acclaimed independent film sweeps major honors at international film festival, earning standing ovations for masterclass cinematography, evocative screenplay, and transformative lead performances.'
    },
    {
      category: 'Science',
      title: 'Deep Space Telescope',
      text: 'Deep space telescope captures unprecedented high-resolution infrared imagery of early cosmic galaxy clusters formed shortly after the Big Bang, challenging existing theoretical astrophysics models.'
    },
    {
      category: 'Health',
      title: 'Oncology Immunotherapy',
      text: 'Clinical medical researchers report breakthrough in Phase 3 oncology immunotherapy trials, demonstrating significant tumor regression and extended survival rates among metastatic patients.'
    },
    {
      category: 'World',
      title: 'UN Climate Summit',
      text: 'United Nations General Assembly convenes high-level multilateral summit to negotiate legally binding international climate accords, humanitarian aid corridors, and sustainable development goals.'
    }
  ]
};

// DOM Elements
document.addEventListener('DOMContentLoaded', () => {
  initLucide();
  initTheme();
  initNavigation();
  initPresetButtons();
  initClassifyHandlers();
  initNLPInspectorHandlers();
  initConfusionMatrixHandlers();
  initDatasetExplorerHandlers();
  
  // Fetch Initial Data
  fetchDatasetStats();
  fetchModelEvaluation();
});

function initLucide() {
  if (window.lucide) {
    window.lucide.createIcons();
  }
}

// Theme Management
function initTheme() {
  const themeToggleBtn = document.getElementById('theme-toggle');
  const themeIcon = document.getElementById('theme-icon');
  
  const savedTheme = localStorage.getItem('newssense_theme') || 'dark';
  setTheme(savedTheme);

  themeToggleBtn.addEventListener('click', () => {
    const nextTheme = state.theme === 'dark' ? 'light' : 'dark';
    setTheme(nextTheme);
  });
}

function setTheme(theme) {
  state.theme = theme;
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('newssense_theme', theme);
  
  const themeIcon = document.getElementById('theme-icon');
  if (themeIcon) {
    themeIcon.setAttribute('data-lucide', theme === 'dark' ? 'sun' : 'moon');
    initLucide();
  }

  // Update existing chart theme colors
  updateChartThemes();
}

function updateChartThemes() {
  const isDark = state.theme === 'dark';
  const textColor = isDark ? '#94a3b8' : '#475569';
  const gridColor = isDark ? '#26334d' : '#e2e8f0';

  Object.values(state.charts).forEach(chart => {
    if (chart && chart.options) {
      if (chart.options.scales) {
        if (chart.options.scales.x) {
          chart.options.scales.x.ticks.color = textColor;
          chart.options.scales.x.grid.color = gridColor;
        }
        if (chart.options.scales.y) {
          chart.options.scales.y.ticks.color = textColor;
          chart.options.scales.y.grid.color = gridColor;
        }
      }
      if (chart.options.plugins && chart.options.plugins.legend) {
        chart.options.plugins.legend.labels.color = textColor;
      }
      chart.update();
    }
  });
}

// Navigation
function initNavigation() {
  const navItems = document.querySelectorAll('.nav-item');
  navItems.forEach(item => {
    item.addEventListener('click', () => {
      const targetView = item.getAttribute('data-view');
      navigateTo(targetView);
    });
  });

  // Word counter
  const articleInput = document.getElementById('article-input');
  if (articleInput) {
    articleInput.addEventListener('input', updateCharWordCount);
  }
}

function navigateTo(viewName) {
  state.activeView = viewName;

  // Update nav tabs
  document.querySelectorAll('.nav-item').forEach(item => {
    if (item.getAttribute('data-view') === viewName) {
      item.classList.add('active');
    } else {
      item.classList.remove('active');
    }
  });

  // Update views
  document.querySelectorAll('.page-view').forEach(view => {
    view.classList.remove('active');
  });

  const activeSection = document.getElementById(`view-${viewName}`);
  if (activeSection) {
    activeSection.classList.add('active');
  }

  // Update header title
  const titles = {
    dashboard: 'Executive Dashboard',
    classify: 'Classify Article & Predictions',
    nlp: 'NLP Preprocessing Pipeline',
    comparison: 'Machine Learning Model Benchmarks',
    confusion: 'Confusion Matrix & Error Metrics',
    dataset: 'Dataset Distribution & Samples',
    theory: 'Academic Formulations & Algorithms'
  };
  const titleEl = document.getElementById('page-title');
  if (titleEl && titles[viewName]) {
    titleEl.textContent = titles[viewName];
  }

  initLucide();
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function updateCharWordCount() {
  const text = document.getElementById('article-input').value.trim();
  const charCount = text.length;
  const wordCount = text ? text.split(/\s+/).length : 0;
  const counterEl = document.getElementById('char-word-counter');
  if (counterEl) {
    counterEl.textContent = `${wordCount} words | ${charCount} chars`;
  }
}

// Presets
function initPresetButtons() {
  const container = document.getElementById('preset-buttons');
  if (!container) return;

  container.innerHTML = '';
  state.samplePresets.forEach(preset => {
    const btn = document.createElement('button');
    btn.className = 'preset-btn';
    btn.innerHTML = `<span class="cat-badge ${preset.category.toLowerCase()}" style="padding: 0.15rem 0.4rem; font-size: 0.7rem;">${preset.category}</span> ${preset.title}`;
    btn.addEventListener('click', () => {
      document.getElementById('article-input').value = preset.text;
      updateCharWordCount();
      // Auto analyze
      classifyCurrentArticle();
    });
    container.appendChild(btn);
  });
}

// ----------------- API Calls & Visualizations -----------------

async function fetchDatasetStats() {
  try {
    const res = await fetch('/api/dataset/stats');
    if (!res.ok) throw new Error('Failed to load dataset stats');
    const data = await res.json();
    state.datasetStats = data;

    // Update Dashboard numbers
    document.getElementById('dash-total-articles').textContent = data.total_articles;
    document.getElementById('dash-total-categories').textContent = data.total_categories;
    if (data.split_metadata) {
      document.getElementById('dash-split-counts').textContent = 
        `${data.split_metadata.train_samples} Train / ${data.split_metadata.test_samples} Test`;
      document.getElementById('ds-vocab-size').textContent = data.split_metadata.vocabulary_size.toLocaleString();
    }

    // Dataset explorer stats
    document.getElementById('ds-total-articles').textContent = data.total_articles;
    document.getElementById('ds-avg-words').textContent = data.word_count_stats.mean;

    renderCategoryDonutChart(data.category_distribution);
  } catch (err) {
    console.error('Error fetching dataset stats:', err);
  }
}

async function fetchModelEvaluation() {
  try {
    const res = await fetch('/api/models/evaluation');
    if (!res.ok) throw new Error('Failed to load evaluation metrics');
    const data = await res.json();
    state.evaluationMetrics = data;

    renderDashboardAccuracyChart(data.models);
    renderDashboardSummaryTable(data.models);
    renderComparisonCharts(data.models);
    renderComparisonTable(data.models);
    
    // Load initial confusion matrix
    const initialModel = document.getElementById('cm-model-select').value || 'naive_bayes';
    fetchConfusionMatrix(initialModel);
  } catch (err) {
    console.error('Error fetching evaluation metrics:', err);
  }
}

// ----------------- Charts Initializations -----------------

function renderCategoryDonutChart(categoryDist) {
  const ctx = document.getElementById('dashCategoryChart');
  if (!ctx) return;

  const labels = Object.keys(categoryDist);
  const data = Object.values(categoryDist);

  const colors = [
    '#ef4444', '#10b981', '#3b82f6', '#8b5cf6',
    '#ec4899', '#06b6d4', '#14b8a6', '#f59e0b'
  ];

  if (state.charts.dashCategory) {
    state.charts.dashCategory.destroy();
  }

  state.charts.dashCategory = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: labels,
      datasets: [{
        data: data,
        backgroundColor: colors,
        borderWidth: 2,
        borderColor: state.theme === 'dark' ? '#161f33' : '#ffffff'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'right',
          labels: {
            color: state.theme === 'dark' ? '#94a3b8' : '#475569',
            font: { family: 'Inter', size: 12 }
          }
        }
      },
      cutout: '65%'
    }
  });
}

function renderDashboardAccuracyChart(modelsData) {
  const ctx = document.getElementById('dashAccuracyChart');
  if (!ctx) return;

  const labels = Object.values(modelsData).map(m => m.name);
  const accuracies = Object.values(modelsData).map(m => (m.accuracy * 100).toFixed(1));

  if (state.charts.dashAccuracy) {
    state.charts.dashAccuracy.destroy();
  }

  state.charts.dashAccuracy = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Test Accuracy (%)',
        data: accuracies,
        backgroundColor: ['#6366f1', '#10b981', '#f59e0b', '#a855f7'],
        borderRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          max: 100,
          ticks: { color: state.theme === 'dark' ? '#94a3b8' : '#475569' },
          grid: { color: state.theme === 'dark' ? '#26334d' : '#e2e8f0' }
        },
        x: {
          ticks: { color: state.theme === 'dark' ? '#94a3b8' : '#475569' },
          grid: { display: false }
        }
      },
      plugins: {
        legend: { display: false }
      }
    }
  });
}

function renderDashboardSummaryTable(modelsData) {
  const tbody = document.getElementById('dash-summary-tbody');
  if (!tbody) return;

  tbody.innerHTML = '';
  Object.values(modelsData).forEach(m => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><strong>${m.name}</strong></td>
      <td><span class="badge-pill">${m.class_type}</span></td>
      <td><strong style="color: var(--accent-emerald);">${(m.accuracy * 100).toFixed(2)}%</strong></td>
      <td>${(m.f1_macro * 100).toFixed(2)}%</td>
      <td>${m.training_time_seconds.toFixed(3)}s</td>
      <td>${m.avg_inference_latency_ms.toFixed(3)} ms</td>
      <td>
        <button class="btn btn-secondary btn-sm" onclick="selectModelAndClassify('${m.id}')">
          <span>Test Model</span>
        </button>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

function renderComparisonCharts(modelsData) {
  const ctxMetrics = document.getElementById('modelComparisonChart');
  const ctxLatency = document.getElementById('modelLatencyChart');

  const modelsList = Object.values(modelsData);
  const labels = modelsList.map(m => m.name);

  // Grouped Bar Chart
  if (ctxMetrics) {
    if (state.charts.comparisonMetrics) state.charts.comparisonMetrics.destroy();

    state.charts.comparisonMetrics = new Chart(ctxMetrics, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Accuracy (%)',
            data: modelsList.map(m => (m.accuracy * 100).toFixed(1)),
            backgroundColor: '#6366f1',
            borderRadius: 4
          },
          {
            label: 'Precision (Macro %)',
            data: modelsList.map(m => (m.precision_macro * 100).toFixed(1)),
            backgroundColor: '#06b6d4',
            borderRadius: 4
          },
          {
            label: 'Recall (Macro %)',
            data: modelsList.map(m => (m.recall_macro * 100).toFixed(1)),
            backgroundColor: '#10b981',
            borderRadius: 4
          },
          {
            label: 'F1-Score (Macro %)',
            data: modelsList.map(m => (m.f1_macro * 100).toFixed(1)),
            backgroundColor: '#a855f7',
            borderRadius: 4
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
            max: 105,
            ticks: { color: state.theme === 'dark' ? '#94a3b8' : '#475569' },
            grid: { color: state.theme === 'dark' ? '#26334d' : '#e2e8f0' }
          },
          x: {
            ticks: { color: state.theme === 'dark' ? '#94a3b8' : '#475569' },
            grid: { display: false }
          }
        },
        plugins: {
          legend: {
            position: 'top',
            labels: { color: state.theme === 'dark' ? '#94a3b8' : '#475569' }
          }
        }
      }
    });
  }

  // Latency Chart
  if (ctxLatency) {
    if (state.charts.comparisonLatency) state.charts.comparisonLatency.destroy();

    state.charts.comparisonLatency = new Chart(ctxLatency, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: 'Inference Latency per Sample (ms)',
          data: modelsList.map(m => m.avg_inference_latency_ms),
          backgroundColor: ['#6366f1', '#10b981', '#f59e0b', '#a855f7'],
          borderRadius: 6
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        indexAxis: 'y',
        scales: {
          x: {
            beginAtZero: true,
            ticks: { color: state.theme === 'dark' ? '#94a3b8' : '#475569' },
            grid: { color: state.theme === 'dark' ? '#26334d' : '#e2e8f0' }
          },
          y: {
            ticks: { color: state.theme === 'dark' ? '#94a3b8' : '#475569' },
            grid: { display: false }
          }
        },
        plugins: { legend: { display: false } }
      }
    });
  }
}

function renderComparisonTable(modelsData) {
  const tbody = document.getElementById('model-comparison-tbody');
  if (!tbody) return;

  tbody.innerHTML = '';
  Object.values(modelsData).forEach(m => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><strong>${m.name}</strong></td>
      <td><span class="badge-pill">${m.class_type}</span></td>
      <td><strong style="color: var(--accent-emerald);">${(m.accuracy * 100).toFixed(2)}%</strong></td>
      <td>${(m.precision_macro * 100).toFixed(2)}%</td>
      <td>${(m.recall_macro * 100).toFixed(2)}%</td>
      <td>${(m.f1_macro * 100).toFixed(2)}%</td>
      <td>${m.training_time_seconds.toFixed(3)}s</td>
      <td>${m.avg_inference_latency_ms.toFixed(3)} ms</td>
    `;
    tbody.appendChild(tr);
  });
}

function selectModelAndClassify(modelId) {
  document.getElementById('model-select').value = modelId;
  navigateTo('classify');
}

// ----------------- Classification Handlers -----------------

function initClassifyHandlers() {
  const btnClassify = document.getElementById('btn-classify');
  const btnClassifyAll = document.getElementById('btn-classify-all');
  const btnClear = document.getElementById('btn-clear-input');

  if (btnClassify) {
    btnClassify.addEventListener('click', classifyCurrentArticle);
  }

  if (btnClassifyAll) {
    btnClassifyAll.addEventListener('click', classifyAllModelsParallel);
  }

  if (btnClear) {
    btnClear.addEventListener('click', () => {
      document.getElementById('article-input').value = '';
      updateCharWordCount();
      document.getElementById('pred-placeholder').style.display = 'block';
      document.getElementById('pred-results-card').style.display = 'none';
      document.getElementById('all-models-result-card').style.display = 'none';
    });
  }
}

async function classifyCurrentArticle() {
  const text = document.getElementById('article-input').value.trim();
  const modelId = document.getElementById('model-select').value;
  const btn = document.getElementById('btn-classify');

  if (!text) {
    alert('Please enter or paste news article text to analyze.');
    return;
  }

  try {
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner"></span> <span>Analyzing...</span>';

    const res = await fetch('/api/classify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: text, model_id: modelId })
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Classification failed');

    displayClassificationResult(data);
    updateNLPInspectorFromData(data.nlp_pipeline, data.top_tfidf_features);
  } catch (err) {
    alert(`Classification Error: ${err.message}`);
  } finally {
    btn.disabled = false;
    btn.innerHTML = '<i data-lucide="search"></i> <span>Analyze Article</span>';
    initLucide();
  }
}

async function classifyAllModelsParallel() {
  const text = document.getElementById('article-input').value.trim();
  const btn = document.getElementById('btn-classify-all');

  if (!text) {
    alert('Please enter or paste news article text to analyze.');
    return;
  }

  try {
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner"></span> <span>Benchmarking All 4 Models...</span>';

    const res = await fetch('/api/classify/all-models', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: text })
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Multi-model classification failed');

    displayAllModelsResult(data.predictions);
    updateNLPInspectorFromData(data.nlp_pipeline, []);
  } catch (err) {
    alert(`Error: ${err.message}`);
  } finally {
    btn.disabled = false;
    btn.innerHTML = '<i data-lucide="git-compare"></i> <span>Compare Predictions Across All 4 Models Simultaneously</span>';
    initLucide();
  }
}

function displayClassificationResult(result) {
  document.getElementById('pred-placeholder').style.display = 'none';
  document.getElementById('pred-results-card').style.display = 'block';

  // Banner
  const cat = result.predicted_category;
  document.getElementById('pred-category-name').textContent = cat;
  
  const badge = document.getElementById('pred-category-badge');
  badge.textContent = cat;
  badge.className = `cat-badge ${cat.toLowerCase()}`;

  document.getElementById('pred-confidence-score').textContent = `${result.confidence_percentage}%`;
  document.getElementById('pred-active-model-name').textContent = result.model_name;

  // Probability List
  const probList = document.getElementById('pred-probability-list');
  probList.innerHTML = '';

  const catColors = {
    politics: '#ef4444', sports: '#10b981', business: '#3b82f6', technology: '#8b5cf6',
    entertainment: '#ec4899', science: '#06b6d4', health: '#14b8a6', world: '#f59e0b'
  };

  result.probabilities.forEach(p => {
    const row = document.createElement('div');
    row.className = 'prob-row';
    const color = catColors[p.category.toLowerCase()] || 'var(--primary)';

    row.innerHTML = `
      <div class="prob-cat">${p.category}</div>
      <div class="prob-bar-track">
        <div class="prob-bar-fill" style="width: ${p.percentage}%; background-color: ${color};"></div>
      </div>
      <div class="prob-pct">${p.percentage}%</div>
    `;
    probList.appendChild(row);
  });

  // Top TF-IDF Chips
  const tfidfContainer = document.getElementById('pred-tfidf-chips');
  tfidfContainer.innerHTML = '';
  if (result.top_tfidf_features && result.top_tfidf_features.length > 0) {
    result.top_tfidf_features.forEach(f => {
      const chip = document.createElement('span');
      chip.className = 'token-chip tfidf-chip';
      chip.textContent = `${f.word} (${f.tfidf_weight})`;
      tfidfContainer.appendChild(chip);
    });
  } else {
    tfidfContainer.innerHTML = '<span style="color: var(--text-muted); font-size: 0.85rem;">No significant TF-IDF features.</span>';
  }
}

function displayAllModelsResult(predictions) {
  const card = document.getElementById('all-models-result-card');
  const grid = document.getElementById('all-models-grid');
  card.style.display = 'block';
  grid.innerHTML = '';

  Object.values(predictions).forEach(p => {
    const col = document.createElement('div');
    col.className = 'card';
    col.style.borderTop = '3px solid var(--primary)';
    col.innerHTML = `
      <div style="font-size: 0.75rem; text-transform: uppercase; color: var(--text-muted); font-weight: 600;">${p.model_type}</div>
      <h4 style="font-family: var(--font-heading); margin-bottom: 0.75rem;">${p.model_name}</h4>
      <div style="margin-bottom: 0.5rem;">
        <span class="cat-badge ${p.predicted_category.toLowerCase()}">${p.predicted_category}</span>
      </div>
      <div style="font-size: 1.5rem; font-weight: 800; color: var(--accent-emerald);">${p.confidence_percentage}%</div>
      <div style="font-size: 0.72rem; color: var(--text-muted);">Confidence Score</div>
    `;
    grid.appendChild(col);
  });
}

// ----------------- NLP Pipeline Inspector -----------------

function initNLPInspectorHandlers() {
  const btn = document.getElementById('btn-inspect-nlp');
  if (btn) {
    btn.addEventListener('click', async () => {
      const text = document.getElementById('nlp-inspector-input').value.trim();
      if (!text) {
        alert('Please enter text to inspect NLP stages.');
        return;
      }
      try {
        btn.disabled = true;
        btn.innerHTML = '<span class="spinner"></span>';
        const res = await fetch('/api/nlp/preprocess', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text: text })
        });
        const data = await res.json();
        updateNLPInspectorFromData(data, []);
      } catch (err) {
        alert(`NLP Error: ${err.message}`);
      } finally {
        btn.disabled = false;
        btn.textContent = 'Analyze Pipeline';
      }
    });
  }
}

function copyFromClassifyTab() {
  const text = document.getElementById('article-input').value.trim();
  if (!text) {
    alert('No text in classification tab. Please enter text there first.');
    return;
  }
  document.getElementById('nlp-inspector-input').value = text;
  document.getElementById('btn-inspect-nlp').click();
}

function updateNLPInspectorFromData(nlpTrace, topTfidf) {
  if (!nlpTrace) return;

  // Step 1: Raw
  document.getElementById('nlp-raw-stats').textContent = 
    `${nlpTrace.raw_stats.character_count} chars | ${nlpTrace.raw_stats.word_count} words`;
  document.getElementById('nlp-step-raw').textContent = nlpTrace.raw_text;

  // Step 2: Cleaned
  document.getElementById('nlp-clean-stats').textContent = 
    `${nlpTrace.cleaned_stats.character_count} chars (${nlpTrace.cleaned_stats.reduction_pct}% reduction)`;
  document.getElementById('nlp-step-cleaned').textContent = nlpTrace.cleaned_text;

  // Step 3: Tokens
  document.getElementById('nlp-tokens-count').textContent = `${nlpTrace.tokens_count} Tokens`;
  const tokensBox = document.getElementById('nlp-step-tokens');
  tokensBox.innerHTML = '';
  nlpTrace.tokens.forEach(t => {
    const chip = document.createElement('span');
    chip.className = 'token-chip';
    chip.textContent = t;
    tokensBox.appendChild(chip);
  });

  // Step 4: Stopwords
  document.getElementById('nlp-stopwords-count').textContent = `${nlpTrace.removed_stopwords_count} Removed`;
  const filteredBox = document.getElementById('nlp-step-filtered');
  filteredBox.innerHTML = '';
  nlpTrace.filtered_tokens.forEach(t => {
    const chip = document.createElement('span');
    chip.className = 'token-chip';
    chip.textContent = t;
    filteredBox.appendChild(chip);
  });

  const removedBox = document.getElementById('nlp-step-removed');
  removedBox.innerHTML = '';
  nlpTrace.removed_stopwords.forEach(t => {
    const chip = document.createElement('span');
    chip.className = 'token-chip removed';
    chip.textContent = t;
    removedBox.appendChild(chip);
  });

  // Step 5: Lemmatization
  document.getElementById('nlp-lemma-count').textContent = `${nlpTrace.lemmatized_count} Lemmatized`;
  const lemmaBox = document.getElementById('nlp-step-lemmas');
  lemmaBox.innerHTML = '';
  nlpTrace.lemmatized_tokens.forEach(t => {
    const chip = document.createElement('span');
    chip.className = 'token-chip lemmatized';
    chip.textContent = t;
    lemmaBox.appendChild(chip);
  });

  // Step 6: TF-IDF Table
  const tbody = document.getElementById('nlp-tfidf-tbody');
  tbody.innerHTML = '';
  if (topTfidf && topTfidf.length > 0) {
    topTfidf.forEach(f => {
      const tr = document.createElement('tr');
      const pct = (f.tfidf_weight * 100).toFixed(1);
      tr.innerHTML = `
        <td><span class="token-chip tfidf-chip">${f.word}</span></td>
        <td><code>${f.tfidf_weight}</code></td>
        <td style="width: 250px;">
          <div class="prob-bar-track">
            <div class="prob-bar-fill" style="width: ${pct}%; background-color: var(--primary);"></div>
          </div>
        </td>
      `;
      tbody.appendChild(tr);
    });
  } else if (nlpTrace.vocabulary_frequency) {
    nlpTrace.vocabulary_frequency.forEach(([word, freq]) => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td><span class="token-chip tfidf-chip">${word}</span></td>
        <td>Frequency: ${freq}</td>
        <td style="width: 250px;">
          <div class="prob-bar-track">
            <div class="prob-bar-fill" style="width: ${Math.min(100, freq * 25)}%; background-color: var(--accent-cyan);"></div>
          </div>
        </td>
      `;
      tbody.appendChild(tr);
    });
  }
}

// ----------------- Confusion Matrix Handlers -----------------

function initConfusionMatrixHandlers() {
  const select = document.getElementById('cm-model-select');
  if (select) {
    select.addEventListener('change', () => {
      fetchConfusionMatrix(select.value);
    });
  }
}

async function fetchConfusionMatrix(modelId) {
  try {
    const res = await fetch(`/api/models/confusion-matrix/${modelId}`);
    if (!res.ok) throw new Error('Failed to load confusion matrix');
    const data = await res.json();

    document.getElementById('cm-accuracy-stat').textContent = `${(data.accuracy * 100).toFixed(2)}%`;
    document.getElementById('cm-f1-stat').textContent = `${(data.f1_macro * 100).toFixed(2)}%`;
    document.getElementById('cm-card-title').textContent = 
      `${data.model_name} – Confusion Matrix Heatmap`;

    renderConfusionMatrixHeatmap(data);
    renderPerClassTable(data.per_class_metrics);
  } catch (err) {
    console.error('Confusion matrix error:', err);
  }
}

function renderConfusionMatrixHeatmap(data) {
  const container = document.getElementById('cm-heatmap-container');
  if (!container) return;

  const cats = data.categories;
  const cm = data.confusion_matrix;
  const cmNorm = data.confusion_matrix_normalized;

  let tableHtml = '<table class="cm-matrix"><thead><tr><th></th>';
  cats.forEach(c => {
    tableHtml += `<th class="cm-header-label" title="Predicted: ${c}">${c.substring(0, 4)}</th>`;
  });
  tableHtml += '</tr></thead><tbody>';

  for (let i = 0; i < cats.length; i++) {
    tableHtml += `<tr><td class="cm-header-label" style="text-align: right;" title="Actual: ${cats[i]}">${cats[i].substring(0, 4)}</td>`;
    for (let j = 0; j < cats.length; j++) {
      const count = cm[i][j];
      const norm = cmNorm[i][j];
      const isDiag = (i === j);

      // Color intensity
      let bgStyle = '';
      if (isDiag) {
        const alpha = Math.max(0.2, norm);
        bgStyle = `background: rgba(16, 185, 129, ${alpha}); color: #ffffff;`;
      } else if (count > 0) {
        bgStyle = `background: rgba(239, 68, 68, 0.4); color: #ffffff;`;
      } else {
        bgStyle = `background: var(--bg-input); color: var(--text-muted);`;
      }

      tableHtml += `
        <td class="cm-cell" style="${bgStyle}" 
            title="Actual: ${cats[i]} | Predicted: ${cats[j]} | Count: ${count} (${(norm*100).toFixed(1)}%)">
          ${count}
        </td>
      `;
    }
    tableHtml += '</tr>';
  }
  tableHtml += '</tbody></table>';

  container.innerHTML = tableHtml;
}

function renderPerClassTable(metrics) {
  const tbody = document.getElementById('cm-per-class-tbody');
  if (!tbody) return;

  tbody.innerHTML = '';
  metrics.forEach(m => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><span class="cat-badge ${m.category.toLowerCase()}">${m.category}</span></td>
      <td><strong>${(m.precision * 100).toFixed(2)}%</strong></td>
      <td><strong>${(m.recall * 100).toFixed(2)}%</strong></td>
      <td><strong>${(m.f1_score * 100).toFixed(2)}%</strong></td>
      <td>${m.support}</td>
    `;
    tbody.appendChild(tr);
  });
}

// ----------------- Dataset Explorer Handlers -----------------

function initDatasetExplorerHandlers() {
  const filter = document.getElementById('ds-filter-category');
  const btnRefresh = document.getElementById('btn-refresh-samples');

  if (filter) {
    filter.addEventListener('change', fetchDatasetSamples);
  }
  if (btnRefresh) {
    btnRefresh.addEventListener('click', fetchDatasetSamples);
  }

  fetchDatasetSamples();
}

async function fetchDatasetSamples() {
  const filter = document.getElementById('ds-filter-category');
  const category = filter ? filter.value : '';

  try {
    const url = category ? `/api/dataset/samples?category=${encodeURIComponent(category)}&limit=10` : '/api/dataset/samples?limit=10';
    const res = await fetch(url);
    if (!res.ok) throw new Error('Failed to load dataset samples');
    const data = await res.json();

    const tbody = document.getElementById('ds-samples-tbody');
    tbody.innerHTML = '';

    data.samples.forEach(sample => {
      const tr = document.createElement('tr');
      const wordLen = sample.text.split(/\s+/).length;
      tr.innerHTML = `
        <td><span class="cat-badge ${sample.category.toLowerCase()}">${sample.category}</span></td>
        <td style="font-size: 0.88rem; color: var(--text-primary); max-width: 500px;">${sample.text}</td>
        <td><span class="badge-pill">${wordLen} words</span></td>
        <td>
          <button class="btn btn-secondary btn-sm" onclick="loadSampleIntoClassifier(${JSON.stringify(sample.text).replace(/"/g, '&quot;')})">
            <i data-lucide="play" style="width: 12px; height: 12px;"></i>
            <span>Test</span>
          </button>
        </td>
      `;
      tbody.appendChild(tr);
    });

    initLucide();
  } catch (err) {
    console.error('Samples fetch error:', err);
  }
}

function loadSampleIntoClassifier(text) {
  document.getElementById('article-input').value = text;
  updateCharWordCount();
  navigateTo('classify');
  classifyCurrentArticle();
}
