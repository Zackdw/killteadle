"""Build the restyled Killteamadle HTML with Kill Team PDF aesthetic."""
import json

# Read data
with open('data.json') as f:
    data = json.load(f)

with open('card_bg_b64.txt') as f:
    card_b64 = f.read().strip()

with open('page_bg_b64.txt') as f:
    page_b64 = f.read().strip()

embedded_json = json.dumps(data, indent=2)

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Killteamadle</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@400;600;700&family=Barlow+Condensed:wght@400;600;700&family=Barlow:wght@400;600&display=swap" rel="stylesheet">
<style>
  :root {{
    --kt-orange: #f15c22;
    --kt-orange-dark: #c44a1a;
    --kt-dark: #231f20;
    --kt-darker: #1a1715;
    --kt-light: #ebeeed;
    --kt-grey: #4f5d56;
    --kt-card-grey: #d1d3d5;
    --kt-green: #2d6a4f;
    --kt-red: #8b1a1a;
    --font-heading: 'Oswald', 'Impact', 'Arial Narrow', sans-serif;
    --font-body: 'Barlow', 'Segoe UI', system-ui, sans-serif;
    --font-condensed: 'Barlow Condensed', 'Arial Narrow', sans-serif;
  }}

  * {{ margin: 0; padding: 0; box-sizing: border-box; }}

  body {{
    font-family: var(--font-body);
    background: var(--kt-darker);
    background-image: url('data:image/jpeg;base64,{page_b64}');
    background-size: cover;
    background-attachment: fixed;
    background-position: center;
    color: var(--kt-light);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
  }}

  /* Title area */
  .title-bar {{
    width: 100%;
    background: linear-gradient(180deg, rgba(35,31,32,0.95) 0%, rgba(35,31,32,0.85) 100%);
    border-bottom: 3px solid var(--kt-orange);
    padding: 18px 0 14px;
    text-align: center;
    margin-bottom: 20px;
  }}

  h1 {{
    font-family: var(--font-heading);
    font-size: 36px;
    font-weight: 700;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: #fff;
    text-shadow: 0 0 20px rgba(241,92,34,0.4);
  }}

  h1 .accent {{
    color: var(--kt-orange);
  }}

  .subtitle {{
    font-family: var(--font-condensed);
    color: #999;
    font-size: 15px;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 4px;
  }}

  /* Guess counter */
  .guess-count {{
    font-family: var(--font-condensed);
    color: #888;
    font-size: 14px;
    margin-bottom: 14px;
    letter-spacing: 1px;
    text-transform: uppercase;
  }}

  .guess-count span {{
    color: var(--kt-orange);
    font-weight: 700;
  }}

  /* Input area */
  .input-area {{
    position: relative;
    width: 440px;
    max-width: 92vw;
    margin-bottom: 24px;
  }}

  .input-row {{
    display: flex;
    gap: 8px;
  }}

  .input-area input {{
    flex: 1;
    padding: 12px 16px;
    font-family: var(--font-condensed);
    font-size: 16px;
    letter-spacing: 0.5px;
    border: 2px solid #444;
    border-radius: 4px;
    background: rgba(35,31,32,0.9);
    color: var(--kt-light);
    outline: none;
    transition: border-color 0.2s;
  }}

  .input-area input:focus {{
    border-color: var(--kt-orange);
    box-shadow: 0 0 8px rgba(241,92,34,0.3);
  }}

  .input-area input:disabled {{
    opacity: 0.4;
    cursor: not-allowed;
  }}

  .input-area input::placeholder {{
    color: #666;
    font-style: italic;
  }}

  .guess-btn {{
    padding: 12px 22px;
    font-family: var(--font-heading);
    font-size: 16px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    background: var(--kt-orange);
    color: #fff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    white-space: nowrap;
    transition: all 0.2s;
  }}

  .guess-btn:hover {{
    background: var(--kt-orange-dark);
    box-shadow: 0 0 12px rgba(241,92,34,0.4);
  }}

  .guess-btn:disabled {{
    opacity: 0.4;
    cursor: not-allowed;
    box-shadow: none;
  }}

  /* Dropdown */
  .dropdown {{
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    max-height: 260px;
    overflow-y: auto;
    background: rgba(35,31,32,0.97);
    border: 1px solid #555;
    border-top: none;
    border-radius: 0 0 4px 4px;
    z-index: 10;
    display: none;
  }}

  .dropdown.visible {{ display: block; }}

  .dropdown-item {{
    padding: 10px 16px;
    cursor: pointer;
    font-family: var(--font-condensed);
    font-size: 14px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    transition: background 0.15s;
  }}

  .dropdown-item:hover,
  .dropdown-item.selected {{
    background: var(--kt-orange);
    color: #fff;
  }}

  .dropdown-item .team-hint {{
    color: #777;
    font-size: 12px;
    margin-left: 8px;
  }}

  .dropdown-item:hover .team-hint,
  .dropdown-item.selected .team-hint {{
    color: rgba(255,255,255,0.7);
  }}

  /* Guess table */
  .guesses {{
    width: 740px;
    max-width: 95vw;
  }}

  .guess-row {{
    display: grid;
    grid-template-columns: 1.5fr 0.6fr 1.2fr 0.8fr 1.8fr;
    gap: 5px;
    margin-bottom: 5px;
  }}

  .guess-header {{
    margin-bottom: 10px;
  }}

  .guess-header .cell {{
    background: rgba(35,31,32,0.85);
    background-image: url('data:image/jpeg;base64,{card_b64}');
    background-size: cover;
    background-blend-mode: overlay;
    color: var(--kt-orange);
    font-family: var(--font-heading);
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
    border: 1px solid rgba(241,92,34,0.3);
    border-bottom: 2px solid var(--kt-orange);
    position: relative;
  }}

  .guess-header .cell.has-tooltip {{
    cursor: help;
  }}

  .guess-header .cell.has-tooltip::after {{
    content: 'ⓘ';
    font-size: 10px;
    margin-left: 4px;
    opacity: 0.6;
  }}

  /* Tooltip */
  .tooltip {{
    visibility: hidden;
    opacity: 0;
    position: absolute;
    bottom: calc(100% + 8px);
    left: 50%;
    transform: translateX(-50%);
    background: var(--kt-dark);
    border: 1px solid var(--kt-orange);
    border-radius: 4px;
    padding: 10px 14px;
    font-family: var(--font-body);
    font-size: 11px;
    font-weight: 400;
    letter-spacing: 0;
    text-transform: none;
    color: var(--kt-light);
    white-space: nowrap;
    z-index: 20;
    transition: opacity 0.2s, visibility 0.2s;
    pointer-events: none;
    box-shadow: 0 4px 12px rgba(0,0,0,0.5);
  }}

  .tooltip::after {{
    content: '';
    position: absolute;
    top: 100%;
    left: 50%;
    transform: translateX(-50%);
    border: 6px solid transparent;
    border-top-color: var(--kt-orange);
  }}

  .guess-header .cell.has-tooltip:hover .tooltip {{
    visibility: visible;
    opacity: 1;
  }}

  .tooltip .tip-label {{
    color: var(--kt-orange);
    font-weight: 700;
    font-family: var(--font-condensed);
    text-transform: uppercase;
    font-size: 10px;
    letter-spacing: 1px;
    margin-bottom: 4px;
  }}

  .tooltip .tip-values {{
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
  }}

  .tooltip .tip-val {{
    background: rgba(241,92,34,0.15);
    border: 1px solid rgba(241,92,34,0.3);
    border-radius: 3px;
    padding: 2px 6px;
    font-size: 10px;
    font-family: var(--font-condensed);
    font-weight: 600;
  }}

  /* Guess cells */
  .cell {{
    padding: 10px 8px;
    border-radius: 3px;
    text-align: center;
    font-family: var(--font-condensed);
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.5px;
    transition: all 0.3s;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }}

  .cell.correct {{
    background: linear-gradient(135deg, #2d6a4f 0%, #1b5e3b 100%);
    border: 1px solid rgba(45,106,79,0.6);
    color: #fff;
    text-shadow: 0 1px 2px rgba(0,0,0,0.3);
  }}

  .cell.wrong {{
    background: linear-gradient(135deg, #7a1a1a 0%, #5a1111 100%);
    border: 1px solid rgba(122,26,26,0.6);
    color: rgba(255,255,255,0.85);
    text-shadow: 0 1px 2px rgba(0,0,0,0.3);
  }}

  /* Status */
  .status {{
    margin: 18px 0;
    font-family: var(--font-heading);
    font-size: 20px;
    font-weight: 700;
    text-align: center;
    min-height: 28px;
    letter-spacing: 1px;
    text-transform: uppercase;
  }}

  .status.win {{
    color: var(--kt-green);
    text-shadow: 0 0 12px rgba(45,106,79,0.5);
  }}

  .status.lose {{
    color: var(--kt-orange);
    text-shadow: 0 0 12px rgba(241,92,34,0.4);
  }}

  /* Play Again */
  .play-again {{
    margin-top: 8px;
    padding: 12px 36px;
    font-family: var(--font-heading);
    font-size: 16px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    background: var(--kt-orange);
    color: #fff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    display: none;
    transition: all 0.2s;
  }}

  .play-again:hover {{
    background: var(--kt-orange-dark);
    box-shadow: 0 0 16px rgba(241,92,34,0.4);
  }}

  /* Decorative orange bar at very bottom */
  .footer-bar {{
    margin-top: auto;
    width: 100%;
    height: 4px;
    background: var(--kt-orange);
  }}

  /* Responsive */
  @media (max-width: 600px) {{
    h1 {{ font-size: 26px; letter-spacing: 2px; }}
    .guess-row {{
      grid-template-columns: 1fr 0.5fr 1fr 0.7fr 1.4fr;
      gap: 3px;
    }}
    .cell {{ font-size: 11px; padding: 8px 4px; }}
    .tooltip {{ font-size: 10px; padding: 8px 10px; }}
  }}
</style>
</head>
<body>

<div class="title-bar">
  <h1>Kill<span class="accent">Team</span>adle</h1>
  <p class="subtitle">Guess the operative in 8 tries</p>
</div>

<p class="guess-count">Guesses: <span id="guessCount">0</span> / 8</p>

<div class="input-area">
  <div class="input-row">
    <input type="text" id="guessInput" placeholder="Type an operative name..." autocomplete="off">
    <button class="guess-btn" id="guessBtn">Guess</button>
  </div>
  <div class="dropdown" id="dropdown"></div>
</div>

<div class="guesses">
  <div class="guess-row guess-header">
    <div class="cell">Team</div>
    <div class="cell has-tooltip">APL
      <div class="tooltip">
        <div class="tip-label">Possible Values</div>
        <div class="tip-values">
          <span class="tip-val">1</span>
          <span class="tip-val">2</span>
          <span class="tip-val">3</span>
          <span class="tip-val">4</span>
        </div>
      </div>
    </div>
    <div class="cell has-tooltip">Faction
      <div class="tooltip">
        <div class="tip-label">Possible Values</div>
        <div class="tip-values">
          <span class="tip-val">IMPERIUM</span>
          <span class="tip-val">CHAOS</span>
          <span class="tip-val">TYRANID</span>
          <span class="tip-val">T\u2019AU EMPIRE</span>
          <span class="tip-val">AELDARI</span>
          <span class="tip-val">LEAGUES OF VOTANN</span>
          <span class="tip-val">ORK</span>
          <span class="tip-val">NECRON</span>
        </div>
      </div>
    </div>
    <div class="cell has-tooltip">Base
      <div class="tooltip">
        <div class="tip-label">Possible Values (mm)</div>
        <div class="tip-values">
          <span class="tip-val">25</span>
          <span class="tip-val">28</span>
          <span class="tip-val">32</span>
          <span class="tip-val">40</span>
          <span class="tip-val">50</span>
          <span class="tip-val">60x35</span>
        </div>
      </div>
    </div>
    <div class="cell">Operative</div>
  </div>
  <div id="guessRows"></div>
</div>

<div class="status" id="status"></div>
<button class="play-again" id="playAgain">Play Again</button>

<div class="footer-bar"></div>

'''

# Inject the embedded data and JS
html += '<script>var EMBEDDED_DATA = ' + embedded_json + ';</script>\\n'

html += '''<script>
let operatives = [];
let target = null;
let guesses = [];
let maxGuesses = 8;
let gameOver = false;

async function loadData() {
  if (typeof EMBEDDED_DATA !== 'undefined' && EMBEDDED_DATA.length > 0) {
    operatives = EMBEDDED_DATA;
  } else {
    try {
      const resp = await fetch('data.json');
      operatives = await resp.json();
    } catch (e) {
      console.error('Failed to load data:', e);
    }
  }
  pickTarget();
}

function pickTarget() {
  target = operatives[Math.floor(Math.random() * operatives.length)];
}

function resetGame() {
  guesses = [];
  gameOver = false;
  pickTarget();
  document.getElementById('guessRows').innerHTML = '';
  document.getElementById('status').textContent = '';
  document.getElementById('status').className = 'status';
  document.getElementById('guessCount').textContent = '0';
  document.getElementById('playAgain').style.display = 'none';
  const input = document.getElementById('guessInput');
  input.disabled = false;
  document.getElementById('guessBtn').disabled = false;
  input.value = '';
  input.focus();
}

// Autocomplete
const input = document.getElementById('guessInput');
const dropdown = document.getElementById('dropdown');
let selectedIdx = -1;
let filteredOps = [];

input.addEventListener('input', () => {
  const val = input.value.trim().toUpperCase();
  if (val.length < 1) {
    dropdown.classList.remove('visible');
    filteredOps = [];
    return;
  }

  const guessedNames = new Set(guesses.map(g => g.name));
  filteredOps = operatives
    .filter(o => !guessedNames.has(o.name) && o.name.toUpperCase().includes(val))
    .slice(0, 15);

  if (filteredOps.length === 0) {
    dropdown.classList.remove('visible');
    return;
  }

  selectedIdx = -1;
  renderDropdown();
  dropdown.classList.add('visible');
});

input.addEventListener('keydown', (e) => {
  if (!dropdown.classList.contains('visible') || filteredOps.length === 0) {
    if (e.key === 'Enter') {
      trySubmit(input.value.trim());
    }
    return;
  }

  if (e.key === 'ArrowDown') {
    e.preventDefault();
    selectedIdx = Math.min(selectedIdx + 1, filteredOps.length - 1);
    renderDropdown();
  } else if (e.key === 'ArrowUp') {
    e.preventDefault();
    selectedIdx = Math.max(selectedIdx - 1, -1);
    renderDropdown();
  } else if (e.key === 'Enter') {
    e.preventDefault();
    if (selectedIdx >= 0 && selectedIdx < filteredOps.length) {
      submitGuess(filteredOps[selectedIdx]);
    } else {
      trySubmit(input.value.trim());
    }
  } else if (e.key === 'Escape') {
    dropdown.classList.remove('visible');
  }
});

function trySubmit(val) {
  const upper = val.toUpperCase();
  const match = operatives.find(o => o.name.toUpperCase() === upper);
  if (match) {
    submitGuess(match);
  }
}

function renderDropdown() {
  dropdown.innerHTML = filteredOps.map((o, i) =>
    `<div class="dropdown-item${i === selectedIdx ? ' selected' : ''}"
          data-idx="${i}">
      ${o.name}<span class="team-hint">${o.team}</span>
    </div>`
  ).join('');

  dropdown.querySelectorAll('.dropdown-item').forEach(el => {
    el.addEventListener('mousedown', (e) => {
      e.preventDefault();
      const idx = parseInt(el.dataset.idx);
      submitGuess(filteredOps[idx]);
    });
  });

  if (selectedIdx >= 0) {
    const sel = dropdown.querySelector('.selected');
    if (sel) sel.scrollIntoView({ block: 'nearest' });
  }
}

input.addEventListener('blur', () => {
  setTimeout(() => dropdown.classList.remove('visible'), 150);
});

input.addEventListener('focus', () => {
  if (input.value.trim().length > 0 && filteredOps.length > 0) {
    dropdown.classList.add('visible');
  }
});

function submitGuess(op) {
  if (gameOver) return;

  if (guesses.find(g => g.name === op.name)) {
    input.value = '';
    dropdown.classList.remove('visible');
    return;
  }

  guesses.push(op);
  dropdown.classList.remove('visible');
  input.value = '';
  filteredOps = [];

  renderGuessRow(op);

  document.getElementById('guessCount').textContent = guesses.length;

  if (op.name === target.name) {
    gameOver = true;
    document.getElementById('status').textContent = `You got it in ${guesses.length} guess${guesses.length > 1 ? 'es' : ''}!`;
    document.getElementById('status').className = 'status win';
    input.disabled = true;
    document.getElementById('guessBtn').disabled = true;
    document.getElementById('playAgain').style.display = 'inline-block';
  } else if (guesses.length >= maxGuesses) {
    gameOver = true;
    document.getElementById('status').textContent = `Game over! It was ${target.name} (${target.team})`;
    document.getElementById('status').className = 'status lose';
    input.disabled = true;
    document.getElementById('guessBtn').disabled = true;
    document.getElementById('playAgain').style.display = 'inline-block';
  } else {
    input.focus();
  }
}

function renderGuessRow(op) {
  const row = document.createElement('div');
  row.className = 'guess-row';

  const fields = [
    { val: op.team, correct: op.team === target.team },
    { val: op.apl, correct: op.apl === target.apl },
    { val: op.faction, correct: op.faction === target.faction },
    { val: op.base_size, correct: op.base_size === target.base_size },
    { val: op.name, correct: op.name === target.name },
  ];

  fields.forEach(f => {
    const cell = document.createElement('div');
    cell.className = `cell ${f.correct ? 'correct' : 'wrong'}`;
    cell.textContent = f.val;
    cell.title = f.val;
    row.appendChild(cell);
  });

  document.getElementById('guessRows').appendChild(row);
}

document.getElementById('playAgain').addEventListener('click', resetGame);

document.getElementById('guessBtn').addEventListener('click', () => {
  if (selectedIdx >= 0 && selectedIdx < filteredOps.length) {
    submitGuess(filteredOps[selectedIdx]);
  } else {
    trySubmit(input.value.trim());
  }
});

loadData();
</script>
</body>
</html>
'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Done! Written index.html')
import os
sz = os.path.getsize('index.html')
print(f'File size: {sz:,} bytes')
