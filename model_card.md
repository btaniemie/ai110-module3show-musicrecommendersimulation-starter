# Model Card: VibeFinder 1.0

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder suggests up to 5 songs from a small catalog based on a user's preferred genre, mood, energy level, and emotional positivity (valence). It is designed for classroom exploration and demonstration purposes only — not for production use with real users. It assumes a single, static user profile and a fixed song catalog.

**Not intended for:** real-time streaming, large catalogs, users with evolving tastes, or any context requiring privacy or fairness guarantees.

---

## 3. How the Model Works

Imagine you told a friend: "I want something pop, happy, high-energy, and uplifting." Your friend looks at every song they know and mentally checks each one: does the genre match? Does the mood match? How close is the energy level to what you asked for? Songs that check more boxes and come closer to your energy target get pushed to the top of the list.

VibeFinder does exactly that. For each song in the catalog it adds up four kinds of points:

- **Genre match** — the biggest bonus. If the song's genre matches your preference, it earns 2 points.
- **Mood match** — if the mood label (happy, chill, intense, etc.) matches, it earns 1 point.
- **Energy closeness** — the closer the song's energy (0.0–1.0) is to your target, the more points it earns (up to 1.5 points when the energy is a perfect match).
- **Valence closeness** — similarly, the closer the song's positivity level is to your preference, the more points it earns (up to 1.0 point).

The maximum possible score is 5.5 (genre + mood + perfect energy + perfect valence). Songs are then ranked from highest to lowest score, and the top 5 are returned with a plain-language explanation of why each one was chosen.

---

## 4. Data

- **Catalog size:** 18 songs (10 original starter songs + 8 added in Phase 2)
- **Features per song:** genre, mood, energy (0.0–1.0), valence (0.0–1.0), danceability (0.0–1.0), acousticness (0.0–1.0), tempo_bpm
- **Genres represented:** pop, lofi, rock, ambient, jazz, synthwave, indie pop, country, electronic, folk, hip-hop, r&b, metal, classical, reggae
- **Moods represented:** happy, chill, intense, relaxed, moody, focused, energetic, melancholic, confident, romantic, peaceful
- **Limitations of the data:** All songs are fictional, created for simulation purposes. Catalog is very small. Genre and mood labels are hand-assigned, not derived from audio analysis. The data does not represent the actual global music landscape — certain cultures, languages, and micro-genres are entirely absent.

---

## 5. Strengths

- Works very reliably for users whose genre and mood preferences are well-represented in the catalog (pop, lofi, rock).
- The proximity-based energy formula produces nuanced results — a song with energy 0.80 scores higher than one with energy 0.60 for a user who wants 0.85.
- Every recommendation comes with a plain-language explanation, making the system fully transparent ("genre match (+2.0) | mood match (+1.0) | energy proximity (+1.46)").
- Simple enough to reason about and debug — no black-box behavior.

---

## 6. Limitations and Bias

**Genre dominance:** The genre weight (2.0) is the single largest factor. A mediocre genre match will almost always beat a great energy + mood match in a different genre. This is the system's most significant bias.

**Genre imbalance in the catalog:** Even after expansion, pop has 3 songs (Sunrise City, Gym Hero, Rooftop Lights) while many other genres have only 1. A pop-preferring user has more songs to draw from, giving them inherently more variety in their top-5.

**Genre-energy conflict:** For the adversarial profile (jazz user who wants high energy), the genre bonus caused Coffee Shop Stories — a slow, relaxed jazz track at energy 0.37 — to rank #1 over genuinely high-energy tracks. The system recommended the opposite of what the user's energy preference implied, purely because of the genre label.

**Static taste model:** The system treats user preferences as a fixed snapshot. There is no ability to say "I sometimes want chill, sometimes want intense" or to weight preferences by time of day.

**No diversity enforcement:** The top results can all be very similar songs. A lofi user will get three lofi tracks in a row with almost identical scores, providing no variety.

---

## 7. Evaluation

**Profiles tested:**

| Profile | Expected top result | Actual top result | Matched intuition? |
|---|---|---|---|
| High-Energy Pop (pop, happy, 0.85) | Sunrise City | Sunrise City (5.44) | Yes |
| Chill Lofi (lofi, chill, 0.38) | Library Rain or Midnight Coding | Library Rain (5.44) | Yes |
| Deep Intense Rock (rock, intense, 0.92) | Storm Runner | Storm Runner (5.35) | Yes |
| Adversarial (jazz, happy, 0.90) | A high-energy happy song | Coffee Shop Stories (3.67) — low energy jazz | No — genre override |

**Weight experiment:** Doubling energy weight (1.5→3.0) and halving genre weight (2.0→1.0) on the adversarial profile flipped the top result from Coffee Shop Stories to Sunrise City. This confirms that genre dominance is a tunable artifact of the weights, not an inherent property of the algorithm.

**Surprise finding:** The adversarial profile exposed that a genre match + no other matches can outscore a near-perfect mood + energy + valence match in a different genre. This is a meaningful failure mode.

---

## 8. Future Work

1. **Normalize weights automatically** — if a user provides a very specific energy target, the energy weight should increase relative to genre to reflect how precise their request was.
2. **Add diversity enforcement** — after scoring, enforce a maximum of 2 songs per genre in the top-K results so recommendations don't cluster.
3. **Expand features** — incorporate `tempo_bpm` ranges (e.g., "I want songs between 80–100 BPM") and `danceability` into the user profile.
4. **Support preference ranges instead of point targets** — instead of `energy: 0.85`, allow `energy: [0.75, 0.95]` and score 0 for songs outside the range.
5. **Add collaborative filtering layer** — track which songs users actually listen to and use that signal to supplement content-based scores.

---

## 9. Personal Reflection

The most surprising discovery was how the adversarial profile exposed the genre-dominance problem. A jazz-preferring user who also wants high-energy music ended up being recommended the calmest song in the catalog just because it had the right genre label. This felt wrong immediately — it is the kind of failure that a real Spotify user would notice after one listen and never trust the recommendation engine again.

Building this system made it clear that real recommenders at scale must balance many competing signals. Collaborative filtering (what similar users liked) exists partly to compensate for exactly this flaw — sometimes the right song for you is in a genre you don't usually listen to, and only behavioral data from millions of users can surface that connection. A purely content-based system is transparent but brittle.

AI tools were helpful for scaffolding structure quickly, but the interesting design decisions — how much should genre matter versus energy? what makes a "good" recommendation feel right? — required human judgment. The tool generates code; it does not know what "good music taste" means.
