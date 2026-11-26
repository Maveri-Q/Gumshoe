// Records video/film.html frame by frame into an MP4. Every frame is set by seek(t), so nothing is dropped.
//   node video/render.mjs assets              take the live-site pictures used at the end
//   node video/render.mjs stills 5 60 92      save single frames to video/out/still-<t>.png
//   node video/render.mjs video 0 190 out.mp4 [fps]   (with WARP=video/out/voice/plan.json, times are on the re-timed film)
// Needs playwright-core (PW env var points at it) and ffmpeg on PATH.
import { createServer } from "node:http";
import { readFileSync, existsSync, statSync, mkdirSync } from "node:fs";
import { join, extname, resolve } from "node:path";
import { spawn } from "node:child_process";
const { chromium } = await import(process.env.PW ?? "playwright-core");

const root = resolve(import.meta.dirname, ".."), out = join(root, "video", "out");
mkdirSync(out, { recursive: true });
const types = { ".html": "text/html", ".js": "text/javascript", ".jpg": "image/jpeg", ".png": "image/png", ".svg": "image/svg+xml" };
const server = createServer((q, r) => {
  const f = join(root, decodeURIComponent(new URL(q.url, "http://x").pathname));
  if (!f.startsWith(root) || !existsSync(f) || statSync(f).isDirectory()) { r.writeHead(404); return r.end(); }
  r.writeHead(200, { "content-type": types[extname(f)] ?? "application/octet-stream" }); r.end(readFileSync(f));
}).listen(4411, "127.0.0.1");

const browser = await chromium.launch({ executablePath: process.env.CHROME });
const [mode, ...args] = process.argv.slice(2);
// The re-timed film: new time -> film time, straight lines between the [new, old] pairs in plan.json.
const warp = process.env.WARP ? JSON.parse(readFileSync(process.env.WARP, "utf8")).warp : null;
const filmTime = t => { if (!warp) return t; for (let k = 1; k < warp.length; k++) { const [n0, o0] = warp[k - 1], [n1, o1] = warp[k]; if (t <= n1) return o0 + (o1 - o0) * (t - n0) / (n1 - n0); } return warp.at(-1)[1]; };
try {
  if (mode === "assets") {
    // Our own live page, read only. Type a solved report into the box, then show the search mid-way.
    const p = await browser.newPage({ viewport: { width: 1500, height: 800 }, deviceScaleFactor: 1.28 });
    await p.goto("https://gumshoe-puce.vercel.app", { waitUntil: "networkidle" });
    await p.fill("#url", "https://github.com/TiddlyWiki/TiddlyWiki5/issues/9574");
    await p.click(".field button"); await p.waitForTimeout(600);
    await p.screenshot({ path: join(root, "video", "assets", "site-1.png") });
    await p.evaluate(() => { document.querySelectorAll("img").forEach(i => i.loading = "eager"); document.querySelectorAll(".step")[5].scrollIntoView({ block: "center" }); });
    await p.waitForFunction(() => [...document.images].every(i => i.complete));
    await p.waitForTimeout(1500);
    await p.screenshot({ path: join(root, "video", "assets", "site-2.png") });
  } else {
    const p = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
    await p.goto("http://127.0.0.1:4411/video/film.html");
    await p.waitForFunction(() => window.READY, null, { timeout: 60000 });
    if (mode === "stills") for (const t of args) { await p.evaluate(t => seek(t), +t); await p.screenshot({ path: join(out, `still-${t}.png`) }); }
    if (mode === "video") {
      const [a, b, name, fps = "30"] = args, n = Math.round((b - a) * fps);
      const ff = spawn("ffmpeg", ["-y", "-f", "image2pipe", "-framerate", fps, "-c:v", "mjpeg", "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", join(out, name)], { stdio: ["pipe", "inherit", "inherit"] });
      for (let i = 0; i < n; i++) {
        await p.evaluate(t => seek(t), filmTime(+a + i / fps));
        const buf = await p.screenshot({ type: "jpeg", quality: 92 });
        if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once("drain", r));
        if (i % 300 === 0) console.log(`frame ${i} of ${n}`);
      }
      ff.stdin.end(); await new Promise(r => ff.on("close", r));
    }
  }
} finally { await browser.close(); server.close(); }
