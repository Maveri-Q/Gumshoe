// Narration for the demo video, made with ElevenLabs. The key is read from .env and never printed.
//   node video/voice.mjs take <voice id>     record the whole script in one take, with the time each line starts
//   node video/voice.mjs plan                cut the take in its pauses and work out the new film timing
//   node video/voice.mjs mix <video> <out>   lay the lines on the (re-timed) film
// One take, not one clip per line: short clips came back chopped ("Twenty." in 0.37 s, no tail).
// The film is then sped up between lines (at most MAXSPEED times) so there are no long silences.
import { readFileSync, writeFileSync, existsSync, mkdirSync } from "node:fs";
import { join, resolve } from "node:path";
import { execFileSync } from "node:child_process";

const root = resolve(import.meta.dirname, ".."), dir = join(root, "video", "out", "voice");
const lines = JSON.parse(readFileSync(join(root, "video", "voice.json"), "utf8"));
const FILM = 190, LEAD = 0.8, GAP = 0.45, COUNT_GAP = 0.75, END_HOLD = 2.2, MAXSPEED = 2.5;
const [mode, ...args] = process.argv.slice(2);
mkdirSync(dir, { recursive: true });
const take = join(dir, "take.mp3"), align = join(dir, "take.json"), planF = join(dir, "plan.json");
const ff = a => execFileSync("ffmpeg", ["-y", "-loglevel", "error", ...a], { stdio: "inherit" });

if (mode === "take") {
  const key = (readFileSync(join(root, ".env"), "utf8").match(/^ELEVENLABS_API_KEY=(.+)$/m) ?? [])[1]?.trim();
  if (!key) throw new Error("No ELEVENLABS_API_KEY in .env");
  const text = lines.map(l => l.text).join("\n\n");
  const r = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${args[0]}/with-timestamps?output_format=mp3_44100_128`, {
    method: "POST", headers: { "xi-api-key": key, "content-type": "application/json" },
    body: JSON.stringify({ text, model_id: "eleven_multilingual_v2",
      voice_settings: { stability: 0.55, similarity_boost: 0.8, style: 0.2, use_speaker_boost: true } }) });
  if (!r.ok) throw new Error(`take: ${r.status} ${await r.text()}`);
  const j = await r.json();
  writeFileSync(take, Buffer.from(j.audio_base64, "base64"));
  const a = j.alignment, chars = a.characters.join("");
  if (chars !== text) throw new Error("the timing doesn't line up with the script");
  let off = 0; const out = lines.map(l => { const s = off, e = off + l.text.length - 1; off += l.text.length + 2;
    return { start: a.character_start_times_seconds[s], end: a.character_end_times_seconds[e] }; });
  writeFileSync(align, JSON.stringify(out, null, 1));
  console.log(`one take, ${text.length} characters, ${out.at(-1).end.toFixed(1)} s of speech`);
}

if (mode === "plan") {
  const t = JSON.parse(readFileSync(align, "utf8")), total = +execFileSync("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", take], { encoding: "utf8" });
  // Cut each line out of the take halfway through the pause after it, so no word is cut.
  const plan = lines.map((l, i) => {
    const a = Math.max(0, t[i].start - 0.08), b = i < lines.length - 1 ? (t[i].end + t[i + 1].start) / 2 : Math.min(total, t[i].end + 0.5);
    const f = join(dir, `line-${String(i).padStart(2, "0")}.wav`);
    ff(["-i", take, "-ss", a.toFixed(3), "-to", b.toFixed(3), "-af", "afade=t=in:d=0.02,areverse,afade=t=in:d=0.04,areverse", "-ar", "44100", f]);
    return { i, old: l.at, speech: t[i].end - t[i].start + 0.08, file: f };
  });
  // New start of each line: right after the one before (plus a pause), but never more than MAXSPEED times faster than the film.
  let now = LEAD;
  plan.forEach((p, i) => { if (i) { const q = plan[i - 1], counting = /^(Eighty|Forty|Twenty|Ten|Five|Three|One|Found)/.test(q.text ?? lines[i - 1].text) && lines[i - 1].text.length < 14;
    now += Math.max(q.speech + (counting ? COUNT_GAP : GAP), (p.old - q.old) / MAXSPEED); } p.at = +now.toFixed(3); });
  const last = plan.at(-1), end = +(last.at + Math.max(last.speech + END_HOLD, (FILM - last.old) / MAXSPEED)).toFixed(3);
  // The film map: [new time, old film time] pairs. Before line 0 and after the last line it runs at the same pace.
  const warp = [[0, 0], ...plan.map(p => [p.at, p.old]), [end, FILM]];
  writeFileSync(planF, JSON.stringify({ end, warp, lines: plan.map(({ i, at, old, speech }) => ({ i, at, old, speech: +speech.toFixed(2) })) }, null, 1));
  plan.forEach((p, i) => { const n = plan[i + 1]?.at ?? end; console.log(`${String(i).padStart(2)} at ${p.at.toFixed(1)}s (was ${p.old}s)  speaks ${p.speech.toFixed(1)}s, then ${(n - p.at - p.speech).toFixed(1)}s quiet`); });
  console.log(`film: ${FILM}s becomes ${end.toFixed(1)}s`);
}

if (mode === "mix") {
  const [video, out] = args, { lines: pl } = JSON.parse(readFileSync(planF, "utf8")), ins = [], parts = [];
  pl.forEach((l, k) => { ins.push("-i", join(dir, `line-${String(l.i).padStart(2, "0")}.wav`)); const ms = Math.round(l.at * 1000); parts.push(`[${k + 1}:a]adelay=${ms}|${ms}[a${k}]`); });
  const filter = parts.join(";") + ";" + pl.map((_, k) => `[a${k}]`).join("") + `amix=inputs=${pl.length}:normalize=0:duration=longest,loudnorm=I=-16:TP=-1.5,aresample=44100,apad[v]`;
  ff(["-i", video, ...ins, "-filter_complex", filter, "-map", "0:v", "-map", "[v]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", out]);
  console.log("wrote", out);
}
