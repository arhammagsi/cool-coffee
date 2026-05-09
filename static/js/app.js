/* ══════════════════════════════════════════
   COOL COFFEE BAR — app.js
   Full frontend: modal, auth, contact, menu
══════════════════════════════════════════ */

/* ── MODAL: check if currently closed ── */
function checkTime() {
  const h = new Date().getHours();
  const closed = h < 9 || h >= 23;
  document.getElementById('closedWarn').classList.toggle('show', closed);
}

/* ── MODAL: enter site ── */
function enterSite() {
  const sel = document.getElementById('branchSel');
  if (!sel.value) {
    sel.style.borderColor = 'var(--orange)';
    sel.style.boxShadow   = '0 0 0 3px rgba(255,82,0,.2)';
    setTimeout(() => { sel.style.borderColor = ''; sel.style.boxShadow = ''; }, 1400);
    return;
  }
  document.getElementById('overlay').classList.add('gone');
  document.getElementById('site').classList.add('on');
  setTimeout(initReveal, 100);
}

/* ── MODAL: show again ── */
function showModal() {
  document.getElementById('overlay').classList.remove('gone');
  document.getElementById('site').classList.remove('on');
}

/* ── SMOOTH SCROLL ── */
function goTo(selector) {
  const el = document.querySelector(selector);
  if (el) el.scrollIntoView({ behavior: 'smooth' });
}

/* ── NAVBAR: stick on scroll ── */
window.addEventListener('scroll', () => {
  document.getElementById('nav').classList.toggle('stuck', window.scrollY > 50);
});

/* ── MENU TABS ── */
function switchTab(btn, id) {
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('on'));
  document.querySelectorAll('.mpanel').forEach(p => p.classList.remove('on'));
  btn.classList.add('on');
  document.getElementById(id).classList.add('on');
}

function switchTabById(id) {
  const tabs   = document.querySelectorAll('.tab');
  const panels = document.querySelectorAll('.mpanel');
  panels.forEach((p, i) => {
    const match = p.id === id;
    p.classList.toggle('on', match);
    if (tabs[i]) tabs[i].classList.toggle('on', match);
  });
}

/* ── SCROLL REVEAL ── */
function initReveal() {
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('visible');
        io.unobserve(e.target);
      }
    });
  }, { threshold: 0.1 });
  document.querySelectorAll('.reveal').forEach(el => io.observe(el));
}

/* ── LIVE HOURS STATUS ── */
(function initHours() {
  const DAYS  = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
  const today = new Date().getDay();
  const h     = new Date().getHours();
  const min   = new Date().getMinutes();

  document.querySelectorAll('#htbl tr').forEach(row => {
    if (row.cells[0]?.textContent.trim() === DAYS[today]) {
      row.classList.add('today');
    }
  });

  const phase8Open = (h > 17 || (h === 17 && min >= 30)) || h < 3;

  const pill = document.getElementById('spill');
  const dot  = document.getElementById('spDot');
  const txt  = document.getElementById('spTxt');

  if (pill && dot && txt) {
    if (phase8Open) {
      pill.style.cssText = 'background:rgba(74,222,128,.1);border:1px solid rgba(74,222,128,.25);color:#4ade80';
      dot.style.background = '#4ade80';
      txt.textContent = 'PHASE 8 OPEN NOW';
    } else {
      pill.style.cssText = 'background:rgba(255,82,0,.1);border:1px solid rgba(255,82,0,.25);color:var(--orange)';
      dot.style.background = 'var(--orange)';
      txt.textContent = 'OPENS AT 5:30 PM';
    }
  }
  checkTime();
})();


/* ══════════════════════════════════════════
   AUTH MODAL
══════════════════════════════════════════ */

function openAuth(panel) {
  document.getElementById('authOverlay').classList.add('open');
  switchAuth(panel || 'login');
}

function closeAuth() {
  document.getElementById('authOverlay').classList.remove('open');
}

function switchAuth(panel) {
  document.querySelectorAll('.auth-panel').forEach(p => p.classList.remove('active'));
  document.getElementById('auth' + panel.charAt(0).toUpperCase() + panel.slice(1)).classList.add('active');
  // Clear errors
  document.getElementById('loginError').textContent    = '';
  document.getElementById('registerError').textContent = '';
}

// Close auth modal on backdrop click
document.addEventListener('DOMContentLoaded', () => {
  const overlay = document.getElementById('authOverlay');
  if (overlay) {
    overlay.addEventListener('click', e => {
      if (e.target === overlay) closeAuth();
    });
  }
});

/* ── LOGIN ── */
async function doLogin() {
  const email    = document.getElementById('loginEmail').value.trim();
  const password = document.getElementById('loginPass').value;
  const errEl    = document.getElementById('loginError');

  if (!email || !password) {
    errEl.textContent = 'Please fill in all fields.';
    return;
  }

  const fd = new FormData();
  fd.append('email',    email);
  fd.append('password', password);

  const res  = await fetch('/login', { method: 'POST', body: fd });
  const data = await res.json();

  if (data.success) {
    showToast(`Welcome back, ${data.name}! ☕`);
    closeAuth();
    setTimeout(() => location.reload(), 800);
  } else {
    errEl.textContent = data.errors?.[0] || 'Login failed.';
  }
}

/* ── REGISTER ── */
async function doRegister() {
  const name     = document.getElementById('regName').value.trim();
  const email    = document.getElementById('regEmail').value.trim();
  const phone    = document.getElementById('regPhone').value.trim();
  const password = document.getElementById('regPass').value;
  const errEl    = document.getElementById('registerError');

  if (!name || !email || !password) {
    errEl.textContent = 'Please fill in all required fields.';
    return;
  }

  const fd = new FormData();
  fd.append('name',     name);
  fd.append('email',    email);
  fd.append('phone',    phone);
  fd.append('password', password);

  const res  = await fetch('/register', { method: 'POST', body: fd });
  const data = await res.json();

  if (data.success) {
    showToast(`Welcome to Cool Coffee, ${data.name}! ☕`);
    closeAuth();
    setTimeout(() => location.reload(), 800);
  } else {
    errEl.textContent = data.errors?.[0] || 'Registration failed.';
  }
}

/* Enter key support on auth forms */
document.addEventListener('keydown', e => {
  if (e.key !== 'Enter') return;
  const loginActive = document.getElementById('authLogin')?.classList.contains('active');
  if (loginActive) doLogin();
  else doRegister();
});


/* ══════════════════════════════════════════
   CONTACT FORM
══════════════════════════════════════════ */

async function submitContact() {
  const name    = document.getElementById('cfName')?.value.trim();
  const email   = document.getElementById('cfEmail')?.value.trim();
  const subject = document.getElementById('cfSubject')?.value.trim();
  const message = document.getElementById('cfMessage')?.value.trim();

  const errEl  = document.getElementById('contactError');
  const succEl = document.getElementById('contactSuccess');

  errEl.style.display  = 'none';
  succEl.style.display = 'none';

  if (!name || !email || !message) {
    errEl.textContent   = '⚠ Please fill in your name, email and message.';
    errEl.style.display = 'block';
    return;
  }

  const fd = new FormData();
  fd.append('name',    name);
  fd.append('email',   email);
  fd.append('subject', subject);
  fd.append('message', message);

  const res  = await fetch('/contact', { method: 'POST', body: fd });
  const data = await res.json();

  if (data.success) {
    succEl.style.display = 'block';
    document.getElementById('cfName').value    = '';
    document.getElementById('cfEmail').value   = '';
    document.getElementById('cfSubject').value = '';
    document.getElementById('cfMessage').value = '';
  } else {
    errEl.textContent   = data.errors?.[0] || 'Something went wrong. Try again.';
    errEl.style.display = 'block';
  }
}


/* ══════════════════════════════════════════
   TOAST NOTIFICATION
══════════════════════════════════════════ */

function showToast(msg) {
  let toast = document.getElementById('coolToast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'coolToast';
    toast.style.cssText = `
      position:fixed; bottom:32px; left:50%; transform:translateX(-50%) translateY(20px);
      background:#1a1a1a; border:1px solid var(--orange); color:var(--white);
      padding:14px 28px; border-radius:60px; font-size:13px; font-weight:500;
      z-index:99999; opacity:0; transition:all .35s cubic-bezier(.16,1,.3,1);
      white-space:nowrap; box-shadow:0 8px 40px rgba(255,82,0,.2);
    `;
    document.body.appendChild(toast);
  }
  toast.textContent = msg;
  requestAnimationFrame(() => {
    toast.style.opacity   = '1';
    toast.style.transform = 'translateX(-50%) translateY(0)';
  });
  setTimeout(() => {
    toast.style.opacity   = '0';
    toast.style.transform = 'translateX(-50%) translateY(20px)';
  }, 3200);
}


/* ══════════════════════════════════════════
   CART SYSTEM
══════════════════════════════════════════ */

let cart = [];   // { name, price, emoji, qty }

/* ── Open / Close ── */
function openCart() {
  document.getElementById('cartOverlay').classList.add('open');
  document.getElementById('cartSidebar').classList.add('open');
  renderCart();
}

function closeCart() {
  document.getElementById('cartOverlay').classList.remove('open');
  document.getElementById('cartSidebar').classList.remove('open');
}

/* ── Add to Cart ── */
function addToCart(name, price, emoji, btn) {
  const existing = cart.find(i => i.name === name);
  if (existing) {
    existing.qty++;
  } else {
    cart.push({ name, price, emoji, qty: 1 });
  }
  // Flash button
  btn.textContent = '✓ ADDED';
  btn.classList.add('added');
  setTimeout(() => {
    btn.textContent = '+ ADD TO CART';
    btn.classList.remove('added');
  }, 1200);

  updateCartCount();
  showToast(`${name} added to cart ☕`);
}

/* ── Update count badge ── */
function updateCartCount() {
  const total = cart.reduce((sum, i) => sum + i.qty, 0);
  const badge = document.getElementById('cartCount');
  badge.textContent = total;
  badge.classList.toggle('show', total > 0);
}

/* ── Render cart items ── */
function renderCart() {
  // Use a dedicated list container so #cartEmpty is never destroyed by innerHTML
  let listEl = document.getElementById('cartItemsList');
  if (!listEl) {
    listEl = document.createElement('div');
    listEl.id = 'cartItemsList';
    document.getElementById('cartItems').appendChild(listEl);
  }

  const footerEl = document.getElementById('cartFooter');
  const emptyEl  = document.getElementById('cartEmpty');

  if (cart.length === 0) {
    if (emptyEl)  emptyEl.style.display  = 'flex';
    if (footerEl) footerEl.style.display = 'none';
    listEl.innerHTML = '';
    return;
  }

  if (emptyEl)  emptyEl.style.display  = 'none';
  if (footerEl) footerEl.style.display = 'block';

  // Build items HTML
  let html = '';
  cart.forEach((item, idx) => {
    html += `
    <div class="cart-item">
      <div class="cart-item-emoji">${item.emoji}</div>
      <div class="cart-item-info">
        <div class="cart-item-name">${item.name}</div>
        <div class="cart-item-price">Rs ${item.price * item.qty}</div>
      </div>
      <div class="cart-item-qty">
        <button class="qty-btn" onclick="changeQty(${idx}, -1)">−</button>
        <span class="qty-num">${item.qty}</span>
        <button class="qty-btn" onclick="changeQty(${idx}, 1)">+</button>
      </div>
    </div>`;
  });

  listEl.innerHTML = html;

  // Update totals
  const total     = cart.reduce((sum, i) => sum + i.price * i.qty, 0);
  const itemCount = cart.reduce((sum, i) => sum + i.qty, 0);
  document.getElementById('cartTotal').textContent     = `Rs ${total}`;
  document.getElementById('cartItemCount').textContent = `${itemCount} item${itemCount !== 1 ? 's' : ''}`;

  // Show/hide login note based on session
  fetch('/api/me').then(r => r.json()).then(data => {
    const note = document.getElementById('cartLoginNote');
    const btn  = document.getElementById('checkoutBtn');
    if (!data.logged_in) {
      note.style.display = 'block';
      btn.textContent    = 'LOG IN TO ORDER';
      btn.onclick        = () => { closeCart(); openAuth('login'); };
    } else {
      note.style.display = 'none';
      btn.textContent    = 'PLACE ORDER';
      btn.onclick        = placeOrder;
    }
  });
}

/* ── Change quantity ── */
function changeQty(idx, delta) {
  cart[idx].qty += delta;
  if (cart[idx].qty <= 0) cart.splice(idx, 1);
  updateCartCount();
  renderCart();
}

/* ── Place Order ── */
async function placeOrder() {
  if (cart.length === 0) return;

  const branch = document.getElementById('cartBranch').value;
  const notes  = document.getElementById('cartNotes').value;
  const btn    = document.getElementById('checkoutBtn');

  btn.disabled    = true;
  btn.textContent = 'PLACING ORDER...';

  const res  = await fetch('/order', {
    method:  'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ items: cart, branch, notes })
  });
  const data = await res.json();

  btn.disabled    = false;
  btn.textContent = 'PLACE ORDER';

  if (data.success) {
    // Clear cart
    cart = [];
    updateCartCount();
    closeCart();

    // Show success modal
    document.getElementById('orderSuccessId').textContent = `Order #${data.order_id}  ·  Rs ${data.total}`;
    document.getElementById('orderSuccess').classList.add('open');
  } else {
    if (data.errors?.[0]?.includes('log in')) {
      showToast('Please log in to place an order!');
      closeCart();
      openAuth('login');
    } else {
      showToast(data.errors?.[0] || 'Something went wrong. Try again.');
    }
  }
}

/* ── Close success modal ── */
function closeOrderSuccess() {
  document.getElementById('orderSuccess').classList.remove('open');
}
