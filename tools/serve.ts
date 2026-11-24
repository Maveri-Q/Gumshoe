// Serves a built app on this machine only.
import { createServer, type Server } from "node:http";
import { readFileSync, existsSync, statSync } from "node:fs";
import { join, extname, sep } from "node:path";
const types: Record<string, string> = {
  ".html": "text/html", ".js": "text/javascript", ".mjs": "text/javascript", ".css": "text/css", ".json": "application/json",
  ".svg": "image/svg+xml", ".png": "image/png", ".woff2": "font/woff2", ".wasm": "application/wasm",
};
export async function serve(dist: string, port: number): Promise<Server> {
  const server = createServer((q, r) => {
    let f = join(dist, decodeURIComponent(new URL(q.url!, "http://x").pathname));
    if (!f.startsWith(dist + sep) || !existsSync(f) || statSync(f).isDirectory()) f = join(dist, "index.html");
    r.writeHead(200, { "content-type": types[extname(f)] ?? "application/octet-stream", "cache-control": "no-store" });
    r.end(readFileSync(f));
  });
  await new Promise<void>((r, x) => { server.once("error", x); server.listen(port, "127.0.0.1", () => r()); });
  return server;
}
