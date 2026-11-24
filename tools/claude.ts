// Runs Claude Code in print mode for three jobs: write the check from an issue, act as the second
// reader of a saved screen, and fix the bug. Each call starts in its own folder, so it can't see
// Gumshoe's files, the git history or the answer.
import { spawn } from "node:child_process";
import { mkdtempSync, rmSync, copyFileSync, existsSync } from "node:fs";
import { join, basename } from "node:path";
import { tmpdir, homedir } from "node:os";

export function claudeCommand(): string {
  const own = join(homedir(), ".local", "bin", process.platform === "win32" ? "claude.exe" : "claude");
  return process.env.CLAUDE_CLI ?? (existsSync(own) ? own : "claude");
}

export async function askClaude(prompt: string, o: { files?: string[]; model?: string; timeoutS?: number; cwd?: string; tools?: string } = {}): Promise<string> {
  const cwd = o.cwd ?? mkdtempSync(join(tmpdir(), "gumshoe-"));
  for (const f of o.files ?? []) copyFileSync(f, join(cwd, basename(f)));
  const tools = o.tools ?? (o.files?.length ? "Read" : "");
  const args = ["-p", "--output-format", "text", "--model", o.model ?? "opus", "--setting-sources", "", "--strict-mcp-config",
    "--tools", tools, ...(tools ? ["--allowedTools", tools] : [])];
  const child = spawn(claudeCommand(), args, { cwd, windowsHide: true });
  child.stdin.end(prompt);
  let out = "", err = "";
  child.stdout.on("data", d => (out += d)); child.stderr.on("data", d => (err += d));
  const timer = setTimeout(() => child.kill(), (o.timeoutS ?? 240) * 1000);
  const code = await new Promise(r => { child.on("close", r); child.on("error", () => r(-1)); });
  clearTimeout(timer);
  if (!o.cwd) try { rmSync(cwd, { recursive: true, force: true }); } catch {}
  if (code !== 0) throw new Error(`Claude exited ${code}: ${(err || out).slice(0, 400)}`);
  return out;
}

/** The last {...} block in the text. */
export function lastJson(s: string): any {
  const end = s.lastIndexOf("}");
  for (let i = s.indexOf("{"); i >= 0 && i < end; i = s.indexOf("{", i + 1)) { try { return JSON.parse(s.slice(i, end + 1)); } catch {} }
  throw new Error("no JSON in the answer: " + s.slice(0, 200));
}

/** A second reader judges the saved screen. It sees one picture and two statements, nothing else.
 *  true = broken, false = working, undefined = it would not say. */
export function readerAnswer(text: string): boolean | undefined {
  try { const j = lastJson(text); return j.a === true && j.b === false ? true : j.a === false && j.b === true ? false : undefined; } catch { return undefined; }
}
export async function secondReader(png: string, broken: string, working: string): Promise<boolean | undefined> {
  const prompt = `Read the picture ${basename(png)} in this folder. It is a screenshot of a web page.\nJudge each statement by the picture only.\nA: ${broken}\nB: ${working}\nIf you can't tell, use null. Answer only with JSON: {"a": true|false|null, "b": true|false|null}`;
  for (let i = 0; i < 2; i++) {
    try { return readerAnswer(await askClaude(prompt, { files: [png], model: "sonnet", timeoutS: 120 })); }
    catch (e) { if (i) console.log("  second reader failed: " + (e as Error).message); }
  }
  return undefined;
}
