"""Build the SFX stem for the R-Hub hero (Edit Lobby cut, hero-b) from a cue sheet.

Every cue lands its PEAK one frame after the picture event it belongs to.
Sources are CC0 (Kenney, Openverse/Freesound CC0) or Pixabay-licensed (bundled);
no attribution-required (CC BY) sounds are used.
Scene start times and the film length are read from index.html, so retiming, moving or
deleting a scene there moves (or drops) its sounds automatically. Each scene's cues below
are written relative to that scene's own start (S).
Run:  python3 audio/build_sfx.py   (from the project root), then python3 audio/mix.py
"""
import json, math, re, subprocess, random

SRC = "assets/audio/src/"
OUT = "assets/audio/sfx-stem.wav"
FRAME = 1 / 30
rng = random.Random(20261117)  # seeded: identical stem every build

# peak offset (s) inside each file, measured with `hyperframes audio --json`
PEAK = {
    "pencil.mp3": 0.0, "paper-slide.mp3": 0.456, "stamp.wav": 0.318, "page-turn.mp3": 0.936,
    "paper-fold.mp3": 0.334, "whoosh.mp3": 0.162, "whoosh-short.mp3": 0.162, "whoosh-cinematic.mp3": 2.503,
    "click-soft.mp3": 0.073, "key-press.mp3": 0.076, "riser.mp3": 3.472, "impact-bass-1.mp3": 0.073,
    "pop.mp3": 0.12, "bong_001.ogg": 0.0, "click_002.ogg": 0.0, "click_003.ogg": 0.0, "rollover2.ogg": 0.025,
}
for n in ("impactPlank_medium_000", "impactPlank_medium_001", "impactPlank_medium_002"):
    PEAK[n + ".ogg"] = 0.015
for n in ("impactSoft_medium_000", "impactSoft_medium_001", "impactSoft_medium_002", "impactSoft_medium_004"):
    PEAK[n + ".ogg"] = 0.004
KEYS = [f"keypress-0{i}.wav" for i in ("03", "07", "11", "15", "19", "23", "27", "31")]
for k in KEYS:
    PEAK[k] = 0.03


def read_timeline(path="index.html"):
    """Scene id -> start (s), and the film length, straight from the root composition."""
    h = open(path).read()
    starts = {m.group(1): float(m.group(2)) for m in
              re.finditer(r'<div id="(s\d+)" data-composition-id="\1"[^>]*?data-start="([\d.]+)"', h)}
    dur = float(re.search(r'id="root"[^>]*?data-duration="([\d.]+)"', h).group(1))
    return starts, dur


START, DUR = read_timeline()
cues = []  # (file, peak_time, gain_db, semitones, extra)


def cue(f, at, gain, st=0.0, **kw):
    """One sound whose PEAK lands at `at` seconds (plus one frame: light before sound)."""
    cues.append(dict(f=f, at=at + FRAME, gain=gain, st=st, **kw))


def vary(g, st, dg=1.5, dst=0.6):
    return g + rng.uniform(-dg, dg), st + rng.uniform(-dst, dst)


PLANK = ["impactPlank_medium_000.ogg", "impactPlank_medium_001.ogg", "impactPlank_medium_002.ogg"]
SOFT = ["impactSoft_medium_000.ogg", "impactSoft_medium_001.ogg", "impactSoft_medium_002.ogg", "impactSoft_medium_004.ogg"]
WH = ["whoosh.mp3", "whoosh-short.mp3"]


def typewriter(times, gain=-17):
    for k, t in enumerate(times):
        g, st = vary(gain, -2, 2, 1.2)
        cue(KEYS[(k * 3) % len(KEYS)], t, g, st)


# ============================ one function per scene ============================
def s1_echo(S):          # "Looking for research mentorship?" echo rows
    typewriter([S + 0.08 + 0.09 * k for k in range(4)], -21)
    for i, t in enumerate((0.62, 0.74, 0.86)):
        cue("whoosh-short.mp3", S + t, -27, 5 + i * 1.5)
    for i, t in enumerate((1.22, 1.37, 1.52)):
        cue("pop.mp3", S + t, -13, i * 2)
    cue("whoosh.mp3", S + 2.6, -21, 3)


def s2_search(S):        # Google-style results page, typing, click, iris
    q = "best research mentorship for students"
    for k in range(1, len(q) + 1, 2):
        g, st = vary(-23, 0, 2.5, 1.0)
        cue(KEYS[k % len(KEYS)], S + 0.12 + k * 0.023, g, st)
    cue("key-press.mp3", S + 1.06, -7)
    cue("rollover2.ogg", S + 1.08, -21, 2)
    cue("click-soft.mp3", S + 1.54, -5)
    cue("whoosh-cinematic.mp3", S + 1.98, -16, 0, seek=1.7, fadeout=0.5)


def s3_logo(S):          # black frame, giant wordmark, flip to the logo
    cue("impact-bass-1.mp3", S + 0.03, -21, -3, fadeout=0.9)
    cue("whoosh.mp3", S + 0.8, -19, -2)
    cue("bong_001.ogg", S + 0.9, -17, -2)


def s4_programs(S):      # collage card + five program cards
    cue("paper-slide.mp3", S + 0.8, -3)
    cue("paper-fold.mp3", S + 1.02, -12, 2)
    typewriter([S + 0.87, S + 0.98, S + 1.09], -16)
    cue("pop.mp3", S + 1.28, -15, 3)
    cue("click_002.ogg", S + 1.47, -22)
    for i, st in enumerate((0, 2, 4, 5)):
        cue(PLANK[i % 3], S + 1.15 + i * 0.3, -14, st)
    cue(SOFT[0], S + 2.46, -10, -3)       # USMLE card
    cue("rollover2.ogg", S + 2.87, -21, 4)


def s5_mentors(S):       # Aryaman + Dr. Neharika (1:1), then the mentor bench
    cue("whoosh-short.mp3", S + 0.45, -20, -3)       # purple panel
    cue(SOFT[1], S + 0.5, -15, 0)                    # student photo lands
    for i in range(6):
        cue("click_003.ogg", S + 0.62 + i * 0.05, -23, i)
    typewriter([S + 0.65 + 0.14 * k for k in range(5)], -16)
    cue("pop.mp3", S + 0.95, -17, 2)
    for i in range(5):
        cue("click_002.ogg", S + 1.42 + i * 0.04, -27, -i * 0.5)
    cue("whoosh-short.mp3", S + 1.62, -19, 4)        # matched mentor carried across
    cue("pop.mp3", S + 1.8, -13, 3)                  # mentor card
    cue("paper-fold.mp3", S + 2.0, -14, 2)           # tape
    cue("whoosh-short.mp3", S + 1.95, -25, 7)        # link draws
    cue(SOFT[2], S + 2.25, -15, -4)                  # 1:1 badge
    cue("pop.mp3", S + 2.62, -17, 5)                 # weekly sticker
    cue("whoosh.mp3", S + 3.8, -18, -4)              # panel floods the frame
    cue("whoosh-short.mp3", S + 3.9, -22, 2)         # the card joins the bench
    for i in range(4):
        cue("click_002.ogg", S + 4.1 + i * 0.1, -22, i)
    typewriter([S + 4.05 + 0.13 * k for k in range(4)], -17)
    cue("pop.mp3", S + 4.36, -16, 3)
    cue("pop.mp3", S + 4.9, -15, 6)                  # GLOBAL tags
    cue("pop.mp3", S + 5.02, -16, 8)


def s6_faculty_lor(S):   # globe + faculty cards, then the letter of recommendation
    typewriter([S + 0.45, S + 0.59], -16)
    cue("pop.mp3", S + 0.82, -15, 1)
    cue(SOFT[0], S + 0.6, -15, -3)                     # globe lands
    cue("whoosh.mp3", S + 1.0, -22, -6)                # globe spins to the Americas
    for i in range(4):
        cue("click_003.ogg", S + 1.8 + i * 0.07, -21, 2 + i)       # pins drop
    for i in range(5):
        cue("whoosh-short.mp3", S + 2.0 + i * 0.07, -26, 6 + i)    # strings shoot out
        cue(PLANK[i % 3], S + 2.22 + i * 0.08, -18, 2 + i)         # cards pinned
    cue("whoosh.mp3", S + 3.65, -20, -5)             # the professors step back
    typewriter([S + 3.7, S + 3.84], -16)
    cue("pop.mp3", S + 4.05, -16, 2)
    cue("paper-fold.mp3", S + 3.85, -10, -1)         # envelope rises
    cue("paper-slide.mp3", S + 4.3, -4)              # letter slides out
    cue("pencil.mp3", S + 4.72, -19, 4, trim=0.3, fadeout=0.1)    # highlighter strokes
    cue("pencil.mp3", S + 5.0, -20, 5, trim=0.26, fadeout=0.1)
    cue("pencil.mp3", S + 5.12, -17, 2, trim=0.42, fadeout=0.15)  # signature
    cue("pop.mp3", S + 5.62, -14, -2)                # wax seal (no stamp)


def s8_students(S):      # three tickets with ADMITTED marks
    for i in range(3):
        cue("paper-slide.mp3", S + 0.85 + i * 0.2, -11, i)
    for i in range(3):
        cue("pop.mp3", S + 1.52 + i * 0.42, -18, i * 1.5)


def s12_testimonials(S): # two rows: in, pause to read, sweep on
    cue("whoosh.mp3", S + 0.85, -19, -2)
    cue("whoosh.mp3", S + 0.97, -20, 1)
    for i in range(6):
        cue("click_002.ogg", S + 1.7 + i * 0.06, -24, i)
    cue("whoosh-short.mp3", S + 5.4, -20, -2)
    cue("whoosh-short.mp3", S + 5.5, -21, 2)


def s9_admits(S):        # university logo cards cascade
    for i in range(8):
        cue("whoosh-short.mp3", S + 0.45 + i * 0.085, -27, 4 + i)
        cue("click_002.ogg", S + 0.55 + i * 0.085, -24, 0)


def s10_numbers(S):      # 50+ / $100K+ / 1:1 count-up
    for i, st in enumerate((-2, 0, -4)):
        cue(SOFT[i], S + 0.45 + i * 0.22, -15, st)
    t, k = S + 0.4, 0
    while t < S + 1.25:
        cue("click_003.ogg", t, -28, k % 3)
        t += 0.05
        k += 1


def s11_end(S):          # collage end card + CTA
    cue("riser.mp3", S + 0.7, -23, 0, seek=1.4, fadeout=0.12)
    cue("whoosh-cinematic.mp3", S + 0.7, -17, 0, seek=1.9, fadeout=0.5)
    for i in range(6):
        cue("click_002.ogg", S + 0.73 + i * 0.05, -26, i)
    cue("bong_001.ogg", S + 0.83, -17, -3)
    cue("pop.mp3", S + 1.17, -12, 2)


SCENE_CUES = {"s1": s1_echo, "s2": s2_search, "s3": s3_logo, "s4": s4_programs, "s5": s5_mentors,
              "s6": s6_faculty_lor, "s8": s8_students, "s12": s12_testimonials, "s9": s9_admits,
              "s10": s10_numbers, "s11": s11_end}
SCROLLS_IN = ["s4", "s5", "s6", "s8", "s12", "s9", "s10", "s11"]   # scenes that glide up from below

for sid, fn in SCENE_CUES.items():
    if sid in START:
        fn(START[sid])
# one soft paper whoosh at the middle of each page scroll
for i, sid in enumerate(s for s in SCROLLS_IN if s in START):
    g, st = vary(-20, -3, 1.0, 1.5)
    cue(WH[i % 2], START[sid] + 0.3, g, st)


# --------------------------------------------------------------------------
def max_db(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", "volumedetect", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = re.search(r"max_volume: ([-\d.]+) dB", r.stderr)
    return float(m.group(1)) if m else 0.0


norm = {f: -6.0 - max_db(SRC + f) for f in {c["f"] for c in cues}}  # every source peaks at -6 dBFS before its cue gain

inputs, chains = [], []
for i, c in enumerate(cues):
    seek = c.get("seek", 0.0)
    rate = 2 ** (c["st"] / 12)
    # the pitch shift (asetrate) also speeds the file up, so its peak moves earlier by the same ratio
    peak = (PEAK[c["f"]] - seek) / rate
    start = max(0.0, c["at"] - peak)
    inputs += ["-ss", f"{seek:.3f}", "-i", SRC + c["f"]] if seek else ["-i", SRC + c["f"]]
    f = [f"aresample=48000", "aformat=channel_layouts=stereo", f"asetrate={48000 * rate:.1f}", "aresample=48000"]
    if "trim" in c:
        f.append(f"atrim=0:{c['trim']}")
    if "fadeout" in c:
        length = c.get("trim", 30)
        fade_at = max(0, length - c['fadeout']) if 'trim' in c else max(0.0, peak) + 0.12
        f.append(f"afade=t=out:st={fade_at:.3f}:d={c['fadeout']}")
    f.append(f"volume={norm[c['f']] + c['gain']:.2f}dB")
    f.append(f"adelay={int(start * 1000)}|{int(start * 1000)}")
    chains.append(f"[{i}:a]{','.join(f)}[c{i}]")

mix = "".join(f"[c{i}]" for i in range(len(cues)))
graph = ";".join(chains) + f";{mix}amix=inputs={len(cues)}:normalize=0:dropout_transition=0," \
    f"aecho=0.85:0.55:38|67:0.16|0.09,apad=whole_dur={DUR},atrim=0:{DUR},alimiter=limit=0.89[out]"
cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *inputs, "-filter_complex", graph, "-map", "[out]",
       "-ar", "48000", "-c:a", "pcm_s16le", OUT]
subprocess.run(cmd, check=True)
json.dump([{k: (round(v, 3) if isinstance(v, float) else v) for k, v in c.items()} for c in cues],
          open("audio/cues.json", "w"), indent=1)
print(f"{len(cues)} cues -> {OUT}")
