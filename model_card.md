# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeFinder 1.0** — A Content-Based Music Recommender

---

## 2. Intended Use  

**VibeFinder** is a classroom simulation of music recommendation systems. It generates personalized playlists by matching song attributes (genre, mood, energy, acousticness) to a user's taste profile. 

**Key Assumptions:**
- Users have stable, consistent musical preferences
- Users can articulate their taste (favorite genre, mood, target energy level, acoustic preference)
- Musical compatibility is primarily attribute-based (no complex social or temporal factors)
- Users prioritize genre and mood, with energy level as a secondary refinement

**Setting:** Educational exploration of recommendation algorithms, not production use.

---

## 3. How the Model Works  

**Simple Explanation:** VibeFinder scores every song by checking how well it matches your taste. It adds up "match points" for genre, mood, energy closeness, and acoustic preference, then ranks songs by total score.

**Scoring Rule (Points System):**
1. **Genre Match**: +2 points if the song's genre matches your favorite
2. **Mood Match**: +2 points if the song's mood matches your favorite
3. **Energy Alignment**: 1.5 × (1 − |song_energy − your_target_energy|)
   - This rewards songs *close* to your energy preference, not just high or low
   - Example: If you like energy 0.7, a song at 0.72 scores ~1.47 points, while 0.4 scores ~0.55
4. **Acoustic Preference**: +acousticness score if you like acoustic, or +(1 − acousticness) if you prefer electronic

**Why This Works:** Instead of saying "higher energy is always better," we ask "how close is this to what I want?" This mirrors how humans think about music vibes.

**Ranking Rule:** After scoring all songs, sort them by score (highest first) and return the top k results.

---

**Why Both Rules Matter:**

*Scoring Rule* (evaluate one song): Answers "How well does this song match the user?" → Enables fair comparison and transparency.

*Ranking Rule* (order all songs): Answers "What order should I show the recommendations?" → Determines what users see first.

**Analogy:** Scoring is like grading individual test papers (0–100 each); Ranking is like sorting students by grade to publish a class ranking. Without scores, you can't rank fairly. Without ranking, scores are useless to users.

**For VibeFinder:** We use *simple score-based ranking* (sort descending, return top 5). In production systems (Spotify, YouTube), ranking is more complex: introducing diversity, prioritizing new releases, or balancing familiar vs. novel recommendations.

---

## 4. Data  

**Dataset:** 10 songs in `data/songs.csv` (small simulation dataset)

**Genres Represented:** pop, lofi, rock, ambient, jazz, synthwave, indie pop

**Moods Represented:** happy, chill, intense, relaxed, moody, focused

**Attributes per Song:**
- id, title, artist (metadata)
- genre, mood (categorical)
- energy, tempo_bpm, valence, danceability, acousticness (numerical, 0.0–1.0 scale)

**Missing Genres:** hip-hop, classical, country, metal, electronic, blues, reggae, k-pop

**Data Limitations:** 
- Very small catalog (10 songs) → unrealistic for production
- Narrow genre diversity → biased toward lo-fi/indie aesthetics
- No user interaction data (plays, skips, ratings) → can't use collaborative filtering
- Artist popularity or release date not tracked

---

## 5. Strengths  

**Works Well For:**
- Users with clear genre/mood preferences (e.g., "I want chill, acoustic music") → Gets top matches
- Energy-conscious listeners → Scoring rewards proximity over extreme values
- Explaining recommendations → Each song gets a readable explanation of why it matched

**What It Captures Correctly:**
- Genre and mood loyalty → Core similarities are weighted heavily (+2 each)
- Energy diversity → A user liking 0.7 energy gets high-energy (0.9) and calm (0.5) songs ranked differently
- Acoustic texture → Distinguishes between live/organic vs. produced/electronic
- Vibe consistency → Songs that "feel right" based on multiple attributes rank together

---

## 6. Limitations and Bias  

**Missing Features:**
- No artist diversity tracking → Could recommend same artist repeatedly
- No temporal context → Ignores time of day, workout vs. study, social vs. solo
- No collaborative signal → If 100 users liked a song, you don't benefit from that wisdom
- No discovery mechanism → Only rewards similarity; never pushes boundaries

**Underrepresented Groups:**
- Hip-hop, classical, metal, country users → Limited catalog genre coverage
- Mood-driven preferences (e.g., users who prioritize "happy" over genre) → Mood match weighted equally to genre
- Niche/experimental music fans → Dataset too homogeneous

**Overfitting Risks:**
- A user saying "favorite_genre=pop, favorite_mood=happy" will see mostly those combinations
- No serendipity → You get consistent but predictable playlists
- Equal weighting → For some users, energy might matter more than mood, but scoring treats equally

**Fairness Concerns:**
- Mainstream genres (pop) have more songs in dataset → Statistical advantage
- Acoustic preference penalizes electronic/produced music equally → Might feel biased to synth lovers

**Key Weakness Discovered During Evaluation:**

Testing a "Reggaeton Fan" profile — a user whose favorite genre is not in the catalog at all — exposed a hard ceiling problem. Because the genre match is worth +2.0 points, users whose genre is missing can never score above ~4.4 points, while users with a matching genre regularly hit 6.0+. This means the recommender is quietly unfair to listeners of genres it doesn't cover. In a real product, a fan of reggaeton, classical, or metal would always receive weaker recommendations than a pop fan, not because the algorithm is wrong, but simply because the catalog was built with certain tastes in mind. This is a form of representation bias: the data reflects the dataset creator's assumptions about what music is worth including.

---

## 7. Evaluation  

**Five Profiles Tested:**

| Profile | Top Result | Score | Surprise? |
|---|---|---|---|
| High-Energy Pop (pop/happy/0.9) | Sunrise City | 6.20 | No — perfect match |
| Chill Lofi (lofi/chill/0.35/acoustic) | Library Rain | 6.36 | No — expected |
| Deep Intense Rock (rock/intense/0.95) | Storm Runner | 6.34 | No — expected |
| Contradictory Listener (synthwave/moody/0.9) | Night Drive Loop | 6.05 | Partially — only 1 song matched genre+mood, so the #1 was obvious, but #2 was a blues track that matched mood but not energy |
| Reggaeton Fan (reggaeton/happy/0.85) | Neon Seoul | 4.38 | Yes — the system had no reggaeton songs, so the top result was a K-pop song that happened to be happy and high-energy. No genre match was ever found. |

**Key Observations:**

1. "Gym Hero" (pop/intense/0.93 energy) appeared in the top 5 for three different profiles. It is an accidental "universal high scorer" — its high energy and low acousticness make it hard to beat for any electronic-leaning user, even if the mood or genre doesn't match.

2. The "Contradictory Listener" profile (high energy + moody mood) revealed a catalog gap: the catalog has no high-energy moody songs. The #2 result was a slow blues track that matched mood but had an energy of only 0.48 — far from the user's 0.9 target. The system technically gave the "best" answer, but intuitively it felt wrong.

3. The weight-shift experiment (genre ÷2, energy ×2) shuffled positions 2–5 but never changed the #1 result. This suggests the algorithm is fairly stable at the top, but the middle rankings are sensitive to weights.

**Testing Methods:**
- Five user archetypes run against the 18-song catalog
- Score inspection to verify algorithm logic
- Weight-shift experiment to test sensitivity
- Edge cases: genre not in catalog, conflicting preference signals

---

## 8. Future Work  

**High Priority:**
1. **Configurable Weights** → Let users specify "genre matters most to me" vs. "energy matters"  
2. **Larger Catalog** → Expand from 10 to 100+ songs across more genres  
3. **Diversity Mode** → Ensure top 5 recommendations don't all have same genre/artist  
4. **Temporal Context** → Adjust recommendations based on time of day or activity type  

**Medium Priority:**
5. **Hybrid Approach** → Add collaborative filtering ("users like you also liked...")  
6. **Serendipity** → Include a "surprise me" mode that temporarily loosens constraints  
7. **Interactive Feedback** → User rates recommendation; system refines preference model  
8. **Beat/Instrumentation** → Extract more granular audio features beyond basic metrics  

**Low Priority:**
9. Lyrical content analysis (NLP on song lyrics for theme/topic matching)  
10. Social features ("friends liked this", trending in your city)

---

## 9. Personal Reflection  

Building this recommender made me realize how much of a system's "intelligence" is really just math applied to assumptions. The scoring logic isn't smart — it just adds up points based on rules I wrote. But when the rules are aligned with what users actually care about (genre, mood, energy), the output feels surprisingly reasonable. What surprised me most was how a song like "Gym Hero" kept showing up across totally different profiles. It wasn't because the system misunderstood anything; it's because that song genuinely scores well on multiple dimensions for multiple user types. That's how real recommender systems create filter bubbles — not through malice, but through patterns in the data.

The "Reggaeton Fan" edge case changed how I think about Spotify or YouTube. Those apps handle millions of genres, but they were also built by teams that made choices about what data to collect and what genres to weight. A content-based system like this one silently fails for users whose tastes aren't reflected in the catalog, and does so without any warning — the user just gets "close enough" results and never knows they're being underserved. That invisibility is what makes representation bias in recommenders so hard to catch and fix.
