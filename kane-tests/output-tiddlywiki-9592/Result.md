---
test: ../tiddlywiki-9592_test.md
status: failed
started: 2026-11-25T18:42:09.522Z
duration_s: 152
session_id: 7aa7cbf1-5a31-4cda-b99c-9a88b4fa9f67
---

# Clicking an HTML anchor link that points to a spot inside the same tiddler keeps that tiddler on screen and does not open another tiddler. — Result

## Get the app ready ✓ passed (7.89s)
md5: c8753d1531e2ada78c9d8ef6e387a33a
In the sidebar on the right side of the page, click the plus icon button (its tooltip says 'Create a new tiddler'). An edit form opens with a title box that says 'New Tiddler'. Leave the title as it is. Click inside the large empty text area below the title and tags and type exactly this on one line, keeping both # characters in a row in the href and the single # in the id: <a href="##my-spot">Jump to spot</a> <span id="#my-spot">Landing place</span>
Then click the tick (checkmark) button at the top right of that edit form (its tooltip says 'Confirm changes to this tiddler'). Scroll to the tiddler titled 'New Tiddler' if it is not in view. Do not click the link 'Jump to spot' yet.
Verify that this is true: A tiddler titled 'New Tiddler' is shown with the link 'Jump to spot' and the text 'Landing place' in its body.

## Check the sentence ✗ failed (80.1s)
md5: 339c2381197f351f45280ee24dca31b5
Reason: Final verification failed: "The text 'Landing place' is shown in the main area, and no tiddler whose title contains 'my-spot' and no missing tiddler message is shown." — bug verdict: Jump to spot opens a missing #my-spot tiddler [application_issue/navigation_defect, confidence 0.97]
In the body of the tiddler titled 'New Tiddler', click the link 'Jump to spot' once. Wait 2 seconds. Do not scroll or click anything else.
Verify that this is true: The text 'Landing place' is shown in the main area, and no tiddler whose title contains 'my-spot' and no missing tiddler message is shown.
