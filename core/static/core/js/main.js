// ---- Footer: email opens Gmail compose on desktop ----
document.querySelectorAll('.ft-contact a[data-gmail]').forEach(a => {
  a.addEventListener('click', e => {
    if (window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
      e.preventDefault();
      window.open(a.dataset.gmail, '_blank', 'noopener');
    }
  });
});

// ---- Sticky navbar shadow on scroll ----
const navbar = document.getElementById('navbar');
const onScroll = () => navbar.classList.toggle('scrolled', window.scrollY > 30);
window.addEventListener('scroll', onScroll);
onScroll();

// ---- Mobile menu ----
const hamburger = document.getElementById('hamburger');
const navMenu = document.getElementById('navMenu');
hamburger.addEventListener('click', () => {
  hamburger.classList.toggle('open');
  navMenu.classList.toggle('open');
});
navMenu.querySelectorAll('a').forEach(a =>
  a.addEventListener('click', () => {
    hamburger.classList.remove('open');
    navMenu.classList.remove('open');
  })
);

// ---- Active link highlight on scroll ----
const links = document.querySelectorAll('.nav-link');
window.addEventListener('scroll', () => {
  let current = '';
  document.querySelectorAll('section[id]').forEach(sec => {
    if (window.scrollY >= sec.offsetTop - 120) current = '#' + sec.id;
  });
  links.forEach(l => l.classList.toggle('active', l.getAttribute('href') === current));
});

// ---- Hero shapes mouse parallax (desktop only) ----
const hero = document.querySelector('.hero');
if (hero && window.innerWidth > 992) {
  hero.addEventListener('mousemove', e => {
    const x = (e.clientX / window.innerWidth - 0.5) * 20;
    const y = (e.clientY / window.innerHeight - 0.5) * 20;
    hero.querySelectorAll('.shape').forEach((s, i) => {
      s.style.translate = `${x * (i + 1) * 0.4}px ${y * (i + 1) * 0.4}px`;
    });
  });
}

// ---- Scroll reveal (next sections ku) ----
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('active'); });
}, { threshold: 0.15 });
document.querySelectorAll('.reveal').forEach(el => observer.observe(el));


// ---- Why Choose Us: image mouse parallax (desktop only) ----
const whySec = document.querySelector('.why');
const whyImg = document.querySelector('.why-visual img');
if (whySec && whyImg && window.matchMedia('(min-width: 993px)').matches
    && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  whySec.addEventListener('mousemove', e => {
    const r = whySec.getBoundingClientRect();
    const x = (e.clientX - r.left) / r.width - 0.5;
    const y = (e.clientY - r.top) / r.height - 0.5;
    whyImg.style.translate = `${x * 18}px ${y * 12}px`;
  });
  whySec.addEventListener('mouseleave', () => { whyImg.style.translate = '0 0'; });
}

// ---- CTA banner: background mouse parallax (desktop only) ----
const ctaCard = document.querySelector('.cta-card');
const ctaImg = document.querySelector('.cta-bg');
if (ctaCard && ctaImg && window.matchMedia('(min-width: 993px)').matches
    && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  ctaCard.addEventListener('mousemove', e => {
    const r = ctaCard.getBoundingClientRect();
    const x = (e.clientX - r.left) / r.width - 0.5;
    const y = (e.clientY - r.top) / r.height - 0.5;
    ctaImg.style.translate = `${-x * 24}px ${-y * 16}px`;
  });
  ctaCard.addEventListener('mouseleave', () => { ctaImg.style.translate = '0 0'; });
}

// ---- Reviews: slider (prev / next / dots / autoplay) ----
(function () {
  const list = document.getElementById('rvList');
  if (!list) return;
  const sec = list.closest('.rv');
  const cards = [...list.querySelectorAll('.rv-card')];
  const controls = document.getElementById('rvControls');
  const dotsBox = document.getElementById('rvDots');
  const prev = document.getElementById('rvPrev');
  const next = document.getElementById('rvNext');
  const adminPer = Math.max(1, parseInt(sec.dataset.perPage, 10) || 3);
  const autoSec = parseInt(sec.dataset.autoplay, 10) || 0;
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let per = adminPer, page = 0, pages = 1, timer = null, paused = false;

  function show(p, dir) {
    page = (p + pages) % pages;
    list.dataset.dir = dir || 'next';
    cards.forEach((c, i) => {
      const on = i >= page * per && i < (page + 1) * per;
      c.hidden = !on;
      c.classList.remove('rv-in');
      if (on && dir) {
        c.style.setProperty('--i', i - page * per);
        void c.offsetWidth;
        c.classList.add('rv-in');
      }
    });
    dotsBox.querySelectorAll('.rv-dot').forEach((d, i) => d.classList.toggle('active', i === page));
  }

  function restart() {
    clearInterval(timer);
    if (autoSec > 0 && pages > 1 && !reduced) {
      timer = setInterval(() => { if (!paused && !document.hidden) show(page + 1, 'next'); }, autoSec * 1000);
    }
  }

  function go(p, dir) { show(p, dir); restart(); }

  function build() {
    per = window.innerWidth <= 576 ? Math.min(2, adminPer) : adminPer;
    pages = Math.max(1, Math.ceil(cards.length / per));
    dotsBox.innerHTML = '';
    for (let i = 0; i < pages; i++) {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'rv-dot';
      b.setAttribute('aria-label', 'Go to page ' + (i + 1));
      b.addEventListener('click', () => go(i, i > page ? 'next' : 'prev'));
      dotsBox.appendChild(b);
    }
    controls.hidden = pages <= 1;
    show(Math.min(page, pages - 1));
    restart();
  }

  prev.addEventListener('click', () => go(page - 1, 'prev'));
  next.addEventListener('click', () => go(page + 1, 'next'));
  sec.querySelectorAll('.rv-list-col, .rv-form-col').forEach(el => {
    el.addEventListener('mouseenter', () => { paused = true; });
    el.addEventListener('mouseleave', () => { paused = false; });
    el.addEventListener('focusin', () => { paused = true; });
    el.addEventListener('focusout', () => { paused = false; });
  });
  let rt;
  window.addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(build, 200); });
  build();
})();

// ---- Reviews: submit form (AJAX) ----
(function () {
  const form = document.getElementById('rvForm');
  if (!form) return;
  const ok = form.querySelector('.rv-success');
  const okMsg = ok.querySelector('p');
  const note = form.querySelector('.rv-note');
  const btn = form.querySelector('.rv-submit');

  const clearErrors = () => {
    form.querySelectorAll('.rv-field').forEach(f => f.classList.remove('invalid'));
    form.querySelectorAll('.rv-err').forEach(s => { s.textContent = ''; });
    note.hidden = true;
  };

  form.querySelector('.rv-again').addEventListener('click', () => ok.classList.remove('show'));

  form.querySelectorAll('input[type="text"], textarea, input[type="radio"]').forEach(el => {
    el.addEventListener('input', () => {
      const f = el.closest('.rv-field');
      if (f) { f.classList.remove('invalid'); f.querySelector('.rv-err').textContent = ''; }
    });
  });

  form.addEventListener('submit', async e => {
    e.preventDefault();
    clearErrors();
    btn.disabled = true;
    btn.classList.add('loading');
    try {
      const res = await fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: { 'X-Requested-With': 'XMLHttpRequest' },
      });
      const data = await res.json();
      if (data.ok) {
        okMsg.textContent = data.message;
        form.reset();
        ok.classList.add('show');
      } else if (data.errors) {
        Object.entries(data.errors).forEach(([k, msg]) => {
          const f = form.querySelector('.rv-field[data-field="' + k + '"]');
          if (f) { f.classList.add('invalid'); f.querySelector('.rv-err').textContent = msg; }
        });
      } else {
        note.textContent = data.error || 'Something went wrong. Please try again.';
        note.hidden = false;
      }
    } catch (err) {
      note.textContent = 'Network error. Please try again.';
      note.hidden = false;
    } finally {
      btn.disabled = false;
      btn.classList.remove('loading');
    }
  });
})();

// ---- Contact enquiry form (dynamic fields per tab) ----
(function () {
  const form = document.getElementById('ctForm');
  if (!form) return;
  const dataEl = document.getElementById('enquiryData');
  const types = dataEl ? JSON.parse(dataEl.textContent) : [];
  const typeInput = document.getElementById('ctType');
  const tabs = [...form.querySelectorAll('.ct-tab')];
  const head = document.getElementById('ctHead');
  const headIcon = head.querySelector('.ct-form-icon i');
  const headTitle = head.querySelector('h3');
  const headSub = head.querySelector('p');
  const dyn = document.getElementById('ctDyn');
  const msgEl = document.getElementById('ctMsg');
  const defaultMsgPh = msgEl.getAttribute('placeholder') || '';
  const nameEl = document.getElementById('ctName');
  const phoneEl = document.getElementById('ctPhone');
  const btn = form.querySelector('.ct-submit');
  const note = form.querySelector('.ct-note');
  const ok = form.querySelector('.ct-success');
  const okMsg = ok.querySelector('p');
  const waBtn = ok.querySelector('.ct-wa');
  const cc = form.dataset.cc || '';
  let current = types[0] || null;
  let built = [];                       // the fields currently shown for the active tab

  const mk = (tag, cls, text) => {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  };
  const field = k => form.querySelector('.ct-field[data-field="' + k + '"]');

  function showError(k, msg) {
    const f = field(k);
    if (!f) return;
    f.classList.remove('invalid');
    f.querySelector('.ct-err').textContent = msg || '';
    if (msg) { void f.offsetWidth; f.classList.add('invalid'); }
  }

  const todayStr = () => {
    const d = new Date();
    d.setMinutes(d.getMinutes() - d.getTimezoneOffset());
    return d.toISOString().slice(0, 10);
  };

  const REQ_MSG = { products: 'Please select at least one product.', quantity: 'Please select a quantity.' };
  function requiredMsg(spec) {
    if (REQ_MSG[spec.key]) return REQ_MSG[spec.key];
    if (spec.type === 'date') return 'Please choose a date.';
    const l = spec.label.toLowerCase();
    return ['select', 'multiselect', 'products'].includes(spec.type) ? 'Please select ' + l + '.' : 'Please enter ' + l + '.';
  }

  // close any open multi-select dropdown when clicking outside
  document.addEventListener('click', e => {
    dyn.querySelectorAll('.ct-multi.open').forEach(m => { if (!m.contains(e.target)) m.classList.remove('open'); });
  });

  // ---------- build one field from the admin settings ----------
  function buildField(spec, idx) {
    const wrap = mk('div', 'ct-field' + (spec.full ? ' ct-full' : ''));
    wrap.dataset.field = spec.key;
    wrap.style.setProperty('--i', idx);
    const id = 'ctf_' + spec.key;

    const label = mk('label');
    label.appendChild(document.createTextNode(spec.label));
    if (spec.required) {
      label.appendChild(document.createTextNode(' '));
      label.appendChild(mk('b', null, '*'));
    } else if (spec.optional_tag) {
      label.appendChild(document.createTextNode(' '));
      label.appendChild(mk('span', 'ct-opt', '(Optional)'));
    }
    wrap.appendChild(label);

    const api = { spec, wrap, focusEl: null, get: () => '' };
    const revalidate = () => { if (wrap.classList.contains('invalid')) showError(spec.key, api.validate()); };

    if (spec.type === 'textarea') {
      const ta = mk('textarea');
      ta.id = id; ta.name = spec.key; ta.maxLength = 500;
      ta.placeholder = spec.placeholder || '';
      ta.dataset.rows = spec.rows;
      ta.style.setProperty('--rows', spec.rows);
      ta.addEventListener('input', revalidate);
      label.htmlFor = id;
      wrap.appendChild(ta);
      api.focusEl = ta; api.get = () => ta.value.trim();

    } else if (spec.type === 'select') {
      const box = mk('div', 'ct-select');
      const sel = mk('select');
      sel.id = id; sel.name = spec.key; sel.required = true;
      const ph = mk('option', null, spec.placeholder || 'Select');
      ph.value = ''; ph.selected = true;
      if (spec.required) ph.disabled = true;
      sel.appendChild(ph);
      spec.options.forEach(o => { const op = mk('option', null, o); op.value = o; sel.appendChild(op); });
      sel.addEventListener('change', () => showError(spec.key, api.validate()));
      box.appendChild(sel);
      box.appendChild(mk('i', 'bi bi-chevron-down'));
      label.htmlFor = id;
      wrap.appendChild(box);
      api.focusEl = sel; api.get = () => sel.value;

    } else if (spec.type === 'multiselect' || spec.type === 'products') {
      let selected = [];
      const multi = mk('div', 'ct-multi');
      const trigger = mk('div', 'ct-multi-btn');
      trigger.setAttribute('role', 'button');
      trigger.tabIndex = 0;
      trigger.setAttribute('aria-haspopup', 'listbox');
      trigger.setAttribute('aria-expanded', 'false');
      const valBox = mk('span', 'ct-multi-val');
      trigger.appendChild(valBox);
      trigger.appendChild(mk('i', 'bi bi-chevron-down ct-caret'));
      const list = mk('ul', 'ct-multi-list');
      list.setAttribute('role', 'listbox');
      list.setAttribute('aria-multiselectable', 'true');
      multi.appendChild(trigger);
      multi.appendChild(list);
      wrap.appendChild(multi);

      const setOpen = o => { multi.classList.toggle('open', o); trigger.setAttribute('aria-expanded', o); };

      const syncList = () => list.querySelectorAll('li').forEach(li => {
        const on = selected.includes(li.dataset.v);
        li.classList.toggle('on', on);
        li.setAttribute('aria-selected', on);
      });

      const renderValue = () => {
        valBox.innerHTML = '';
        if (!selected.length) { valBox.appendChild(mk('span', 'ct-ph', spec.placeholder || '')); return; }
        selected.forEach(v => {
          const chip = mk('span', 'ct-chip');
          chip.appendChild(document.createTextNode(v));
          const x = mk('i', 'bi bi-x-lg');
          x.setAttribute('aria-label', 'Remove ' + v);
          x.addEventListener('click', e => { e.stopPropagation(); toggle(v); });
          chip.appendChild(x);
          valBox.appendChild(chip);
        });
      };

      function toggle(v) {
        selected = selected.includes(v) ? selected.filter(x => x !== v) : [...selected, v];
        renderValue(); syncList();
        if (selected.length) showError(spec.key, '');
      }

      spec.options.forEach(p => {
        const li = mk('li');
        li.setAttribute('role', 'option');
        li.dataset.v = p;
        li.innerHTML = '<span class="ct-box"><i class="bi bi-check-lg"></i></span><span></span>';
        li.lastChild.textContent = p;
        li.addEventListener('click', () => toggle(p));
        list.appendChild(li);
      });

      trigger.addEventListener('click', () => setOpen(!multi.classList.contains('open')));
      trigger.addEventListener('keydown', e => {
        if (['Enter', ' ', 'ArrowDown'].includes(e.key)) { e.preventDefault(); setOpen(true); }
        if (e.key === 'Escape') setOpen(false);
      });
      renderValue();
      api.focusEl = trigger; api.get = () => selected;

    } else {                              // text or date
      const inp = mk('input');
      inp.id = id; inp.name = spec.key;
      if (spec.type === 'date') { inp.type = 'date'; inp.min = todayStr(); }
      else { inp.type = 'text'; inp.maxLength = 200; inp.placeholder = spec.placeholder || ''; }
      inp.addEventListener('input', revalidate);
      label.htmlFor = id;
      wrap.appendChild(inp);
      api.focusEl = inp; api.get = () => inp.value.trim();
    }

    api.validate = () => {
      const v = api.get();
      const empty = Array.isArray(v) ? !v.length : !String(v).trim();
      return spec.required && empty ? requiredMsg(spec) : '';
    };

    wrap.appendChild(mk('small', 'ct-err'));
    return api;
  }

  function renderFields() {
    dyn.innerHTML = '';
    built = (current ? current.fields : []).map((s, i) => buildField(s, i));
    built.forEach(b => dyn.appendChild(b.wrap));
    msgEl.placeholder = (current && current.message_placeholder) || defaultMsgPh;
  }

  // ---------- name / phone rules ----------
  const rules = {
    name: () => nameEl.value.trim().replace(/\s+/g, ' ').length >= 3 ? '' : 'Name must be at least 3 characters.',
    phone: () => /^\d{10}$/.test(phoneEl.value) ? '' : 'Enter a valid 10-digit phone number (without country code).',
  };
  const check = k => { const m = rules[k](); showError(k, m); return m; };

  nameEl.addEventListener('blur', () => { if (nameEl.value) check('name'); });
  nameEl.addEventListener('input', () => { if (field('name').classList.contains('invalid')) check('name'); });
  phoneEl.addEventListener('blur', () => { if (phoneEl.value) check('phone'); });

  // phone: digits only, max 10, strips country code on paste
  phoneEl.addEventListener('input', () => {
    let v = phoneEl.value.replace(/\D/g, '');
    if (v.length > 10 && cc && v.startsWith(cc)) v = v.slice(cc.length);
    else if (v.length > 10 && v.startsWith('0')) v = v.replace(/^0+/, '');
    phoneEl.value = v.slice(0, 10);
    if (field('phone').classList.contains('invalid')) check('phone');
  });

  // ---------- enquiry type tabs ----------
  function setType(id, force) {
    const t = types.find(x => String(x.id) === String(id));
    if (!t) return;
    if (!force && current && t.id === current.id && built.length) return;   // same tab clicked again
    current = t;
    typeInput.value = t.id;
    tabs.forEach(b => {
      const on = b.dataset.id === String(t.id);
      b.classList.toggle('active', on);
      b.setAttribute('aria-selected', on);
    });
    head.classList.remove('swap'); void head.offsetWidth; head.classList.add('swap');
    headIcon.className = t.form_icon;
    headTitle.textContent = t.form_title;
    headSub.textContent = t.form_subtitle;
    renderFields();
  }
  tabs.forEach(b => b.addEventListener('click', () => setType(b.dataset.id)));
  renderFields();

  // ---------- success overlay ----------
  form.querySelector('.ct-again').addEventListener('click', () => ok.classList.remove('show'));

  // ---------- submit ----------
  form.addEventListener('submit', async e => {
    e.preventDefault();
    note.hidden = true;

    let firstBad = null;
    ['name', 'phone'].forEach(k => { if (check(k) && !firstBad) firstBad = { el: k === 'name' ? nameEl : phoneEl }; });
    built.forEach(b => {
      const m = b.validate();
      showError(b.spec.key, m);
      if (m && !firstBad) firstBad = { el: b.focusEl };
    });
    if (firstBad) { firstBad.el.focus(); return; }

    const fd = new FormData(form);
    built.forEach(b => { const v = b.get(); if (Array.isArray(v)) v.forEach(x => fd.append(b.spec.key, x)); });

    btn.disabled = true;
    btn.classList.add('loading');
    try {
      const res = await fetch(form.action, { method: 'POST', body: fd, headers: { 'X-Requested-With': 'XMLHttpRequest' } });
      if (!(res.headers.get('content-type') || '').includes('json')) {
        throw new Error('Server error (' + res.status + ')');
      }
      const data = await res.json();
      if (data.ok) {
        okMsg.textContent = data.message;
        if (data.whatsapp_url) { waBtn.href = data.whatsapp_url; waBtn.hidden = false; } else { waBtn.hidden = true; }
        ok.classList.add('show');
        form.reset();
        if (types[0]) setType(types[0].id, true);
      } else if (data.errors) {
        Object.entries(data.errors).forEach(([k, msg]) => showError(k, msg));
      } else {
        note.textContent = data.error || 'Something went wrong. Please try again.';
        note.hidden = false;
      }
    } catch (err) {
      note.textContent = err.message && err.message.startsWith('Server error') ? err.message + '. Please try again later.' : 'Network error. Please try again.';
      note.hidden = false;
    } finally {
      btn.disabled = false;
      btn.classList.remove('loading');
    }
  });
})();

// ---- Contact info: email opens Gmail compose on desktop ----
document.querySelectorAll('.ct-info-row[data-gmail]').forEach(a => {
  a.addEventListener('click', e => {
    if (window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
      e.preventDefault();
      window.open(a.dataset.gmail, '_blank', 'noopener');
    }
  });
});