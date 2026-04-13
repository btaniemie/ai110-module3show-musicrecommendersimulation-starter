"""
Command line runner for the Music Recommender Simulation.
Run with:  python -m src.main
"""

from src.recommender import load_songs, recommend_songs


PROFILES = {
    "High-Energy Pop": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.85,
        "valence": 0.82,
    },
    "Chill Lofi": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.38,
        "valence": 0.58,
    },
    "Deep Intense Rock": {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.92,
        "valence": 0.35,
    },
    "Adversarial (conflicting prefs)": {
        # High energy but melancholic mood — tests whether scoring handles tension
        "genre": "jazz",
        "mood": "happy",
        "energy": 0.90,
        "valence": 0.75,
    },
}


def print_recommendations(profile_name: str, recs, top_k: int = 5) -> None:
    """Print a formatted block of recommendations for one user profile."""
    print(f"\n{'='*60}")
    print(f"  Profile: {profile_name}")
    print(f"{'='*60}")
    for rank, (song, score, explanation) in enumerate(recs[:top_k], start=1):
        print(f"\n  #{rank}  {song['title']} by {song['artist']}")
        print(f"       Score : {score:.2f}")
        print(f"       Why   : {explanation}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for profile_name, user_prefs in PROFILES.items():
        recs = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(profile_name, recs)


if __name__ == "__main__":
    main()
