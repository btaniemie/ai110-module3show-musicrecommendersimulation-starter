import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass, field


@dataclass
class Song:
    """Represents a song and its audio feature attributes."""
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
    """Represents a user's musical taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    target_valence: float = 0.7


class Recommender:
    """OOP wrapper around the scoring and ranking logic."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Score every song against the user profile and return the top k sorted by score."""
        scored = []
        for song in self.songs:
            score = 0.0
            if song.genre == user.favorite_genre:
                score += 2.0
            if song.mood == user.favorite_mood:
                score += 1.0
            score += 1.5 * (1.0 - abs(song.energy - user.target_energy))
            score += 1.0 * (1.0 - abs(song.valence - user.target_valence))
            scored.append((score, song))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [song for _, song in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a plain-language string explaining why a song was recommended."""
        reasons = []
        if song.genre == user.favorite_genre:
            reasons.append(f"genre match ({song.genre})")
        if song.mood == user.favorite_mood:
            reasons.append(f"mood match ({song.mood})")
        energy_gap = abs(song.energy - user.target_energy)
        reasons.append(f"energy closeness ({1.0 - energy_gap:.2f})")
        valence_gap = abs(song.valence - user.target_valence)
        reasons.append(f"valence closeness ({1.0 - valence_gap:.2f})")
        return "; ".join(reasons)


def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv and return a list of dicts with numeric fields cast to float/int."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": int(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a single song against user preferences; returns (total_score, reasons)."""
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs.get("genre", ""):
        score += 2.0
        reasons.append(f"genre match (+2.0)")

    if song["mood"] == user_prefs.get("mood", ""):
        score += 1.0
        reasons.append(f"mood match (+1.0)")

    target_energy = user_prefs.get("energy", 0.5)
    energy_points = 1.5 * (1.0 - abs(song["energy"] - target_energy))
    score += energy_points
    reasons.append(f"energy proximity (+{energy_points:.2f})")

    target_valence = user_prefs.get("valence", 0.7)
    valence_points = 1.0 * (1.0 - abs(song["valence"] - target_valence))
    score += valence_points
    reasons.append(f"valence proximity (+{valence_points:.2f})")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort highest to lowest, and return the top k as (song, score, explanation)."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = " | ".join(reasons)
        scored.append((song, score, explanation))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
