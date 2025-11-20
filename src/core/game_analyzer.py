"""
Game Analyzer - Analyzes chess games and identifies mistakes
"""

from typing import List, Dict, Optional, Tuple
import chess.pgn
from enum import Enum
import os
from dotenv import load_dotenv

from .chess_engine import ChessEngine

load_dotenv()


class MistakeType(Enum):
    """Classification of move mistakes"""
    BLUNDER = "blunder"
    MISTAKE = "mistake"
    INACCURACY = "inaccuracy"
    GOOD = "good"
    EXCELLENT = "excellent"


class GameAnalyzer:
    """
    Analyzes complete chess games and provides move-by-move evaluation.
    """

    def __init__(self, engine: Optional[ChessEngine] = None):
        """
        Initialize the game analyzer.

        Args:
            engine: ChessEngine instance. If None, creates a new one.
        """
        self.engine = engine or ChessEngine()
        self.owns_engine = engine is None

        # Load thresholds from environment or use defaults (in centipawns)
        self.blunder_threshold = int(os.getenv("BLUNDER_THRESHOLD", "300"))
        self.mistake_threshold = int(os.getenv("MISTAKE_THRESHOLD", "100"))
        self.inaccuracy_threshold = int(os.getenv("INACCURACY_THRESHOLD", "50"))

    def __enter__(self):
        """Context manager entry."""
        if self.owns_engine:
            self.engine.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        if self.owns_engine:
            self.engine.stop()

    def classify_move(self, eval_loss: float) -> MistakeType:
        """
        Classify a move based on evaluation loss.

        Args:
            eval_loss: Loss in centipawns (positive = worse position)

        Returns:
            MistakeType classification
        """
        if eval_loss >= self.blunder_threshold:
            return MistakeType.BLUNDER
        elif eval_loss >= self.mistake_threshold:
            return MistakeType.MISTAKE
        elif eval_loss >= self.inaccuracy_threshold:
            return MistakeType.INACCURACY
        elif eval_loss < -50:  # Improved position significantly
            return MistakeType.EXCELLENT
        else:
            return MistakeType.GOOD

    def analyze_move(
        self, fen: str, move: str, move_number: int, player: str
    ) -> Dict:
        """
        Analyze a single move in detail.

        Args:
            fen: Position before the move (FEN notation)
            move: The move played (UCI notation)
            move_number: Move number in the game
            player: "white" or "black"

        Returns:
            Dictionary with detailed move analysis
        """
        # Get best move and evaluation before the move
        before_analysis = self.engine.analyze_position(fen)
        best_move = before_analysis["best_move"]
        eval_before = before_analysis["score"]

        # Evaluate the move actually played
        eval_before_played, eval_after_played = self.engine.evaluate_move(move, fen)

        # Calculate evaluation loss
        eval_loss = eval_before - eval_after_played if eval_after_played is not None else 0

        # Classify the move
        mistake_type = self.classify_move(eval_loss)

        # Get top 3 moves for comparison
        top_moves = self.engine.get_top_moves(fen, num_moves=3)

        return {
            "move_number": move_number,
            "player": player,
            "move_played": move,
            "best_move": str(best_move) if best_move else None,
            "eval_before": eval_before,
            "eval_after": eval_after_played,
            "eval_loss": eval_loss,
            "mistake_type": mistake_type.value,
            "is_best_move": move == str(best_move) if best_move else False,
            "top_moves": top_moves,
            "fen_before": fen,
        }

    def analyze_game_from_pgn(self, pgn_path: str) -> Dict:
        """
        Analyze a complete game from a PGN file.

        Args:
            pgn_path: Path to PGN file

        Returns:
            Dictionary with complete game analysis
        """
        with open(pgn_path, "r") as pgn_file:
            game = chess.pgn.read_game(pgn_file)

        if not game:
            raise ValueError("No valid game found in PGN file")

        return self.analyze_game(game)

    def analyze_game(self, game: chess.pgn.Game) -> Dict:
        """
        Analyze a complete chess game.

        Args:
            game: chess.pgn.Game object

        Returns:
            Dictionary with complete game analysis including:
            - Game metadata
            - Move-by-move analysis
            - Statistics and summary
        """
        board = game.board()
        moves_analysis = []
        move_number = 1

        # Analyze each move
        for move in game.mainline_moves():
            fen_before = board.fen()
            player = "white" if board.turn == chess.WHITE else "black"

            move_analysis = self.analyze_move(
                fen_before,
                move.uci(),
                move_number if player == "white" else move_number,
                player,
            )

            moves_analysis.append(move_analysis)

            board.push(move)

            # Increment move number after black's move
            if player == "black":
                move_number += 1

        # Calculate statistics
        stats = self._calculate_statistics(moves_analysis)

        return {
            "metadata": {
                "event": game.headers.get("Event", "Unknown"),
                "white": game.headers.get("White", "Unknown"),
                "black": game.headers.get("Black", "Unknown"),
                "result": game.headers.get("Result", "*"),
                "date": game.headers.get("Date", "Unknown"),
            },
            "moves": moves_analysis,
            "statistics": stats,
            "total_moves": len(moves_analysis),
        }

    def _calculate_statistics(self, moves_analysis: List[Dict]) -> Dict:
        """
        Calculate game statistics from move analysis.

        Args:
            moves_analysis: List of move analysis dictionaries

        Returns:
            Dictionary with statistics for white and black
        """
        white_stats = self._player_statistics(
            [m for m in moves_analysis if m["player"] == "white"]
        )
        black_stats = self._player_statistics(
            [m for m in moves_analysis if m["player"] == "black"]
        )

        return {
            "white": white_stats,
            "black": black_stats,
        }

    def _player_statistics(self, player_moves: List[Dict]) -> Dict:
        """
        Calculate statistics for a single player.

        Args:
            player_moves: List of moves for one player

        Returns:
            Dictionary with player statistics
        """
        if not player_moves:
            return {}

        total_moves = len(player_moves)
        blunders = sum(1 for m in player_moves if m["mistake_type"] == "blunder")
        mistakes = sum(1 for m in player_moves if m["mistake_type"] == "mistake")
        inaccuracies = sum(1 for m in player_moves if m["mistake_type"] == "inaccuracy")
        good_moves = sum(1 for m in player_moves if m["mistake_type"] == "good")
        excellent_moves = sum(1 for m in player_moves if m["mistake_type"] == "excellent")
        best_moves = sum(1 for m in player_moves if m["is_best_move"])

        # Calculate average centipawn loss (ACPL)
        total_loss = sum(m["eval_loss"] for m in player_moves)
        acpl = total_loss / total_moves if total_moves > 0 else 0

        # Calculate accuracy percentage
        # Accuracy = 100% if no loss, decreases with eval loss
        accuracies = []
        for move in player_moves:
            loss = max(0, move["eval_loss"])
            accuracy = max(0, 100 - (loss / 10))  # Each 10cp loss = 1% accuracy
            accuracies.append(accuracy)

        avg_accuracy = sum(accuracies) / len(accuracies) if accuracies else 0

        return {
            "total_moves": total_moves,
            "blunders": blunders,
            "mistakes": mistakes,
            "inaccuracies": inaccuracies,
            "good_moves": good_moves,
            "excellent_moves": excellent_moves,
            "best_moves": best_moves,
            "best_move_percentage": (best_moves / total_moves * 100) if total_moves > 0 else 0,
            "average_centipawn_loss": acpl,
            "accuracy": round(avg_accuracy, 1),
        }

    def get_critical_positions(
        self, game_analysis: Dict, threshold: int = 200
    ) -> List[Dict]:
        """
        Extract critical positions where evaluation changed significantly.

        Args:
            game_analysis: Complete game analysis from analyze_game()
            threshold: Minimum eval change to consider position critical (centipawns)

        Returns:
            List of critical position dictionaries
        """
        critical = []

        for move in game_analysis["moves"]:
            if abs(move["eval_loss"]) >= threshold:
                critical.append({
                    "move_number": move["move_number"],
                    "player": move["player"],
                    "fen": move["fen_before"],
                    "move_played": move["move_played"],
                    "best_move": move["best_move"],
                    "eval_loss": move["eval_loss"],
                    "mistake_type": move["mistake_type"],
                })

        return critical
