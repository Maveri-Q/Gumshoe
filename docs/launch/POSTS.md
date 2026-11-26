# Launch posts

You post these yourself, from your own accounts. The hackathon needs at least two public posts.

Before posting:
1. Make the GitHub repo public. The posts link to it, and judges need it.
2. Check the hackathon page for the official hashtag and the TestMu AI account to tag. Add them where it says [tag].
3. Attach the demo video or a short screen recording of the page. Posts with a video get far more views.

Best order: X and LinkedIn first (today), then Show HN, then Reddit.

---

## X

Paste a GitHub bug report. Gumshoe finds the commit that broke it.

Kane CLI checks the bug in a real browser on older and older versions until one commit is left. Then a coding agent fixes it.

Real bugs, no planted ones. 6 of 6 matched the maintainers.

https://gumshoe-puce.vercel.app [tag]

(Reply to your own post with the second part:)

The one I like most: TiddlyWiki 9574. Nobody in the report agreed on a cause. Gumshoe named a commit. A plain script then checked it: works just before, broken from there.

Repo: https://github.com/Maveri-Q/Gumshoe

---

## LinkedIn

I built Gumshoe for the KaneCLI hackathon by TestMu AI. [tag]

The problem: a feature that used to work breaks. Somewhere in hundreds of commits is the one that broke it. Finding it by hand takes hours.

Gumshoe starts from the bug report. No test needed.
1. It turns the report into one plain sentence, like "Ctrl+Enter in the tags box saves the tiddler".
2. Kane CLI checks that sentence in a real browser, on older and older versions of the app.
3. git bisect halves the suspects each time, until one commit is left.
4. A coding agent fixes it, and the sentence is saved as a Kane test.

What happened on real open-source bugs:
- 6 of 6 times it named the same commit as the maintainers.
- On one TiddlyWiki bug, the people in the report hadn't settled on a cause. Gumshoe named a commit, and a plain script agreed.
- Run 10 times on each side of that commit, the check gave the same answer 20 of 20 times.

What it can't do yet: old versions must still build, and it costs Kane credits.

Try it: https://gumshoe-puce.vercel.app
Code: https://github.com/Maveri-Q/Gumshoe

---

## Hacker News (Show HN)

Title: Show HN: Gumshoe: paste a bug report, get the commit that broke it

Link: https://github.com/Maveri-Q/Gumshoe

First comment (post it yourself right after):

I built this for a hackathon around Kane CLI, a browser testing agent. Gumshoe reads a GitHub issue, writes one sentence about what should happen, and uses it as the test for git bisect. Each commit is built, opened in Chrome, and checked by Kane plus a second reader that only sees the screenshot. If they disagree, the commit is skipped, never guessed.

I ran it on 6 real reports from TiddlyWiki and Excalidraw. Where the maintainers named a commit, it found the same one 6 of 6 times. It's slow (20 to 150 minutes per search) and costs credits, and the README lists where it went wrong. `npm run replay` checks every recorded verdict without a Kane account.

Live page: https://gumshoe-puce.vercel.app

---

## Reddit (r/SideProject)

Title: I made a tool that reads a bug report and finds the commit that broke it

Body: use the LinkedIn text. Add a screen recording of the page. Check the subreddit's rules on self-promotion before posting.
