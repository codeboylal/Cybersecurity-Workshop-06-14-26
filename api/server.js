/**
 * InnovateTech Vulnerable API Service
 * Demonstrates: JWT vulnerabilities, GraphQL introspection, API key auth
 * Educational use only
 */
const express = require('express');
const cors = require('cors');
const jwt = require('jsonwebtoken');
const { buildSchema } = require('graphql');
const { graphqlHTTP } = require('express-graphql');

const app = express();
app.use(cors());
app.use(express.json());

const JWT_SECRET = process.env.JWT_SECRET || 'secret123';
const API_KEY = process.env.API_KEY || 'sk-prod-7f3k9x2mAbCdEf123456';
const PORT = process.env.PORT || 4000;

const USERS = {
  'user': { id: 1, username: 'user', password: 'password123', role: 'user', email: 'user@innovatetech.com' },
  'admin': { id: 999, username: 'admin', password: 'Adm1n@InnovateTech2024', role: 'admin', email: 'admin@innovatetech.com' },
};

// ── LOGIN - issues JWT ──────────────────────────────────────
app.post('/api/login', (req, res) => {
  const { username, password } = req.body;
  const user = USERS[username];
  if (!user || user.password !== password) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }
  // Signs with HS256 and weak secret 'secret123'
  const token = jwt.sign(
    { id: user.id, username: user.username, role: user.role },
    JWT_SECRET,
    { algorithm: 'HS256', expiresIn: '24h' }
  );
  res.json({
    token,
    message: 'Login successful',
    user: { id: user.id, username: user.username, role: user.role },
    hint: 'Try cracking this JWT with hashcat or jwt_tool!'
  });
});

// ── JWT MIDDLEWARE ──────────────────────────────────────────
function verifyToken(req) {
  const auth = req.headers['authorization'] || '';
  const token = auth.replace('Bearer ', '');
  if (!token) return null;
  try {
    // VULNERABLE: accepts 'none' algorithm implicitly in some configs
    // Also weak secret is crackable
    return jwt.verify(token, JWT_SECRET, { algorithms: ['HS256', 'none'] });
  } catch (e) {
    // Try decoding without verification (simulates 'none' alg bypass)
    try {
      const parts = token.split('.');
      if (parts.length === 3) {
        const header = JSON.parse(Buffer.from(parts[0], 'base64').toString());
        const payload = JSON.parse(Buffer.from(parts[1], 'base64').toString());
        if (header.alg === 'none' || header.alg === 'None' || header.alg === 'NONE') {
          return payload; // Accept token with no signature!
        }
      }
    } catch (_) {}
    return null;
  }
}

// ── PROFILE - requires JWT ──────────────────────────────────
app.get('/api/profile', (req, res) => {
  const user = verifyToken(req);
  if (!user) return res.status(401).json({ error: 'Authentication required', hint: 'Get a token from POST /api/login' });
  res.json({ user, message: 'Profile data', flag: user.role === 'admin' ? 'FLAG{jwt_n0n3_4lg_byp4ss_4dm1n}' : null });
});

// ── ADMIN ENDPOINTS ─────────────────────────────────────────
app.get('/api/admin/flag', (req, res) => {
  const user = verifyToken(req);
  if (!user) return res.status(401).json({ error: 'Authentication required' });
  if (user.role !== 'admin') {
    return res.status(403).json({ error: 'Admin access required', your_role: user.role,
      hint: 'Try JWT none algorithm attack or crack the JWT secret!' });
  }
  res.json({ flag: 'FLAG{jwt_n0n3_4lg_byp4ss_4dm1n}', message: 'Welcome, admin!' });
});

app.get('/api/admin/secret', (req, res) => {
  const apiKey = req.headers['x-api-key'];
  if (!apiKey) return res.status(401).json({ error: 'API key required in X-API-Key header', hint: 'Check the JavaScript source files on the main site!' });
  if (apiKey !== API_KEY) return res.status(401).json({ error: 'Invalid API key' });
  res.json({
    flag: 'FLAG{4p1_k3y_1n_js_1s_publ1c}',
    message: 'You found the leaked API key!',
    secret_data: { internal_endpoint: 'http://internal-flag:9999', db_password: 'root', encryption_key: 'aes256_key_123' }
  });
});

// ── JWT WEAK SECRET endpoint ─────────────────────────────────
app.get('/api/admin/cracked', (req, res) => {
  const user = verifyToken(req);
  if (!user || user.role !== 'admin') {
    return res.status(403).json({ error: 'Admin only', hint: 'Crack the JWT secret with: hashcat -a 0 -m 16500 TOKEN /usr/share/wordlists/rockyou.txt' });
  }
  res.json({ flag: 'FLAG{w34k_jwt_s3cr3t_cr4ck3d}', secret_used: JWT_SECRET });
});

// ── GRAPHQL ─────────────────────────────────────────────────
const schema = buildSchema(`
  type Query {
    hello: String
    user(id: Int): User
    publicData: [Product]
    secretFlag: SecretData
    adminData: AdminData
  }
  type User {
    id: Int
    username: String
    email: String
    role: String
  }
  type Product {
    id: Int
    name: String
    price: Float
  }
  type SecretData {
    flag: String
    message: String
    internalEndpoint: String
  }
  type AdminData {
    users: [User]
    revenue: Float
    secretKey: String
  }
`);

const root = {
  hello: () => 'InnovateTech GraphQL API v2.0',
  user: ({ id }) => ({ id, username: 'user' + id, email: `user${id}@example.com`, role: 'user' }),
  publicData: () => [
    { id: 1, name: 'CloudSync Pro', price: 299.99 },
    { id: 2, name: 'AI Analytics', price: 499.99 },
  ],
  // Hidden via introspection - challenge #42
  secretFlag: () => ({
    flag: 'FLAG{gr4phql_1ntr0sp3ct10n_l34ks}',
    message: 'You found the hidden GraphQL query via introspection!',
    internalEndpoint: 'http://internal-flag:9999/flag'
  }),
  adminData: () => ({
    users: Object.values(USERS).map(u => ({ id: u.id, username: u.username, email: u.email, role: u.role })),
    revenue: 2400000.00,
    secretKey: JWT_SECRET
  }),
};

app.use('/graphql', graphqlHTTP({
  schema,
  rootValue: root,
  graphiql: true,  // Introspection enabled! (vulnerability)
}));

// ── INFO ─────────────────────────────────────────────────────
app.get('/', (req, res) => {
  res.json({
    service: 'InnovateTech API',
    version: '2.1.0',
    endpoints: {
      'POST /api/login': 'Get JWT token (user:password123 or admin:Adm1n@InnovateTech2024)',
      'GET /api/profile': 'Get profile (requires Bearer JWT)',
      'GET /api/admin/flag': 'Admin flag (requires admin JWT)',
      'GET /api/admin/secret': 'Secret data (requires X-API-Key header)',
      'GET /graphql': 'GraphQL endpoint (introspection enabled!)',
    },
    challenges: ['JWT None Algorithm', 'JWT Weak Secret', 'API Key in JS', 'GraphQL Introspection']
  });
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`🔌 Vulnerable API running on port ${PORT}`);
  console.log(`   JWT Secret: ${JWT_SECRET}`);
  console.log(`   GraphQL: http://localhost:${PORT}/graphql`);
});
