// Draws the report page from the replayed runs. Every number on it comes from the recordings.
import { mkdirSync, existsSync, copyFileSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { join } from "node:path";
import { readFileSync } from "node:fs";

const esc = (s: any) => String(s ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
const short = (s?: string) => (s ?? "").slice(0, 8);
const mins = (m: number) => `${Math.round(m)} min`;

function picture(root: string, from: string, name: string) {
  const to = join(root, "site", "img", name + ".jpg");
  if (!existsSync(to) && existsSync(from)) {
    mkdirSync(join(root, "site", "img"), { recursive: true });
    const r = spawnSync("ffmpeg", ["-y", "-loglevel", "error", "-i", from, "-vf", "scale=1120:-1", "-q:v", "5", to]);
    if (r.status !== 0) copyFileSync(from, to);
  }
  return existsSync(to) ? `img/${name}.jpg` : "";
}

/** One row per commit Kane judged: how many suspects were left, and what the screen showed. */
function rows(h: any, root: string) {
  const idx = (s: string) => h.commits.findIndex((c: any) => c.sha === s);
  let lo = -1, hi = h.commits.length - 1;
  const out: any[] = [];
  const row = (j: any, stage: string) => {
    const t = j.tries.filter((x: any) => x.verdict === j.verdict).at(-1) ?? j.tries.at(-1);
    return {
      sha: short(j.sha), subject: j.subject, verdict: j.verdict, at: idx(j.sha), tries: j.tries.map((x: any) => ({ v: x.verdict, why: x.why })), link: t?.testUrl,
      img: t ? picture(root, join(root, j.dir, `try-${t.try}`, "after.png"), `${h.id}-${stage}-${short(j.sha)}`) : "",
    };
  };
  const bad = h.ends.filter((e: any) => e.verdict === "bad").at(-1), good = h.ends.find((e: any) => e.verdict === "good");
  if (bad) out.push({ ...row(bad, "e"), what: "reported", at: h.commits.length - 1, lo, hi });
  if (good) out.push({ ...row(good, "e"), what: "older", at: -1, lo, hi });
  for (const j of h.judged) {
    const i = idx(j.sha);
    if (j.verdict === "good") lo = Math.max(lo, i);
    if (j.verdict === "bad") hi = Math.min(hi, i);
    out.push({ ...row(j, "b"), lo, hi });
  }
  return out;
}

export function renderSite(hunts: any[], root: string): string {
  const found = hunts.filter(h => h.outcome === "found");
  const known = found.filter(h => h.same !== undefined), same = known.filter(h => h.same);
  const hero = found.find(h => h.fix?.outcome === "fixed" && h.same) ?? found.find(h => h.by === "issue" && h.same) ?? found[0];
  const data = [hero, ...found.filter(h => h !== hero)].map(h => ({
    app: h.app, no: h.issue.split("/").pop(), issue: h.issue, title: h.title, sentence: h.sentence, range: h.range, culprit: short(h.culprit), subject: h.culpritSubject,
    commitUrl: `${h.issue.replace(/\/(issues|pull)\/.*/, "")}/commit/${h.culprit}`, same: h.same, who: h.truth?.who, note: h.truth?.note,
    minutes: Math.round(h.minutes), credits: Math.round(h.credits), n: h.commits.length, rows: rows(h, root), diff: h.diff,
    fix: h.fix && {
      outcome: h.fix.outcome, green: h.fix.test?.green.status, red: h.fix.test?.red.status, file: h.fix.test?.file,
      attempts: h.fix.attempts.map((a: any) => ({
        n: a.n, verdict: a.verdict, said: a.said, diff: a.diff, link: a.tries?.at(-1)?.testUrl,
        img: a.sha ? picture(root, join(root, "runs", h.id, "fix", `attempt-${a.n}`, short(a.sha), `try-${a.tries?.at(-1)?.try}`, "after.png"), `${h.id}-fix-${a.n}`) : "",
      })),
    },
  }));
  const board = hunts.map(h => `<tr>
<th scope="row"><a href="${esc(h.issue)}">${esc(h.app)} ${esc(h.issue.split("/").pop())}</a><span>${esc(h.title)}</span></th>
<td>${h.outcome === "found" ? `<code>${short(h.culprit)}</code>` : esc(h.outcome)}</td>
<td>${h.truth?.culprit ? `<code>${esc(short(h.truth.culprit))}</code>` : "No commit named"}</td>
<td>${h.same === undefined ? (h.outcome === "found" ? `<b class="na">Nothing to compare</b>` : `<b class="no">Not found</b>`) : h.same ? `<b class="yes">Same</b>` : `<b class="no">Different</b>`}</td>
<td>${h.range ?? ""}</td><td>${h.tries}${h.refused ? ` <small>(${h.refused} refused)</small>` : ""}</td><td>${mins(h.minutes)}</td><td>${Math.round(h.credits)}</td>
<td>${esc(h.truth?.took ?? "Not known")}</td>
<td>${h.by === "hand" ? "By hand" : "By Gumshoe"}</td>
<td>${h.fix ? (h.fix.outcome === "fixed" ? `<b class="yes">Attempt ${h.fix.attempts.length}</b>` : `<b class="no">${esc(h.fix.outcome)}</b>`) : "Not tried"}</td></tr>`).join("\n");
  const total = hunts.reduce((a, h) => a + h.tries, 0), refused = hunts.reduce((a, h) => a + h.refused, 0);
  const page = readFileSync(join(root, "tools", "site.html"), "utf8");
  const fill: Record<string, string> = {
    BOARD: board, FOUND: String(found.length), HUNTS: String(hunts.length), SAME: String(same.length), KNOWN: String(known.length), TOTAL: String(total), REFUSED: String(refused),
    APPS: String(new Set(hunts.map(h => h.app)).size), DATA: JSON.stringify(data).replace(/</g, "\\u003c"),
  };
  return page.replace(/%%([A-Z]+)%%/g, (_, k) => fill[k]);
}
