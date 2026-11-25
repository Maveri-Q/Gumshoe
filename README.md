# Gumshoe

**Live:** https://gumshoe-puce.vercel.app

**Which commit broke it? Give Gumshoe a bug report and it finds out.**

Gumshoe turns a GitHub issue into one plain sentence. [Kane CLI](https://www.npmjs.com/package/@testmuai/kane-cli) checks that sentence in a real browser, on older and older versions of the app, driven by `git bisect`. One commit is left at the end. A coding agent fixes it, Kane proves the fix with the same sentence, and the sentence is saved as a Kane test.

## For judges

No Kane account, no Claude, no network needed:

```bash
npm run replay
```

This reads Kane's own recorded output for every commit again, works out every verdict with the same code the live run used, walks the bisects again, and rebuilds the report page. It stops with an error if anything differs from what was recorded. One thing is taken as recorded: the second reader's answer about each saved screen. Needs Node 22.18 or newer. The pictures are already in `site/img`.

```bash
npm test
```

To run a live hunt you need Kane (`kane-cli login`), Claude Code, git and Chrome. It costs about 400 to 1,000 Kane credits and 1 to 2 hours:

```bash
git clone --filter=blob:none https://github.com/TiddlyWiki/TiddlyWiki5.git clones/tiddlywiki
npm run hunt -- https://github.com/TiddlyWiki/TiddlyWiki5/issues/9592 --app tiddlywiki
npm run fix -- tiddlywiki-9592
```

## The best one: TiddlyWiki issue 9592

- The report was written on 18 Jan 2026. The maintainers named the cause on 26 Jan, 8 days later.
- Gumshoe got only the title and the first post. Comments were left out, because they can hold the answer.
- It wrote the sentence: "Clicking an HTML anchor link that points to a spot inside the same tiddler keeps that tiddler on screen and does not open another tiddler."
- 168 commits were searched. It ended on `48eeb460`, "Deprecate and simplify some utility functions (#9251)".
- We had not looked up the answer. Then we did: the maintainers' fix, [#9622](https://github.com/TiddlyWiki/TiddlyWiki5/pull/9622), blames #9251.

- Claude Code fixed it on the first attempt, without seeing the maintainers' fix. Kane checked the same sentence twice: it works.
- The saved test, [kane-tests/tiddlywiki-9592_test.md](kane-tests/tiddlywiki-9592_test.md), passes on the fix and fails on the broken version.
- TiddlyWiki's own tests give the same result before and after the fix: 72 of 1,404 fail here on Windows both times.

## Scoreboard

| Report | Gumshoe says | Maintainers say | Commits searched | Tries (refused) | Time | Credits |
|---|---|---|---|---|---|---|
| TiddlyWiki 9592 | 48eeb460 | same | 168 | 22 (3) | 83 min | 790 |
| TiddlyWiki 9678 | c305eb01 | same, through a linked report | 234 | 27 (4) | 93 min | 972 |
| TiddlyWiki 9760 | c305eb01 | same | 262 | 31 (10) | 146 min | 1,526 |
| Excalidraw 10772 | 63e11482 | same | 48 | 19 (2) | 65 min | 664 |
| Excalidraw 10772, by hand | 63e11482 | same | 56 | 17 (1) | 35 min | 369 |
| Excalidraw 12053, by hand | e1bb9ff8 | same | 70 | 18 (0) | 35 min | 356 |

6 hunts, 5 reports, 4 different guilty commits. Only 9592 was run without us having looked for the answer first. We knew the answer for 9760 and 10772, and a likely one for 9678. Gumshoe itself was not told any of them, except that 10772's own title names #10578.

Time counts the commits in the final result. Our real spend on the whole project was about 6,460 credits, including failed drafts, calibrations and tries cut off by sleep.

More on the report page (`site/index.html`), or run `npm run replay`.

## How it works

1. **Read the issue** ([tools/issue.ts](tools/issue.ts)). Title and first post only.
2. **Write the check** ([tools/write-check.ts](tools/write-check.ts)). Claude writes the sentence, the steps, and two opposite statements about the end screen. It can't see the git history.
3. **Show the bug** ([tools/hunt.ts](tools/hunt.ts)). Kane runs the check on the version the reporter used. If the bug doesn't show, Claude gets Kane's notes and tries again, three drafts at most. After that the check is frozen.
4. **Find a version that works.** The one the report names, or the releases before it.
5. **Bisect.** The real `git bisect run`. Each commit is built, served on this computer, and judged.
6. **Fix it** ([tools/fix.ts](tools/fix.ts)). Claude Code gets the source without its git history. Three attempts at most, then a human. Gumshoe compares hashes to make sure the agent did not touch the check.
7. **Keep it.** The sentence becomes a Kane test file in [kane-tests](kane-tests), run once on the fix and once on the broken version.

### Why Kane
A bug hunt goes back through months of code. Tests that look for elements by code name break along the way. A sentence still means the same thing on an old version.

### How a verdict is made
All the decisions are plain code in [tools/verdict.ts](tools/verdict.ts).
- One Kane run does the steps and says if the app was ready.
- A second Kane run only looks at the page (`--analyzer-only --condition`). It judges "broken" and "working". If it says both or neither, the try is refused.
- A second reader (Claude) sees the saved screenshot and nothing else. If it disagrees, the try is refused.
- Two tries must agree. Three tries at most. If they don't, the commit is skipped, never guessed.
- A crash, a lost connection or a failed build can't count as "broken".

## Where it went wrong
- **Kane's answer was wrong 3 times out of 3** on a good commit in our first calibration. Its own screenshots showed the right thing. That is why a separate look-only run exists. ([validation/phase1](validation/phase1))
- **Kane contradicted itself** many times. Those tries are in the recordings, refused.
- **First drafts failed, and we helped.** In 9592 and 9678 the first draft didn't give a clear result on the reported version. Claude rewrote the check. Between the drafts we also changed how Gumshoe asks Kane "is the app ready", because Kane had stored the words "yes or no" as its answer. That was before either bisect began.
- **We changed Gumshoe while hunts were running.** We added resuming after sleep, skipping lost connections, looking for older versions by weeks (10772 needed it), and reading git's newer wording (9760 and 9678 ended on their commit before this, but Gumshoe missed the line). The check and the rules for a verdict stayed the same during each bisect.
- **The short app notes in `apps` were written by us after we had read the reports.** They say things like where the control panel is. They help the check writer, and they don't name a cause.
- **The computer slept during three hunts.** Tries that were cut off were set aside (`runs/*/cut-off`) and those commits were judged again, with the same frozen check. Finished verdicts were kept. Because of that, real credits spent are higher than the scoreboard shows.
- The steps in the first two hunts were written by hand, by us. The scoreboard says which.
- **9760 was the hardest:** 10 of 31 tries were refused and three commits were skipped (one didn't build). It still ended on one commit.

## What it can't do
- Old versions must still build. If one doesn't, it is skipped.
- The report must say clearly what should happen.
- Kane can misread, and so can the second reader. If both misread a screen the same way twice, the answer is wrong.
- It names where the behaviour changed. That is not always the real cause.
- A handful of bugs in two apps is a small sample. Two of the TiddlyWiki reports come from the same commit.
- Each app needs a short build file ([apps](apps)), written once by a person.
- The fix is made on the version in the report, because these bugs are already fixed in the newest one.
- It is slow and costs credits. If a script can check the bug, plain `git bisect` is faster. On 9760 a maintainer did that in about 80 minutes.

## Prior work
Kane wrapper code ([tools/kane.ts](tools/kane.ts), [tools/browsers.ts](tools/browsers.ts)) was first written for our earlier hackathon projects, Fessup and Screenplay. The rest was written for Gumshoe.

MIT licence.
