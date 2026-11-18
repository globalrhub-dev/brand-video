"""Final audio mix: HeyGen catalog music bed + SFX stem -> mastered mix.wav.

Music: "warm acoustic corporate, hopeful and welcoming piano" (HeyGen catalog,
track_id 4aa36ea47e804a7287890af38fd8798b), 100 BPM, started 0.51 s in so a strong
beat lands on the logo reveal (32.515 s).
Static master gain to -16 LUFS + true-peak limiter (no dynamic loudnorm pumping).
Run from the project root after audio/build_sfx.py:  python3 audio/mix.py [--music-only]
"""
import re, subprocess, sys

OFFSET = 0.985  # music starts 0.985 s in, so a beat lands on the black logo hit (5.03 s)
DUR = float(re.search(r'id="root"[^>]*?data-duration="([\d.]+)"', open("index.html").read()).group(1))
MUSIC, SFX = "assets/audio/src/music-bed.wav", "assets/audio/sfx-stem.wav"
MUSIC_DB, SFX_DB = -14, 10
music_only = "--music-only" in sys.argv
OUT = "assets/audio/_music_only.wav" if music_only else "assets/audio/mix.wav"


def premix(extra):
    sfx_db = -120 if music_only else SFX_DB
    # music extended with a beat-matched loop: 24.0 s on (40 beats) re-enters under a 2 s crossfade at 30-32 s
    return (f"[0:a]aresample=48000,atrim=0:32.0,asetpts=PTS-STARTPTS[ma];[2:a]aresample=48000,asetpts=PTS-STARTPTS[mb];"
            f"[ma][mb]acrossfade=d=2:c1=tri:c2=tri,atrim=0:{DUR},asetpts=PTS-STARTPTS,afade=t=in:d=0.25,"
            f"afade=t=out:st={DUR - 1.8}:d=1.8,volume={MUSIC_DB}dB[m];"
            f"[1:a]aresample=48000,volume={SFX_DB}dB,asplit=2[s1][s2];"
            "[m][s2]sidechaincompress=threshold=0.06:ratio=1.8:attack=10:release=300:makeup=1[md];"
            f"[s1]volume={sfx_db - SFX_DB}dB[s3];[md][s3]amix=inputs=2:normalize=0{extra}[out]")


base = ["ffmpeg", "-hide_banner", "-y", "-ss", str(OFFSET), "-i", MUSIC, "-i", SFX, "-ss", str(OFFSET + 24.0), "-i", MUSIC]
# pass 1: measure the full mix (always with SFX, so music-only shares the same master gain)
mo, music_only = music_only, False
r = subprocess.run(base + ["-filter_complex", premix(",ebur128=framelog=quiet"), "-map", "[out]", "-t", str(DUR), "-f", "null", "-"],
                   capture_output=True, text=True)
music_only = mo
I = float(re.findall(r"I:\s+([-\d.]+) LUFS", r.stderr)[-1])
gain = -16.0 - I
subprocess.run(base[:2] + ["-loglevel", "error"] + base[2:] + ["-filter_complex",
               premix(f",volume={gain:.2f}dB,alimiter=limit=0.84:level=false,aresample=48000"),
               "-map", "[out]", "-t", str(DUR), "-c:a", "pcm_s16le", OUT], check=True)
print(f"pre-master {I} LUFS, gain {gain:+.2f} dB ->", OUT)
