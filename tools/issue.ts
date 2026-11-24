// Reads a GitHub issue (title and first post only, as the reporter wrote it). Comments are left
// out on purpose: they often name the guilty commit.
import { writeFileSync, existsSync, readFileSync } from "node:fs";
export interface Issue { url: string; repo: string; number: number; title: string; body: string; createdAt: string }

export function parseIssueUrl(url: string) {
  const m = url.match(/^https:\/\/github\.com\/([\w.-]+\/[\w.-]+)\/(?:issues|pull)\/(\d+)/);
  if (!m) throw new Error("Give me a GitHub issue link, like https://github.com/owner/repo/issues/123");
  return { repo: m[1], number: Number(m[2]) };
}
export async function readIssue(url: string, saveTo: string): Promise<Issue> {
  if (existsSync(saveTo)) return JSON.parse(readFileSync(saveTo, "utf8"));
  const { repo, number } = parseIssueUrl(url);
  const r = await fetch(`https://api.github.com/repos/${repo}/issues/${number}`, { headers: { "user-agent": "gumshoe-cli" } });
  if (!r.ok) throw new Error(`GitHub answered ${r.status} for ${url}`);
  const j: any = await r.json();
  const issue = { url: `https://github.com/${repo}/issues/${number}`, repo, number, title: j.title, body: (j.body ?? "").replace(/<!--[\s\S]*?-->/g, ""), createdAt: j.created_at };
  writeFileSync(saveTo, JSON.stringify(issue, null, 2));
  return issue;
}
