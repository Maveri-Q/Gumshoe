// Plain script, no Kane and no AI: does Ctrl+Enter in the tag name box save the tiddler?
//   node validation/9574-script/check.mjs <commit> ...
// Uses the TiddlyWiki copy in clones/hunt-tiddlywiki-9574 and headless Chrome over its debug port.
import { execFileSync } from "node:child_process";
import { resolve } from "node:path";
import { mkdirSync, rmSync, writeFileSync } from "node:fs";
import { launchRole, closeRole } from "../../tools/browsers.ts";
import { serve } from "../../tools/serve.ts";
const src = "clones/hunt-tiddlywiki-9574", dist = "dist/script-9574", port = 4399, results = [];
const wait = ms => new Promise(r => setTimeout(r, ms));
let dbg = 10990;
for (const sha of process.argv.slice(2)) {
  execFileSync("git", ["checkout", "-q", "--force", sha], { cwd: src });
  rmSync(dist, { recursive: true, force: true }); mkdirSync(dist, { recursive: true });
  execFileSync("node", [src + "/tiddlywiki.js", src + "/editions/tw5.com", "--output", process.cwd() + "/" + dist, "--build", "index"], { stdio: "ignore" });
  const server = await serve(resolve(dist), port);
  for (const [what, box] of [["tag name", 'input[placeholder="tag name"]'], ["field name", 'input[placeholder="field name"]']]) {
    const br = await launchRole("script-" + Date.now(), ++dbg, ".kane-profiles");
    const t = (await (await fetch(br.endpoint + "/json")).json()).find(x => x.type === "page");
    const ws = new WebSocket(t.webSocketDebuggerUrl); await new Promise(r => (ws.onopen = r));
    let id = 0; const waits = {};
    ws.onmessage = m => { const j = JSON.parse(m.data); waits[j.id]?.(j.result); };
    const send = (method, params = {}) => new Promise(r => { waits[++id] = r; ws.send(JSON.stringify({ id, method, params })); });
    const js = async e => (await send("Runtime.evaluate", { expression: e, returnByValue: true, userGesture: true })).result?.value;
    await send("Page.navigate", { url: `http://127.0.0.1:${port}/#HelloThere` }); await wait(6000);
    await js(`document.querySelector('[data-tiddler-title="HelloThere"] button[aria-label="edit"], [data-tiddler-title="HelloThere"] .tc-tiddler-controls button[title*="Edit"]')?.click()`); await wait(2500);
    const open = await js(`document.querySelectorAll(".tc-tiddler-edit-frame").length`);
    await js(`document.querySelector('${box}')?.focus()`); await wait(800);
    const focused = await js(`document.activeElement?.placeholder`);
    const key = { key: "Enter", code: "Enter", windowsVirtualKeyCode: 13, modifiers: 2 };
    await send("Input.dispatchKeyEvent", { type: "rawKeyDown", ...key }); await send("Input.dispatchKeyEvent", { type: "keyUp", ...key }); await wait(2500);
    const still = await js(`document.querySelectorAll(".tc-tiddler-edit-frame").length`);
    const r = { commit: sha.slice(0, 8), box: what, editorOpened: open, focused, editorsAfter: still, result: open !== 1 || focused !== what ? "could not test" : still ? "BROKEN" : "works" };
    results.push(r); console.log(JSON.stringify(r));
    ws.close(); closeRole(br, true); await wait(1500);
  }
  server.close();
}
writeFileSync("validation/9574-script/result.json", JSON.stringify(results, null, 1));
