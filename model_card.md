# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0** — A Content-Based Music Recommender

---

## 2. Goal / Task

VibeFinder tries to answer one question: *"Given what a user tells us they like, which songs in the catalog are the best match?"*

It does not predict what a user will click on or learn from listening history. Instead, it takes a user's stated preferences (favorite genre, mood, energy level, and acoustic taste) and compares them against every song in the catalog using a point-based scoring system. The output is a ranked list of the top 5 songs most likely to match that taste profile.

---

## 3. Data Used

**Catalog size:** 18 songs in `data/songs.csv`

**Features per song:**

| Feature | Type | Range |
|---|---|---|
| genre | categorical | pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop, classical, country, metal, k-pop, blues, reggae, electronic |
| mood | categorical | happy, chill, intense, relaxed, moody, focused |
| energy | number | 0.0 (very calm) to 1.0 (very intense) |
| tempo_bpm | number | beats per minute |
| valence | number | 0.0 (dark) to 1.0 (upbeat) |
| danceability | number | 0.0 to 1.0 |
| acousticness | number | 0.0 (electronic) to 1.0 (fully acoustic) |

**Limits:**
- 18 songs is tiny. A real app like Spotify has tens of millions.
- Songs were chosen manually — the dataset reflects the creator's taste, not a real population of listeners.
- No listening history, ratings, or skips are tracked, so the system can't learn or improve over time.
- Some genres only have one song in the catalog (e.g., rock, blues, reggae), so users of those genres have very limited options.

---

## 4. Algorithm Summary

VibeFinder gives every song a score based on how well it matches the user's preferences, then returns the highest-scoring songs.

Here's how the score is calculated in plain language:

1. **Genre check:** If the song's genre matches the user's favorite genre, add 2 points.
2. **Mood check:** If the song's mood matches the user's favorite mood, add 2 points.
3. **Energy closeness:** Calculate how far the song's energy is from the user's target. The closer it is, the more points it earns (up to 1.5 points for a perfect match, 0 for a song that's as far away as possible).
4. **Acoustic preference:** If the user likes acoustic music, songs with higher acousticness earn more points. If the user prefers electronic, songs with lower acousticness earn more points.

After all songs are scored, they are sorted from highest to lowest. The top 5 are returned as recommendations.

The maximum possible score is about 6.5 points. A song that matches genre, mood, energy perfectly, and hits the acoustic preference would score near that ceiling.

---

## 5. Observed Behavior / Biases

**What works well:**
- Users with a genre and mood that exist in the catalog get strong, intuitive top results.
- The energy scoring rewards proximity, not just "high" or "low," which feels natural.
- Each recommendation comes with a plain-language explanation of why it was chosen.

**What doesn't work well:**

- **Genre ceiling problem:** If a user's favorite genre is not in the catalog (e.g., reggaeton), they can never earn the genre match bonus (+2 points). Their top score is capped around 4.4, while users with a matching genre regularly score 6+. This silently disadvantages listeners of underrepresented genres — they get worse recommendations and have no way of knowing why.

- **"Universal high scorers":** Songs with high energy and low acousticness (like "Gym Hero") tend to show up in recommendations for many different profiles because they score well on the energy and electronic preference dimensions even without matching genre or mood. This is how real apps create filter bubbles — a popular song ends up on too many people's playlists just because it hits a few common signals well.

- **Catalog gaps:** The catalog has no high-energy moody songs. A user who wants both (e.g., "Contradictory Listener" profile) gets results that technically score highest but feel intuitively wrong — a slow blues song ranked second because it matched mood, even though the user wanted 0.9 energy.

- **Fixed weights:** Every user is assumed to care equally about genre and mood. In reality, some people care far more about energy or acoustics than genre. The system has no way to learn or adjust for that.

---

## 6. Evaluation Process

Five user profiles were tested against the 18-song catalog:

| Profile | genre | mood | energy | acoustic | Top Result | Score |
|---|---|---|---|---|---|---|
| High-Energy Pop | pop | happy | 0.9 | No | Sunrise City | 6.20 |
| Chill Lofi | lofi | chill | 0.35 | Yes | Library Rain | 6.36 |
| Deep Intense Rock | rock | intense | 0.95 | No | Storm Runner | 6.34 |
| Contradictory Listener | synthwave | moody | 0.9 | No | Night Drive Loop | 6.05 |
| Reggaeton Fan | reggaeton | happy | 0.85 | No | Neon Seoul | 4.38 |

A weight-shift experiment was also run: genre weight was cut in half (2.0 → 1.0) and energy weight was doubled (1.5× → 3.0×). The #1 result stayed the same for all three standard profiles. Positions 2–5 shuffled noticeably. This shows the algorithm is stable at the top but the middle of the list is sensitive to weight choices.

Key finding: The Reggaeton Fan profile exposed the genre ceiling bias. Its best score (4.38) was nearly 2 full points below the Pop fan (6.20) just because reggaeton is not in the catalog — not because the algorithm made a mistake.

---

## 7. Intended Use and Non-Intended Use

**This system is designed for:**
- Classroom exploration of how recommendation algorithms work
- Learning about content-based filtering and scoring logic
- Demonstrating how small dataset choices produce biased outputs

**This system should NOT be used for:**
- Making real music recommendations to real users — the catalog is too small and the scoring too simple
- Any situation where fairness across genres or listener demographics matters
- Production deployment — there is no error handling for invalid profiles, no user privacy considerations, and no mechanism to improve with feedback
- Evaluating whether a song is objectively "good" — it only measures fit to a stated preference, not quality

---

## 8. Ideas for Improvement

1. **User-configurable weights** — Let the user say "energy matters twice as much as genre to me" and adjust the scoring formula dynamically. This would make the system far more personalized and fix the one-size-fits-all weight problem.

2. **Diversity enforcement** — Add a rule that prevents the same artist or genre from appearing more than once in the top 5. This would stop "universal high scorers" like Gym Hero from dominating every playlist.

3. **Larger, more representative catalog** — Expand from 18 to 200+ songs with balanced genre coverage. This is the single change that would do the most to fix the genre ceiling bias and give all types of listeners a fair experience.

---

## 9. Personal Reflection

**Biggest learning moment:** The "Reggaeton Fan" edge case. I expected the algorithm to just do less well — I didn't expect it to silently cap the score at a completely different ceiling than every other profile. That gap isn't obvious until you look at the numbers side by side. It made me realize that bias in a recommender system doesn't usually look like an error. It looks like a quietly worse experience for some users while everything appears to be working normally.

**Using AI tools:** AI tools helped me think through the scoring formula and quickly generate diverse song data. The place where I had to double-check them most carefully was the scoring math itself — the tools would sometimes suggest formulas that looked right but rewarded wrong edge cases (like giving negative energy scores for a song too far from the target, which would unfairly penalize it). I had to trace through specific examples by hand to catch those.

**Why simple algorithms feel like recommendations:** The scoring formula has four rules. That's it. But when those four rules align with what someone actually cares about — genre, mood, energy, and acoustic texture — the output feels almost intelligent. I think this is because humans also use a small number of quick filters when they pick music. The algorithm mimics that shortcut. The difference is that a human can bend the rules for a song that surprises them. VibeFinder can't.

**What I'd try next:** I'd add a "surprise mode" — a toggle that randomly boosts one or two songs that scored just outside the top 5. Real discovery in music happens at the edges of your taste, not the dead center of it. A recommender that only shows you what you already know you like is useful, but it's also a closed loop.
