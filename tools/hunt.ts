// gumshoe <issue link>: from a bug report to the commit that broke it.
//   node tools/hunt.ts <issue link> --app tiddlywiki [--port 4310] [--good <sha>] [--bad <sha>] [--cheap]
// --cheap: Kane does the steps once, and every other version replays them (tools/recording.ts)
// 1 read the issue  2 write the check  3 check the bug shows on the reported version
// 4 find a good older version  5 git bisect run  6 save the result
import { execFileSync, spawnSync } from "node:child_process";
import { readFileSync, writeFileSync, mkdirSync, existsSync, appendFileSync, readdirSync } from "node:fs";
import { join, resolve } from "node:path";
import { readIssue, parseIssueUrl } from "./issue.ts";
import { writeCheck, type Check } from "./write-check.ts";

const root = resolve(import.meta.dirname, "..");
const [url, ...rest] = process.argv.slice(2);
const opt = (n: string) => { const i = rest.indexOf("--" + n); return i >= 0 ? rest[i + 1] : undefined; };
const appName = opt("app")!, app = JSON.parse(readFileSync(join(root, "apps", appName, "app.json"), "utf8"));
const { repo, number } = parseIssueUrl(url);
if (repo.toLowerCase() !== app.repo.toLowerCase()) throw new Error(`--app ${appName} is for ${app.repo}, the issue is in ${repo}`);
const id = `${appName}-${number}`, port = Number(opt("port") ?? 4310);
const run = `runs/${id}`, dir = join(root, run), srcRel = (app.src ?? "clones/hunt-{id}").replace("{id}", id), src = join(root, srcRel);
mkdirSync(dir, { recursive: true });
const started = Date.now();
const log = (s: string) => { console.log(s); appendFileSync(join(dir, "hunt.log"), `${new Date().toISOString()} ${s}\n`); };
const cloneDir = join(root, app.clone);
const inClone = (...a: string[]) => execFileSync("git", a, { cwd: cloneDir, encoding: "utf8", maxBuffer: 1e8 }).trim();
const git = (...a: string[]) => execFileSync("git", a, { cwd: src, encoding: "utf8", maxBuffer: 1e8, stdio: ["ignore", "pipe", "pipe"] }).trim();
let check: Check | undefined;

const issue = await readIssue(url, join(dir, "issue.json"));
log(`ISSUE ${issue.repo}#${issue.number} ${issue.title}`);

// The version the reporter used: the last commit on the main branch before they wrote the issue.
const branch = inClone("rev-parse", "--abbrev-ref", "origin/HEAD");
const bad = inClone("rev-parse", opt("bad") ?? inClone("rev-list", "-1", "--first-parent", `--before=${issue.createdAt}`, branch));
if (!existsSync(src)) inClone("worktree", "add", "--detach", src, bad);
log(`REPORTED VERSION ${bad.slice(0, 8)} ${inClone("log", "-1", "--format=%cd %s", "--date=short", bad)}`);

const bugFile = `${run}/bug.json`;
const cheap = rest.includes("--cheap");
const save = (c: Check, draft: number) => writeFileSync(join(root, bugFile), JSON.stringify({ id, ...c, witness: { reader: true }, ...(existsSync(join(dir, "frozen-check.sha256")) && !readFileSync(join(root, bugFile), "utf8").includes("lookAgain") ? {} : { lookAgain: true }), ...(cheap ? { recording: `${run}/recording-${draft}` } : {}), source: issue.url, repo: srcRel,
  build: app.build, unpack: app.unpack, dist: app.dist ?? `dist/${id}`, env: app.env ?? {}, port }, null, 2));
function judge(sha: string, folder: string): any {
  const f = join(dir, folder, sha.slice(0, 8), "verdict.json");
  if (existsSync(f)) return JSON.parse(readFileSync(f, "utf8")); // picking up after a stop
  git("checkout", "-q", "--force", sha);
  spawnSync(process.execPath, [join(root, "tools/step.mjs"), bugFile, `${run}/${folder}`], { cwd: root, stdio: "inherit" });
  if (!existsSync(f)) throw new Error("no verdict, stopping");
  return JSON.parse(readFileSync(f, "utf8"));
}

// Write the check and make sure it shows the bug on the reported version. Three drafts at most.
let shown = false, feedback: any;
for (let draft = 1; draft <= 3 && !shown; draft++) {
  const saved = join(dir, `check-${draft}.json`);
  check = existsSync(saved) ? JSON.parse(readFileSync(saved, "utf8")) as Check : await writeCheck(issue, app.about, feedback);
  writeFileSync(saved, JSON.stringify(check, null, 2)); save(check, draft);
  log(`DRAFT ${draft}: ${check.sentence}`);
  const recDir = join(dir, `recording-${draft}`);
  if (cheap && !existsSync(join(recDir, "output-steps", ".internal"))) {
    const rec = spawnSync(process.execPath, [join(root, "tools/record.ts"), bugFile, bad], { cwd: root, encoding: "utf8" });
    log(`  recording the steps: ${rec.status === 0 ? "done" : "failed"}`);
    writeFileSync(join(recDir, "record.out.txt"), (rec.stdout ?? "") + (rec.stderr ?? ""));
    if (rec.status !== 0) { feedback = { previous: check, notes: "Kane could not finish the steps: " + (rec.stdout ?? "").slice(-1500), screens: [join(recDir, "after.png")].filter(p => existsSync(p)) }; continue; }
  }
  const v = judge(bad, `reported-${draft}`);
  shown = v.verdict === "bad";
  log(`  on the reported version: ${v.verdict}`);
  feedback = {
    previous: check,
    notes: v.tries.map((t: any) => `try ${t.try}: ready=${t.ready}; broken statement judged ${t.look?.[0]}, working statement judged ${t.look?.[1]}; second reader says broken=${t.screenSaysBroken}; ${t.why}; agent said: ${t.summary ?? ""}`).join("\n") || v.note,
    screens: v.tries.map((t: any) => join(dir, `reported-${draft}`, bad.slice(0, 8), `try-${t.try}`, "after.png")).slice(-1).filter((p: string) => existsSync(p)),
  };
}
if (!shown) done({ outcome: "could not show the bug on the reported version", bad });

// Find a good version: the one the report names, else step back through releases, else by weeks.
const candidates: string[] = [];
const add = (s: string) => {
  try {
    const m = inClone("merge-base", inClone("rev-parse", s + "^{commit}"), bad);
    if (m !== bad && !candidates.includes(m)) candidates.push(m);
  } catch {}
};
if (opt("good")) add(opt("good")!);
if (check!.goodVersion) add(app.versionTag.replace("{version}", check!.goodVersion));
const at = Date.parse(issue.createdAt);
const tags = inClone("for-each-ref", "refs/tags", "--sort=-creatordate", "--format=%(refname:short) %(creatordate:unix)").split("\n").map(l => l.split(" "))
  .filter(([t, d]) => /^v?\d+(\.\d+)+$/.test(t) && Number(d) * 1000 < at && Number(d) * 1000 > at - 400 * 864e5);
for (const [t] of tags.slice(0, 4)) add(t);
// Releases can be too old to build, so going back by weeks comes after them.
for (const w of [2, 6, 14, 30]) add(inClone("rev-list", "-1", "--first-parent", `--before=${new Date(at - w * 7 * 864e5).toISOString()}`, branch));
let good: string | undefined, knownBad = bad;
for (const c of candidates.slice(0, 8)) {
  const v = judge(c, "older");
  log(`OLDER ${c.slice(0, 8)} ${inClone("log", "-1", "--format=%cd", "--date=short", c)}: ${v.verdict}`);
  if (v.verdict === "good") { good = c; break; }
  if (v.verdict === "bad") knownBad = c;
}
if (!good) done({ outcome: "found no older version where it works", bad });

// The real git bisect. Merges count as one step (first-parent).
try { git("bisect", "reset"); } catch {}
const range = Number(git("rev-list", "--count", "--first-parent", `${good}..${knownBad}`));
log(`BISECT ${good!.slice(0, 8)}..${knownBad.slice(0, 8)}, ${range} commits`);
const frozenFile = join(dir, "frozen-check.sha256"), frozen = execFileSync("git", ["hash-object", join(root, bugFile), ...frozenRecording()], { encoding: "utf8" });
if (existsSync(frozenFile)) {
  if (readFileSync(frozenFile, "utf8") !== frozen) throw new Error("the check changed since the bisect began");
  process.env.GUMSHOE_RESUME = "1"; log("Picking up after a stop, with the same frozen check");
}
writeFileSync(frozenFile, frozen);
git("bisect", "start", "--first-parent", knownBad, good!);
const b = spawnSync("git", ["bisect", "run", "node", join(root, "tools/step.mjs").replace(/\\/g, "/"), bugFile, `${run}/bisect`], { cwd: src, encoding: "utf8", maxBuffer: 1e8 });
writeFileSync(join(dir, "bisect.out.txt"), (b.stdout ?? "") + (b.stderr ?? ""));
writeFileSync(join(dir, "bisect.log.txt"), git("bisect", "log"));
const m = (b.stdout ?? "").match(/([0-9a-f]{40}) is the first '?bad'? commit/);
if (!m) done({ outcome: "the bisect could not name one commit", range, good, bad: knownBad });
const culprit = m![1];
writeFileSync(join(dir, "culprit.txt"), git("show", "-m", "--first-parent", "--format=%H%n%an%n%cI%n%s%n%b", "--stat=120", culprit));
writeFileSync(join(dir, "culprit.diff"), git("show", "-m", "--first-parent", "--format=", culprit));
log(`CULPRIT ${culprit.slice(0, 8)} ${git("log", "-1", "--format=%s", culprit)}`);
done({ outcome: "found", culprit, culpritSubject: git("log", "-1", "--format=%s", culprit), culpritDate: git("log", "-1", "--format=%cI", culprit), range, good, bad: knownBad });

/** In cheap mode the recording is part of the frozen check. */
function frozenRecording(): string[] {
  const r = JSON.parse(readFileSync(join(root, bugFile), "utf8")).recording, at = r && join(root, r, "output-steps", ".internal");
  return at ? (readdirSync(at, { recursive: true }) as string[]).filter(f => f.endsWith(".ndjson")).sort().map(f => join(at, f)) : [];
}
function done(r: any): never {
  let credits = 0, tries = 0, refused = 0;
  const steps: any[] = [];
  for (const part of readdirSync(dir, { withFileTypes: true })) {
    if (!part.isDirectory()) continue;
    for (const c of readdirSync(join(dir, part.name))) {
      const f = join(dir, part.name, c, "verdict.json");
      if (!existsSync(f)) continue;
      const v = JSON.parse(readFileSync(f, "utf8"));
      credits += v.credits; tries += v.tries.length; refused += v.tries.filter((t: any) => t.verdict === "unsure").length;
      steps.push({ part: part.name, sha: v.sha, subject: v.subject, verdict: v.verdict, credits: v.credits, seconds: v.totalSeconds, date: git("log", "-1", "--format=%cI", v.sha), finished: v.finishedAt });
    }
  }
  steps.sort((a, b) => String(a.finished).localeCompare(String(b.finished)));
  const out = { id, issue: issue.url, title: issue.title, issueCreatedAt: issue.createdAt, sentence: check?.sentence, ...r, tries, refused, credits: Math.round(credits * 10) / 10,
    minutes: Math.round((Date.now() - started) / 6000) / 10, finishedAt: new Date().toISOString(), steps };
  writeFileSync(join(dir, "result.json"), JSON.stringify(out, null, 2));
  log(`DONE ${r.outcome} ${out.credits} credits, ${out.minutes} min`);
  process.exit(r.outcome === "found" ? 0 : 1);
}
