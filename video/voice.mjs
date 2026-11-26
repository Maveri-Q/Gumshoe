// Narration for the demo video, made with ElevenLabs. The key is read from .env and never printed.
//   node video/voice.mjs voices                 list the voices this account can use
//   node video/voice.mjs make <voice id>        one audio clip per line in voice.json, then check the timing
//   node video/voice.mjs mix <video> <out>      lay the clips on the film at their times
import { readFileSync, writeFileSync, existsSync, mkdirSync } from "node:fs";
import { join, resolve } from "node:path";
import { execFileSync } from "node:child_process";

const root = resolve(import.meta.dirname, ".."), dir = join(root, "video", "out", "voice");
const key = (readFileSync(join(root, ".env"), "utf8").match(/^ELEVENLABS_API_KEY=(.+)$/m) ?? [])[1]?.trim();
const lines = JSON.parse(readFileSync(join(root, "video", "voice.json"), "utf8"));
const api = (path, init = {}) => fetch("https://api.elevenlabs.io" + path, { ...init, headers: { "xi-api-key": key, "content-type": "application/json", ...init.headers } });
const dur = f => +execFileSync("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], { encoding: "utf8" }).trim();
const [mode, ...args] = process.argv.slice(2);
if (!key && mode !== "mix") throw new Error("No ELEVENLABS_API_KEY in .env");
mkdirSync(dir, { recursive: true });

if (mode === "voices") {
  const r = await api("/v1/voices"); if (!r.ok) throw new Error(`voices: ${r.status} ${await r.text()}`);
  for (const v of (await r.json()).voices) console.log(v.voice_id, "|", v.name, "|", Object.values(v.labels ?? {}).join(", "));
}

if (mode === "make") {
  const voice = args[0];
  for (const [i, l] of lines.entries()) {
    const f = join(dir, `${String(i).padStart(2, "0")}.mp3`);
    if (existsSync(f) && !args.includes("--again")) continue;
    const r = await api(`/v1/text-to-speech/${voice}?output_format=mp3_44100_128`, { method: "POST", body: JSON.stringify({
      text: l.text, model_id: "eleven_multilingual_v2",
      previous_text: lines[i - 1]?.text, next_text: lines[i + 1]?.text,
      voice_settings: { stability: 0.45, similarity_boost: 0.8, style: 0.35, use_speaker_boost: true } }) });
    if (!r.ok) throw new Error(`line ${i}: ${r.status} ${await r.text()}`);
    writeFileSync(f, Buffer.from(await r.arrayBuffer()));
    console.log(`made ${i}: ${l.text.slice(0, 50)}`);
  }
}

if (mode === "make" || mode === "check") {
  let bad = 0;
  lines.forEach((l, i) => { const d = dur(join(dir, `${String(i).padStart(2, "0")}.mp3`)), next = lines[i + 1]?.at ?? 190, room = next - l.at;
    console.log(`${String(i).padStart(2)} at ${l.at}s  ${d.toFixed(1)}s of ${room.toFixed(1)}s ${d > room - 0.15 ? "  TOO LONG" : ""}`); if (d > room - 0.15) bad++; });
  console.log(bad ? `${bad} lines run into the next one` : "Every line fits.");
}

if (mode === "mix") {
  const [video, out] = args, ins = [], parts = [];
  lines.forEach((l, i) => { ins.push("-i", join(dir, `${String(i).padStart(2, "0")}.mp3`)); const ms = Math.round(l.at * 1000); parts.push(`[${i + 1}:a]adelay=${ms}|${ms}[a${i}]`); });
  const filter = parts.join(";") + ";" + lines.map((_, i) => `[a${i}]`).join("") + `amix=inputs=${lines.length}:normalize=0,loudnorm=I=-16:TP=-1.5[v]`;
  execFileSync("ffmpeg", ["-y", "-loglevel", "error", "-i", video, ...ins, "-filter_complex", filter, "-map", "0:v", "-map", "[v]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", out], { stdio: "inherit" });
  console.log("wrote", out);
}
