# Launch posts (X only)

These follow the hackathon's own templates. You post them yourself, from your own account.
Tags from the hackathon page: @kane_cli, @testmuai, #KaneCLIHackathon, #KaneCLI.

Today's plan (the deadline is 18:29 UTC):
1. **Now:** the kickoff post. It needs nothing attached.
2. **When the video is ready:** make the repo public, then post the launch thread. Attach the video to post 1.
   A free X account takes videos up to 2 minutes 20 seconds, so attach the short clip there. The full demo goes on YouTube.
3. **Then submit the form.** Paste the links to the kickoff post and to post 1 of the thread under "Launch buzz".
   To copy a link on X: tap the share icon on the post, then "Copy link".
4. Reply to people who comment. Each post and reply counts.

X shows a character counter while you type. If a post goes over 280, tell me and I'll shorten it.

---

## Kickoff post (one post, no thread)

I built Gumshoe this week for the KaneCLI Online Hackathon.

Claude Code writes the code. Kane CLI checks it in a real browser, so the agent sees its own failures.

Launch thread with the demo later today. Tested with @kane_cli from @testmuai.

#KaneCLIHackathon #KaneCLI

---

## Launch thread (6 posts, links only in the first and last)

To make a thread on X: write post 1, tap the + button to add the next post, and so on. Then post them all at once.

**1/** (attach the clip)

We built Gumshoe: paste a bug report, get the commit that broke it.

Built with Claude Code, tested with @kane_cli from @testmuai. Demo and code:
https://gumshoe-puce.vercel.app

#KaneCLIHackathon #KaneCLI

**2/**

The problem: a feature that worked last month breaks. Somewhere in hundreds of commits is the one that did it. Finding it by hand means building and clicking through old versions for hours.

**3/**

The Kane CLI moment: we gave it one sentence from a TiddlyWiki bug report. Ctrl+Enter in the tags box saves the tiddler. Kane said works or broken on old versions until one commit of 161 was left. Claude Code fixed it. Kane ran the same sentence. It passed.

**4/**

The build: Claude Code wrote Gumshoe, the test sentences and the fixes. One tradeoff: it's slow. A search takes 20 to 150 minutes, because every old version is built and opened in a real browser.

**5/**

Where it went wrong: in our first test, Kane's answer was wrong 3 times out of 3 on a version that worked, though its screenshots were right. So now a separate Kane look and a second reader must agree. On a repeat test, the check gave the same answer 20 of 20 times.

**6/**

Built by [your X handle]. Thanks @kane_cli and @testmuai for the week. Repo: https://github.com/Maveri-Q/Gumshoe
