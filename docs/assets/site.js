/* Berger Landscaping — site behavior. No dependencies. */
(function () {
  "use strict";
  // ---- Owner-editable config -------------------------------------------
  // quoteForm: set to true AND set formEndpoint (FormSubmit AJAX or Formspree URL; set in _source/data.py FORM_ENDPOINT) to show the online quote form.
  // beforeAfter: add pairs like {before:"img/x-before.webp", after:"img/x-after.webp", caption:"Front bed refresh"}.
  var CONFIG = window.BERGER_CONFIG || { quoteForm: false, formEndpoint: "", beforeAfter: [] };
  // ----------------------------------------------------------------------
  var d = document, root = d.documentElement;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var finePointer = window.matchMedia("(pointer: fine)").matches;
  function $(s, c) { return (c || d).querySelector(s); }
  function $$(s, c) { return Array.prototype.slice.call((c || d).querySelectorAll(s)); }
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }

  // year
  $$("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });

  // ---- theme ----
  var themeBtn = $("[data-theme-toggle]");
  var MOON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 14.5A8.5 8.5 0 0 1 9.5 4a8.5 8.5 0 1 0 10.5 10.5z"/></svg>';
  var SUN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2.5v2M12 19.5v2M4.6 4.6 6 6M18 18l1.4 1.4M2.5 12h2M19.5 12h2M4.6 19.4 6 18M18 6l1.4-1.4"/></svg>';
  function isDark() { var t = root.getAttribute("data-theme"); return t ? t === "dark" : window.matchMedia("(prefers-color-scheme: dark)").matches; }
  function paintThemeBtn() { if (!themeBtn) return; var dk = isDark(); themeBtn.innerHTML = dk ? SUN : MOON; themeBtn.setAttribute("aria-label", dk ? "Switch to light theme" : "Switch to dark theme"); }
  paintThemeBtn();
  if (themeBtn) themeBtn.addEventListener("click", function () { var next = isDark() ? "light" : "dark"; root.setAttribute("data-theme", next); store("berger-theme", next); paintThemeBtn(); });
  window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", paintThemeBtn);

  // ---- header shrink + progress + back to top ----
  var header = $(".site-header"), bar = $(".progress"), totop = $(".totop"), ticking = false;
  function onScroll() {
    var y = window.scrollY, h = d.documentElement.scrollHeight - window.innerHeight;
    if (header) header.classList.toggle("is-scrolled", y > 24);
    if (bar) bar.style.transform = "scaleX(" + (h > 0 ? Math.min(1, y / h) : 0) + ")";
    if (totop) totop.classList.toggle("show", y > 1100);
    parallax(y);
    ticking = false;
  }
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  if (totop) totop.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" }); var m = $("#main"); if (m) m.focus({ preventScroll: true }); });

  // ---- hero parallax (≤12px) ----
  var layers = $$(".mist .layer"), px = 0;
  function parallax(y) {
    if (reduce || !layers.length || y > 900) return;
    layers.forEach(function (l) { var dpt = +l.getAttribute("data-depth") || 0; var ty = -Math.min(12, (y / 900) * dpt); l.style.transform = "translate(" + (px * dpt * 0.5).toFixed(2) + "px," + ty.toFixed(2) + "px)"; });
  }
  var hero = $(".hero");
  if (hero && finePointer && !reduce) hero.addEventListener("pointermove", function (e) { var r = hero.getBoundingClientRect(); px = ((e.clientX - r.left) / r.width - 0.5) * 2 * 0.9; parallax(window.scrollY); });
  onScroll();

  // ---- services dropdown (tap + click + hover on fine pointers) ----
  $$(".nav-dd").forEach(function (dd) {
    var btn = $("button", dd), panel = $(".dd-panel", dd), t, hoverAt = 0;
    function set(open) { btn.setAttribute("aria-expanded", open); panel.hidden = !open; }
    btn.addEventListener("click", function () { if (Date.now() - hoverAt < 500) { set(true); return; } set(btn.getAttribute("aria-expanded") !== "true"); });
    if (finePointer) {
      dd.addEventListener("mouseenter", function () { clearTimeout(t); if (panel.hidden) hoverAt = Date.now(); set(true); });
      dd.addEventListener("mouseleave", function () { t = setTimeout(function () { set(false); }, 160); });
    }
    dd.addEventListener("keydown", function (e) { if (e.key === "Escape") { set(false); btn.focus(); } });
    d.addEventListener("click", function (e) { if (!dd.contains(e.target)) set(false); });
    dd.addEventListener("focusout", function (e) { if (!dd.contains(e.relatedTarget)) set(false); });
  });

  // ---- mobile sheet ----
  var sheet = $("#sheet"), menuBtn = $(".menu-btn"), lastFocus;
  function sheetOpen(open) {
    if (!sheet) return;
    sheet.hidden = !open; menuBtn.setAttribute("aria-expanded", open); d.body.classList.toggle("no-scroll", open);
    if (open) { lastFocus = d.activeElement; var f = $("button, a", sheet); if (f) f.focus(); } else if (lastFocus) lastFocus.focus();
  }
  if (menuBtn) menuBtn.addEventListener("click", function () { sheetOpen(true); });
  $$("[data-close-sheet]").forEach(function (b) { b.addEventListener("click", function () { sheetOpen(false); }); });
  if (sheet) sheet.addEventListener("keydown", function (e) {
    if (e.key === "Escape") sheetOpen(false);
    if (e.key === "Tab") { var f = $$("a,button", sheet); var first = f[0], last = f[f.length - 1]; if (e.shiftKey && d.activeElement === first) { e.preventDefault(); last.focus(); } else if (!e.shiftKey && d.activeElement === last) { e.preventDefault(); first.focus(); } }
  });

  // ---- command palette ----
  var cmdk = $(".cmdk"), q = $("#cmdk-q"), list = $("#cmdk-list"), sel = 0, results = [];
  function norm(s) { return (s || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, ""); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function search(term) {
    var idx = window.SEARCH_INDEX || [];
    var t = norm(term).trim();
    if (!t) return idx.filter(function (x) { return x.k === "Service" || x.k === "Page"; }).slice(0, 12);
    var words = t.split(/\s+/);
    return idx.map(function (x) {
      var T = norm(x.t), D = norm(x.d), K = norm(x.k), s = 0;
      for (var i = 0; i < words.length; i++) {
        var w = words[i], hit = false;
        if (T.indexOf(w) > -1) { s += T.indexOf(w) === 0 ? 6 : 4; hit = true; }
        if (K.indexOf(w) > -1) { s += 3; hit = true; }
        if (D.indexOf(w) > -1) { s += 1; hit = true; }
        if (!hit) return null;
      }
      if (x.k === "Service") s += 3; if (x.k === "Page") s += 2;
      return { x: x, s: s };
    }).filter(Boolean).sort(function (a, b) { return b.s - a.s; }).slice(0, 30).map(function (r) { return r.x; });
  }
  function render() {
    results = search(q.value);
    if (!results.length) { list.innerHTML = '<li class="cmdk-empty" role="option" aria-disabled="true">No matches. Call or text (610) 420-3338.</li>'; return; }
    sel = Math.min(sel, results.length - 1);
    list.innerHTML = results.map(function (r, i) { return '<li role="option" id="opt-' + i + '" aria-selected="' + (i === sel) + '"><a href="' + esc(r.u) + '"><span class="k">' + esc(r.k) + '</span><span>' + esc(r.t) + '</span><small>' + esc(r.d) + '</small></a></li>'; }).join("");
    q.setAttribute("aria-activedescendant", "opt-" + sel);
  }
  function openCmdk() { if (!cmdk) return; if (typeof cmdk.showModal === "function") cmdk.showModal(); else cmdk.setAttribute("open", ""); q.value = ""; sel = 0; render(); setTimeout(function () { q.focus(); }, 10); }
  $$("[data-cmdk]").forEach(function (b) { b.addEventListener("click", openCmdk); });
  d.addEventListener("keydown", function (e) {
    if ((e.metaKey || e.ctrlKey) && (e.key === "k" || e.key === "K")) { e.preventDefault(); if (cmdk && cmdk.open) cmdk.close(); else openCmdk(); }
    else if (e.key === "/" && !/input|textarea|select/i.test(d.activeElement.tagName) && !(cmdk && cmdk.open)) { e.preventDefault(); openCmdk(); }
  });
  if (cmdk) {
    q.addEventListener("input", function () { sel = 0; render(); });
    q.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown") { e.preventDefault(); sel = Math.min(sel + 1, results.length - 1); render(); scrollSel(); }
      else if (e.key === "ArrowUp") { e.preventDefault(); sel = Math.max(sel - 1, 0); render(); scrollSel(); }
      else if (e.key === "Enter" && results[sel]) { e.preventDefault(); go(results[sel].u); }
      else if (e.key === "Escape") { e.preventDefault(); cmdk.close(); }
    });
    list.addEventListener("click", function (e) { var a = e.target.closest("a"); if (a) { e.preventDefault(); go(a.getAttribute("href")); } });
    cmdk.addEventListener("click", function (e) { if (e.target === cmdk) cmdk.close(); });
  }
  function scrollSel() { var el = $("#opt-" + sel); if (el) el.scrollIntoView({ block: "nearest" }); }
  function go(u) {
    cmdk.close();
    var here = location.pathname.split("/").pop() || "index.html", parts = u.split("#");
    if (parts[0] === here && parts[1]) { location.hash = parts[1]; openHash(); } else location.href = u;
  }

  // ---- open accordion targeted by hash ----
  function openHash() {
    var id = decodeURIComponent(location.hash.slice(1)); if (!id) return;
    var el = d.getElementById(id); if (!el) return;
    if (el.tagName === "DETAILS") { el.open = true; setTimeout(function () { el.scrollIntoView({ block: "start", behavior: reduce ? "auto" : "smooth" }); $("summary", el).focus({ preventScroll: true }); }, 60); }
  }
  window.addEventListener("hashchange", openHash); openHash();

  // ---- seasonal rail ----
  var tabs = $$('[role="tab"]');
  if (tabs.length) {
    var SEASON_TITLES = { spring: "Spring: beds, mulch, and the first cuts of the year.", summer: "Summer: steady cuts and sharp edges through the heat.", fall: "Fall: leaves off the lawn before winter sets in.", winter: "Winter: safe drives, walks, and lots after every storm." };
    var m = new Date().getMonth(), current = m >= 2 && m <= 4 ? "spring" : m >= 5 && m <= 7 ? "summer" : m >= 8 && m <= 10 ? "fall" : "winter";
    var title = $("[data-season-title]"), note = $("[data-season-note]");
    function pick(k, focus) {
      tabs.forEach(function (t) { var on = t.id === "tab-" + k; t.setAttribute("aria-selected", on); t.tabIndex = on ? 0 : -1; if (on && focus) t.focus(); });
      $$('[role="tabpanel"]').forEach(function (p) { p.hidden = p.getAttribute("data-season") !== k; });
      if (title) title.textContent = SEASON_TITLES[k];
      if (note) note.textContent = k === current ? "Showing the current season. Pick another to plan ahead." : "Planning ahead for " + k + ".";
    }
    pick(current);
    tabs.forEach(function (t, i) {
      t.addEventListener("click", function () { pick(t.id.slice(4)); });
      t.addEventListener("keydown", function (e) {
        var n = e.key === "ArrowRight" ? 1 : e.key === "ArrowLeft" ? -1 : 0; if (!n) return;
        e.preventDefault(); var j = (i + n + tabs.length) % tabs.length; pick(tabs[j].id.slice(4), true);
      });
    });
  }

  // ---- magnetic buttons ----
  if (finePointer && !reduce) $$(".magnetic").forEach(function (b) {
    b.addEventListener("pointermove", function (e) { var r = b.getBoundingClientRect(); var x = (e.clientX - r.left - r.width / 2) / r.width, y = (e.clientY - r.top - r.height / 2) / r.height; b.style.transform = "translate(" + (x * 6).toFixed(1) + "px," + (y * 5).toFixed(1) + "px)"; });
    b.addEventListener("pointerleave", function () { b.style.transform = ""; });
  });

  // ---- skeleton: stop shimmer once the image is in ----
  $$(".sk img").forEach(function (img) { function done() { img.closest(".sk").classList.add("loaded"); } if (img.complete && img.naturalWidth) done(); else { img.addEventListener("load", done); img.addEventListener("error", done); } });

  // ---- carousel controls ----
  $$(".carousel-ctl").forEach(function (c) {
    var track = d.getElementById(c.getAttribute("data-for")); if (!track) return;
    $$("button", c).forEach(function (b) { b.addEventListener("click", function () { track.scrollBy({ left: (+b.getAttribute("data-dir")) * track.clientWidth * 0.8, behavior: reduce ? "auto" : "smooth" }); }); });
  });

  // ---- gallery filter + lightbox ----
  var gal = $("[data-gallery]");
  if (gal) {
    var tiles = $$("button", gal), chips = $$(".chip"), status = $("[data-gallery-status]");
    var PAGE = +gal.getAttribute("data-page") || 36, limit = PAGE, filter = "all";
    var moreBtn = $("[data-gallery-more]"), countEl = $("[data-gallery-count]");
    function applyGallery(focusFrom) {
      var matched = tiles.filter(function (t) { return filter === "all" || t.getAttribute("data-cat") === filter; });
      tiles.forEach(function (t) { t.hidden = true; });
      matched.forEach(function (t, i) { t.hidden = i >= limit; });
      var shown = Math.min(limit, matched.length), left = matched.length - shown;
      if (moreBtn) { moreBtn.hidden = left <= 0; moreBtn.textContent = "Show " + Math.min(PAGE, left) + " more photos"; }
      if (countEl) countEl.textContent = "Showing " + shown + " of " + matched.length + " photos";
      if (status) status.textContent = "Showing " + shown + " of " + matched.length + " photos";
      if (focusFrom != null && matched[focusFrom]) matched[focusFrom].focus({ preventScroll: true });
    }
    chips.forEach(function (c) {
      c.addEventListener("click", function () {
        filter = c.getAttribute("data-filter"); limit = PAGE;
        chips.forEach(function (x) { x.setAttribute("aria-pressed", x === c); });
        applyGallery();
      });
    });
    if (moreBtn) moreBtn.addEventListener("click", function () { var from = limit; limit += PAGE; applyGallery(from); });
    applyGallery();
    var lb = $(".lb"), lbImg = $(".lb-stage img"), lbCap = $(".lb-cap"), lbCount = $(".lb-count"), cur = 0, opener;
    function visible() { return tiles.filter(function (t) { return !t.hidden; }); }
    function show(i) {
      var v = visible(); cur = (i + v.length) % v.length; var t = v[cur];
      lbImg.onerror = function () { lbImg.onerror = null; lbImg.src = t.getAttribute("data-fallback"); };
      lbImg.src = t.getAttribute("data-full"); lbImg.alt = t.getAttribute("data-cap");
      lbCap.textContent = t.getAttribute("data-cap"); lbCount.textContent = (cur + 1) + " / " + v.length;
    }
    tiles.forEach(function (t) { t.addEventListener("click", function () { opener = t; show(visible().indexOf(t)); lb.showModal(); $(".lb-close").focus(); }); });
    $(".lb-prev").addEventListener("click", function () { show(cur - 1); });
    $(".lb-next").addEventListener("click", function () { show(cur + 1); });
    $(".lb-close").addEventListener("click", function () { lb.close(); });
    lb.addEventListener("close", function () { if (opener) opener.focus(); });
    lb.addEventListener("keydown", function (e) { if (e.key === "ArrowRight") show(cur + 1); if (e.key === "ArrowLeft") show(cur - 1); });
    var sx = null, stage = $(".lb-stage");
    stage.addEventListener("pointerdown", function (e) { if (e.target.closest("button")) return; sx = e.clientX; });
    stage.addEventListener("pointerup", function (e) { if (sx === null) return; var dx = e.clientX - sx; sx = null; if (Math.abs(dx) > 40) show(cur + (dx < 0 ? 1 : -1)); });
    stage.addEventListener("click", function (e) { if (e.target === stage) lb.close(); });
  }

  // ---- before/after (shown only when pairs are configured) ----
  var baSec = $("[data-ba-section]");
  if (baSec && CONFIG.beforeAfter && CONFIG.beforeAfter.length) {
    var listEl = $("[data-ba-list]", baSec);
    CONFIG.beforeAfter.forEach(function (p, i) {
      var fig = d.createElement("figure"); fig.style.margin = "0";
      fig.innerHTML = '<div class="ba"><img src="' + esc(p.before) + '" alt="Before: ' + esc(p.caption || "") + '"><img class="ba-after" src="' + esc(p.after) + '" alt="After: ' + esc(p.caption || "") + '"><input type="range" min="0" max="100" value="50" aria-label="Before and after comparison, ' + esc(p.caption || "photo " + (i + 1)) + '" id="ba-' + i + '"><span class="ba-line"></span><span class="ba-tag t-before">Before</span><span class="ba-tag t-after">After</span></div>' + (p.caption ? '<figcaption style="margin-top:.5rem;color:var(--muted)">' + esc(p.caption) + "</figcaption>" : "");
      var box = $(".ba", fig), r = $("input", fig);
      r.addEventListener("input", function () { box.style.setProperty("--pos", r.value + "%"); });
      listEl.appendChild(fig);
    });
    baSec.hidden = false;
  }

  // ---- FAQ search + sticky nav ----
  var fq = $("#faq-q");
  if (fq) {
    var groups = $$("[data-faq-group]"), count = $("[data-faq-count]"), empty = $("[data-faq-empty]");
    $$("details", d.querySelector(".faq-layout")).forEach(function (det) { det._q = $(".q", det); det._qt = det._q.textContent; det._t = norm(det.textContent); });
    fq.addEventListener("input", function () {
      var t = norm(fq.value).trim(), total = 0;
      groups.forEach(function (g) {
        var n = 0;
        $$("details", g).forEach(function (det) {
          var hit = !t || t.split(/\s+/).every(function (w) { return det._t.indexOf(w) > -1; });
          det.hidden = !hit; if (hit) n++;
          det._q.innerHTML = esc(det._qt);
          if (t && hit) { var i = norm(det._qt).indexOf(t); if (i > -1) det._q.innerHTML = esc(det._qt.slice(0, i)) + '<mark class="mark">' + esc(det._qt.slice(i, i + t.length)) + "</mark>" + esc(det._qt.slice(i + t.length)); }
        });
        g.hidden = n === 0; total += n;
      });
      count.textContent = t ? total + (total === 1 ? " question matches" : " questions match") : (count.getAttribute("data-all-text") || "");
      empty.hidden = total !== 0;
    });
    var links = $$("[data-faq-link]");
    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) { links.forEach(function (l) { var on = l.getAttribute("data-faq-link") === e.target.id; l.classList.toggle("is-active", on); if (on) { l.setAttribute("aria-current", "true"); if (l.parentNode.scrollWidth > l.parentNode.clientWidth) l.parentNode.scrollTo({ left: l.offsetLeft - 20, behavior: reduce ? "auto" : "smooth" }); } else l.removeAttribute("aria-current"); }); } });
      }, { rootMargin: "-30% 0px -60% 0px" });
      groups.forEach(function (g) { io.observe(g); });
    }
  }

  // ---- consent-gated map ----
  var map = $("[data-map]");
  if (map) {
    function loadMap() {
      if ($("iframe", map)) return;
      var f = d.createElement("iframe");
      f.src = map.getAttribute("data-src"); f.title = "Google Map showing Berger Landscaping, 110 Holby Lane, Pottstown, PA"; f.loading = "lazy"; f.referrerPolicy = "no-referrer-when-downgrade";
      map.classList.add("sk"); f.addEventListener("load", function () { map.classList.add("loaded"); var g = $(".map-gate", map); if (g) g.remove(); });
      map.appendChild(f); store("berger-map", "1");
    }
    $("[data-map-load]", map).addEventListener("click", loadMap);
    if (store("berger-map") === "1") loadMap();
  }

  // ---- copy buttons ----
  $$("[data-copy]").forEach(function (b) {
    b.addEventListener("click", function () {
      var v = b.getAttribute("data-copy"), label = b.textContent;
      function ok() { b.textContent = "Copied"; setTimeout(function () { b.textContent = label; }, 1600); }
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(v).then(ok, fallback); else fallback();
      function fallback() { var s = window.getSelection(), r = d.createRange(); var tgt = b.closest(".cblock").querySelector(".big"); r.selectNodeContents(tgt); s.removeAllRanges(); s.addRange(r); b.textContent = "Selected: press Ctrl+C"; setTimeout(function () { b.textContent = label; }, 2200); }
    });
  });

  // ---- optional quote form ----
  var form = $("[data-quote-form]");
  if (form && CONFIG.quoteForm && CONFIG.formEndpoint) {
    form.hidden = false;
    var MAX_FILES = 5, MAX_BYTES = 10 * 1024 * 1024;
    var fileInput = $("#qf-files", form), fileList = $(".file-list", form), files = [];
    var st = $(".form-status", form);
    function fmt(n) { return n < 1048576 ? Math.max(1, Math.round(n / 1024)) + " KB" : (n / 1048576).toFixed(1) + " MB"; }
    function total() { return files.reduce(function (a, f) { return a + f.size; }, 0); }
    function renderFiles() {
      fileList.innerHTML = "";
      files.forEach(function (f, i) {
        var li = d.createElement("li"), sp = d.createElement("span"), rm = d.createElement("button");
        sp.textContent = f.name + " (" + fmt(f.size) + ")";
        rm.type = "button"; rm.textContent = "Remove"; rm.setAttribute("aria-label", "Remove " + f.name);
        rm.addEventListener("click", function () { files.splice(i, 1); renderFiles(); fileInput.focus(); });
        li.appendChild(sp); li.appendChild(rm); fileList.appendChild(li);
      });
    }
    if (fileInput) fileInput.addEventListener("change", function () {
      var msg = "";
      Array.prototype.forEach.call(fileInput.files, function (f) {
        if (!/^image\//.test(f.type) && !/\.(heic|heif|pdf|jpe?g|png|webp)$/i.test(f.name)) { msg = f.name + " isn't a photo or PDF."; return; }
        if (files.length >= MAX_FILES) { msg = "Up to " + MAX_FILES + " files."; return; }
        if (total() + f.size > MAX_BYTES) { msg = f.name + " would go over the 10 MB total. Text us larger photos at (610) 420-3338."; return; }
        files.push(f);
      });
      fileInput.value = "";
      renderFiles();
      setStatus(msg, !!msg);
    });
    window.addEventListener("pageshow", function () { fileInput.disabled = false; var bt = form.querySelector("button[type=submit]"); if (bt) bt.disabled = false; setStatus(""); });
    function setStatus(t, err) { st.textContent = t; st.classList.toggle("is-err", !!err); }
    function fieldErr(el, msg) {
      var lab = el.closest("label"), e = lab && lab.querySelector(".field-err");
      if (msg) {
        el.setAttribute("aria-invalid", "true");
        if (lab && !e) { e = d.createElement("span"); e.className = "field-err"; e.id = el.id + "-err"; lab.appendChild(e); el.setAttribute("aria-describedby", e.id); }
        if (e) e.textContent = msg;
      } else {
        el.removeAttribute("aria-invalid"); el.removeAttribute("aria-describedby");
        if (e) e.remove();
      }
    }
    function check(el) {
      var v = (el.value || "").trim(), msg = "";
      if (el.required && !v) msg = "Required";
      else if (el.type === "email" && v && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) msg = "Enter a valid email";
      else if (el.name === "phone" && v && v.replace(/\D/g, "").replace(/^1(?=\d{10}$)/, "").length !== 10) msg = "Enter a 10-digit phone number";
      else if (el.name === "zip" && v && !/^\d{5}(-\d{4})?$/.test(v)) msg = "Enter a 5-digit ZIP code";
      fieldErr(el, msg);
      return !msg;
    }
    var fields = Array.prototype.slice.call(form.querySelectorAll("input:not([type=hidden]):not([type=file]):not(#qf-website), select, textarea"));
    fields.forEach(function (el) {
      el.addEventListener("blur", function () { if (el.value || el.hasAttribute("aria-invalid")) check(el); });
      el.addEventListener("input", function () { if (el.hasAttribute("aria-invalid")) check(el); });
    });
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if ($("#qf-website", form).value) return; // honeypot
      var bad = fields.filter(function (el) { return !check(el); });
      if (bad.length) { setStatus("Please fix the " + (bad.length === 1 ? "highlighted field" : bad.length + " highlighted fields") + ".", true); bad[0].focus(); return; }
      // Standard (non-AJAX) multipart POST: FormSubmit's /ajax/ endpoint drops file attachments.
      Array.prototype.forEach.call(form.querySelectorAll(".file-gen"), function (n) { n.remove(); });
      if (files.length) {
        var dtOk = typeof DataTransfer === "function";
        if (dtOk) {
          try {
            files.forEach(function (f, i) {
              var dt = new DataTransfer(); dt.items.add(f);
              var inp = d.createElement("input"); inp.type = "file"; inp.name = "attachment_" + (i + 1); inp.className = "file-gen"; inp.hidden = true;
              inp.files = dt.files; form.appendChild(inp);
            });
          } catch (err) { dtOk = false; }
        }
        if (!dtOk) { setStatus("Your browser can't attach photos here. Remove them and text photos to (610) 420-3338.", true); return; }
      }
      fileInput.disabled = true; // its own (empty) value isn't sent
      $("[name=_next]", form).value = new URL("thanks.html", location.href).href;
      form.action = CONFIG.formEndpoint;
      form.querySelector("button[type=submit]").disabled = true;
      setStatus(files.length ? "Sending… (uploading photos can take a moment)" : "Sending…");
      HTMLFormElement.prototype.submit.call(form);
    });
  }
})();
