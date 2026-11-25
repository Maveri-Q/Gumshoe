#!/usr/bin/env node
// gumshoe <issue link> --app <name> | gumshoe fix <run id> | gumshoe replay
import { spawnSync } from "node:child_process";
import { join, resolve } from "node:path";
const root = resolve(import.meta.dirname, ".."), [first, ...rest] = process.argv.slice(2);
if (!first) { console.log("gumshoe <issue link> --app tiddlywiki\ngumshoe fix <run id>\ngumshoe replay"); process.exit(0); }
const [tool, args] = first === "fix" || first === "replay" ? [first, rest] : ["hunt", [first, ...rest]];
process.exit(spawnSync(process.execPath, [join(root, "tools", tool + ".ts"), ...args], { cwd: root, stdio: "inherit" }).status ?? 1);
