/* Berger Landscaping — 3D homepage sample.
   A procedural version of the logo: layered misty hills, pine forest, a standing deer and birds.
   Camera drifts forward as you scroll through the hero; mouse/touch adds a little parallax.
   Falls back to the hero photo when WebGL isn't available; static frame for reduced motion. */
(function () {
  "use strict";
  var d = document, reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  var wrap = d.querySelector("[data-scene]"), canvas = d.querySelector("[data-scene] canvas");
  if (!wrap || !canvas) return;
  function fallback() { wrap.classList.add("no-webgl"); }
  if (typeof THREE === "undefined") return fallback();
  var renderer;
  try { renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: false, powerPreference: "low-power" }); }
  catch (e) { return fallback(); }
  if (!renderer.getContext()) return fallback();
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.75));

  // ---- palette from the logo (tracks light/dark theme) ----
  function css(v) { return getComputedStyle(d.documentElement).getPropertyValue(v).trim(); }
  function isDark() { var t = d.documentElement.getAttribute("data-theme"); return t ? t === "dark" : matchMedia("(prefers-color-scheme: dark)").matches; }
  var PAL = {
    light: { sky: 0xE6ECEA, fog: 0xE6ECEA, far: 0xB9C6C4, mid: 0x7E8F92, near: 0x4F6066, front: 0x2B3A42, tree: 0x2B3A42, deer: 0x22313A },
    dark:  { sky: 0x141D22, fog: 0x141D22, far: 0x22313A, mid: 0x2E3F48, near: 0x3B4E58, front: 0x51666F, tree: 0x8EA1A5, deer: 0xC9D6D4 }
  };

  var scene = new THREE.Scene();
  var camera = new THREE.PerspectiveCamera(48, 1, 0.1, 400);
  scene.fog = new THREE.Fog(0xE6ECEA, 18, 120);
  scene.add(new THREE.HemisphereLight(0xffffff, 0x9aa9aa, 0.95));
  var sun = new THREE.DirectionalLight(0xffffff, 0.55); sun.position.set(-20, 30, 10); scene.add(sun);

  // seeded random so the forest is the same on every visit
  var seed = 7; function rnd() { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; }

  // ---- hills: displaced planes, flat-shaded ----
  function hill(z, width, depth, amp, y, freq, phase) {
    var g = new THREE.PlaneGeometry(width, depth, 80, 12); g.rotateX(-Math.PI / 2);
    var p = g.attributes.position;
    for (var i = 0; i < p.count; i++) {
      var x = p.getX(i), zz = p.getZ(i);
      var h = Math.sin(x * freq + phase) * amp + Math.sin(x * freq * 2.3 + phase * 1.7) * amp * 0.35 + Math.cos(zz * 0.35 + x * 0.05) * amp * 0.25;
      p.setY(i, h);
    }
    g.computeVertexNormals();
    var m = new THREE.Mesh(g, new THREE.MeshLambertMaterial({ color: 0xffffff, flatShading: true }));
    m.position.set(0, y, z); scene.add(m); return m;
  }
  var hills = [
    hill(-70, 260, 40, 3.2, -1, 0.045, 0.3),
    hill(-45, 220, 30, 2.4, -2, 0.06, 1.4),
    hill(-22, 180, 26, 1.6, -3, 0.08, 2.2),
    hill(4, 160, 40, 0.9, -3.6, 0.1, 0.8)
  ];
  function groundHeight(x, z) {
    // approximate height of the nearest hill layer at (x,z) for planting trees
    var best = -3.6, layers = [[-70, -1, 3.2, 0.045, 0.3], [-45, -2, 2.4, 0.06, 1.4], [-22, -3, 1.6, 0.08, 2.2], [4, -3.6, 0.9, 0.1, 0.8]];
    for (var i = 0; i < layers.length; i++) { var L = layers[i]; if (Math.abs(z - L[0]) < 14) { best = L[1] + Math.sin(x * L[3] + L[4]) * L[2] + Math.sin(x * L[3] * 2.3 + L[4] * 1.7) * L[2] * 0.35; } }
    return best;
  }

  // ---- pine forest: instanced stacked cones + trunks ----
  var N = window.innerWidth < 700 ? 150 : 260;
  var tiers = [[1.0, 0.0], [0.78, 0.32], [0.55, 0.6]]; // radius scale, height offset
  var coneGeo = new THREE.ConeGeometry(1, 1.6, 7, 1);
  var trunkGeo = new THREE.CylinderGeometry(0.08, 0.12, 1, 5);
  var treeMat = new THREE.MeshLambertMaterial({ color: 0x2B3A42, flatShading: true });
  var trunkMat = new THREE.MeshLambertMaterial({ color: 0x2B3A42 });
  var tierMeshes = tiers.map(function () { var m = new THREE.InstancedMesh(coneGeo, treeMat, N); scene.add(m); return m; });
  var trunks = new THREE.InstancedMesh(trunkGeo, trunkMat, N); scene.add(trunks);
  var dummy = new THREE.Object3D(), trees = [];
  for (var i = 0; i < N; i++) {
    var z = -85 + rnd() * 95, x = (rnd() - 0.5) * (70 + (-z) * 1.2);
    if (z > -6 && Math.abs(x) < 6) x += x < 0 ? -7 : 7;          // keep a clearing in front of the camera
    if (z > -16 && z < -8 && x > 2 && x < 9) x += 9;              // clearing for the deer
    var h = 2.2 + rnd() * 3.4, r = h * (0.22 + rnd() * 0.06), y = groundHeight(x, z);
    trees.push({ x: x, y: y, z: z, h: h, r: r, sway: rnd() * 6.28 });
  }
  function placeTrees(t) {
    for (var i = 0; i < trees.length; i++) {
      var T = trees[i], lean = reduce ? 0 : Math.sin(t * 0.6 + T.sway) * 0.012;
      for (var k = 0; k < tiers.length; k++) {
        dummy.position.set(T.x, T.y + T.h * (0.42 + tiers[k][1]), T.z);
        dummy.scale.set(T.r * tiers[k][0], T.h * 0.42, T.r * tiers[k][0]);
        dummy.rotation.set(0, T.sway, lean); dummy.updateMatrix(); tierMeshes[k].setMatrixAt(i, dummy.matrix);
      }
      dummy.position.set(T.x, T.y + T.h * 0.18, T.z); dummy.scale.set(1, T.h * 0.4, 1); dummy.rotation.set(0, 0, 0); dummy.updateMatrix(); trunks.setMatrixAt(i, dummy.matrix);
    }
    tierMeshes.forEach(function (m) { m.instanceMatrix.needsUpdate = true; }); trunks.instanceMatrix.needsUpdate = true;
  }
  placeTrees(0);

  // ---- deer + birds: drawn from the same silhouette paths as the site's deer icon ----
  function silhouette(pathD, strokeD, w, h) {
    var c = d.createElement("canvas"); c.width = w * 8; c.height = h * 8; var x = c.getContext("2d");
    x.scale(8, 8); x.fillStyle = "#fff"; x.strokeStyle = "#fff"; x.lineWidth = 1.7; x.lineCap = "round";
    x.fill(new Path2D(pathD)); if (strokeD) x.stroke(new Path2D(strokeD));
    var t = new THREE.CanvasTexture(c); t.anisotropy = 4; return t;
  }
  var DEER = "M14 26c0-4 6-6 14-6h12c4 0 6-3 7-7l3-1 4 2-1 2h-3c-1 4-3 8-4 11v13h-2l-1-10h-5l-1 10h-2l-1-11H24l-2 11h-2V30c-2 1-3 3-3 10h-2v-9c-2-1-2-3-1-5z";
  var ANT = "M48 12.5 46 6.5 43 2.5M46 6.5l2-3.5M49.5 12l2.5-5 3-4M52 7l3-1M44.6 4.6 42 4";
  var deerMat = new THREE.SpriteMaterial({ map: silhouette(DEER, ANT, 64, 44), color: 0x22313A, fog: true });
  var deer = new THREE.Sprite(deerMat); deer.scale.set(2.6, 1.8, 1); deer.position.set(5.2, groundHeight(5.2, -12) + 1.05, -12); scene.add(deer);
  var birdTex = silhouette("M2 8 Q8 2 14 8 Q20 2 26 8 L26 9 Q20 4 14 10 Q8 4 2 9Z", null, 28, 12);
  var birds = [];
  for (var b = 0; b < 11; b++) {
    var s = new THREE.Sprite(new THREE.SpriteMaterial({ map: birdTex, color: 0x2B3A42, fog: true }));
    s.scale.set(0.9, 0.4, 1); s.userData = { a: rnd() * 6.28, r: 2 + rnd() * 3, y: 11 + rnd() * 3, z: -38 + rnd() * 8, x: 8 + rnd() * 6 };
    scene.add(s); birds.push(s);
  }

  function applyTheme() {
    var P = isDark() ? PAL.dark : PAL.light;
    scene.background = new THREE.Color(P.sky); scene.fog.color.setHex(P.fog);
    [P.far, P.mid, P.near, P.front].forEach(function (c, i) { hills[i].material.color.setHex(c); });
    treeMat.color.setHex(P.tree); trunkMat.color.setHex(P.tree); deerMat.color.setHex(P.deer);
    birds.forEach(function (s) { s.material.color.setHex(P.tree); });
    needs = true;
  }
  new MutationObserver(applyTheme).observe(d.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
  matchMedia("(prefers-color-scheme: dark)").addEventListener("change", applyTheme);

  // ---- sizing, scroll, pointer ----
  var stage = wrap.querySelector(".scene-stage"), needs = true, progress = 0, px = 0, py = 0, tx = 0, ty = 0;
  function resize() { var w = stage.clientWidth, h = stage.clientHeight; renderer.setSize(w, h, false); camera.aspect = w / h; camera.fov = w < 700 ? 60 : 48; camera.updateProjectionMatrix(); needs = true; }
  addEventListener("resize", resize); resize();
  var captions = [].slice.call(wrap.querySelectorAll("[data-cap]"));
  function onScroll() {
    var r = wrap.getBoundingClientRect(), span = wrap.offsetHeight - innerHeight;
    progress = span > 0 ? Math.min(1, Math.max(0, -r.top / span)) : 0;
    var idx = Math.min(captions.length - 1, Math.floor(progress * captions.length * 0.999));
    captions.forEach(function (c, i) { var on = i === idx; c.classList.toggle("on", on); c.inert = !on; if (on) c.removeAttribute("aria-hidden"); else c.setAttribute("aria-hidden", "true"); });
    needs = true;
  }
  addEventListener("scroll", onScroll, { passive: true }); onScroll();
  if (!reduce) {
    stage.addEventListener("pointermove", function (e) { var r = stage.getBoundingClientRect(); tx = ((e.clientX - r.left) / r.width - 0.5) * 2; ty = ((e.clientY - r.top) / r.height - 0.5) * 2; });
    stage.addEventListener("pointerleave", function () { tx = ty = 0; });
  }

  // render only while the scene is on screen
  var visible = true;
  if ("IntersectionObserver" in window) new IntersectionObserver(function (es) { visible = es[0].isIntersecting; if (visible) loop(); }, { threshold: 0 }).observe(stage);

  applyTheme();
  var start = performance.now(), running = false;
  function frame(now) {
    running = false;
    var t = (now - start) / 1000;
    px += (tx - px) * 0.05; py += (ty - py) * 0.05;
    var z = 22 - progress * 30, y = 3.2 - progress * 1.1;
    camera.position.set(px * 1.6, y - py * 0.6, z);
    camera.lookAt(px * 0.6, 1.6 - progress * 0.4, z - 30);
    if (!reduce) {
      placeTrees(t);
      birds.forEach(function (s, i) { var u = s.userData; s.position.set(u.x + Math.cos(t * 0.25 + u.a) * u.r, u.y + Math.sin(t * 1.3 + i) * 0.25, u.z + Math.sin(t * 0.25 + u.a) * u.r * 0.5); });
    } else if (!birds[0].position.y) {
      birds.forEach(function (s) { var u = s.userData; s.position.set(u.x + Math.cos(u.a) * u.r, u.y, u.z); });
    }
    renderer.render(scene, camera); needs = false;
    if (visible && (!reduce || needs)) loop();
  }
  function loop() { if (!running) { running = true; requestAnimationFrame(frame); } }
  if (reduce) { addEventListener("scroll", loop, { passive: true }); }
  loop();
  wrap.classList.add("ready");
})();

/* ---- 3D photo ring (CSS 3D) ---- */
(function () {
  "use strict";
  var ring = document.querySelector("[data-ring]"); if (!ring) return;
  var items = [].slice.call(ring.querySelectorAll(".ring-item")), n = items.length, angle = 0, target = 0, auto = !matchMedia("(prefers-reduced-motion: reduce)").matches;
  var step = 360 / n, pauseBtn = document.querySelector("[data-ring-pause]"), live = document.querySelector("[data-ring-status]");
  function radius() { var w = ring.parentElement.clientWidth; var itemW = Math.min(300, Math.max(180, w * 0.42)); ring.style.setProperty("--w", itemW + "px"); return Math.round((itemW / 2) / Math.tan(Math.PI / n)) + 24; }
  var R = radius(); addEventListener("resize", function () { R = radius(); layout(); });
  function layout() { items.forEach(function (it, i) { it.style.transform = "rotateY(" + (i * step) + "deg) translateZ(" + R + "px)"; }); ring.style.transform = "translateZ(" + (-R) + "px) rotateY(" + angle + "deg)"; }
  function front() { var k = Math.round(-target / step) % n; return (k + n) % n; }
  function go(dir) { target -= dir * step; if (live) live.textContent = "Photo " + (front() + 1) + " of " + n + ": " + items[front()].querySelector("img").alt; }
  document.querySelectorAll("[data-ring-dir]").forEach(function (b) { b.addEventListener("click", function () { auto = false; setPause(); go(+b.getAttribute("data-ring-dir")); }); });
  function setPause() { if (!pauseBtn) return; pauseBtn.textContent = auto ? "Pause" : "Play"; pauseBtn.setAttribute("aria-pressed", auto ? "false" : "true"); }
  if (pauseBtn) pauseBtn.addEventListener("click", function () { auto = !auto; setPause(); });
  setPause();
  ring.parentElement.addEventListener("keydown", function (e) { if (e.key === "ArrowRight") { auto = false; setPause(); go(1); } if (e.key === "ArrowLeft") { auto = false; setPause(); go(-1); } });
  var sx = null; ring.parentElement.addEventListener("pointerdown", function (e) { sx = e.clientX; });
  addEventListener("pointerup", function (e) { if (sx === null) return; var dx = e.clientX - sx; sx = null; if (Math.abs(dx) > 30) { auto = false; setPause(); go(dx < 0 ? 1 : -1); } });
  var last = performance.now();
  function tick(now) { var dt = Math.min(64, now - last); last = now; if (auto && !document.hidden) target -= dt * 0.006; angle += (target - angle) * 0.08; ring.style.transform = "translateZ(" + (-R) + "px) rotateY(" + angle + "deg)"; requestAnimationFrame(tick); }
  layout(); requestAnimationFrame(tick);
})();

/* ---- tilt cards ---- */
(function () {
  if (matchMedia("(prefers-reduced-motion: reduce)").matches || !matchMedia("(pointer: fine)").matches) return;
  document.querySelectorAll("[data-tilt]").forEach(function (el) {
    el.addEventListener("pointermove", function (e) { var r = el.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5; el.style.transform = "perspective(900px) rotateX(" + (-y * 8).toFixed(2) + "deg) rotateY(" + (x * 10).toFixed(2) + "deg) translateZ(6px)"; el.style.setProperty("--gx", (x + 0.5) * 100 + "%"); el.style.setProperty("--gy", (y + 0.5) * 100 + "%"); });
    el.addEventListener("pointerleave", function () { el.style.transform = ""; });
  });
})();
