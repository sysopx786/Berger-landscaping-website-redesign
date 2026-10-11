const { chromium } = require('playwright'); const fs=require('fs');
const FD='node_modules/@fontsource-variable/';
const R=[]; const ok=(n,c,x='')=>R.push(`${c?'PASS':'FAIL'} ${n} ${x}`);
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell'});
const U='http://localhost:8770/';
let ctx=await b.newContext({viewport:{width:1440,height:900}}); await ctx.route(/fonts\.(googleapis|gstatic)\.com/,r=>r.fulfill({body:''}));
let p=await ctx.newPage(); const errs=[]; p.on('pageerror',e=>errs.push(e.message));
await p.goto(U+'index.html');
await p.click('.nav-dd>button'); ok('dropdown opens on click', await p.isVisible('#dd-services'));
await p.keyboard.press('Escape'); ok('dropdown closes on Esc', !(await p.isVisible('#dd-services')));
await p.keyboard.press('Control+k'); ok('Ctrl-K opens palette', await p.isVisible('.cmdk-box'));
await p.fill('#cmdk-q','pet-safe'); await p.waitForTimeout(100); const first=await p.textContent('#cmdk-list li:first-child');
ok('palette search finds pet-safe', /pet-safe/i.test(first), first.slice(0,80));
await p.keyboard.press('Enter'); await p.waitForURL(/snow-services/); await p.waitForTimeout(300);
ok('palette navigates + opens FAQ', await p.evaluate(()=>document.getElementById('pet-safe').open), p.url());
await p.goto(U+'index.html');
const sel=await p.getAttribute('[role=tab][aria-selected=true]','id'); ok('season defaults to current (Oct→fall)', sel==='tab-fall', sel);
await p.focus('#tab-fall'); await p.keyboard.press('ArrowRight'); ok('season arrow key → winter', await p.isVisible('#panel-winter') && !(await p.isVisible('#panel-fall')));
await p.evaluate(()=>document.getElementById('mosaic').scrollIntoView()); await p.waitForTimeout(1500);
const imgs=await p.evaluate(()=>[...document.querySelectorAll('#mosaic img')].map(i=>i.complete&&i.naturalWidth>0)); ok('mosaic images load', imgs.every(Boolean), JSON.stringify(imgs));
await p.click('[data-theme-toggle]'); const th=await p.evaluate(()=>[document.documentElement.dataset.theme,localStorage.getItem('berger-theme')]); ok('theme toggle sets + stores', th[0]==='dark'&&th[1]==='dark');
await p.reload(); ok('theme persists on reload', await p.evaluate(()=>document.documentElement.dataset.theme)==='dark');
const vis=await p.evaluate(()=>[...document.querySelectorAll('.brand img')].filter(i=>getComputedStyle(i).display!=='none').map(i=>i.className)); ok('dark: exactly one header logo', vis.length===1, vis.join());
await p.evaluate(()=>localStorage.clear());
// gallery
await p.goto(U+'gallery.html');
await p.click('[data-filter=snow]'); const n=await p.evaluate(()=>[...document.querySelectorAll('[data-gallery] button')].filter(t=>!t.hidden).length); ok('gallery filter snow = 1', n===1, n);
await p.click('[data-filter=all]'); await p.click('[data-gallery] button:nth-child(3)'); ok('lightbox opens', await p.isVisible('.lb'));
const c1=await p.textContent('.lb-count'); await p.keyboard.press('ArrowRight'); const c2=await p.textContent('.lb-count'); ok('lightbox arrow next', c1!==c2, c1+'→'+c2);
await p.waitForTimeout(500); ok('lightbox image loads', await p.evaluate(()=>{const i=document.querySelector('.lb-stage img');return i.complete&&i.naturalWidth>0}));
await p.keyboard.press('Escape'); await p.waitForTimeout(100); ok('lightbox closes on Esc + focus returns', !(await p.isVisible('.lb')) && await p.evaluate(()=>document.activeElement.matches('[data-gallery] button')));
ok('before/after hidden without pairs', !(await p.isVisible('[data-ba-section]')));
// FAQ
await p.goto(U+'faqs.html'); await p.fill('#faq-q','steep hill'); await p.waitForTimeout(100);
ok('FAQ search filters', /match/.test(await p.textContent('[data-faq-count]')), await p.textContent('[data-faq-count]'));
await p.fill('#faq-q','zzzzqq'); ok('FAQ empty state', await p.isVisible('[data-faq-empty]'));
await p.fill('#faq-q',''); await p.click('#mowing details:first-child summary'); ok('accordion opens by click', await p.evaluate(()=>document.querySelector('#mowing details').open));
await p.focus('#mowing details:nth-child(2) summary'); await p.keyboard.press('Enter'); ok('accordion opens by keyboard', await p.evaluate(()=>document.querySelectorAll('#mowing details')[1].open));
const ld=await p.evaluate(()=>[...document.querySelectorAll('script[type="application/ld+json"]')].map(s=>{try{JSON.parse(s.textContent);return 1}catch(e){return 0}})); ok('JSON-LD parses (faqs)', ld.every(Boolean));
// contact map
await p.goto(U+'contact.html'); ok('map not loaded before consent', (await p.$('[data-map] iframe'))===null);
await p.click('[data-map-load]'); ok('map iframe inserted on click', (await p.$('[data-map] iframe'))!==null);
ok('quote form hidden by default', !(await p.isVisible('[data-quote-form]')));
// all pages JSON-LD
for (const f of JSON.parse(fs.readFileSync('pages.json')).map(x=>x.file)){ await p.goto(U+f); const bad=await p.evaluate(()=>[...document.querySelectorAll('script[type="application/ld+json"]')].filter(s=>{try{JSON.parse(s.textContent);return 0}catch(e){return 1}}).length); if(bad) ok('JSON-LD '+f,false); }
// broken links / images crawl
const files=new Set(fs.readdirSync('/home/claude/site')); const broken=[];
for (const f of JSON.parse(fs.readFileSync('pages.json')).map(x=>x.file)){ const h=fs.readFileSync('/home/claude/berger-landscaping-website-redesign/docs/'+f,'utf8'); for(const m of h.matchAll(/(?:href|src)="([^"#:?]+)[^"]*"/g)){ const u=m[1]; if(u.startsWith('//')||/^(https?|tel|sms|mailto)$/.test(u))continue; if(!fs.existsSync('/home/claude/berger-landscaping-website-redesign/docs/'+u)) broken.push(f+'→'+u);} for(const m of h.matchAll(/srcset="([^"]+)"/g)) m[1].split(',').forEach(s=>{const u=s.trim().split(' ')[0]; if(!fs.existsSync('/home/claude/berger-landscaping-website-redesign/docs/'+u)) broken.push(f+'→'+u);}); const ids=new Set([...h.matchAll(/id="([^"]+)"/g)].map(x=>x[1])); for (const m of h.matchAll(/href="#([^"]+)"/g)) if(!ids.has(m[1])) broken.push(f+'→#'+m[1]); }
ok('no broken internal links/images/anchors', broken.length===0, broken.slice(0,8).join(' '));
// cross-page anchors
const anch=[]; for (const f of JSON.parse(fs.readFileSync('pages.json')).map(x=>x.file)){ const h=fs.readFileSync('/home/claude/berger-landscaping-website-redesign/docs/'+f,'utf8'); for(const m of h.matchAll(/href="([a-z0-9-]+\.html)#([^"]+)"/g)){ const t=fs.readFileSync('/home/claude/berger-landscaping-website-redesign/docs/'+m[1],'utf8'); if(!t.includes(`id="${m[2]}"`)) anch.push(f+'→'+m[1]+'#'+m[2]); } }
const idx=fs.readFileSync('/home/claude/berger-landscaping-website-redesign/docs/assets/search-index.js','utf8'); for (const m of idx.matchAll(/"u":"([a-z0-9-]+\.html)#([^"]+)"/g)){ const t=fs.readFileSync('/home/claude/berger-landscaping-website-redesign/docs/'+m[1],'utf8'); if(!t.includes(`id="${m[2]}"`)) anch.push('idx→'+m[1]+'#'+m[2]); }
ok('cross-page anchors resolve (incl. 120 search targets)', anch.length===0, anch.slice(0,5).join(' '));
await ctx.close();
// mobile
ctx=await b.newContext({viewport:{width:390,height:844},hasTouch:true,isMobile:true}); await ctx.route(/fonts\.(googleapis|gstatic)\.com/,r=>r.fulfill({body:''})); p=await ctx.newPage(); p.on('pageerror',e=>errs.push(e.message));
await p.goto(U+'index.html'); ok('mobile action bar visible', await p.isVisible('.actionbar'));
const hrefs=await p.$$eval('.actionbar a',a=>a.map(x=>x.getAttribute('href'))); ok('action bar tel/sms/quote', hrefs[0].startsWith('tel:+1610')&&hrefs[1].startsWith('sms:')&&hrefs[2].includes('#quote'), hrefs.join(' '));
await p.tap('.menu-btn'); ok('mobile menu opens', await p.isVisible('#sheet'));
const gap=await p.evaluate(()=>{const a=[...document.querySelectorAll('#sheet nav a')].map(x=>x.getBoundingClientRect());return {n:a.length,gap:Math.round(a[1].top-a[0].top),allIn:a.every(r=>r.height<90)}}); ok('mobile menu lists 7 links compactly', gap.n===7&&gap.gap<90&&gap.allIn, JSON.stringify(gap));
const big=await p.evaluate(()=>[...document.querySelectorAll('#sheet svg')].filter(s=>s.getBoundingClientRect().width>48).length); ok('mobile menu icons sized', big===0, big); await p.keyboard.press('Escape'); ok('mobile menu closes on Esc', !(await p.isVisible('#sheet')));
const tgt=await p.evaluate(()=>[...document.querySelectorAll('a,button')].filter(e=>{const r=e.getBoundingClientRect();const s=getComputedStyle(e);return r.width>0&&s.visibility!=='hidden'&&(r.height<40)&&!e.closest('.prose,.ans,.foot,.crumbs,.attr,p,li,.map-links,.trust,.skip')}).map(e=>e.className+':'+e.textContent.trim().slice(0,20)+':'+Math.round(e.getBoundingClientRect().height)).slice(0,10)); ok('mobile tap targets ≥40px (non-inline)', tgt.length===0, tgt.join(' | '));
const hdr=await p.evaluate(()=>{const h=document.querySelector('h1').getBoundingClientRect(),s=document.querySelector('.site-header').getBoundingClientRect();return h.top>=s.bottom}); ok('sticky header does not overlap H1', hdr);
await p.goto(U+'gallery.html'); await p.tap('[data-gallery] button'); await p.waitForTimeout(300);
const c3=await p.textContent('.lb-count'); const box=await p.$eval('.lb-stage',e=>{const r=e.getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]});
await p.mouse.move(box[0]+100,box[1]); await p.mouse.down(); await p.mouse.move(box[0]-100,box[1],{steps:5}); await p.mouse.up(); await p.waitForTimeout(100);
ok('lightbox swipe', c3!==await p.textContent('.lb-count'), c3+'→'+await p.textContent('.lb-count'));
await ctx.close();
// reduced motion + before/after + form via config injection
ctx=await b.newContext({viewport:{width:1280,height:900},reducedMotion:'reduce'}); await ctx.route(/fonts\.(googleapis|gstatic)\.com/,r=>r.fulfill({body:''}));
await ctx.addInitScript(()=>{window.BERGER_CONFIG={quoteForm:true,formEndpoint:'https://example.invalid/f',beforeAfter:[{before:'img/berger-beds-20-1280.webp',after:'img/berger-beds-12-1280.webp',caption:'Test pair'}]}});
p=await ctx.newPage(); p.on('pageerror',e=>errs.push(e.message));
await p.goto(U+'index.html'); await p.mouse.move(700,500); await p.mouse.wheel(0,400); await p.waitForTimeout(200);
ok('reduced motion: parallax off', await p.evaluate(()=>[...document.querySelectorAll('.mist .layer')].every(l=>!l.style.transform)));
await p.goto(U+'gallery.html'); ok('before/after shows when configured', await p.isVisible('.ba'));
await p.focus('.ba input'); await p.keyboard.press('ArrowRight'); await p.keyboard.press('ArrowRight'); ok('before/after keyboard', (await p.$eval('.ba',e=>e.style.getPropertyValue('--pos')))==='52%');
await p.goto(U+'contact.html'); ok('quote form shows when enabled', await p.isVisible('[data-quote-form]'));
await p.click('[data-quote-form] button[type=submit]'); ok('form validates name/phone', /name and phone/.test(await p.textContent('.form-status')));
ok('no page JS errors', errs.length===0, errs.join(' | '));
await b.close(); fs.writeFileSync('func.txt',R.join('\n')); console.log(R.join('\n'));})();
