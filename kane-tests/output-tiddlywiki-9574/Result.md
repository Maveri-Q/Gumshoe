---
test: ../tiddlywiki-9574_test.md
status: passed
started: 2026-11-25T21:59:15.852Z
duration_s: 92
session_id: 7477c60e-c755-4505-b554-08ae089fcf04
---

# While editing a tiddler, pressing Ctrl+Enter with the cursor in the tag name input saves the tiddler and closes its editor. — Result

## Get the app ready ✓ passed (16.86s)
md5: 89aacf8a2d98479dc1247470c2a4e557
Wait until the page has fully loaded and the tiddler titled HelloThere is visible. In the row of buttons at the top right of the HelloThere tiddler, click the edit button (a pencil icon). Wait 2 seconds until the tiddler changes into an editor with a title box at the top and a large text box. In that editor, find the small input below the title box that shows the grey placeholder text 'tag name', and click once inside it so the cursor is there. Do not type anything. If a list of tags drops down below the input, leave it open and do not click anything else.
Verify that this is true: The HelloThere tiddler is open in an editor, with a title box, a tag input with the placeholder text 'tag name', and a large text box.

## Check the sentence ✓ passed (67.8s)
md5: 9bc24790da4ea8fd61228709be79a7ca
With the cursor still in the 'tag name' input, press Ctrl+Enter once on the keyboard (hold Control and press Enter). Do not click anything else. Wait 2 seconds.
Verify that this is true: The HelloThere tiddler is no longer being edited: HelloThere is shown as a plain heading above its normal reading text, and no title box or tag input with the placeholder text 'tag name' is visible in it.
