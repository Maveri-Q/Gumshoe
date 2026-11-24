import { test } from "node:test";
import assert from "node:assert/strict";
import { tryVerdict, combine, bisectCode } from "../tools/verdict.ts";

test("a try only counts when the app was ready", () => assert.equal(tryVerdict({ ready: "no", broken: "no", witness: false }).verdict, "unsure"));
test("yes and no map to bad and good", () => {
  assert.equal(tryVerdict({ ready: "Yes.", broken: "yes", witness: true }).verdict, "bad");
  assert.equal(tryVerdict({ ready: "yes", broken: "no", witness: false }).verdict, "good");
});
test("a saved screen that disagrees stops the try counting", () => {
  assert.equal(tryVerdict({ ready: "yes", broken: "no", witness: true }).verdict, "unsure");
  assert.equal(tryVerdict({ ready: "yes", broken: "yes", witness: false }).verdict, "unsure");
});
test("no answer or no saved screen is unsure", () => {
  assert.equal(tryVerdict({ ready: "yes", witness: true }).verdict, "unsure");
  assert.equal(tryVerdict({ ready: "yes", broken: "no" }).verdict, "unsure");
});
test("two tries must agree", () => {
  assert.equal(combine(["good"]), undefined);
  assert.equal(combine(["good", "bad"]), undefined);
  assert.equal(combine(["good", "bad", "bad"]), "bad");
  assert.equal(combine(["unsure", "unsure", "good"]), "unsure");
});
test("git bisect exit codes", () => assert.deepEqual([bisectCode("good"), bisectCode("bad"), bisectCode("unsure")], [0, 1, 125]));
