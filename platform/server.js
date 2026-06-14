const express = require('express');
const fs = require('fs');
const path = require('path');
const cors = require('cors');

const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

const challenges = JSON.parse(
  fs.readFileSync(path.join(__dirname, 'data', 'challenges.json'), 'utf-8')
);

// In-memory store: key = "sessionId:challengeId"
const attemptStore = {};
const solvedStore = {};

function getSessionKey(req) {
  return req.headers['x-session-id'] || req.ip || 'default';
}

// GET all challenges (strip flag and solution)
app.get('/api/challenges', (req, res) => {
  const safe = challenges.map(c => ({
    id: c.id,
    title: c.title,
    category: c.category,
    difficulty: c.difficulty,
    points: c.points,
    description: c.description,
    target: c.target,
    tools: c.tools,
    hints: c.hints,
  }));
  res.json(safe);
});

// GET attempt state for a challenge
app.get('/api/challenges/:id/state', (req, res) => {
  const session = getSessionKey(req);
  const id = parseInt(req.params.id);
  const key = `${session}:${id}`;
  const attempts = attemptStore[key] || 0;
  const solved = !!(solvedStore[key]);
  const solutionUnlocked = attempts >= 6;

  const challenge = challenges.find(c => c.id === id);
  let unlockedHints = [];
  if (attempts >= 1) unlockedHints = [challenge.hints[0]];
  if (attempts >= 3) unlockedHints = challenge.hints.slice(0, 2);
  if (attempts >= 5) unlockedHints = challenge.hints;

  res.json({
    id,
    attempts,
    solved,
    solutionUnlocked,
    unlockedHints,
  });
});

// POST submit flag
app.post('/api/challenges/:id/submit', (req, res) => {
  const session = getSessionKey(req);
  const id = parseInt(req.params.id);
  const key = `${session}:${id}`;
  const { flag } = req.body;

  const challenge = challenges.find(c => c.id === id);
  if (!challenge) return res.status(404).json({ error: 'Challenge not found' });

  if (solvedStore[key]) {
    return res.json({ correct: true, message: 'Already solved!', alreadySolved: true });
  }

  attemptStore[key] = (attemptStore[key] || 0) + 1;
  const attempts = attemptStore[key];

  const correct = flag && flag.trim().toUpperCase() === challenge.flag.toUpperCase();

  if (correct) {
    solvedStore[key] = true;
    return res.json({
      correct: true,
      message: '🎉 Correct! Flag accepted!',
      points: challenge.points,
      attempts,
    });
  }

  const solutionUnlocked = attempts >= 6;
  let unlockedHints = [];
  if (attempts >= 1) unlockedHints = [challenge.hints[0]];
  if (attempts >= 3) unlockedHints = challenge.hints.slice(0, 2);
  if (attempts >= 5) unlockedHints = challenge.hints;

  res.json({
    correct: false,
    message: attempts < 3
      ? `❌ Wrong flag. Keep trying! (Attempt ${attempts}/6 before solution unlocks)`
      : `❌ Wrong flag. A new hint has been unlocked! (Attempt ${attempts}/6)`,
    attempts,
    unlockedHints,
    solutionUnlocked,
  });
});

// GET solution (only after 6 attempts)
app.get('/api/challenges/:id/solution', (req, res) => {
  const session = getSessionKey(req);
  const id = parseInt(req.params.id);
  const key = `${session}:${id}`;
  const attempts = attemptStore[key] || 0;

  if (attempts < 6 && !solvedStore[key]) {
    return res.status(403).json({
      error: `Solution unlocks after 6 attempts. You have ${attempts} attempts so far.`
    });
  }

  const challenge = challenges.find(c => c.id === id);
  res.json({
    solution: challenge.solution,
    flag: challenge.flag,
  });
});

// GET leaderboard (session scores)
app.get('/api/leaderboard', (req, res) => {
  const session = getSessionKey(req);
  let totalPoints = 0;
  let solved = 0;

  for (const [key, isSolved] of Object.entries(solvedStore)) {
    if (key.startsWith(session + ':') && isSolved) {
      const challengeId = parseInt(key.split(':')[1]);
      const challenge = challenges.find(c => c.id === challengeId);
      if (challenge) {
        totalPoints += challenge.points;
        solved++;
      }
    }
  }

  res.json({ totalPoints, solved, total: challenges.length });
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`\n🔐 InnovateTech Security Lab - CTF Platform`);
  console.log(`🌐 Running at http://localhost:${PORT}`);
  console.log(`📚 Loaded ${challenges.length} challenges\n`);
});
