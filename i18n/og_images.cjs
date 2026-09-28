// Renders 1200x630 share images (Open Graph / Twitter cards) with Chromium.
// Run through make_og_images.py, which passes the list of cards as JSON.
// Needs Playwright: npm i -g playwright (and its Chromium).
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const [, , listPath, repo] = process.argv;
const cards = JSON.parse(fs.readFileSync(listPath, 'utf8'));
const icon = 'data:image/png;base64,' + fs.readFileSync(path.join(repo, 'assets/icon.png')).toString('base64');

const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

function page(card) {
  const len = card.title.length;
  const size = len > 70 ? 54 : len > 50 ? 62 : 72;
  return `<!doctype html><html><head><meta charset="utf-8"><style>
    html,body{margin:0;width:1200px;height:630px;}
    body{font-family:"Liberation Sans","DejaVu Sans",Arial,sans-serif;color:#fff;
      background:radial-gradient(circle at 85% 15%,#7c74ff 0%,rgba(124,116,255,0) 45%),
                 linear-gradient(135deg,#2b2680 0%,#4f46c9 55%,#6d5bd8 100%);
      display:flex;flex-direction:column;justify-content:space-between;box-sizing:border-box;padding:64px 72px;}
    .top{display:flex;align-items:center;gap:20px;font-size:30px;font-weight:700;letter-spacing:.2px;}
    .top img{width:64px;height:64px;border-radius:15px;box-shadow:0 6px 18px rgba(0,0,0,.25);}
    .eyebrow{font-size:24px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;color:#d9d6ff;margin-bottom:18px;}
    h1{font-size:${size}px;line-height:1.1;margin:0;font-weight:700;letter-spacing:-.5px;max-width:1040px;}
    .bottom{display:flex;justify-content:space-between;align-items:flex-end;font-size:24px;color:#e4e1ff;}
  </style></head><body>
    <div class="top"><img src="${icon}" alt="">Velo Workspaces</div>
    <div><div class="eyebrow">${esc(card.eyebrow)}</div><h1>${esc(card.title)}</h1></div>
    <div class="bottom"><span>${esc(card.footer)}</span><span>veloworkspaces.com</span></div>
  </body></html>`;
}

(async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
  const tab = await context.newPage();
  for (const card of cards) {
    await tab.setContent(page(card), { waitUntil: 'load' });
    await tab.screenshot({ path: path.join(repo, card.out), type: 'jpeg', quality: 88 });
  }
  await browser.close();
  console.log(`rendered ${cards.length} images`);
})();
