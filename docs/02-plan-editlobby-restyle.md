# R-Hub hero — "Edit Lobby" restyle (for approval)

## 1. What the two reference reels do

**Reel 1, "Brain Dead" (creative talking head, 29 s)**
- Two flat, saturated colour fields (pink + green) with a paper-grain texture. Every scene sits on one of them.
- **Collage objects:** a torn paper card with punched holes, a photo with a tape strip, a postage-stamp frame, a **ticket with a "SOLD" rubber stamp**, B&W **halftone cut-out heads**, and tiny flat people.
- **Type:** a typewriter font for narration, with key words in **highlight boxes** (white or pink chips) that pop in word by word.
- **Motion:** objects slide in and settle with a slight tilt, icons **orbit in a circle** around a photo, a wavy colour shape wipes the scene, and the camera punches in.
- Few hard cuts (about 10 in 29 s). The motion inside each scene carries the pace.

**Reel 2, "Littlebird" (premium product ad, 17 s)**
- Warm off-white ground, lots of space, and a calm **editorial serif** typeface.
- **Echo type:** the same line repeated in rows above and below ("You have 47 tabs open"), blurred and faded at the edges, then app icons pop in beside it.
- **Card cascade:** small UI cards drifting diagonally in a staircase.
- **Logo moment:** a tiny mark grows into a **full-black frame with a giant serif wordmark**, then flips back to white with a tagline.
- **Real product UI:** a prompt being typed and the answer streaming in.
- **End card:** a split card, scenic image on the left and black on the right with a **checkerboard border**, a serif tagline and a white pill button.

## 2. The combined R-Hub style ("Edit Lobby × R-Hub")

| From the reels | For R-Hub |
|---|---|
| pink + green colour fields | **R-Hub purple #413894 + warm orange #FFAA3E** fields, with lavender #EAE8F6 and off-white #FBFAF7 grounds |
| typewriter + highlight chips | typewriter captions (Space Mono / IBM Plex Mono) with key words in **white or orange chips** |
| editorial serif | **EB Garamond** for big statements and numbers; Quicksand stays for the brand logo only |
| ticket + SOLD stamp | student tickets with an **"ADMITTED"** stamp, and a letter with a **"RECOMMENDED"** stamp |
| halftone cut-out heads | faculty and mentor photos as **halftone cut-outs** (real people only) |
| icons orbiting a photo | many mentor icons orbit the student, then **one** stays: **1 : 1** |
| card staircase | the 5 programs, and later the university logos, cascade as cards |
| echo-stacked line | "Looking for research mentorship?" echoed in rows, and the numbers echoed too |
| black frame + giant wordmark | **Global R-Hub** wordmark reveal |
| split end card with checker border | campus image left, black right: "Book a free session" |

Texture stays: paper grain, a slight print offset, soft drop shadows under the collage pieces.
It is **lighter on the laptop** than the 3D version (2D HTML instead of a WebGL world), so previews and renders run cooler.

## 3. Storyboard (~32 s, 16:9, readable with the sound off)

| Time | Scene (style source) | On screen |
|---|---|---|
| 0.0–3.0 | **Echo question** (R2): off-white, the line repeats in blurred rows; small icons (book, flask, cap) pop in | *Looking for research mentorship?* |
| 3.0–5.0 | **Search** (R2 UI): a clean search bar types; the result card **globalrhub.org** is clicked | `best research mentorship for students` |
| 5.0–6.6 | **Logo reveal** (R2): the favicon grows into a black frame with a giant serif **Global R-Hub**, then flips back to white | tagline: *Research mentorship, done right.* |
| 6.6–11.0 | **Programs** (R2 cascade + R1 chips): 5 program cards drop in a diagonal staircase on a lavender field, in order | Young Scholar · High School Scholar · Undergraduate Scholar · Graduate Scholar · **USMLE** · *+ more* |
| 11.0–14.5 | **1-on-1** (R1 orbit): the student photo in a **postage-stamp frame**; 8 mentor icons orbit, 7 drop away, 1 stays (a real mentor photo) | typewriter: *one student,* chip: **one PhD mentor** |
| 14.5–18.0 | **Global faculty** (R1 halftone): 5 halftone faculty cut-outs slide onto a purple field, each with a university tag | *Reviewed by* chip: **global faculty** |
| 18.0–20.5 | **LOR** (R1 ticket): a cream letter card slides in, then a **RECOMMENDED** rubber stamp slams on | *Letters of Recommendation* |
| 20.5–24.5 | **Students** (R1 ticket + SOLD): three tickets (photo, name, "Published paper"), each stamped **ADMITTED**: Curtin · NYU Stern · HKU | *Real students. Real results.* |
| 24.5–27.0 | **Admits** (R2 cascade): university logo cards drift diagonally on off-white | *Where our students got in* |
| 27.0–29.5 | **Numbers** (R2 echo): each number echoes, then sharpens | **50+** students mentored · **$100K+** in scholarships won by our students · **1:1** |
| 29.5–32.0 | **End card** (R2 split): campus illustration left; black right with a checker border | *Your research, mentored.* · button **Book a free session** · globalrhub.org |

Transitions: a wavy colour-field wipe (R1), the card zoom-through (R2), and the black-frame flip (R2). Three to five kinds, each caused by something on screen.

## 4. Sound

The same HeyGen piano track at 100 BPM. Effects become collage foley: paper slides, tape rips, typewriter keys under the captions, rubber-stamp thuds on ADMITTED and RECOMMENDED, soft card whooshes, and a low hit on the black logo frame. Still mild: each effect 3–6 dB over the music, mastered to −16 LUFS.

## 5. What happens to the isometric version

It stays as it is in `hero-a/` (rendered master in `hero-a/renders/`). The new style is a separate project, `hero-b/`, so you can compare the two side by side.
