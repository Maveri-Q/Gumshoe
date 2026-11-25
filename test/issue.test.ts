import { test } from "node:test";
import assert from "node:assert/strict";
import { parseIssueUrl } from "../tools/issue.ts";
import { validCheck } from "../tools/write-check.ts";
import { lastJson, readerAnswer } from "../tools/claude.ts";
import { testFile } from "../tools/kane-test.ts";
const c = { sentence: "s", path: "/", setup: "a", ready: "b", action: "c", broken: "d", working: "e" };
test("reads an issue link", () => assert.deepEqual(parseIssueUrl("https://github.com/a/b.c/issues/12#x"), { repo: "a/b.c", number: 12 }));
test("other links are refused", () => assert.throws(() => parseIssueUrl("https://example.com/a/b/issues/1")));
test("a check must have every part and two different statements", () => {
  assert.equal(validCheck(c), true);
  assert.equal(validCheck({ ...c, broken: "e" }), false);
  assert.equal(validCheck({ ...c, path: "https://x" }), false);
  assert.equal(validCheck({ ...c, setup: "" }), false);
});
test("finds the JSON in an answer", () => assert.deepEqual(lastJson('Here {not json} it is: {"a":{"b":1}}'), { a: { b: 1 } }));
test("the second reader only counts when it is clear", () => {
  assert.equal(readerAnswer('{"a":true,"b":false}'), true);
  assert.equal(readerAnswer('{"a":false,"b":true}'), false);
  for (const s of ['{"a":true,"b":true}', '{"a":null,"b":false}', "no idea"]) assert.equal(readerAnswer(s), undefined);
});
test("the Kane test file holds the sentence and the check", () => assert.match(testFile(c, 1), /^---\nmode: testing\nurl: http:\/\/127\.0\.0\.1:1\/\n[\s\S]*# s\n[\s\S]*Verify that this is true: e\n$/));
