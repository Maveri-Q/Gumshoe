// One Chrome per role, each with its own profile, so each stays logged in as that role.
// Kane drives each one through --cdp-endpoint (Chrome DevTools Protocol), like Fessup.
// Plain code also uses CDP to take a screenshot and read the page text of every role
// after every line, without reloading, so we can see what each person had on screen.
import { spawn, type ChildProcess } from "node:child_process";
import { mkdirSync, rmSync, existsSync, writeFileSync } from "node:fs";
import { join } from "node:path";

export interface RoleBrowser {
  role: string;
  port: number;
  endpoint: string;
  profile: string;
  proc: ChildProcess;
}

function findChrome(): string {
  if (process.env.CHROME_PATH) return process.env.CHROME_PATH;
  const c = [`${process.env.LOCALAPPDATA}\\Google\\Chrome\\Application\\chrome.exe`,
    `${process.env.PROGRAMFILES}\\Google\\Chrome\\Application\\chrome.exe`,
    `${process.env["PROGRAMFILES(X86)"]}\\Google\\Chrome\\Application\\chrome.exe`,
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "/usr/bin/google-chrome"];
  const hit = c.find(p => existsSync(p));
  if (!hit) throw new Error("Chrome not found. Set CHROME_PATH.");
  return hit;
}

export async function launchRole(role: string, port: number, profileRoot: string, size = "1440,1000"): Promise<RoleBrowser> {
  const profile = join(profileRoot, role.toLowerCase());
  mkdirSync(profile, { recursive: true });
  const proc = spawn(findChrome(), ["--headless=new", `--remote-debugging-port=${port}`, `--user-data-dir=${profile}`,
    "--no-first-run", "--no-default-browser-check", `--window-size=${size}`, "about:blank"], { stdio: "ignore" });
  const endpoint = `http://127.0.0.1:${port}`;
  for (let i = 0; i < 75; i++) {
    try { await (await fetch(`${endpoint}/json/version`)).json(); return { role, port, endpoint, profile, proc }; }
    catch { await new Promise(r => setTimeout(r, 200)); }
  }
  proc.kill();
  throw new Error(`Chrome for ${role} didn't start.`);
}

export function closeRole(b: RoleBrowser, removeProfile: boolean) {
  try { b.proc.kill(); } catch {}
  if (removeProfile) setTimeout(() => { try { rmSync(b.profile, { recursive: true, force: true }); } catch {} }, 1500);
}

/** Send CDP commands to the role's visible page (the first "page" target). */
async function withPage<T>(b: RoleBrowser, fn: (send: (m: string, p?: object) => Promise<any>) => Promise<T>): Promise<T> {
  const list: any[] = await (await fetch(`${b.endpoint}/json/list`)).json();
  const page = list.find(t => t.type === "page" && !t.url.startsWith("devtools"));
  if (!page) throw new Error(`No page open for ${b.role}`);
  const ws = new WebSocket(page.webSocketDebuggerUrl);
  await new Promise<void>((res, rej) => { ws.onopen = () => res(); ws.onerror = () => rej(new Error("CDP failed")); });
  let id = 0;
  const pending = new Map<number, (v: any) => void>();
  ws.onmessage = ev => { const m = JSON.parse(String(ev.data)); if (m.id && pending.has(m.id)) { pending.get(m.id)!(m.result ?? m.error); pending.delete(m.id); } };
  const send = (method: string, params: object = {}) => new Promise<any>(res => { pending.set(++id, res); ws.send(JSON.stringify({ id, method, params })); });
  try { return await fn(send); } finally { ws.close(); }
}

export async function currentUrl(b: RoleBrowser): Promise<string> {
  const list: any[] = await (await fetch(`${b.endpoint}/json/list`)).json();
  return list.find(t => t.type === "page" && !t.url.startsWith("devtools"))?.url ?? "about:blank";
}

/** Screenshot + visible text of the role's page as it is right now. No reload, no clicks. */
export async function snapshot(b: RoleBrowser, outPng: string): Promise<{ url: string; text: string }> {
  return withPage(b, async send => {
    const shot = await send("Page.captureScreenshot", { format: "png" });
    if (shot?.data) writeFileSync(outPng, Buffer.from(shot.data, "base64"));
    const r = await send("Runtime.evaluate", { expression: "JSON.stringify({url: location.href, text: document.body ? document.body.innerText : ''})", returnByValue: true });
    try { return JSON.parse(r.result.value); } catch { return { url: "", text: "" }; }
  });
}

/** Reload the role's page, like a person pressing refresh. Plain code, not Kane. */
export async function reload(b: RoleBrowser): Promise<void> {
  await withPage(b, async send => { await send("Page.reload", { ignoreCache: true }); });
  await new Promise(r => setTimeout(r, 3000));
}

/** The colour on screen at a point, read from a real screenshot (not from the app's own data). */
export async function readPixel(b: RoleBrowser, [x, y]: [number, number]): Promise<number[] | undefined> {
  return withPage(b, async send => {
    const shot = await send("Page.captureScreenshot", { format: "png", clip: { x, y, width: 1, height: 1, scale: 1 } });
    if (!shot?.data) return undefined;
    const expression = `(async () => { const i = new Image(); i.src = "data:image/png;base64,${shot.data}"; await i.decode(); const c = document.createElement("canvas"); c.width = c.height = 1; const g = c.getContext("2d"); g.drawImage(i, 0, 0); return JSON.stringify([...g.getImageData(0, 0, 1, 1).data.slice(0, 3)]); })()`;
    const r = await send("Runtime.evaluate", { expression, awaitPromise: true, returnByValue: true });
    try { return JSON.parse(r.result.value); } catch { return undefined; }
  });
}
