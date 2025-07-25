import json
import os
from datetime import datetime

class ScoreManager:
    """Manages scoring and leaderboard functionality"""
    
    def __init__(self, scores_file='scores.json'):
        self.scores_file = scores_file
        self.ensure_scores_file()
    
    def ensure_scores_file(self):
        """Create scores file if it doesn't exist"""
        if not os.path.exists(self.scores_file):
            with open(self.scores_file, 'w') as f:
                json.dump([], f)
    
    def calculate_points(self, level, time_taken):
        """
        Calculate points based on level difficulty and time taken
        
        Args:
            level (int): Current level/scenario number
            time_taken (float): Time in seconds to complete
            
        Returns:
            int: Points earned
        """
        # Base points by level (scenarios get harder = more points)
        base_points = 100 * level
        
        # Time bonus (faster = more points)
        if time_taken <= 5:
            time_bonus = 100  # Lightning fast!
        elif time_taken <= 10:
            time_bonus = 75   # Very fast
        elif time_taken <= 20:
            time_bonus = 50   # Fast
        elif time_taken <= 30:
            time_bonus = 25   # Decent
        else:
            time_bonus = 0    # No bonus for slow completion
        
        # Level difficulty multiplier
        difficulty_multipliers = {
            1: 1.0,   # Easy levels
            2: 1.0,
            3: 1.2,   # Medium levels
            4: 1.2,
            5: 1.5,   # Hard levels
            6: 1.5,
        }
        
        multiplier = difficulty_multipliers.get(level, 1.0)
        
        total_points = int((base_points + time_bonus) * multiplier)
        return total_points
    
    def save_score(self, player_name, final_score, levels_completed):
        """
        Save a player's final score to the leaderboard
        
        Args:
            player_name (str): Player's name
            final_score (int): Final score achieved
            levels_completed (int): Number of levels completed
        """
        try:
            with open(self.scores_file, 'r') as f:
                scores = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            scores = []
        
        new_score = {
            'player_name': player_name,
            'score': final_score,
            'levels_completed': levels_completed,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'rank': None  # Will be calculated when displaying
        }
        
        scores.append(new_score)
        
        # Sort by score (highest first)
        scores.sort(key=lambda x: x['score'], reverse=True)
        
        # Keep only top 50 scores
        scores = scores[:50]
        
        with open(self.scores_file, 'w') as f:
            json.dump(scores, f, indent=2)
    
    def get_top_scores(self, limit=10):
        """
        Get top scores for leaderboard
        
        Args:
            limit (int): Number of top scores to return
            
        Returns:
            list: Top scores with rank information
        """
        try:
            with open(self.scores_file, 'r') as f:
                scores = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
        
        # Add rank to each score
        for i, score in enumerate(scores[:limit], 1):
            score['rank'] = i
        
        return scores[:limit]
    
    def get_player_best_score(self, player_name):
        """Get a specific player's best score"""
        try:
            with open(self.scores_file, 'r') as f:
                scores = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return None
        
        player_scores = [s for s in scores if s['player_name'].lower() == player_name.lower()]
        
        if player_scores:
            return max(player_scores, key=lambda x: x['score'])
        
        return None
    
    def get_score_stats(self):
        """Get general statistics about all scores"""
        try:
            with open(self.scores_file, 'r') as f:
                scores = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {
                'total_players': 0,
                'average_score': 0,
                'highest_score': 0,
                'total_games': 0
            }
        
        if not scores:
            return {
                'total_players': 0,
                'average_score': 0,
                'highest_score': 0,
                'total_games': 0
            }
        
        unique_players = len(set(s['player_name'] for s in scores))
        average_score = sum(s['score'] for s in scores) / len(scores)
        highest_score = max(s['score'] for s in scores)
        
        return {
            'total_players': unique_players,
            'average_score': round(average_score, 1),
            'highest_score': highest_score,
            'total_games': len(scores)
        }
    
    def award_achievement(self, level, time_taken, score):
        """
        Check for and return any achievements earned
        
        Args:
            level (int): Level completed
            time_taken (float): Time to complete
            score (int): Current total score
            
        Returns:
            list: List of achievement names earned
        """
        achievements = []
        
        # Speed achievements
        if time_taken <= 3:
            achievements.append("Lightning Fingers ⚡")
        elif time_taken <= 5:
            achievements.append("Speed Demon 🏃")
        
        # Level achievements
        if level == 1:
            achievements.append("First Steps 👶")
        elif level == 3:
            achievements.append("Getting the Hang of It 🎯")
        elif level == 6:
            achievements.append("Permission Master 🏆")
        
        # Score achievements
        if score >= 1000:
            achievements.append("Point Collector 💎")
        elif score >= 2000:
            achievements.append("High Achiever 🌟")
        
        return achievements