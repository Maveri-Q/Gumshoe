# Phase 1 result: GO rule met, 2 bugs out of 2

| | Bug 1: menu won't close | Bug 2: colour code with transparency |
|---|---|---|
| App | Excalidraw | Excalidraw |
| Report | [PR #12053](https://github.com/excalidraw/excalidraw/pull/12053) (no issue found) | [Issue #10772](https://github.com/excalidraw/excalidraw/issues/10772) |
| Maintainers blame | #11974, e1bb9ff8 | #10578, 63e11482 |
| Gumshoe landed on | e1bb9ff8 (same) | 63e11482 (same) |
| Commits judged | 7 | 6 |
| Kane tries | 14 | 13 |
| Refused tries | 0 | 1 (Kane contradicted itself) |
| Wrong final verdicts | 0 | 0 |
| Bisect credits | 269.1 | 278.8 |
| Bisect time | 27 min | 27 min |
| Final calibration | 86.7 credits, 8 min | 89.7 credits, 8 min |

Real cost of the whole phase: 1,019.6 credits by balance, including failed calibrations.

## Kane got things wrong
- Calibration 1: 3 of 3 answers on the good commit were wrong (it said broken; Kane's own pictures show it working).
- Fix: a second Kane run that only looks, judging two opposite statements. After that: 1 self-contradiction, refused.
- Every verdict needs two Kane tries that agree with each other and with a screen check done by plain code.

## Limits
- The answers were known beforehand. The good and bad ends were picked knowing the guilty commit lay between them.
  A test on a bug with no known answer has not been done.
- The sentence was expanded by hand into steps, and the plain-code screen check was written by hand for each bug.
  That screen check alone could have found both commits. Kane did the clicking and the first judgement.
- For bug 1 the report is the fix PR itself. No separate issue was found.
- Both bugs are in one app. Old builds used one set of packages for the whole range, not each commit's own.
- For bug 2, a check of the steps was needed once: my first wording contradicted itself.
- Git ranges: bug 1 cd514d72..f1a79b73, bug 2 8d18078f..a70417f2.
