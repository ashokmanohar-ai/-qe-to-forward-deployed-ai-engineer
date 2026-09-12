const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 3000;
const PUBLIC_DIR = path.join(__dirname, 'public');

const mime = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml'
};

function sendJson(res, status, payload) {
  const body = JSON.stringify(payload, null, 2);
  res.writeHead(status, {
    'Content-Type': 'application/json; charset=utf-8',
    'Content-Length': Buffer.byteLength(body),
    'Cache-Control': 'no-store'
  });
  res.end(body);
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    let raw = '';
    req.on('data', chunk => {
      raw += chunk;
      if (raw.length > 1_000_000) reject(new Error('Payload too large'));
    });
    req.on('end', () => {
      try { resolve(raw ? JSON.parse(raw) : {}); }
      catch { reject(new Error('Invalid JSON')); }
    });
    req.on('error', reject);
  });
}

function blueprint(input = {}) {
  const problem = String(input.problem || 'Enterprise AI workflow').trim();
  const users = String(input.users || 'Business and engineering users').trim();
  const constraints = String(input.constraints || 'Security, reliability, explainability').trim();
  const data = String(input.data || 'Enterprise APIs and governed knowledge').trim();
  const risk = String(input.risk || 'Medium').trim();

  const riskLower = risk.toLowerCase();
  const governance = riskLower.includes('high')
    ? ['Human approval gate', 'Policy checks', 'Audit trail', 'Rollback plan']
    : ['Automated quality gate', 'Trace logging', 'Release checklist'];

  return {
    title: `${problem} — Delivery Blueprint`,
    summary: `A production-oriented FDE plan for ${users}, balancing fast discovery with measurable quality and operational safety.`,
    architecture: [
      'Experience layer: responsive SaaS UI and API-first workflows',
      'Orchestration layer: deterministic workflow + optional agent routing',
      `Context layer: ${data}`,
      'Quality layer: evaluation, test automation, guardrails and observability',
      'Runtime layer: Railway service, health checks and deployment telemetry'
    ],
    deliveryPlan: [
      'Discover: map user journey, constraints and measurable success criteria',
      'Prototype: build the thinnest end-to-end workflow with realistic data contracts',
      'Validate: exercise functional, AI quality, security and failure-mode tests',
      'Harden: add governance, retries, observability and operational runbooks',
      'Deploy: release with health checks, rollback readiness and adoption metrics'
    ],
    qualityGates: [
      'Acceptance criteria mapped to automated checks',
      'API contract and negative-path validation',
      'AI/RAG evaluation where probabilistic components are used',
      'Latency, reliability and graceful-degradation checks',
      ...governance
    ],
    constraints,
    risk,
    kpis: ['Time-to-first-value', 'Task success rate', 'Quality gate pass rate', 'P95 latency', 'Production incident rate']
  };
}

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://${req.headers.host || 'localhost'}`);

  if (req.method === 'GET' && url.pathname === '/health') {
    return sendJson(res, 200, {
      status: 'ok',
      service: 'fde-solution-studio-railway',
      runtime: 'node',
      timestamp: new Date().toISOString()
    });
  }

  if (req.method === 'GET' && url.pathname === '/api/capabilities') {
    return sendJson(res, 200, {
      capabilities: [
        'Discovery & problem framing',
        'Architecture blueprinting',
        'Agentic AI & RAG patterns',
        'AI quality engineering',
        'API and Playwright automation',
        'Deployment readiness',
        'Observability & governance'
      ]
    });
  }

  if (req.method === 'POST' && url.pathname === '/api/blueprint') {
    try {
      const body = await readBody(req);
      return sendJson(res, 200, blueprint(body));
    } catch (error) {
      return sendJson(res, 400, { error: error.message });
    }
  }

  if (req.method !== 'GET' && req.method !== 'HEAD') {
    return sendJson(res, 405, { error: 'Method not allowed' });
  }

  let relative = url.pathname === '/' ? 'index.html' : url.pathname.replace(/^\/+/, '');
  const filePath = path.normalize(path.join(PUBLIC_DIR, relative));
  if (!filePath.startsWith(PUBLIC_DIR)) return sendJson(res, 403, { error: 'Forbidden' });

  fs.readFile(filePath, (err, data) => {
    if (err) {
      fs.readFile(path.join(PUBLIC_DIR, 'index.html'), (fallbackErr, fallback) => {
        if (fallbackErr) return sendJson(res, 404, { error: 'Not found' });
        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
        if (req.method === 'HEAD') return res.end();
        res.end(fallback);
      });
      return;
    }
    res.writeHead(200, {
      'Content-Type': mime[path.extname(filePath)] || 'application/octet-stream',
      'Cache-Control': path.extname(filePath) === '.html' ? 'no-cache' : 'public, max-age=3600'
    });
    if (req.method === 'HEAD') return res.end();
    res.end(data);
  });
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(`FDE Solution Studio listening on port ${PORT}`);
});
