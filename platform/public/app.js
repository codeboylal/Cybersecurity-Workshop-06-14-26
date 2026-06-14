// InnovateTech Security Lab - CTF Frontend
'use strict';

const SESSION_ID = localStorage.getItem('lab_session') || (() => {
  const id = Math.random().toString(36).slice(2);
  localStorage.setItem('lab_session', id);
  return id;
})();

const API = '/api';
let allChallenges = [];
let challengeStates = {};
let currentChallenge = null;
let timerInterval = null;
let workshopSeconds = 4 * 60 * 60;

const CAT_COLORS = {
  'Network': '#00d4ff',
  'Server & Linux': '#a855f7',
  'Web Security': '#ffd700',
  'Web Advanced': '#ff8c00',
  'Real World': '#ff4444',
};
const CAT_SHORT = {
  'Network': 'Network',
  'Server & Linux': 'Server',
  'Web Security': 'Web',
  'Web Advanced': 'Advanced',
  'Real World': 'RealWorld',
};

// ── INIT ────────────────────────────────────────────
async function init() {
  startTimer();
  await loadChallenges();
  await loadScore();
  renderChallenges('All');
  bindTabs();
}

// ── TIMER ────────────────────────────────────────────
function startTimer() {
  const saved = localStorage.getItem('lab_timer_start');
  if (saved) {
    const elapsed = Math.floor((Date.now() - parseInt(saved)) / 1000);
    workshopSeconds = Math.max(0, 4 * 60 * 60 - elapsed);
  } else {
    localStorage.setItem('lab_timer_start', Date.now().toString());
  }
  updateTimer();
  timerInterval = setInterval(() => {
    if (workshopSeconds > 0) workshopSeconds--;
    updateTimer();
  }, 1000);
}

function updateTimer() {
  const h = Math.floor(workshopSeconds / 3600);
  const m = Math.floor((workshopSeconds % 3600) / 60);
  const s = workshopSeconds % 60;
  const el = document.getElementById('timer');
  el.textContent = `${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`;
  el.className = 'timer';
  if (workshopSeconds < 900) el.classList.add('danger');
  else if (workshopSeconds < 1800) el.classList.add('warning');
}

// ── API CALLS ────────────────────────────────────────
async function api(path, opts = {}) {
  const r = await fetch(API + path, {
    headers: { 'Content-Type': 'application/json', 'x-session-id': SESSION_ID },
    ...opts,
  });
  return r.json();
}

async function loadChallenges() {
  allChallenges = await api('/challenges');
  for (const c of allChallenges) {
    challengeStates[c.id] = await api(`/challenges/${c.id}/state`);
  }
}

async function loadScore() {
  const data = await api('/leaderboard');
  document.getElementById('totalScore').textContent = data.totalPoints;
  document.getElementById('solvedCount').textContent = data.solved;
  document.getElementById('totalCount').textContent = data.total;
  const pct = Math.round((data.solved / data.total) * 100);
  document.getElementById('progressPct').textContent = pct + '%';
  const circumference = 150.8;
  const offset = circumference - (pct / 100) * circumference;
  document.getElementById('progressRing').style.strokeDashoffset = offset;
}

// ── RENDER ───────────────────────────────────────────
function bindTabs() {
  document.querySelectorAll('.cat-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.cat-tab').forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      renderChallenges(tab.dataset.cat);
    });
  });
}

function renderChallenges(cat) {
  const grid = document.getElementById('challengeGrid');
  const filtered = cat === 'All' ? allChallenges : allChallenges.filter(c => c.category === cat);

  grid.innerHTML = filtered.map(c => {
    const state = challengeStates[c.id] || {};
    const solved = state.solved;
    const catShort = CAT_SHORT[c.category] || 'Other';
    const catColor = CAT_COLORS[c.category] || '#888';
    const diffClass = `badge-${c.difficulty.toLowerCase()}`;

    return `
    <div class="challenge-card cat-${catShort} ${solved ? 'solved' : ''}"
         style="--cat-color:${catColor}"
         onclick="openChallenge(${c.id})">
      ${solved ? '<div class="solved-badge">✓ SOLVED</div>' : ''}
      <div class="card-header">
        <span class="card-id">#${String(c.id).padStart(2,'0')}</span>
        <span class="card-points">${c.points} pts</span>
      </div>
      <div class="card-title">${c.title}</div>
      <div class="card-desc">${c.description}</div>
      <div class="card-footer">
        <span class="badge ${diffClass}">${c.difficulty}</span>
        <span class="card-tools">${(c.tools || []).slice(0,2).join(' · ')}</span>
      </div>
    </div>`;
  }).join('');
}

// ── MODAL ────────────────────────────────────────────
async function openChallenge(id) {
  currentChallenge = allChallenges.find(c => c.id === id);
  if (!currentChallenge) return;

  const state = await api(`/challenges/${id}/state`);
  challengeStates[id] = state;

  const c = currentChallenge;
  document.getElementById('modalCategory').textContent = c.category;
  document.getElementById('modalDifficulty').textContent = c.difficulty;
  document.getElementById('modalDifficulty').className = `modal-difficulty badge badge-${c.difficulty.toLowerCase()}`;
  document.getElementById('modalPoints').textContent = `${c.points} pts`;
  document.getElementById('modalTitle').textContent = `#${c.id}. ${c.title}`;
  document.getElementById('modalTarget').textContent = c.target;
  document.getElementById('modalTools').textContent = (c.tools || []).join(', ');
  document.getElementById('modalDescription').textContent = c.description;

  renderHints(state, c);
  renderAttempts(state);
  renderSolution(state);

  const input = document.getElementById('flagInput');
  input.value = '';
  input.className = 'flag-input';
  document.getElementById('flagFeedback').textContent = '';
  document.getElementById('flagFeedback').className = 'flag-feedback';

  if (state.solved) {
    input.value = '*** SOLVED ***';
    input.className = 'flag-input correct';
    input.disabled = true;
    document.getElementById('flagFeedback').textContent = '✅ You already solved this challenge!';
    document.getElementById('flagFeedback').className = 'flag-feedback correct';
  } else {
    input.disabled = false;
    input.focus();
  }

  document.getElementById('modalOverlay').classList.add('open');
}

function renderHints(state, c) {
  const container = document.getElementById('hintsList');
  const unlocked = state.unlockedHints || [];
  const total = c.hints.length;
  const attempts = state.attempts || 0;

  const infoEl = document.getElementById('hintUnlockInfo');
  infoEl.textContent = `${unlocked.length}/${total} unlocked`;

  let html = '';
  for (let i = 0; i < total; i++) {
    if (i < unlocked.length) {
      html += `<div class="hint-item">
        <span class="hint-num">H${i+1}</span>
        <span class="hint-text">${unlocked[i]}</span>
      </div>`;
    } else {
      const needed = i === 0 ? 1 : i === 1 ? 3 : 5;
      html += `<div class="hint-locked">🔒 Hint ${i+1} unlocks after ${needed} attempts (${attempts}/${needed})</div>`;
    }
  }
  container.innerHTML = html;
}

function renderAttempts(state) {
  const el = document.getElementById('attemptCounter');
  const attempts = state.attempts || 0;
  if (state.solved) {
    el.textContent = '✅ Challenge solved!';
  } else {
    const remaining = Math.max(0, 6 - attempts);
    el.textContent = `Attempts: ${attempts} | Solution unlocks in: ${remaining} more wrong answer${remaining !== 1 ? 's' : ''}`;
  }
}

function renderSolution(state) {
  const section = document.getElementById('solutionSection');
  const btn = document.getElementById('solutionBtn');
  const content = document.getElementById('solutionContent');

  if (state.solutionUnlocked || state.solved) {
    section.style.display = 'block';
    btn.textContent = '📖 Show Solution';
    btn.classList.add('unlocked');
    content.style.display = 'none';
  } else {
    section.style.display = 'none';
  }
}

async function requestSolution() {
  if (!currentChallenge) return;
  const content = document.getElementById('solutionContent');

  if (content.style.display === 'block') {
    content.style.display = 'none';
    return;
  }

  const confirmed = confirm('⚠️ Are you sure you want to see the solution?\n\nTry a bit more first — the learning comes from the struggle! 💪');
  if (!confirmed) return;

  const data = await api(`/challenges/${currentChallenge.id}/solution`);
  if (data.error) {
    alert(data.error);
    return;
  }

  document.getElementById('solutionText').textContent = data.solution;
  document.getElementById('flagReveal').textContent = `Flag: ${data.flag}`;
  content.style.display = 'block';
}

// ── FLAG SUBMISSION ───────────────────────────────────
async function submitFlag() {
  if (!currentChallenge) return;
  const input = document.getElementById('flagInput');
  const feedback = document.getElementById('flagFeedback');
  const flag = input.value.trim();

  if (!flag) { input.focus(); return; }

  const result = await api(`/challenges/${currentChallenge.id}/submit`, {
    method: 'POST',
    body: JSON.stringify({ flag }),
  });

  challengeStates[currentChallenge.id] = await api(`/challenges/${currentChallenge.id}/state`);
  const state = challengeStates[currentChallenge.id];

  if (result.correct) {
    input.className = 'flag-input correct';
    input.disabled = true;
    feedback.textContent = result.message;
    feedback.className = 'flag-feedback correct';
    renderAttempts(state);
    renderSolution(state);
    renderHints(state, currentChallenge);
    await loadScore();
    renderChallenges(document.querySelector('.cat-tab.active').dataset.cat);
    if (!result.alreadySolved) showCelebration(currentChallenge);
  } else {
    input.className = 'flag-input wrong';
    setTimeout(() => input.classList.remove('wrong'), 400);
    feedback.textContent = result.message;
    feedback.className = 'flag-feedback wrong';
    renderAttempts(state);
    renderHints(state, currentChallenge);
    renderSolution(state);
    input.select();
  }
}

function showCelebration(c) {
  document.getElementById('celebrationMsg').textContent =
    `You captured "${c.title}" for ${c.points} points!`;
  document.getElementById('celebration').style.display = 'flex';
  setTimeout(() => {
    document.getElementById('celebration').style.display = 'none';
  }, 4000);
}

// ── MODAL CLOSE ───────────────────────────────────────
function closeModal(e) {
  if (e.target === document.getElementById('modalOverlay')) closeModalBtn();
}
function closeModalBtn() {
  document.getElementById('modalOverlay').classList.remove('open');
  document.getElementById('solutionContent').style.display = 'none';
  currentChallenge = null;
}

document.addEventListener('keydown', e => {
  if (e.key === 'Escape') closeModalBtn();
});

// ── START ─────────────────────────────────────────────
init();
