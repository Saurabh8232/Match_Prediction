/* ═══════════════════════════════════════════════
   CricketAI — main.js
   Handles: Navbar · API calls · Predictions
════════════════════════════════════════════════ */

const API = 'http://127.0.0.1:8000';

/* ── Navbar toggle ── */
function toggleNav() {
  document.getElementById('navLinks').classList.toggle('open');
}

/* ── Fill a <select> with options ── */
function fillSelect(id, items) {
  const sel = document.getElementById(id);
  if (!sel) return;
  items.forEach(v => {
    const o = document.createElement('option');
    o.value = o.textContent = v;
    sel.appendChild(o);
  });
}

/* ── Load dropdown data from Django /meta/ ── */
async function loadMeta() {
  try {
    const res  = await fetch(`${API}/meta/`);
    const meta = await res.json();
    fillSelect('batting_team',   meta.teams);
    fillSelect('bowling_team',   meta.teams);
    fillSelect('venue',          meta.venues);
    fillSelect('pitch_condition',meta.pitch_conditions);
  } catch {
    // Fallback static data if API not running yet
    const teams      = ['CSK','DC','GT','KKR','LSG','MI','PBKS','RCB','RR','SRH'];
    const venues     = ['Arun Jaitley Stadium','Chepauk Stadium','Chinnaswamy Stadium',
                        'Eden Gardens','Narendra Modi Stadium','Rajiv Gandhi Stadium',
                        'Sawai Mansingh Stadium','Wankhede Stadium'];
    const conditions = ['Dry','Dusty','Flat','Green','Hard'];
    fillSelect('batting_team',   teams);
    fillSelect('bowling_team',   teams);
    fillSelect('venue',          venues);
    fillSelect('pitch_condition',conditions);
  }
}

/* ── Auto-calculate run rate & overs remaining ── */
function autoCalc() {
  const score = parseFloat(document.getElementById('current_score')?.value);
  const overs = parseFloat(document.getElementById('overs_completed')?.value);
  const rrEl  = document.getElementById('run_rate');
  const orEl  = document.getElementById('overs_remaining');

  if (score > 0 && overs > 0 && rrEl) {
    rrEl.value = (score / overs).toFixed(2);
  }
  if (!isNaN(overs) && overs >= 0 && orEl) {
    orEl.value = Math.max(0, 20 - overs).toFixed(1);
  }
}

/* ── Show / hide error message ── */
function showErr(msg) {
  const box  = document.getElementById('errorMsg');
  const text = document.getElementById('errorText');
  if (!box) return;
  if (text) text.textContent = msg;
  box.style.display = 'flex';
}
function hideErr() {
  const box = document.getElementById('errorMsg');
  if (box) box.style.display = 'none';
}

/* ── Set text content of an element by id ── */
function setText(id, value) {
  const el = document.getElementById(id);
  if (el) el.textContent = value;
}

/* ── Pop animation ── */
function popAnimate(id) {
  const el = document.getElementById(id);
  if (!el) return;
  el.classList.remove('pop');
  void el.offsetWidth;
  el.classList.add('pop');
}

/* ── Main predict function ── */
async function predict() {
  const btn = document.getElementById('predictBtn');
  hideErr();

  const g = id => document.getElementById(id)?.value || '';

  // Required fields validation
  const required = [
    'batting_team','bowling_team','venue','pitch_condition',
    'current_score','overs_completed','wickets_out',
    'runs_last_5_overs','overs_remaining','run_rate'
  ];
  for (const f of required) {
    if (!g(f)) {
      showErr('Please fill in: ' + f.replace(/_/g, ' '));
      return;
    }
  }

  if (g('batting_team') === g('bowling_team')) {
    showErr('Batting and bowling team cannot be the same.');
    return;
  }

  // Loading state
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span> Predicting...';

  try {
    const payload = {
      batting_team:      g('batting_team'),
      bowling_team:      g('bowling_team'),
      venue:             g('venue'),
      pitch_condition:   g('pitch_condition'),
      current_score:     parseFloat(g('current_score')),
      overs_completed:   parseFloat(g('overs_completed')),
      wickets_out:       parseInt(g('wickets_out')),
      runs_last_5_overs: parseFloat(g('runs_last_5_overs')),
      overs_remaining:   parseFloat(g('overs_remaining')),
      run_rate:          parseFloat(g('run_rate')),
    };

    const res = await fetch(`${API}/predict/`, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify(payload)
    });

    if (!res.ok) {
      const d = await res.json();
      throw new Error(d.error || 'Server error');
    }

    const data = await res.json();

    // ── Update result cards ──
    setText('predScore',      data.predicted_score);
    setText('predScoreSub',   `Polynomial Regression · ${payload.batting_team} vs ${payload.bowling_team}`);
    setText('predWickets',    data.wickets_remaining);
    setText('predWicketsSub', `${data.wickets_lost} lost · ${data.wickets_remaining} in hand`);

    const extra = data.predicted_score - payload.current_score;
    setText('predRuns',    extra > 0 ? `+${extra}` : `${extra}`);
    setText('predRunsSub', `in ${payload.overs_remaining} overs · ~${(extra / payload.overs_remaining).toFixed(1)} per over`);

    const runsBox = document.getElementById('runsBox');
    if (runsBox) runsBox.style.display = 'block';

    document.getElementById('scoreBox')?.classList.add('highlighted');
    document.getElementById('wicketsBox')?.classList.add('highlighted');

    // ── Fill summary card ──
    setText('s_bat',   payload.batting_team);
    setText('s_bowl',  payload.bowling_team);
    setText('s_score', `${payload.current_score} / ${payload.wickets_out}`);
    setText('s_overs', payload.overs_completed);
    setText('s_rr',    payload.run_rate);
    setText('s_pitch', payload.pitch_condition);

    document.getElementById('summaryCard')?.classList.add('show');

    // Pop animations
    ['predScore', 'predWickets', 'predRuns'].forEach(popAnimate);

  } catch (err) {
    showErr(
      err.message.includes('fetch')
        ? 'Cannot connect to server. Make sure Django is running on port 8000.'
        : err.message
    );
  } finally {
    btn.disabled = false;
    btn.innerHTML = '<i class="fa-solid fa-wand-magic-sparkles"></i> Get Prediction';
  }
}

/* ── Init on page load ── */
document.addEventListener('DOMContentLoaded', () => {
  loadMeta();

  // Attach auto-calc listeners (only on predictor page)
  document.getElementById('current_score')?.addEventListener('input', autoCalc);
  document.getElementById('overs_completed')?.addEventListener('input', autoCalc);
});
