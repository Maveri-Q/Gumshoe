// Saves the list of commits each hunt searched, so the replay needs no clone.
//   node tools/save-range.ts
import { execFileSync } from "node:child_process";
import { readFileSync, writeFileSync, existsSync, readdirSync } from "node:fs";
import { join, resolve } from "node:path";
const root = resolve(import.meta.dirname, "..");
for (const id of existsSync(join(root, "runs")) ? readdirSync(join(root, "runs")) : []) {
  const f = join(root, "runs", id, "result.json");
  if (!existsSync(f)) continue;
  const r = JSON.parse(readFileSync(f, "utf8"));
  if (!r.good || !r.bad) continue;
  const app = JSON.parse(readFileSync(join(root, "apps", id.replace(/-\d+$/, ""), "app.json"), "utf8"));
  save(join(root, app.clone), r.good, r.bad, join(root, "runs", id, "commits.json"), true);
}
// Phase 1 searched the whole history, not only first parents.
for (const [bug, folder] of [["excalidraw-menu", "excalidraw-bisect"], ["excalidraw-alpha-hex", "alpha-bisect"]]) {
  const b = JSON.parse(readFileSync(join(root, "bugs", bug + ".json"), "utf8"));
  save(join(root, "work/excalidraw"), b.good, b.bad, join(root, "validation/phase1", folder, "commits.json"), false);
}
function save(cwd: string, good: string, bad: string, out: string, firstParent: boolean) {
  if (!existsSync(cwd)) return;
  const l = execFileSync("git", ["log", "--reverse", ...(firstParent ? ["--first-parent"] : []), "--format=%H%x09%cI%x09%s", `${good}..${bad}`], { cwd, encoding: "utf8", maxBuffer: 1e8 }).trim().split("\n");
  writeFileSync(out, JSON.stringify(l.map(x => { const [sha, date, subject] = x.split("\t"); return { sha, date, subject }; }), null, 0));
  console.log(out, l.length);
}
