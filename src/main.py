"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


PROFILES = {
    "High-Energy Pop": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.9,
        "likes_acoustic": False,
    },
    "Chill Lofi": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.35,
        "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.95,
        "likes_acoustic": False,
    },
    # Edge case: conflicting preferences (high energy + moody mood)
    "Contradictory Listener": {
        "favorite_genre": "synthwave",
        "favorite_mood": "moody",
        "target_energy": 0.9,
        "likes_acoustic": False,
    },
    # Edge case: genre not in catalog
    "Reggaeton Fan": {
        "favorite_genre": "reggaeton",
        "favorite_mood": "happy",
        "target_energy": 0.85,
        "likes_acoustic": False,
    },
}


def print_recommendations(label: str, songs: list, prefs: dict) -> None:
    """Print a labeled recommendation block for one user profile."""
    results = recommend_songs(prefs, songs, k=5)
    print(f"\n{'=' * 50}")
    print(f"Profile: {label}")
    print(f"  genre={prefs['favorite_genre']}, mood={prefs['favorite_mood']}, "
          f"energy={prefs['target_energy']}, acoustic={prefs['likes_acoustic']}")
    print(f"{'=' * 50}")
    for rank, (song, score, reasons) in enumerate(results, start=1):
        print(f"{rank}. {song['title']} by {song['artist']}  |  Score: {score:.2f}")
        for reason in reasons:
            print(f"   • {reason}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for label, prefs in PROFILES.items():
        print_recommendations(label, songs, prefs)


if __name__ == "__main__":
    main()
