# Global R-Hub — homepage hero video

The 16:9 hero video for **https://globalrhub.org**. It is built with
[HyperFrames](https://hyperframes.heygen.com): every scene is an HTML file animated with GSAP, then rendered to MP4.
Each frame renders the same way every time, so any edit is safe to re-render.

| Path | What it is |
|---|---|
| `hero-b/` | **The video**: "Edit Lobby" collage + editorial style, purple/orange, continuous page scroll, 41 s |
| `docs/` | The Edit Lobby restyle plan |
| `tools/fetch_website_assets.py` | Re-downloads any photo/logo from globalrhub.org |
| `website-assets.json` | Every photo, logo and image used, with its globalrhub.org URL and website-repo path |

The website itself lives in `../GlobalRhub/Rhub-marketing` (Laravel). Images in it are under `public/` and are also
live at `https://globalrhub.org/<path>`. Photos of students, mentors and faculty are admin uploads at
`https://globalrhub.org/shared-uploads/...`. `website-assets.json` records the exact source of each file.

---

## Requirements

- **Node.js 22+** and **FFmpeg** (`brew install node ffmpeg`)
- **Python 3**, for the audio scripts (standard library only).
- The HyperFrames CLI is pinned in each project's `package.json` (`hyperframes@0.9.61`), so `npm run …` fetches it
  automatically. Chrome for rendering is managed by the CLI.

## Everyday commands (run inside `hero-b/`)

```bash
npm run dev                      # live preview in the browser (Studio); stop it with Ctrl+C
npm run check                    # lint + layout + contrast checks — run after every edit
npx --yes hyperframes@0.9.61 snapshot --at 12,20,30   # PNG frames to look at without a full render
npm run render -- --quality delivery -o renders/globalrhub-hero.mp4   # final MP4 (~1.5 min)

python3 audio/build_sfx.py       # rebuild the sound-effects stem (after any timing change)
python3 audio/mix.py             # mix music + effects, master to -16 LUFS -> assets/audio/mix.wav
```

Rendering and previewing are CPU/GPU heavy. Stop the preview when you are done.

---

## hero-b: scene map

`hero-b/index.html` mounts the scenes in order. Each line there has a `data-start` and a `data-duration` (seconds).
Scenes from `s4` onward **scroll in from below** and **overlap the previous scene by 0.6 s**. That overlap is the
continuous "one long page" feel.

| id | file | start | dur | what's in it | where to edit text / people |
|---|---|---|---|---|---|
| s1 | `compositions/s1-echo.html` | 0 | 3.0 | "Looking for research mentorship?" echo rows | the `.e1-row` lines |
| s2 | `compositions/s2-search.html` | 3.0 | 2.0 | Search-results page, typing, click → iris to black | `const Q = …` (typed query), `#s2-r1/2/3` results, `#s2-word` logo word |
| s3 | `compositions/s3-logo.html` | 5.0 | 2.5 | Black frame → giant wordmark → logo + tagline | `#s3-tag` |
| s4 | `compositions/s4-programs.html` | 6.9 | 4.8 | Collage card + 5 program cards (brochure-popup characters) | `#p4-c1…c5`, `#p4-more` |
| s5 | `compositions/s5-mentors.html` | 11.1 | 6.5 | Aryaman ↔ Dr. Neharika (1:1), then mentors lineup (GLOBAL tags) | `#m5-c0` (paired mentor), `#m5-c1…c5` cards, `#m5-capA/B` captions |
| s6 | `compositions/s6-faculty-lor.html` | 17.0 | 7.1 | Globe with pins → 5 faculty cards (publications), then the Letter of Recommendation | `#f6-c1…c5` cards, `uni` array (pin lat/lon), `cardPos`, letter text in `#f6-letter` |
| s8 | `compositions/s8-students.html` | 23.5 | 4.5 | Sonam / Aryaman / Suhas tickets, ADMITTED | `#t8-k1…k3` |
| s12 | `compositions/s12-testimonials.html` | 27.4 | 7.0 | Two-row testimonials (in, 2.5 s pause, sweep out) | the six `.q12` cards (quotes are exact excerpts from the site) |
| s9 | `compositions/s9-admits.html` | 33.8 | 2.6 | University logo cascade | `.a9-c` cards |
| s10 | `compositions/s10-numbers.html` | 35.8 | 2.6 | 50+ / $100K+ / 1:1 echo numbers | the `.row` texts and the count-up loop at the bottom |
| s11 | `compositions/s11-end.html` | 37.8 | 3.2 | Collage + "Your research, mentored." + CTA | CTA text is the `cta` variable in `index.html` |
| — | `compositions/texture.html` | 0 | 41 | Paper fibre + film grain over everything | grain opacity in `#t-grain` |

Root length: `data-duration="41"` on `#root` in `index.html`.

### Common edits

- **Change any text:** edit it in the scene file, then run `npm run check` and look at a snapshot.
- **Swap a photo:** put the new file in `assets/img/people/` with the same name. Or change the `src` and add the
  new file to `website-assets.json`.
- **Faculty publication numbers:** the `<b>5+</b>` etc. in the `.pub` row of each `#f6-c*` card. The "100+
  publications" line is `#f6-subA`.
- **Mentors:** cards are authored at 430 × 560 and shown scaled down (`.m5-slot`). To add or remove one, change the
  `left:` positions and the list in the `["#m5-c1", …].forEach` line.
- **Colours:** purple `#413894`, ink `#1F1A47`, orange `#FFAA3E`, lavender `#EAE8F6`, paper `#FBFAF7`.
- **Fonts:** EB Garamond (serif), Space Mono (typewriter captions), Inter (UI). All are bundled with HyperFrames.

### Add, remove or retime a scene

1. In `index.html`, add, delete or edit the scene's host `<div id="sN" data-composition-id="sN" …>`. Its `id` and
   `data-composition-id` must both equal the id registered in the scene file (`window.__timelines["sN"]`).
   Keep the 0.6 s overlap for scroll-in scenes, and keep `z-index` increasing in playback order.
2. Update the root `data-duration` and the texture's `data-duration`. For the grain, set the animation count to
   `ceil(duration / 0.333)`.
3. Rebuild the sound with `python3 audio/build_sfx.py && python3 audio/mix.py`. **Sound follows automatically:** the
   cue script reads every scene's start from `index.html`, so a moved scene's sounds move with it and a deleted
   scene's sounds disappear. For a brand-new scene, add a cue function to `SCENE_CUES` in `audio/build_sfx.py`
   (and its id to `SCROLLS_IN` if it scrolls in).
4. Run `npm run check`, take snapshots, then render.

---

## Sound

- `audio/build_sfx.py` holds one function per scene. Each sound's **peak** lands one frame after its picture
  event. Repeats vary slightly in pitch and level. The output is `assets/audio/sfx-stem.wav`.
- `audio/mix.py` takes the music bed (`assets/audio/src/music-bed.wav`, started 0.985 s in, so a beat lands on the
  black logo hit) and gently ducks it under the effects. The track is 38 s, so it is extended with a beat-matched
  loop: a section 10 beats back re-enters under a 2 s crossfade at 30–32 s. It masters to −16 LUFS / −1 dBTP and
  writes `assets/audio/mix.wav`, the file the video plays.
- Levels: each effect sits about 3–6 dB over the music ("mild but present").

**Sources and licences**
- Music: HeyGen music catalog, "warm acoustic corporate, hopeful and welcoming piano" (track id
  `4aa36ea47e804a7287890af38fd8798b`), retrieved with a HeyGen account. Check HeyGen's terms cover
  commercial website use for your plan.
- Effects: Kenney (CC0); Openverse/Freesound CC0 (pencil, paper slide, page turn, paper fold); the HyperFrames
  bundle (Pixabay Content License). No CC BY sounds are used, so no attribution is required.

---

## Website assets

```bash
python3 tools/fetch_website_assets.py           # restore any missing photo/logo from globalrhub.org
python3 tools/fetch_website_assets.py --force   # re-download all (e.g. after a photo changed on the site)
```

The one derived file (the HKU crest, cropped from the HKU logo) is listed under `derived` in `website-assets.json`.

**Before publishing, confirm:** consent to show students' photos and names; the current numbers (50+ students,
$100K+ in scholarships won by students); faculty publication counts; and the sample letter wording in s6 (it is
not attributed to any named professor).

---

## Tooling

The HyperFrames and isometric skills used to build this were installed with
`npx skills add heygen-com/hyperframes` and `npx skills add iart-ai/explainer-video-skills --skill isometric-animation`
(`skills-lock.json` pins them). They are ignored by git and only needed for AI-assisted editing.

## Putting it on GitHub

```bash
cd globalrhub_video
git init && git add . && git commit -m "Global R-Hub hero video"
```

Renders are not committed: they are over GitHub's 100 MB limit. Attach the final MP4 to a GitHub Release, or use
Git LFS.
