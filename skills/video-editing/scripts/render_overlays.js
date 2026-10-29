// Frame-accurate HTML -> video renderer for motion graphics (Playwright + ffmpeg).
// usage: node render_overlays.js manifest.json [name1,name2]
// manifest: [{ "name", "html", "w", "h", "dur", "fps"?, "opaque"? }]
//   opaque=false -> out/<name>.mov ProRes 4444 with alpha (convert for CapCut with to_hevc_alpha.sh)
//   opaque=true  -> out/<name>.mp4 H.264 CRF 15
// Pages animate with CSS/Web Animations; scripted parts expose window.tick(ms).
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), { execFileSync } = require('child_process');
(async () => {
  const man = JSON.parse(fs.readFileSync(process.argv[2]));
  const only = process.argv[3] ? process.argv[3].split(',') : null;
  const outDir = path.join(path.dirname(path.resolve(process.argv[2])), 'out'); fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch();
  for (const a of man) {
    if (only && !only.includes(a.name)) continue;
    const fps = a.fps || 30, n = Math.round(a.dur * fps);
    const page = await browser.newPage({ viewport: { width: a.w, height: a.h }, deviceScaleFactor: 1 });
    await page.goto('file://' + path.resolve(a.html));
    await page.evaluate(() => document.fonts.ready); await page.waitForTimeout(150);
    const fdir = fs.mkdtempSync(path.join(require('os').tmpdir(), a.name + '-'));
    for (let i = 0; i < n; i++) {
      const t = (i / fps) * 1000;
      await page.evaluate((t) => { document.getAnimations().forEach(x => { x.pause(); x.currentTime = t; }); if (window.tick) window.tick(t); }, t);
      await page.screenshot({ path: path.join(fdir, String(i).padStart(4, '0') + '.png'), omitBackground: !a.opaque });
    }
    await page.close();
    const src = ['-v', 'error', '-y', '-framerate', String(fps), '-i', path.join(fdir, '%04d.png')];
    const out = path.join(outDir, a.name + (a.opaque ? '.mp4' : '.mov'));
    if (a.opaque) execFileSync('ffmpeg', [...src, '-c:v', 'libx264', '-crf', '15', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out]);
    else execFileSync('ffmpeg', [...src, '-c:v', 'prores_ks', '-profile:v', '4', '-qscale:v', '10', '-alpha_bits', '8', '-pix_fmt', 'yuva444p10le', '-vendor', 'apl0', out]);
    fs.rmSync(fdir, { recursive: true, force: true });
    console.log('rendered', a.name, n, 'frames', (fs.statSync(out).size / 1e6).toFixed(1) + 'MB');
  }
  await browser.close();
})();
