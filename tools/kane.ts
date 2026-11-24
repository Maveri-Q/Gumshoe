// Runs Kane CLI and reads its NDJSON output and Evidence Pack.
// Copied from Fessup (packages/cli/src/kane.ts). Flags checked against `kane-cli run --help` 0.10.6.
import { spawn, execFileSync } from "node:child_process";
import { writeFileSync, readFileSync, mkdirSync, existsSync, readdirSync, appendFileSync } from "node:fs";
import { join } from "node:path";
export interface KaneResult {
  exitCode: number | null; status?: string; reasonCode?: string; resultCode?: number; credits: number;
  testUrl?: string; oneLiner?: string; summary?: string; answers: Record<string, string>;
  evidencePack?: string; ndjsonPath: string; durationS?: number;
}

/** On Windows `kane-cli` is a .cmd shim that Node can't spawn without a shell, and a shell
 *  would mangle a multi-line objective. So run Kane's JS entry with Node directly. */
function kaneCommand(): { cmd: string; pre: string[] } {
  if (process.env.KANE_CLI_ENTRY) return { cmd: process.execPath, pre: [process.env.KANE_CLI_ENTRY] };
  if (process.platform === "win32") {
    const entry = join(process.env.APPDATA ?? "", "npm", "node_modules", "@testmuai", "kane-cli", "bin", "kane-cli.cjs");
    if (existsSync(entry)) return { cmd: process.execPath, pre: [entry] };
  }
  return { cmd: "kane-cli", pre: [] };
}

export interface RunOpts {
  objective: string;
  /** Leave out to start from the page the browser is already on (no reload). */
  url?: string;
  cdpEndpoint?: string;
  name: string;
  outDir: string;
  timeoutS?: number;
  maxSteps?: number;
  cwd?: string;
}

export function parseNdjson(text: string): any[] {
  return text.split(/\r?\n/).filter(Boolean).map(l => { try { return JSON.parse(l.replace(/^﻿/, "")); } catch { return null; } }).filter(Boolean);
}

/** Stored values survive in run_end.context.variables even when the run fails
 *  (final_state is empty on failure). Read both. */
export function resultFromEvents(events: any[], ndjsonPath: string, exitCode: number | null): KaneResult {
  const end = events.filter(e => e.type === "run_end").at(-1);
  const answers: Record<string, string> = {};
  for (const [k, v] of Object.entries<any>(end?.context?.variables ?? {})) if (v && typeof v.value === "string") answers[k] = v.value;
  for (const [k, v] of Object.entries<any>(end?.final_state ?? {})) if (typeof v === "string" && !answers[k]) answers[k] = v;
  const pack = events.find(e => e.type === "coverage" && e.pack)?.pack;
  return {
    exitCode, status: end?.status, reasonCode: end?.reason_code, resultCode: end?.result_code,
    credits: Number(end?.credits_consumed ?? end?.credits ?? 0), testUrl: end?.test_url,
    oneLiner: end?.one_liner, summary: end?.summary, answers, evidencePack: pack, ndjsonPath, durationS: end?.duration,
  };
}

export async function runKane(o: RunOpts): Promise<KaneResult> {
  mkdirSync(o.outDir, { recursive: true });
  const { cmd, pre } = kaneCommand();
  const args = [...pre, "run", o.objective, ...(o.url ? ["--url", o.url] : ["--allow-missing-url"]), "--agent", "--timeout", String(o.timeoutS ?? 480),
    "--max-steps", String(o.maxSteps ?? 60), "--name", o.name.replace(/[^a-zA-Z0-9_-]/g, "-")];
  if (o.cdpEndpoint) args.push("--cdp-endpoint", o.cdpEndpoint);
  else args.push("--headless");
  const ndjsonPath = join(o.outDir, "kane.ndjson");
  writeFileSync(join(o.outDir, "objective.txt"), o.objective);
  // Stream output to disk as it arrives, so a stuck run can be inspected while it runs.
  writeFileSync(ndjsonPath, "");
  writeFileSync(join(o.outDir, "kane.stderr.txt"), "");
  const child = spawn(cmd, args, { windowsHide: true, cwd: o.cwd ?? o.outDir });
  const out: Buffer[] = [];
  child.stdout.on("data", d => { out.push(d); appendFileSync(ndjsonPath, d); });
  child.stderr.on("data", d => appendFileSync(join(o.outDir, "kane.stderr.txt"), d));
  // Kane's own --timeout didn't stop a run stuck on a page (seen twice). Back it up with a hard limit.
  const hardLimitMs = ((o.timeoutS ?? 480) + 120) * 1000;
  let killed = false;
  const timer = setTimeout(() => {
    killed = true;
    appendFileSync(join(o.outDir, "kane.stderr.txt"), `
[gumshoe] Kane ran past ${hardLimitMs / 1000}s, so Gumshoe stopped it.
`);
    killTree(child.pid);
  }, hardLimitMs);
  const code: number | null = await new Promise(r => { child.on("close", r); child.on("error", () => r(-1)); });
  clearTimeout(timer);
  const text = Buffer.concat(out).toString("utf8");
  const result = resultFromEvents(parseNdjson(text), ndjsonPath, code);
  if (killed && !result.status) result.status = "stopped_by_gumshoe";
  return result;
}

function killTree(pid?: number) {
  if (!pid) return;
  try {
    if (process.platform === "win32") execFileSync("taskkill", ["/PID", String(pid), "/T", "/F"], { stdio: "ignore" });
    else process.kill(-pid, "SIGKILL");
  } catch { try { process.kill(pid, "SIGKILL"); } catch {} }
}

/** Pull screenshots out of the Evidence Pack (a zip). Uses the system `tar`, which reads zips
 *  on Windows 10+, macOS and most Linux. Returns paths of the extracted screenshots, in step order. */
export function extractScreenshots(pack: string | undefined, dest: string): string[] {
  if (!pack || !existsSync(pack)) return [];
  mkdirSync(dest, { recursive: true });
  // On Windows use the built-in bsdtar (reads zips). Git's GNU tar can come first on PATH,
  // can't read zips, and treats "C:" as a remote host.
  const sysTar = join(process.env.SystemRoot ?? "C:\\Windows", "System32", "tar.exe");
  const tar = process.platform === "win32" && existsSync(sysTar) ? sysTar : "tar";
  try { execFileSync(tar, ["-xf", pack, "-C", dest], { stdio: "ignore" }); } catch { return []; }
  const shots: string[] = [];
  const walk = (d: string) => {
    for (const e of readdirSync(d, { withFileTypes: true })) {
      const p = join(d, e.name);
      if (e.isDirectory()) walk(p);
      else if (/^screenshot\.(jpg|png)$/.test(e.name)) shots.push(p);
    }
  };
  walk(dest);
  const ord = (p: string) => Number(p.match(/steps[\\/](\d+)-/)?.[1] ?? 0);
  return shots.sort((a, b) => ord(a) - ord(b));
}

export function readKaneResult(dir: string): KaneResult {
  const p = join(dir, "kane.ndjson");
  return resultFromEvents(parseNdjson(readFileSync(p, "utf8")), p, null);
}

/** The non-GET requests a run sent (method + path), read from the HAR inside the Evidence Pack.
 *  Returns undefined if there is no pack or no HAR, so "nothing sent" is never guessed. */
export function changesSent(pack: string | undefined, dest: string): string[] | undefined {
  if (!pack || !existsSync(pack)) return undefined;
  mkdirSync(dest, { recursive: true });
  const sysTar = join(process.env.SystemRoot ?? "C:\Windows", "System32", "tar.exe");
  const tar = process.platform === "win32" && existsSync(sysTar) ? sysTar : "tar";
  try { execFileSync(tar, ["-xf", pack, "-C", dest], { stdio: "ignore" }); } catch { return undefined; }
  const hars: string[] = [];
  const walk = (d: string) => { for (const e of readdirSync(d, { withFileTypes: true })) { const p = join(d, e.name); if (e.isDirectory()) walk(p); else if (e.name.endsWith(".har")) hars.push(p); } };
  walk(dest);
  if (!hars.length) return undefined;
  const out: string[] = [];
  for (const h of hars) {
    try {
      for (const e of JSON.parse(readFileSync(h, "utf8")).log.entries) {
        const m = e.request.method;
        if (m !== "GET" && m !== "HEAD" && m !== "OPTIONS") out.push(`${m} ${new URL(e.request.url).pathname} ${e.response.status}`);
      }
    } catch {}
  }
  return out;
}
