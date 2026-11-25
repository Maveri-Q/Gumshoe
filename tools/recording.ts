// Cheap mode. Kane does the steps once and saves a recording. Every later version replays the
// recorded clicks with no AI. Only the look at the end uses Kane's AI.
// Format and flags from the Kane docs pages "testmd" and "testmd running".
import { spawn } from "node:child_process";
import { cpSync, mkdirSync, writeFileSync, existsSync } from "node:fs";
import { join } from "node:path";
import { kaneCommand, parseNdjson } from "./kane.ts";

/** The steps only. There is no check of the outcome here: a recorded outcome check fails on a broken version and Kane then works it all out again. */
export const stepsFile = (bug: any, port: number) => `---
mode: testing
url: http://127.0.0.1:${port}${bug.path ?? "/"}
max_steps: 30
---

# ${bug.id}

## Get the app ready
${bug.setup}
Verify that this is true: ${bug.ready}

## Do the last step
${bug.action}
`;

/** Was every step done from the recording, with the app ready? Read from Kane's own output. */
export function replayResult(events: any[]) {
  const ends = events.filter(e => e.type === "run_end"), done = events.filter(e => e.type === "test_md_done").at(-1);
  const credits = ends.reduce((a, e) => a + Number(e.credits_consumed ?? e.credits ?? 0), 0);
  return { finished: !!done, passed: done?.overall_status === "passed" && ends.length >= 2 && ends.every(e => e.status === "passed"), replayed: ends.length >= 2 && ends.every(e => e.reason === "replay completed"), why: ends.map(e => e.reason ?? e.status).join(", "), credits, testUrl: ends.at(-1)?.test_url as string | undefined };
}

/** Each try works on its own copy, so a replay can never change the recording. */
export async function runSteps(o: { recording: string; work: string; url: string; cdpEndpoint: string; ndjson: string; record?: boolean }) {
  mkdirSync(o.work, { recursive: true });
  cpSync(o.recording, o.work, { recursive: true });
  const { cmd, pre } = kaneCommand();
  const args = [...pre, "testmd", "run", join(o.work, "steps_test.md"), "--agent", "--cdp-endpoint", o.cdpEndpoint, "--timeout", "300", "--bug-detection", "off", ...(o.record ? [] : ["--no-adaptive-heal", "--override-start-url", o.url])];
  const child = spawn(cmd, args, { cwd: o.work, windowsHide: true });
  let out = "", err = "";
  child.stdout.on("data", d => (out += d)); child.stderr.on("data", d => (err += d));
  const timer = setTimeout(() => child.kill(), 420000);
  await new Promise(r => { child.on("close", r); child.on("error", r); });
  clearTimeout(timer);
  out = out.replace(/"share_url":"[^"]*",?/g, ""); // a link that opens the run for anyone who has it
  writeFileSync(o.ndjson, out); if (!o.record) writeFileSync(o.ndjson + ".stderr.txt", err);
  const made = join(o.work, "output-steps");
  if (o.record && existsSync(made)) cpSync(made, join(o.recording, "output-steps"), { recursive: true });
  return replayResult(parseNdjson(out));
}
