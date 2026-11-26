# Launch posts (X only)

The rule is at least two public posts. We use X for all of them. You post them yourself, from your own account.

Before posting:
1. Make the GitHub repo public. Post 1's reply links to it.
2. Check the hackathon page for the official hashtag and the TestMu AI account to tag. Put them where it says [tag].
3. Attach the demo video to post 1. For posts 2 to 4, a screenshot of the page works.

Plan for today (the deadline is 18:29 UTC):
- Post 1 first, with the video. Pin it to your profile.
- Posts 2, 3 and 4 a couple of hours apart, each as a new post (not replies), so they count as separate posts.
- Reply to everyone who comments. Engagement earns extra points.

Each post is under 280 characters. X counts a link as 23.

---

## Post 1: the launch (attach the demo video)

Paste a GitHub bug report. Gumshoe finds the commit that broke it.

Kane CLI checks the bug in a real browser on older and older versions until one commit is left. Then a coding agent fixes it.

6 of 6 matched the maintainers.

https://gumshoe-puce.vercel.app [tag]

**Reply to your own post 1:**

Real open-source bugs from TiddlyWiki and Excalidraw. None planted. Every run is recorded, and `npm run replay` checks them all again.

Code: https://github.com/Maveri-Q/Gumshoe

---

## Post 2: the case nobody had settled

A TiddlyWiki bug: Ctrl+Enter stopped saving in the tags box.

Nobody in the report settled which change caused it. The one suspect named didn't hold up.

Gumshoe searched 161 commits and named 3889a2a0. A plain script checked it: works just before, broken from there.

[tag]

---

## Post 3: can you trust it

Can you trust an AI test to find the commit that broke something?

Gumshoe only counts a result when Kane and a second reader agree. If not, the commit is skipped, never guessed.

We ran one check 10 times on each side of the guilty commit. Same answer 20 of 20 times.

[tag]

---

## Post 4: cheap mode

Kane does the clicks once and saves a recording. Every older version replays it, and Kane's AI only looks at the end.

Same search, same answer:
531 credits down to 46, plus 42 once to record.
59 minutes down to 20.

https://gumshoe-puce.vercel.app [tag]
