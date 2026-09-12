const form = document.getElementById('blueprint-form');
const output = document.getElementById('output');
const state = document.getElementById('api-state');

function escapeHtml(value = '') {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

function list(items = []) {
  return `<ul>${items.map(item => `<li>${escapeHtml(item)}</li>`).join('')}</ul>`;
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  state.textContent = 'Generating';
  state.className = 'status neutral';
  output.innerHTML = '<div class="empty-state"><div class="spark">✦</div><h3>Building delivery blueprint…</h3><p>Mapping architecture, delivery phases, quality gates and measurable KPIs.</p></div>';

  const payload = {
    problem: document.getElementById('problem').value,
    users: document.getElementById('users').value,
    data: document.getElementById('data').value,
    constraints: document.getElementById('constraints').value,
    risk: document.getElementById('risk').value
  };

  try {
    const response = await fetch('/api/blueprint', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!response.ok) throw new Error('Blueprint API returned an error');
    const data = await response.json();

    output.innerHTML = `
      <div class="blueprint">
        <div>
          <h3>${escapeHtml(data.title)}</h3>
          <p class="summary">${escapeHtml(data.summary)}</p>
        </div>
        <div class="blueprint-block"><h4>Architecture</h4>${list(data.architecture)}</div>
        <div class="blueprint-block"><h4>Delivery plan</h4>${list(data.deliveryPlan)}</div>
        <div class="blueprint-block"><h4>Quality gates</h4>${list(data.qualityGates)}</div>
        <div class="blueprint-block"><h4>Success metrics</h4><div class="kpis">${data.kpis.map(k => `<span>${escapeHtml(k)}</span>`).join('')}</div></div>
      </div>`;
    state.textContent = 'Generated';
    state.className = 'status';
  } catch (error) {
    state.textContent = 'API error';
    state.className = 'status neutral';
    output.innerHTML = `<div class="empty-state"><h3>Could not generate blueprint</h3><p>${escapeHtml(error.message)}</p></div>`;
  }
});
