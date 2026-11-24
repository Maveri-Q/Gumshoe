// A small build config for Excalidraw, used for every commit in the bisect.
// It keeps the app's own source aliases and leaves out things that don't affect
// behaviour on the page (offline mode, sitemap, lint overlay, analytics).
import { existsSync } from "node:fs"; import path from "node:path"; import { createRequire } from "node:module";
const root = path.resolve(import.meta.dirname, "../excalidraw"); // copied next to the checkout when used
const req = createRequire(path.join(root, "x.js"));
const { defineConfig } = req("vite"); const react = req("@vitejs/plugin-react"); const svgr = req("vite-plugin-svgr"); const { ViteEjsPlugin } = req("vite-plugin-ejs");
const pk = p => path.join(root, "packages", p);
const alias = [{ find: new RegExp("^excalidraw-app/"), replacement: path.join(root, "excalidraw-app") + "/" }];
for (const n of ["common", "element", "math", "utils", "fractional-indexing", "laser-pointer"]) {
  if (!existsSync(pk(`${n}/src/index.ts`))) continue; // not part of the repo yet at this commit
  alias.push({ find: new RegExp(`^@excalidraw/${n}$`), replacement: pk(`${n}/src/index.ts`) });
  alias.push({ find: new RegExp(`^@excalidraw/${n}/(.*?)`), replacement: pk(`${n}/src/$1`) });
}
alias.push({ find: /^@excalidraw\/excalidraw$/, replacement: pk("excalidraw/index.tsx") }, { find: /^@excalidraw\/excalidraw\/(.*?)/, replacement: pk("excalidraw/$1") });
export default defineConfig({
  root: path.join(root, "excalidraw-app"), envDir: root, publicDir: path.join(root, "public"), resolve: { alias },
  build: { outDir: path.resolve(import.meta.dirname, "../dist"), emptyOutDir: true, minify: false, assetsInlineLimit: 0, reportCompressedSize: false },
  plugins: [{ name: "no-pwa", resolveId: id => (id === "virtual:pwa-register" ? "VIRT:pwa" : null), load: id => (id === "VIRT:pwa" ? "export const registerSW = () => () => {}" : null) }, req("./scripts/woff2/woff2-vite-plugins.js").woff2BrowserPlugin(), (react.default ?? react)(), (svgr.default ?? svgr)(), ViteEjsPlugin()],
});
