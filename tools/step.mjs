// What `git bisect run` calls. A crash normally exits with 1, which git reads as "bad".
// So the exit code only counts when the judge wrote a fresh verdict for this exact commit.
// Anything else exits 200, which stops the whole bisect.
import { spawnSync, execFileSync } from "node:child_process";
import { readFileSync, rmSync } from "node:fs";
import { join, resolve } from "node:path";
const root = resolve(import.meta.dirname, ".."), [bugFile, evidence] = process.argv.slice(2);
const bug = JSON.parse(readFileSync(join(root, bugFile), "utf8"));
const sha = execFileSync("git", ["rev-parse", "HEAD"], { cwd: join(root, bug.repo), encoding: "utf8" }).trim();
const file = join(root, evidence, sha.slice(0, 8), "verdict.json");
rmSync(file, { force: true });
spawnSync(process.execPath, [join(root, "tools/judge.ts"), bugFile, evidence], { cwd: root, stdio: ["ignore", "inherit", "inherit"] });
try {
  const v = JSON.parse(readFileSync(file, "utf8"));
  if (v.sha !== sha || !["good", "bad", "unsure"].includes(v.verdict)) throw new Error("wrong verdict file");
  process.exit({ good: 0, bad: 1, unsure: 125 }[v.verdict]);
} catch (e) { console.error("No verdict for this commit, so the bisect stops:", e.message); process.exit(200); }
