"""
Feedback Generator - Generates personalized training feedback
"""

from typing import Dict, List, Optional
from collections import Counter

from .llm_integration import LLMIntegration


class FeedbackGenerator:
    """
    Generates personalized feedback based on game analysis.
    """

    def __init__(self, llm: Optional[LLMIntegration] = None):
        """
        Initialize feedback generator.

        Args:
            llm: LLMIntegration instance for AI-powered feedback
        """
        self.llm = llm or LLMIntegration()

    def generate_game_feedback(self, game_analysis: Dict) -> Dict:
        """
        Generate comprehensive feedback for a complete game.

        Args:
            game_analysis: Complete game analysis from GameAnalyzer

        Returns:
            Dictionary with feedback for both players
        """
        white_feedback = self._generate_player_feedback(
            game_analysis, "white"
        )
        black_feedback = self._generate_player_feedback(
            game_analysis, "black"
        )

        # Get AI summary
        ai_summary = self.llm.summarize_game(game_analysis)

        return {
            "white": white_feedback,
            "black": black_feedback,
            "ai_summary": ai_summary,
            "game_metadata": game_analysis["metadata"],
        }

    def _generate_player_feedback(
        self, game_analysis: Dict, player: str
    ) -> Dict:
        """
        Generate feedback for a specific player.

        Args:
            game_analysis: Complete game analysis
            player: "white" or "black"

        Returns:
            Dictionary with player feedback
        """
        stats = game_analysis["statistics"][player]
        player_moves = [m for m in game_analysis["moves"] if m["player"] == player]

        # Identify patterns
        patterns = self._identify_patterns(player_moves)

        # Get worst mistakes
        worst_mistakes = self._get_worst_mistakes(player_moves, limit=3)

        # Get best moves
        best_moves = self._get_best_moves(player_moves, limit=3)

        # Generate improvement suggestions
        suggestions = self._generate_suggestions(stats, patterns)

        return {
            "statistics": stats,
            "patterns": patterns,
            "worst_mistakes": worst_mistakes,
            "best_moves": best_moves,
            "suggestions": suggestions,
            "overall_assessment": self._assess_performance(stats),
        }

    def _identify_patterns(self, player_moves: List[Dict]) -> Dict:
        """
        Identify patterns in a player's moves.

        Args:
            player_moves: List of moves for one player

        Returns:
            Dictionary with identified patterns
        """
        # Analyze mistake types distribution
        mistake_types = Counter(m["mistake_type"] for m in player_moves)

        # Analyze by game phase (rough approximation)
        opening_moves = player_moves[:10] if len(player_moves) >= 10 else player_moves
        middle_moves = player_moves[10:25] if len(player_moves) >= 25 else []
        endgame_moves = player_moves[25:] if len(player_moves) > 25 else []

        opening_accuracy = (
            sum(1 for m in opening_moves if m["mistake_type"] in ["good", "excellent"])
            / len(opening_moves) * 100
            if opening_moves
            else 0
        )

        middle_accuracy = (
            sum(1 for m in middle_moves if m["mistake_type"] in ["good", "excellent"])
            / len(middle_moves) * 100
            if middle_moves
            else 0
        )

        endgame_accuracy = (
            sum(1 for m in endgame_moves if m["mistake_type"] in ["good", "excellent"])
            / len(endgame_moves) * 100
            if endgame_moves
            else 0
        )

        return {
            "mistake_distribution": dict(mistake_types),
            "opening_accuracy": round(opening_accuracy, 1),
            "middlegame_accuracy": round(middle_accuracy, 1),
            "endgame_accuracy": round(endgame_accuracy, 1),
            "weakest_phase": self._identify_weakest_phase(
                opening_accuracy, middle_accuracy, endgame_accuracy
            ),
        }

    def _identify_weakest_phase(
        self, opening: float, middle: float, endgame: float
    ) -> str:
        """Identify the weakest game phase."""
        phases = {"opening": opening, "middlegame": middle, "endgame": endgame}
        # Filter out phases with 0 (no moves in that phase)
        phases = {k: v for k, v in phases.items() if v > 0}
        if not phases:
            return "unknown"
        return min(phases, key=phases.get)

    def _get_worst_mistakes(self, player_moves: List[Dict], limit: int = 3) -> List[Dict]:
        """
        Get the worst mistakes in the game.

        Args:
            player_moves: List of player's moves
            limit: Maximum number to return

        Returns:
            List of worst mistakes
        """
        # Sort by eval loss (descending)
        sorted_moves = sorted(
            player_moves,
            key=lambda m: m["eval_loss"],
            reverse=True
        )

        # Get top mistakes (blunders and mistakes)
        worst = [
            m for m in sorted_moves
            if m["mistake_type"] in ["blunder", "mistake"]
        ][:limit]

        return [
            {
                "move_number": m["move_number"],
                "move": m["move_played"],
                "best_move": m["best_move"],
                "eval_loss": m["eval_loss"],
                "mistake_type": m["mistake_type"],
                "fen": m["fen_before"],
            }
            for m in worst
        ]

    def _get_best_moves(self, player_moves: List[Dict], limit: int = 3) -> List[Dict]:
        """
        Get the best moves in the game.

        Args:
            player_moves: List of player's moves
            limit: Maximum number to return

        Returns:
            List of best moves
        """
        # Get excellent moves or moves that improved position significantly
        excellent = [
            m for m in player_moves
            if m["mistake_type"] == "excellent" or m["is_best_move"]
        ]

        # Sort by eval improvement (negative loss = improvement)
        sorted_excellent = sorted(
            excellent,
            key=lambda m: m["eval_loss"]
        )[:limit]

        return [
            {
                "move_number": m["move_number"],
                "move": m["move_played"],
                "eval_gain": -m["eval_loss"],  # Negative loss = gain
                "fen": m["fen_before"],
            }
            for m in sorted_excellent
        ]

    def _generate_suggestions(self, stats: Dict, patterns: Dict) -> List[str]:
        """
        Generate improvement suggestions based on statistics and patterns.

        Args:
            stats: Player statistics
            patterns: Identified patterns

        Returns:
            List of suggestion strings
        """
        suggestions = []

        # Overall accuracy feedback
        accuracy = stats["accuracy"]
        if accuracy < 70:
            suggestions.append(
                "Focus on calculating moves more carefully before playing. "
                "Take your time to look for tactical threats."
            )
        elif accuracy < 85:
            suggestions.append(
                "Good overall accuracy! Work on reducing blunders to reach the next level."
            )
        else:
            suggestions.append(
                "Excellent accuracy! You're playing very precisely."
            )

        # Blunder-specific feedback
        if stats["blunders"] > 2:
            suggestions.append(
                f"You made {stats['blunders']} blunders in this game. "
                "Before each move, check: Is any piece hanging? Are there any checks or captures?"
            )

        # Phase-specific feedback
        weakest = patterns["weakest_phase"]
        if weakest == "opening":
            suggestions.append(
                "Your opening needs work. Study opening principles: "
                "control the center, develop pieces, castle early."
            )
        elif weakest == "middlegame":
            suggestions.append(
                "Focus on middlegame strategy: creating plans, identifying weaknesses, "
                "improving piece positions."
            )
        elif weakest == "endgame":
            suggestions.append(
                "Practice endgame techniques: king activation, pawn promotion, "
                "opposition in king and pawn endgames."
            )

        # ACPL feedback
        acpl = stats["average_centipawn_loss"]
        if acpl > 100:
            suggestions.append(
                "Your average centipawn loss is high. Practice tactics puzzles "
                "to improve your calculation skills."
            )

        return suggestions

    def _assess_performance(self, stats: Dict) -> str:
        """
        Provide an overall performance assessment.

        Args:
            stats: Player statistics

        Returns:
            Assessment string
        """
        accuracy = stats["accuracy"]
        blunders = stats["blunders"]

        if accuracy >= 90 and blunders == 0:
            return "Excellent"
        elif accuracy >= 85 and blunders <= 1:
            return "Very Good"
        elif accuracy >= 75:
            return "Good"
        elif accuracy >= 65:
            return "Fair"
        else:
            return "Needs Improvement"

    def explain_critical_position(
        self, position_dict: Dict, player_level: str = "intermediate"
    ) -> str:
        """
        Generate detailed explanation for a critical position.

        Args:
            position_dict: Critical position dictionary
            player_level: Player skill level

        Returns:
            Detailed explanation
        """
        # Build a more detailed analysis for the LLM
        move_analysis = {
            "move_played": position_dict["move_played"],
            "best_move": position_dict["best_move"],
            "eval_loss": position_dict["eval_loss"],
            "mistake_type": position_dict["mistake_type"],
            "fen_before": position_dict["fen"],
        }

        return self.llm.explain_mistake(move_analysis, player_level)
