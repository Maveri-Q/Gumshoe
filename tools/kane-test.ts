// The sentence as a permanent Kane test file (*_test.md). Format from the Kane docs page
// "testmd": frontmatter, then one "## heading" per step with plain words that end in a check.
import { spawn } from "node:child_process";
import { mkdirSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import { kaneCommand, parseNdjson } from "./kane.ts";
import { serve } from "./serve.ts";

export function testFile(bug: any, port: number): string {
  return `---
mode: testing
url: http://127.0.0.1:${port}${bug.path ?? "/"}
max_steps: 30
---

# ${bug.sentence}

## Get the app ready
${bug.setup}
Verify that this is true: ${bug.ready}

## Check the sentence
${bug.action}
Verify that this is true: ${bug.working}
`;
}

export async function runTestFile(file: string, dist: string, port: number, outDir: string) {
  mkdirSync(outDir, { recursive: true });
  const server = await serve(resolve(dist), port);
  const { cmd, pre } = kaneCommand(), t0 = Date.now();
  const child = spawn(cmd, [...pre, "testmd", "run", file, "--agent", "--headless", "--timeout", "480"], { cwd: outDir, windowsHide: true });
  let out = "", err = "";
  child.stdout.on("data", d => (out += d)); child.stderr.on("data", d => (err += d));
  const timer = setTimeout(() => child.kill(), 600000);
  const exit = await new Promise<number | null>(r => { child.on("close", r); child.on("error", () => r(-1)); });
  clearTimeout(timer); server.close();
  writeFileSync(`${outDir}/kane.ndjson`, out); writeFileSync(`${outDir}/kane.stderr.txt`, err);
  const events = parseNdjson(out);
  const credits = Math.round(events.filter(e => e.type === "run_end").reduce((a, e) => a + Number(e.credits_consumed ?? e.credits ?? 0), 0) * 10) / 10;
  // Exit codes from the docs: 0 passed, 1 a step failed, 2 error, 3 cancelled or timed out.
  return { exit, status: exit === 0 ? "passed" : exit === 1 ? "failed" : "error", credits, seconds: Math.round((Date.now() - t0) / 1000), testUrl: events.filter(e => e.type === "run_end").at(-1)?.test_url };
}
