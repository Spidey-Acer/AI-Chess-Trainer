"""
Chess Trainer - Main AI training logic
"""

from typing import Dict, List, Optional
import random

from ..core import ChessEngine, GameAnalyzer, PositionEvaluator
from .feedback_generator import FeedbackGenerator
from .llm_integration import LLMIntegration


class ChessTrainer:
    """
    Main AI chess trainer providing personalized training experiences.
    """

    def __init__(
        self,
        engine: Optional[ChessEngine] = None,
        llm: Optional[LLMIntegration] = None,
    ):
        """
        Initialize the chess trainer.

        Args:
            engine: ChessEngine instance
            llm: LLMIntegration instance
        """
        self.engine = engine or ChessEngine()
        self.llm = llm or LLMIntegration()
        self.analyzer = GameAnalyzer(self.engine)
        self.evaluator = PositionEvaluator(self.engine)
        self.feedback_gen = FeedbackGenerator(self.llm)

        self.owns_engine = engine is None

    def __enter__(self):
        """Context manager entry."""
        if self.owns_engine:
            self.engine.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        if self.owns_engine:
            self.engine.stop()

    def analyze_game_with_feedback(self, pgn_path: str) -> Dict:
        """
        Analyze a game and generate comprehensive feedback.

        Args:
            pgn_path: Path to PGN file

        Returns:
            Dictionary with analysis and feedback
        """
        # Analyze the game
        game_analysis = self.analyzer.analyze_game_from_pgn(pgn_path)

        # Generate feedback
        feedback = self.feedback_gen.generate_game_feedback(game_analysis)

        return {
            "analysis": game_analysis,
            "feedback": feedback,
        }

    def generate_training_positions(
        self,
        game_analysis: Dict,
        position_type: str = "mistakes",
        count: int = 5,
    ) -> List[Dict]:
        """
        Generate training positions from analyzed game.

        Args:
            game_analysis: Game analysis from GameAnalyzer
            position_type: "mistakes", "critical", or "tactical"
            count: Number of positions to generate

        Returns:
            List of training position dictionaries
        """
        if position_type == "mistakes":
            # Get positions where player made mistakes
            mistake_moves = [
                m for m in game_analysis["moves"]
                if m["mistake_type"] in ["blunder", "mistake", "inaccuracy"]
            ]
            selected = random.sample(
                mistake_moves,
                min(count, len(mistake_moves))
            )

        elif position_type == "critical":
            # Get critical positions with big eval swings
            critical = self.analyzer.get_critical_positions(game_analysis)
            selected = random.sample(
                critical,
                min(count, len(critical))
            ) if critical else []

        else:  # tactical
            # Get positions that appear tactical
            tactical_positions = [
                m for m in game_analysis["moves"]
                if self.evaluator.is_tactical_position(m["fen_before"])
            ]
            selected = random.sample(
                tactical_positions,
                min(count, len(tactical_positions))
            )

        return selected

    def create_position_trainer(
        self,
        fen: str,
        objective: str = "find_best_move"
    ) -> Dict:
        """
        Create an interactive training position.

        Args:
            fen: Position in FEN notation
            objective: "find_best_move", "avoid_blunder", or "find_tactic"

        Returns:
            Training position dictionary
        """
        # Analyze the position
        position_eval = self.evaluator.evaluate_position(fen)
        top_moves = self.engine.get_top_moves(fen, num_moves=3)

        # Get AI explanation
        explanation = self.llm.explain_position(
            fen,
            position_eval,
            context=f"Objective: {objective}"
        )

        return {
            "fen": fen,
            "objective": objective,
            "evaluation": position_eval,
            "best_move": top_moves[0]["move"] if top_moves else None,
            "top_moves": top_moves,
            "explanation": explanation,
        }

    def check_move_solution(
        self,
        fen: str,
        player_move: str,
        best_move: str,
    ) -> Dict:
        """
        Check if player's move matches the best move or is acceptable.

        Args:
            fen: Position FEN
            player_move: Move played by user (UCI notation)
            best_move: Best move according to engine

        Returns:
            Dictionary with feedback on the move
        """
        # Check if move is legal
        if not self.engine.is_legal_move(player_move, fen):
            return {
                "correct": False,
                "reason": "illegal_move",
                "message": "This move is not legal in the current position.",
            }

        # Evaluate the player's move
        eval_before, eval_after = self.engine.evaluate_move(player_move, fen)

        # Get best move evaluation
        best_eval_before, best_eval_after = self.engine.evaluate_move(best_move, fen)

        # Calculate difference
        player_score = eval_after if eval_after else 0
        best_score = best_eval_after if best_eval_after else 0
        difference = abs(player_score - best_score)

        # Determine if move is acceptable
        if player_move == best_move:
            return {
                "correct": True,
                "reason": "best_move",
                "message": "Perfect! That's the best move.",
                "score_difference": 0,
            }
        elif difference <= 30:  # Within 0.3 pawns
            return {
                "correct": True,
                "reason": "acceptable",
                "message": "Good! This move is nearly as good as the best move.",
                "score_difference": difference,
                "best_move": best_move,
            }
        else:
            return {
                "correct": False,
                "reason": "suboptimal",
                "message": f"Not quite. The best move was {best_move}.",
                "score_difference": difference,
                "best_move": best_move,
            }

    def identify_weaknesses(self, game_analyses: List[Dict]) -> Dict:
        """
        Identify patterns of weaknesses across multiple games.

        Args:
            game_analyses: List of game analysis dictionaries

        Returns:
            Dictionary with identified weaknesses
        """
        if not game_analyses:
            return {"error": "No games provided"}

        # Aggregate statistics across all games
        total_blunders = 0
        total_mistakes = 0
        total_inaccuracies = 0
        total_moves = 0
        opening_errors = 0
        middlegame_errors = 0
        endgame_errors = 0

        for analysis in game_analyses:
            stats = analysis["statistics"]
            # Assuming we're analyzing for one player
            player_stats = stats.get("white", stats.get("black", {}))

            total_blunders += player_stats.get("blunders", 0)
            total_mistakes += player_stats.get("mistakes", 0)
            total_inaccuracies += player_stats.get("inaccuracies", 0)
            total_moves += player_stats.get("total_moves", 0)

        # Identify weaknesses
        weaknesses = []
        if total_blunders / len(game_analyses) > 2:
            weaknesses.append("Tactical oversight - frequent blunders")

        if total_mistakes / len(game_analyses) > 3:
            weaknesses.append("Calculation errors in complex positions")

        # Generate personalized recommendations
        study_plan = self.llm.generate_study_plan(
            weaknesses=weaknesses,
            strengths=["Persistence", "Willingness to learn"],
            goals="Improve overall chess strength"
        )

        return {
            "games_analyzed": len(game_analyses),
            "average_blunders": total_blunders / len(game_analyses),
            "average_mistakes": total_mistakes / len(game_analyses),
            "weaknesses": weaknesses,
            "study_plan": study_plan,
        }
