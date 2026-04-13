from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """
        Recommends top k songs based on user profile using content-based scoring.
        Scoring rules:
        - Genre match: +2 points
        - Mood match: +2 points
        - Energy alignment: 1.5 * (1 - abs(song.energy - target_energy))
        - Acoustic preference: +1.0 if matches preference, else 0
        """
        scored_songs = []
        for song in self.songs:
            score = self._calculate_score(user, song)
            scored_songs.append((song, score))
        
        # Sort by score descending and return top k
        scored_songs.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored_songs[:k]]
    
    def _calculate_score(self, user: UserProfile, song: Song) -> float:
        """
        Calculates recommendation score for a song based on user profile.
        """
        score = 0.0
        
        # Genre match
        if song.genre.lower() == user.favorite_genre.lower():
            score += 2.0
        
        # Mood match
        if song.mood.lower() == user.favorite_mood.lower():
            score += 2.0
        
        # Energy alignment
        energy_diff = abs(song.energy - user.target_energy)
        energy_score = 1.5 * (1.0 - energy_diff)
        score += energy_score
        
        # Acoustic preference
        if user.likes_acoustic:
            score += song.acousticness
        else:
            score += (1.0 - song.acousticness)
        
        return score

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """
        Provides a human-readable explanation of why a song was recommended.
        """
        explanations = []
        
        # Genre match
        if song.genre.lower() == user.favorite_genre.lower():
            explanations.append(f"Matches your favorite genre ({song.genre})")
        
        # Mood match
        if song.mood.lower() == user.favorite_mood.lower():
            explanations.append(f"Matches your favorite mood ({song.mood})")
        
        # Energy alignment
        energy_diff = abs(song.energy - user.target_energy)
        if energy_diff < 0.2:
            explanations.append(f"Perfect energy level match (target: {user.target_energy:.2f}, song: {song.energy:.2f})")
        elif energy_diff < 0.5:
            explanations.append(f"Good energy level match (target: {user.target_energy:.2f}, song: {song.energy:.2f})")
        
        # Acoustic preference
        if user.likes_acoustic and song.acousticness > 0.6:
            explanations.append(f"You like acoustic music, and this is highly acoustic ({song.acousticness:.2f})")
        elif not user.likes_acoustic and song.acousticness < 0.4:
            explanations.append(f"You prefer electronic/produced music, and this track is electronic ({song.acousticness:.2f})")
        
        # Fallback explanation
        if not explanations:
            explanations.append("Similar vibes to your preferences")
        
        return "; ".join(explanations)

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file and returns as list of dictionaries.
    Required by src/main.py
    """
    import csv
    print(f"Loading songs from {csv_path}...")
    songs = []
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert numeric fields to appropriate types
                song = {
                    'id': int(row['id']),
                    'title': row['title'],
                    'artist': row['artist'],
                    'genre': row['genre'],
                    'mood': row['mood'],
                    'energy': float(row['energy']),
                    'tempo_bpm': float(row['tempo_bpm']),
                    'valence': float(row['valence']),
                    'danceability': float(row['danceability']),
                    'acousticness': float(row['acousticness']),
                }
                songs.append(song)
        
        print(f"Successfully loaded {len(songs)} songs.")
    except FileNotFoundError:
        print(f"Error: CSV file not found at {csv_path}")
    except Exception as e:
        print(f"Error loading CSV: {e}")
    
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a single song against user preferences; returns (score, reasons)."""
    score = 0.0
    reasons = []

    # Genre match: +2.0
    if song['genre'].lower() == user_prefs.get('favorite_genre', '').lower():
        score += 2.0
        reasons.append('genre match (+2.0)')

    # Mood match: +2.0
    if song['mood'].lower() == user_prefs.get('favorite_mood', '').lower():
        score += 2.0
        reasons.append('mood match (+2.0)')

    # Energy alignment: 1.5 * (1 - |song_energy - target|)
    target_energy = user_prefs.get('target_energy', 0.7)
    energy_pts = round(1.5 * (1.0 - abs(song['energy'] - target_energy)), 2)
    score += energy_pts
    reasons.append(f'energy alignment (+{energy_pts:.2f})')

    # Acoustic preference
    if user_prefs.get('likes_acoustic', False):
        acoustic_pts = round(song['acousticness'], 2)
        reasons.append(f'acoustic preference (+{acoustic_pts:.2f})')
    else:
        acoustic_pts = round(1.0 - song['acousticness'], 2)
        reasons.append(f'electronic preference (+{acoustic_pts:.2f})')
    score += acoustic_pts

    return round(score, 2), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, List[str]]]:
    """Score every song, sort by score descending, and return the top k with reasons."""
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
