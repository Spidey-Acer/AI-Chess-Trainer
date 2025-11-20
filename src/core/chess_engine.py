"""
Chess Engine Wrapper - Interface to Stockfish and chess logic
"""

import os
from typing import Optional, List, Dict, Tuple
import chess
import chess.engine
from dotenv import load_dotenv

load_dotenv()


class ChessEngine:
    """
    Wrapper for chess engine (Stockfish) providing analysis capabilities.
    """

    def __init__(self, engine_path: Optional[str] = None, depth: int = 20):
        """
        Initialize the chess engine.

        Args:
            engine_path: Path to Stockfish binary. If None, uses STOCKFISH_PATH from .env
            depth: Analysis depth (default: 20)
        """
        self.engine_path = engine_path or os.getenv("STOCKFISH_PATH", "stockfish")
        self.depth = depth
        self.engine: Optional[chess.engine.SimpleEngine] = None
        self.board = chess.Board()

    def start(self) -> None:
        """Start the chess engine."""
        try:
            self.engine = chess.engine.SimpleEngine.popen_uci(self.engine_path)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Stockfish engine not found at: {self.engine_path}. "
                "Please download Stockfish and set STOCKFISH_PATH in .env"
            )

    def stop(self) -> None:
        """Stop the chess engine."""
        if self.engine:
            self.engine.quit()
            self.engine = None

    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()

    def set_position(self, fen: str) -> None:
        """
        Set the current board position from FEN notation.

        Args:
            fen: Position in Forsyth-Edwards Notation
        """
        self.board = chess.Board(fen)

    def set_position_from_moves(self, moves: List[str]) -> None:
        """
        Set position by playing a sequence of moves from the starting position.

        Args:
            moves: List of moves in UCI notation (e.g., ['e2e4', 'e7e5'])
        """
        self.board = chess.Board()
        for move in moves:
            self.board.push_uci(move)

    def analyze_position(
        self, fen: Optional[str] = None, depth: Optional[int] = None
    ) -> Dict:
        """
        Analyze the current position and return evaluation.

        Args:
            fen: Optional FEN string. If provided, analyzes this position.
            depth: Optional analysis depth. Uses instance depth if not provided.

        Returns:
            Dictionary with analysis results including score, best move, and variations
        """
        if not self.engine:
            raise RuntimeError("Engine not started. Call start() first or use context manager.")

        if fen:
            self.set_position(fen)

        analysis_depth = depth or self.depth
        info = self.engine.analyse(self.board, chess.engine.Limit(depth=analysis_depth))

        # Extract score from perspective of side to move
        score = info.get("score")
        if score:
            score_cp = score.relative.score(mate_score=10000)  # Convert to centipawns
        else:
            score_cp = None

        return {
            "fen": self.board.fen(),
            "score": score_cp,
            "best_move": info.get("pv", [None])[0],
            "pv": info.get("pv", []),  # Principal variation
            "depth": info.get("depth"),
            "nodes": info.get("nodes"),
        }

    def get_top_moves(
        self, fen: Optional[str] = None, num_moves: int = 3, depth: Optional[int] = None
    ) -> List[Dict]:
        """
        Get the top N moves for the current position.

        Args:
            fen: Optional FEN string
            num_moves: Number of top moves to return (default: 3)
            depth: Optional analysis depth

        Returns:
            List of dictionaries with move and evaluation
        """
        if not self.engine:
            raise RuntimeError("Engine not started. Call start() first or use context manager.")

        if fen:
            self.set_position(fen)

        analysis_depth = depth or self.depth
        info_list = self.engine.analyse(
            self.board,
            chess.engine.Limit(depth=analysis_depth),
            multipv=num_moves,
        )

        results = []
        for info in info_list:
            score = info.get("score")
            score_cp = score.relative.score(mate_score=10000) if score else None

            results.append({
                "move": info.get("pv", [None])[0],
                "score": score_cp,
                "pv": info.get("pv", []),
            })

        return results

    def evaluate_move(
        self, move: str, fen: Optional[str] = None
    ) -> Tuple[float, float]:
        """
        Evaluate a specific move by comparing position before and after.

        Args:
            move: Move in UCI notation (e.g., 'e2e4')
            fen: Optional starting position FEN

        Returns:
            Tuple of (score_before, score_after) in centipawns from current player's perspective
        """
        if fen:
            self.set_position(fen)

        # Analyze before move
        before_analysis = self.analyze_position()
        score_before = before_analysis["score"]

        # Make move and analyze
        self.board.push_uci(move)
        after_analysis = self.analyze_position()
        score_after = -after_analysis["score"] if after_analysis["score"] else None

        # Undo move
        self.board.pop()

        return score_before, score_after

    def is_legal_move(self, move: str, fen: Optional[str] = None) -> bool:
        """
        Check if a move is legal in the current position.

        Args:
            move: Move in UCI notation
            fen: Optional position FEN

        Returns:
            True if move is legal
        """
        if fen:
            self.set_position(fen)

        try:
            chess_move = chess.Move.from_uci(move)
            return chess_move in self.board.legal_moves
        except (ValueError, chess.InvalidMoveError):
            return False

    def get_legal_moves(self, fen: Optional[str] = None) -> List[str]:
        """
        Get all legal moves in the current position.

        Args:
            fen: Optional position FEN

        Returns:
            List of legal moves in UCI notation
        """
        if fen:
            self.set_position(fen)

        return [move.uci() for move in self.board.legal_moves]

    def is_game_over(self, fen: Optional[str] = None) -> bool:
        """
        Check if the game is over.

        Args:
            fen: Optional position FEN

        Returns:
            True if game is over (checkmate, stalemate, etc.)
        """
        if fen:
            self.set_position(fen)

        return self.board.is_game_over()

    def get_game_result(self, fen: Optional[str] = None) -> Optional[str]:
        """
        Get the game result if game is over.

        Args:
            fen: Optional position FEN

        Returns:
            "1-0" (white wins), "0-1" (black wins), "1/2-1/2" (draw), or None
        """
        if fen:
            self.set_position(fen)

        if not self.board.is_game_over():
            return None

        result = self.board.result()
        return result
