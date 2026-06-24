const BASE = 'https://apipwa.sembrandodatos.com'

function token() {
  return localStorage.getItem('_obs_tk') || ''
}

function headers() {
  return {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${token()}`,
  }
}

export async function obsLogin(handle, secret) {
  const r = await fetch(`${BASE}/sys/status/auth`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ handle, secret }),
  })
  if (!r.ok) throw new Error('Credenciales incorrectas')
  const d = await r.json()
  localStorage.setItem('_obs_tk', d.token)
  return d
}

export function obsLogout() {
  localStorage.removeItem('_obs_tk')
}

export function isLoggedIn() {
  const tk = token()
  if (!tk) return false
  try {
    const payload = JSON.parse(atob(tk.split('.')[1]))
    return payload.exp > Date.now() / 1000
  } catch {
    return false
  }
}

export async function fetchData(params = {}) {
  const q = new URLSearchParams()
  for (const [k, v] of Object.entries(params)) {
    if (v !== null && v !== undefined && v !== '') q.set(k, v)
  }
  const r = await fetch(`${BASE}/sys/status/data?${q}`, { headers: headers() })
  if (r.status === 401) { obsLogout(); throw new Error('session') }
  if (!r.ok) throw new Error('Error al cargar datos')
  return r.json()
}

export async function fetchFilters() {
  const r = await fetch(`${BASE}/sys/status/actions`, { headers: headers() })
  if (!r.ok) return { actions: [], modules: [] }
  return r.json()
}
