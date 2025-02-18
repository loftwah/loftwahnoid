import json
import os

class HighScoreManager:
    def __init__(self):
        self.scores_file = os.path.join(os.path.dirname(__file__), '../../highscores.json')
        self.high_scores = self._load_scores()

    def _load_scores(self):
        try:
            with open(self.scores_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_scores(self):
        with open(self.scores_file, 'w') as f:
            json.dump(self.high_scores, f)

    def add_score(self, name, score, level):
        entry = {"name": name, "score": score, "level": level}
        self.high_scores.append(entry)
        self.high_scores.sort(key=lambda x: x["score"], reverse=True)
        self.high_scores = self.high_scores[:10]  # Keep only top 10
        self._save_scores()

    def get_high_scores(self):
        return self.high_scores 