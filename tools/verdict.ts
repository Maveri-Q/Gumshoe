// Plain code decides every verdict. Kane judges two opposite statements, "it is broken"
// and "it works", and plain code checks that they don't contradict each other.
export type Try = { ready?: string; look?: boolean[]; witness?: boolean };
export type Verdict = "good" | "bad" | "unsure";

const yn = (s?: string) => {
  const a = (s ?? "").trim().toLowerCase().replace(/[^a-z]/g, "");
  return a === "yes" || a === "true" ? "yes" : a === "no" || a === "false" ? "no" : undefined;
};

/** One Kane try. It only counts if Kane got the app ready, and only if the screen saved by
 *  plain code says the same thing Kane said. */
export function tryVerdict(t: Try): { verdict: Verdict; why: string } {
  if (yn(t.ready) !== "yes") return { verdict: "unsure", why: "Kane did not get the app ready" };
  if (t.look?.length !== 2) return { verdict: "unsure", why: "Kane gave no clear answer" };
  if (t.look[0] === t.look[1]) return { verdict: "unsure", why: "Kane contradicted itself" };
  const b = t.look[0];
  if (t.witness === undefined) return { verdict: "unsure", why: "no saved screen to compare with" };
  if (t.witness !== b) return { verdict: "unsure", why: `Kane said broken=${b}, the saved screen says ${t.witness ? "yes" : "no"}` };
  return { verdict: b ? "bad" : "good", why: "Kane and the saved screen agree" };
}

/** Two tries must agree. `undefined` means run another try. Three tries at most. */
export function combine(tries: Verdict[]): Verdict | undefined {
  for (const v of ["good", "bad"] as const) if (tries.filter(t => t === v).length >= 2) return v;
  return tries.length < 3 ? undefined : "unsure";
}

/** git bisect run: 0 good, 1 bad, 125 skip. */
export const bisectCode = (v: Verdict) => (v === "good" ? 0 : v === "bad" ? 1 : 125);

/** Broken when the colour on screen is not close to the colour it should be. */
export const pixelSaysBroken = (px: number[] | undefined, working: number[]) =>
  px ? px.some((v, i) => Math.abs(v - working[i]) > 12) : undefined;
