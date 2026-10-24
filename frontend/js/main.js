/**
 * JobShield AI - Core JavaScript (Theme Manager & Particle Animation)
 * Implements Aivent-style floating particle mesh and persistent dark/light mode.
 */

// ==========================================
// 1. THEME SWITCHER (DARK / LIGHT MODE)
// ==========================================
function initTheme() {
  const savedTheme = localStorage.getItem('jobshield_theme') || 'dark';
  const toggleBtn = document.getElementById('themeToggleBtn');
  
  if (savedTheme === 'light') {
    document.body.classList.add('light-mode');
    if (toggleBtn) toggleBtn.innerHTML = '☀️';
  } else {
    document.body.classList.remove('light-mode');
    if (toggleBtn) toggleBtn.innerHTML = '🌙';
  }
}

function toggleTheme() {
  const isLight = document.body.classList.toggle('light-mode');
  const toggleBtn = document.getElementById('themeToggleBtn');
  
  if (isLight) {
    localStorage.setItem('jobshield_theme', 'light');
    if (toggleBtn) toggleBtn.innerHTML = '☀️';
  } else {
    localStorage.setItem('jobshield_theme', 'dark');
    if (toggleBtn) toggleBtn.innerHTML = '🌙';
  }
}

// ==========================================
// 2. AIVENT-STYLE FLOATING PARTICLE MESH CANVAS
// ==========================================
function initParticleCanvas() {
  const canvas = document.getElementById('particleCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  let width = canvas.width = window.innerWidth;
  let height = canvas.height = window.innerHeight;

  window.addEventListener('resize', () => {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
  });

  const numParticles = Math.min(65, Math.floor(width / 22));
  const particles = [];

  for (let i = 0; i < numParticles; i++) {
    particles.push({
      x: Math.random() * width,
      y: Math.random() * height,
      vx: (Math.random() - 0.5) * 0.7,
      vy: (Math.random() - 0.5) * 0.7,
      radius: Math.random() * 2 + 1,
      color: Math.random() > 0.5 ? 'rgba(99, 102, 241,' : 'rgba(6, 182, 212,'
    });
  }

  function render() {
    ctx.clearRect(0, 0, width, height);

    const isLight = document.body.classList.contains('light-mode');
    const lineAlphaBase = isLight ? 0.08 : 0.15;
    const nodeAlpha = isLight ? 0.4 : 0.7;

    for (let i = 0; i < particles.length; i++) {
      const p = particles[i];
      p.x += p.vx;
      p.y += p.vy;

      if (p.x < 0) p.x = width;
      if (p.x > width) p.x = 0;
      if (p.y < 0) p.y = height;
      if (p.y > height) p.y = 0;

      // Draw particle node
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
      ctx.fillStyle = `${p.color} ${nodeAlpha})`;
      ctx.fill();

      // Connect near particles
      for (let j = i + 1; j < particles.length; j++) {
        const p2 = particles[j];
        const dx = p.x - p2.x;
        const dy = p.y - p2.y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < 130) {
          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          ctx.lineTo(p2.x, p2.y);
          const alpha = (1 - dist / 130) * lineAlphaBase;
          ctx.strokeStyle = `rgba(99, 102, 241, ${alpha})`;
          ctx.lineWidth = 1;
          ctx.stroke();
        }
      }
    }

    requestAnimationFrame(render);
  }

  render();
}

// ==========================================
// 3. ANIMATED NUMBER COUNTERS
// ==========================================
function animateCounters() {
  const counters = document.querySelectorAll('.counter-val');
  counters.forEach(counter => {
    const target = parseInt(counter.getAttribute('data-target') || '0', 10);
    const prefix = counter.getAttribute('data-prefix') || '';
    const suffix = counter.getAttribute('data-suffix') || '';
    let current = 0;
    const step = Math.max(1, Math.floor(target / 40));

    const timer = setInterval(() => {
      current += step;
      if (current >= target) {
        current = target;
        clearInterval(timer);
      }
      counter.innerText = `${prefix}${current.toLocaleString()}${suffix}`;
    }, 30);
  });
}

// ==========================================
// 4. API GATEWAY HEALTH PROBE
// ==========================================
async function checkApiGateway() {
  const el = document.getElementById('apiGatewayStatus');
  if (!el) return;

  function resolveApi() {
    if (typeof window !== 'undefined' && window.location && window.location.protocol.startsWith('http')) {
      if ((window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') && 
          window.location.port !== '8000' && window.location.port !== '') {
        return `http://${window.location.hostname}:8000/api`;
      }
      return `${window.location.origin}/api`;
    }
    return "http://127.0.0.1:8000/api";
  }

  const base = resolveApi();
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 3500);
    const res = await fetch(`${base}/health`, { signal: controller.signal });
    clearTimeout(timeoutId);

    if (res.ok) {
      el.innerHTML = `API Gateway: <strong style="color: var(--accent-success);">Online (Active)</strong>`;
    } else {
      el.innerHTML = `API Gateway: <strong style="color: var(--accent-warning);">Local Engine Mode</strong>`;
    }
  } catch (e) {
    el.innerHTML = `API Gateway: <strong style="color: var(--accent-cyan);">Ready (Standalone)</strong>`;
  }
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initParticleCanvas();
  animateCounters();
  checkApiGateway();
});
