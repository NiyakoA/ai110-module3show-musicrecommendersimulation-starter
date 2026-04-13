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

---

## 7. Evaluation  

**Test Profiles:**
1. Pop-happy user (genre=pop, mood=happy, energy=0.8, likes_acoustic=False)
   - Expected: Upbeat pop songs with high energy and danceability
   - Result: "Sunrise City" (0.82 energy, pop, happy) ranked #1 ✓

2. Chill-acoustic user (genre=lofi, mood=chill, energy=0.4, likes_acoustic=True)
   - Expected: Low-energy, highly acoustic tracks
   - Result: "Library Rain" (0.35 energy, 0.86 acoustic) ranks high ✓

3. Intense-rock user (genre=rock, mood=intense, energy=0.9, likes_acoustic=False)
   - Expected: Energetic, electronic-leaning rock
   - Result: "Storm Runner" (0.91 energy, rock) ranked high ✓

**What Surprised Me:**
- Energy alignment produces intuitive rankings even across genres
- Acoustic weighting helped distinguish tracks well
- Equal feature weighting sometimes masked preference priorities

**Testing Methods:**
- Manual profile testing (3 user archetypes)
- Score inspection to verify algorithm logic
- Explanation readability check

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

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
