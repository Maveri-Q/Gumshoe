// Judges the commit that is checked out right now. Used by `git bisect run`.
//   node tools/judge.ts bugs/excalidraw-menu.json <evidence folder>
// Builds the app, serves it, asks Kane in a fresh browser (2 tries that agree), writes evidence.
// Exit codes: 0 good, 1 bad, 125 skip, 200 stop the whole bisect (Kane itself is not working).
import { spawnSync, execFileSync } from "node:child_process";
import { createServer } from "node:http";
import { readFileSync, writeFileSync, mkdirSync, existsSync, statSync, appendFileSync, rmSync } from "node:fs";
import { join, resolve, extname, sep } from "node:path";
import { runKane } from "./kane.ts";
import { launchRole, snapshot, closeRole, readPixel } from "./browsers.ts";
import { secondReader } from "./claude.ts";
import { tryVerdict, combine, pixelSaysBroken, bisectCode, type Verdict } from "./verdict.ts";

const root = resolve(import.meta.dirname, "..");
const bug = JSON.parse(readFileSync(resolve(root, process.argv[2]), "utf8"));
const evidence = resolve(root, process.argv[3]);
const repo = resolve(root, bug.repo);
const git = (...a: string[]) => execFileSync("git", a, { cwd: repo, encoding: "utf8" }).trim();
const sha = git("rev-parse", "HEAD"), subject = git("log", "-1", "--format=%s");
const dir = join(evidence, sha.slice(0, 8));
mkdirSync(dir, { recursive: true });
const started = Date.now();
const log = (s: string) => { console.log(s); appendFileSync(join(evidence, "log.txt"), `${new Date().toISOString()} ${s}\n`); };
log(`COMMIT ${sha.slice(0, 8)} ${subject}`);

// 1. Build. The old build is removed first, so a failed build can never be judged by mistake.
const dist = resolve(root, bug.dist);
rmSync(dist, { recursive: true, force: true });
mkdirSync(dist, { recursive: true });
const cmd: string[] = bug.build.map((a: string) => a.replaceAll("{src}", repo).replaceAll("{dist}", dist));
const b = spawnSync(cmd[0], cmd.slice(1), { cwd: root, encoding: "utf8", env: { ...process.env, ...bug.env }, maxBuffer: 1e8 });
const buildS = Math.round((Date.now() - started) / 1000);
if (b.status === 0 && bug.unpack) execFileSync(process.platform === "win32" ? join(process.env.SystemRoot!, "System32", "tar.exe") : "tar", ["-xf", bug.unpack], { cwd: dist });
if (b.status !== 0 || !existsSync(join(dist, "index.html"))) {
  writeFileSync(join(dir, "build.log"), (b.stdout ?? "") + (b.stderr ?? ""));
  finish("unsure", [], `build failed (${buildS}s)`);
}
log(`  built in ${buildS}s`);

// 2. Serve it on this machine only.
const types: Record<string, string> = {
  ".html": "text/html", ".js": "text/javascript", ".mjs": "text/javascript", ".css": "text/css", ".json": "application/json",
  ".svg": "image/svg+xml", ".png": "image/png", ".woff2": "font/woff2", ".wasm": "application/wasm",
};
const server = createServer((q, r) => {
  let f = join(dist, decodeURIComponent(new URL(q.url!, "http://x").pathname));
  if (!f.startsWith(dist + sep) || !existsSync(f) || statSync(f).isDirectory()) f = join(dist, "index.html");
  r.writeHead(200, { "content-type": types[extname(f)] ?? "application/octet-stream", "cache-control": "no-store" });
  r.end(readFileSync(f));
});
const port = bug.port ?? 4300;
await new Promise<void>((r, x) => { server.once("error", x); server.listen(port, "127.0.0.1", () => r()); });

// 3. Ask Kane.
const objective = [
  `Do these steps in order.`,
  `1. ${bug.setup}`,
  `2. Is this true right now: "${bug.ready}"? If it is true, store the word yes as 'ready'. If it is not true, store the word no as 'ready'.`,
  `3. ${bug.action}`,
  `Then stop.`,
].join("\n");
const tries: any[] = [], verdicts: Verdict[] = [];
let final: Verdict | undefined;
while (!(final = combine(verdicts))) {
  const n = tries.length + 1, tdir = join(dir, `try-${n}`), t0 = Date.now();
  const br = await launchRole(`t${sha.slice(0, 8)}-${n}-${t0}`, 9700 + (port - 4300) * 10 + n, join(root, ".kane-profiles"));
  let lookedAgain = false, k, look, pixel: number[] | undefined, screen = { url: "", text: "" };
  try {
    k = await runKane({ objective, url: `http://127.0.0.1:${port}${bug.path ?? "/"}`, cdpEndpoint: br.endpoint, name: `gumshoe-${bug.id}-${sha.slice(0, 8)}-${n}`, outDir: tdir, timeoutS: 300, maxSteps: 20 });
    // A separate look-only Kane run judges the page as it is now. In calibration 1 the run that
    // did the clicks answered wrongly about its own last screenshot.
    if (k.status) look = await runKane({ objective: "", conditions: [bug.broken, bug.working], cdpEndpoint: br.endpoint, name: "look", outDir: join(tdir, "look"), timeoutS: 120 });
    // Kane contradicted itself: let it look at the same page once more before refusing the try.
    if (bug.lookAgain && look?.conditionResults?.length === 2 && look.conditionResults[0] === look.conditionResults[1]) {
      const first = look;
      look = await runKane({ objective: "", conditions: [bug.broken, bug.working], cdpEndpoint: br.endpoint, name: "look", outDir: join(tdir, "look"), timeoutS: 120 });
      look.credits += first.credits; lookedAgain = true;
    }
    screen = await snapshot(br, join(tdir, "after.png"));
    if (bug.witness.pixel) pixel = await readPixel(br, bug.witness.pixel);
  } finally { closeRole(br, true); }
  await new Promise(r => setTimeout(r, 2500)); // let the browser profile be removed
  writeFileSync(join(tdir, "after.txt"), screen.text);
  // Kane's look came back with nothing in it. That is a lost connection, not a judgement.
  const lost = look?.conditionResults?.some((x: any) => typeof x !== "boolean");
  if (!k.status || !look?.status || lost) { log(`  Kane gave no result at all (exit ${k.exitCode}). Stopping the bisect.`); process.exit(200); }
  const witness = bug.witness.reader ? await secondReader(join(tdir, "after.png"), bug.broken, bug.working) : bug.witness.pixel ? pixelSaysBroken(pixel, bug.witness.workingRgb) : screen.text ? screen.text.includes(bug.witness.brokenText) : undefined;
  const v = tryVerdict({ ready: k.answers.ready, look: look.conditionResults, witness });
  const t = {
    try: n, verdict: v.verdict, why: v.why, ready: k.answers.ready, look: look.conditionResults, lookStatus: look.status, ...(lookedAgain ? { lookedAgain } : {}),
    screenSaysBroken: witness, pixel, kaneStatus: k.status, summary: k.summary ?? k.oneLiner, credits: k.credits + look.credits, seconds: Math.round((Date.now() - t0) / 1000), testUrl: k.testUrl,
  };
  tries.push(t); verdicts.push(v.verdict);
  log(`  try ${n}: ${v.verdict} (${v.why}) ready=${t.ready} look[broken,working]=${JSON.stringify(t.look)} screenSaysBroken=${witness} ${t.credits.toFixed(1)} credits ${t.seconds}s`);
}
finish(final, tries, "");

function finish(v: Verdict, tries: any[], note: string): never {
  const credits = Math.round(tries.reduce((a, t) => a + t.credits, 0) * 10) / 10;
  const out = { finishedAt: new Date().toISOString(), sha, subject, verdict: v, note, buildSeconds: buildS, totalSeconds: Math.round((Date.now() - started) / 1000), credits, tries };
  writeFileSync(join(dir, "verdict.json"), JSON.stringify(out, null, 2));
  log(`  => ${v.toUpperCase()} ${note} ${credits} credits, ${out.totalSeconds}s`);
  process.exit(bisectCode(v));
}
