// npm run replay: rebuilds every verdict and every result from the recorded real runs.
// No Kane account, no Claude, no network. It reads Kane's own output files again, works out each
// verdict with the same code as the live run, and stops if anything differs from what was recorded.
// One thing is taken as recorded: the second reader's answer about each saved screen.
import { readFileSync, existsSync, readdirSync, writeFileSync } from "node:fs";
import { join, resolve, relative } from "node:path";
import { parseNdjson, resultFromEvents } from "./kane.ts";
import { replayResult } from "./recording.ts";
import { tryVerdict, combine, type Verdict } from "./verdict.ts";
import { renderSite } from "./site.ts";

const root = resolve(import.meta.dirname, "..");
const read = (f: string) => JSON.parse(readFileSync(f, "utf8"));
const problems: string[] = [];
let checkedTries = 0, checkedCommits = 0;

/** Work out one commit's verdict again from Kane's recorded output. */
function replayCommit(dir: string) {
  const v = read(join(dir, "verdict.json")), verdicts: Verdict[] = [];
  const tries = v.tries.map((t: any) => {
    const kf = join(dir, `try-${t.try}`, "kane.ndjson"), lf = join(dir, `try-${t.try}`, "look", "kane.ndjson");
    // Cheap mode: "ready" means every recorded step, with its ready check, passed in Kane's own output.
    const steps = t.how === "replay" ? replayResult(parseNdjson(readFileSync(join(dir, `try-${t.try}`, "steps.ndjson"), "utf8"))) : undefined;
    const k = steps ? { answers: { ready: steps.passed ? "yes" : undefined }, testUrl: steps.testUrl } as any : resultFromEvents(parseNdjson(readFileSync(kf, "utf8")), kf, 0);
    const look = existsSync(lf) ? resultFromEvents(parseNdjson(readFileSync(lf, "utf8")), lf, 0).conditionResults : undefined;
    const again = tryVerdict({ ready: k.answers.ready, look, witness: t.screenSaysBroken });
    checkedTries++;
    if (again.verdict !== t.verdict) problems.push(`${relative(root, dir)} try ${t.try}: recorded ${t.verdict}, replay says ${again.verdict}`);
    verdicts.push(again.verdict);
    return { ...t, testUrl: k.testUrl };
  });
  const final = verdicts.length ? combine(verdicts) ?? "unsure" : "unsure"; // no tries: the build failed
  checkedCommits++;
  if (final !== v.verdict) problems.push(`${relative(root, dir)}: recorded ${v.verdict}, replay says ${final}`);
  return { ...v, tries, verdict: final, dir: relative(root, dir).replace(/\\/g, "/") };
}
const commitDirs = (d: string) => existsSync(d) ? readdirSync(d).map(x => join(d, x)).filter(x => existsSync(join(x, "verdict.json"))) : [];
const byTime = (a: any, b: any) => String(a.finishedAt ?? "").localeCompare(String(b.finishedAt ?? ""));

/** The guilty commit, worked out from the verdicts alone: the bad one right after a good one. */
function culpritFrom(commits: any[], good: string, judged: any[]) {
  let lo = -1, hi = commits.length - 1; // the good end sits just before the list, the bad end is last
  const idx = (s: string) => commits.findIndex(c => c.sha === s);
  for (const j of judged) {
    const i = idx(j.sha);
    if (i < 0) continue;
    if (j.verdict === "good") lo = Math.max(lo, i);
    if (j.verdict === "bad") hi = Math.min(hi, i);
  }
  return hi - lo === 1 ? commits[hi] : undefined;
}

const hunts: any[] = [];
// Phase 1: the two hunts where the steps and the screen check were written by hand.
for (const [bugName, bisect, cal] of [["excalidraw-menu", "excalidraw-bisect", "excalidraw-calibration-2"], ["excalidraw-alpha-hex", "alpha-bisect", "alpha-calibration-2"]]) {
  const b = read(join(root, "bugs", bugName + ".json")), base = join(root, "validation/phase1", bisect);
  const judged = commitDirs(base).map(replayCommit), logText = readFileSync(join(base, "log.txt"), "utf8");
  const when = (s: string) => logText.indexOf(`COMMIT ${s.slice(0, 8)}`);
  judged.sort((x, y) => when(x.sha) - when(y.sha));
  const ends = commitDirs(join(root, "validation/phase1", cal)).map(replayCommit);
  const commits = read(join(base, "commits.json")), c = culpritFrom(commits, b.good, judged);
  if (!c) problems.push(`${bugName}: the verdicts don't lead to one commit`);
  const all = [...ends, ...judged];
  hunts.push({ id: bugName, by: "hand", app: "Excalidraw", issue: b.source, title: b.title, sentence: b.sentence, outcome: "found", culprit: c?.sha, culpritSubject: c?.subject, range: commits.length, commits, judged, ends,
    credits: sum(all, "credits"), minutes: sum(all, "totalSeconds") / 60, tries: all.flatMap(x => x.tries).length, refused: all.flatMap(x => x.tries).filter((t: any) => t.verdict === "unsure").length,
    truth: { culprit: b.maintainersCulprit, who: "the maintainers", source: b.source, took: b.took } });
}
for (const id of existsSync(join(root, "runs")) ? readdirSync(join(root, "runs")).sort() : []) {
  const base = join(root, "runs", id);
  if (!existsSync(join(base, "result.json"))) continue;
  const r = read(join(base, "result.json")), app = read(join(root, "apps", id.replace(/-\d+$/, ""), "app.json"));
  const ends = readdirSync(base).filter(x => /^(reported-\d|older)$/.test(x)).sort((a, b) => (a === "older" ? 1 : 0) - (b === "older" ? 1 : 0)).flatMap(x => commitDirs(join(base, x)).map(d => ({ ...replayCommit(d), part: x })));
  const judged = commitDirs(join(base, "bisect")).map(replayCommit).sort(byTime);
  const h: any = { ...r, by: "issue", app: app.name ?? app.repo.split("/")[1], commits: [], judged, ends, drafts: readdirSync(base).filter(x => /^check-\d/.test(x)).length };
  if (existsSync(join(base, "commits.json"))) {
    h.commits = read(join(base, "commits.json"));
    const c = culpritFrom(h.commits, r.good, [...ends.filter(e => !/^reported/.test(e.part)), ...judged]);
    if (r.outcome === "found" && c?.sha !== r.culprit) problems.push(`${id}: recorded culprit ${r.culprit?.slice(0, 8)}, replay says ${c?.sha.slice(0, 8)}`);
  }
  const all = [...ends, ...judged];
  // Cheap mode: making the recording counts too.
  const recs = readdirSync(base).filter(x => /^recording-\d/.test(x) && existsSync(join(base, x, "record.json"))).map(x => read(join(base, x, "record.json")));
  h.cheap = recs.length > 0;
  h.credits = Math.round((sum(all, "credits") + sum(recs, "credits")) * 10) / 10; h.minutes = (sum(all, "totalSeconds") + sum(recs, "seconds")) / 60; h.tries = all.flatMap(x => x.tries).length; h.refused = all.flatMap(x => x.tries).filter((t: any) => t.verdict === "unsure").length;
  if (existsSync(join(root, "truth", id + ".json"))) h.truth = read(join(root, "truth", id + ".json"));
  if (existsSync(join(base, "culprit.diff"))) h.diff = readFileSync(join(base, "culprit.diff"), "utf8").slice(0, 20000);
  if (existsSync(join(base, "fix", "fix.json"))) {
    h.fix = read(join(base, "fix", "fix.json"));
    for (const a of h.fix.attempts) {
      const d = commitDirs(join(base, "fix", `attempt-${a.n}`))[0];
      if (d && replayCommit(d).verdict !== a.verdict) problems.push(`${id} fix attempt ${a.n} differs`);
      const df = join(base, "fix", `attempt-${a.n}.diff`);
      if (existsSync(df)) a.diff = readFileSync(df, "utf8").slice(0, 12000);
    }
  }
  hunts.push(h);
}
// The same hunt a second time in cheap mode (validation/cheap-9592). It has to end on the same commit.
{
  const base = join(root, "validation/cheap-9592"), judged = commitDirs(join(base, "bisect")).map(replayCommit), first = read(join(root, "runs/tiddlywiki-9592/result.json"));
  const c = culpritFrom(read(join(root, "runs/tiddlywiki-9592/commits.json")), first.good, judged);
  if (c?.sha !== first.culprit) problems.push(`cheap 9592 ends on ${c?.sha.slice(0, 8)}`);
  console.log(`9592 again, cheap mode: ${c?.sha.slice(0, 8)}, ${sum(judged, "credits")} credits, ${(sum(judged, "totalSeconds") / 60).toFixed(0)} min
`);
}
function sum(l: any[], k: string) { return Math.round(l.reduce((a, x) => a + (x[k] ?? 0), 0) * 10) / 10; }
/** Same commit as the maintainers? undefined when they never named one. */
export const sameCulprit = (h: any) => h.truth?.culprit ? !!h.culprit?.startsWith(h.truth.culprit.slice(0, 8)) : undefined;
for (const h of hunts) h.same = sameCulprit(h);

for (const h of hunts) console.log(`${h.id.padEnd(22)} ${h.outcome.padEnd(10)} ${(h.culprit ?? "").slice(0, 8)} maintainers: ${h.truth?.culprit?.slice(0, 8) ?? "no commit named"} ${h.same === undefined ? "" : h.same ? "SAME" : "DIFFERENT"} | ${h.tries} tries, ${h.refused} refused, ${h.credits} credits, ${h.minutes.toFixed(0)} min${h.fix ? ` | fix: ${h.fix.outcome}` : ""}`);
console.log(`\nChecked ${checkedCommits} commit verdicts and ${checkedTries} Kane tries against the recordings.`);
if (problems.length) { console.error("\nNOT THE SAME AS RECORDED:\n" + problems.join("\n")); process.exit(1); }
console.log("Everything matches what was recorded.");
writeFileSync(join(root, "site", "index.html"), renderSite(hunts, root));
console.log("Wrote site/index.html");
