const { chromium } = require('playwright');
const fs = require('fs');
const axeSrc = fs.readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8');
const FD='node_modules/@fontsource-variable/';
const FA=FD+'archivo/files/archivo-latin-wdth-normal.woff2', FF=FD+'fraunces/files/fraunces-latin-full-normal.woff2', FFI=FD+'fraunces/files/fraunces-latin-full-italic.woff2';
const FONTCSS=`@font-face{font-family:'Archivo';font-style:normal;font-weight:100 900;font-stretch:62% 125%;src:url(https://fonts.gstatic.com/arch.woff2) format('woff2')}
@font-face{font-family:'Fraunces';font-style:normal;font-weight:100 900;src:url(https://fonts.gstatic.com/fr.woff2) format('woff2')}
@font-face{font-family:'Fraunces';font-style:italic;font-weight:100 900;src:url(https://fonts.gstatic.com/fr-ital.woff2) format('woff2')}`;
const pages = JSON.parse(fs.readFileSync('pages.json')).map(p => p.file);
(async () => {
  const browser = await chromium.launch({executablePath:'/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell'});
  const report = { overflow: [], console: [], axe: {}, h1: [] };
  for (const scheme of ['light', 'dark']) {
    for (const w of [320, 390, 768, 1440]) {
      const ctx = await browser.newContext({ viewport: { width: w, height: 900 }, colorScheme: scheme });
      await ctx.route(/fonts\.googleapis\.com/, r => r.fulfill({ contentType: 'text/css', body: FONTCSS }));
      await ctx.route(/fonts\.gstatic\.com/, r => { const u = r.request().url(); r.fulfill({ contentType: 'font/woff2', body: fs.readFileSync(u.includes('arch') ? FA : (u.includes('ital') ? FFI : FF)) }); });
      const pg = await ctx.newPage();
      pg.on('console', m => { if (m.type() === 'error') report.console.push(`${scheme} ${w} ${pg.url()}: ${m.text()}`); });
      pg.on('pageerror', e => report.console.push(`${scheme} ${w} ${pg.url()}: PAGEERROR ${e.message}`));
      for (const f of pages) {
        await pg.goto('http://localhost:8770/' + f, { waitUntil: 'networkidle' }).catch(e => report.console.push('nav ' + f + e));
        const o = await pg.evaluate(() => {
          const de = document.documentElement; const bad = [];
          if (de.scrollWidth > de.clientWidth + 1) {
            document.querySelectorAll('body *').forEach(el => { const r = el.getBoundingClientRect(); if (r.right > de.clientWidth + 1 && r.width > 0 && getComputedStyle(el).position !== 'fixed') { let p = el.parentElement, clipped = false; while (p) { const ov = getComputedStyle(p).overflowX; if (ov === 'auto' || ov === 'hidden' || ov === 'scroll') { clipped = true; break; } p = p.parentElement; } if (!clipped) bad.push(el.tagName + '.' + el.className.toString().slice(0, 40)); } });
          }
          return { sw: de.scrollWidth, cw: de.clientWidth, bad: bad.slice(0, 5), h1: document.querySelectorAll('h1').length };
        });
        if (o.sw > o.cw + 1) report.overflow.push(`${scheme} ${w} ${f} ${o.sw}>${o.cw} ${o.bad.join(',')}`);
        if (o.h1 !== 1) report.h1.push(`${f}: ${o.h1}`);
        if ((w === 390 || w === 1440)) {
          await pg.addScriptTag({ content: axeSrc });
          const r = await pg.evaluate(async () => { const res = await axe.run(document, { runOnly: ['wcag2a', 'wcag2aa', 'best-practice'] }); return res.violations.map(v => ({ id: v.id, impact: v.impact, n: v.nodes.length, ex: v.nodes.slice(0, 2).map(n => n.target.join(' ') + ' | ' + (n.failureSummary || '').slice(0, 140)) })); });
          r.forEach(v => { const k = `${scheme}:${v.id}`; (report.axe[k] = report.axe[k] || []).push(`${w} ${f} (${v.impact}, ${v.n}) ${v.ex.join(' || ')}`); });
        }
      }
      if (w === 1440 || w === 390) {
        for (const f of ['index.html', 'mowing.html', 'gallery.html', 'faqs.html', 'contact.html']) {
          await pg.goto('http://localhost:8770/' + f, { waitUntil: 'networkidle' });
          try{ for(let y=0;y<12000;y+=500){ await pg.mouse.wheel(0,500); await pg.waitForTimeout(50);} await pg.evaluate(()=>window.scrollTo(0,0)); await pg.waitForTimeout(400);}catch(e){console.log('scrollerr',f,w,pg.url(),e.message.slice(0,80))}
          await pg.screenshot({ path: `shots/${f.replace('.html', '')}-${w}-${scheme}.png`, fullPage: true });
        }
      }
      await ctx.close();
    }
  }
  await browser.close();
  fs.writeFileSync('report.json', JSON.stringify(report, null, 1));
  console.log('overflow', report.overflow.length, 'console', report.console.length, 'h1', report.h1.length, 'axe keys', Object.keys(report.axe));
})();
