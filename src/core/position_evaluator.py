"""
Position Evaluator - Provides detailed position evaluation and insights
"""

from typing import Dict, List, Optional
import chess
from .chess_engine import ChessEngine


class PositionEvaluator:
    """
    Evaluates chess positions and provides insights beyond raw engine evaluation.
    """

    def __init__(self, engine: Optional[ChessEngine] = None):
        """
        Initialize the position evaluator.

        Args:
            engine: ChessEngine instance. If None, creates a new one.
        """
        self.engine = engine or ChessEngine()
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

    def evaluate_position(self, fen: str, depth: Optional[int] = None) -> Dict:
        """
        Comprehensive position evaluation.

        Args:
            fen: Position in FEN notation
            depth: Analysis depth (optional)

        Returns:
            Dictionary with evaluation metrics
        """
        board = chess.Board(fen)

        # Get engine evaluation
        engine_eval = self.engine.analyze_position(fen, depth)

        # Material count
        material = self._count_material(board)

        # Tactical features
        tactics = self._detect_tactical_features(board)

        # Game phase
        phase = self._determine_game_phase(board)

        return {
            "engine_evaluation": engine_eval,
            "material": material,
            "material_balance": material["white_total"] - material["black_total"],
            "tactical_features": tactics,
            "game_phase": phase,
            "side_to_move": "white" if board.turn == chess.WHITE else "black",
            "is_check": board.is_check(),
            "is_checkmate": board.is_checkmate(),
            "is_stalemate": board.is_stalemate(),
            "legal_moves_count": len(list(board.legal_moves)),
        }

    def _count_material(self, board: chess.Board) -> Dict:
        """
        Count material for both sides.

        Args:
            board: Chess board

        Returns:
            Dictionary with material counts
        """
        piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0,
        }

        white_material = {}
        black_material = {}

        for piece_type in [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]:
            white_count = len(board.pieces(piece_type, chess.WHITE))
            black_count = len(board.pieces(piece_type, chess.BLACK))

            white_material[chess.piece_name(piece_type)] = white_count
            black_material[chess.piece_name(piece_type)] = black_count

        white_total = sum(
            piece_values[pt] * len(board.pieces(pt, chess.WHITE))
            for pt in piece_values.keys()
        )
        black_total = sum(
            piece_values[pt] * len(board.pieces(pt, chess.BLACK))
            for pt in piece_values.keys()
        )

        return {
            "white": white_material,
            "black": black_material,
            "white_total": white_total,
            "black_total": black_total,
        }

    def _detect_tactical_features(self, board: chess.Board) -> Dict:
        """
        Detect tactical features in the position.

        Args:
            board: Chess board

        Returns:
            Dictionary with tactical features
        """
        features = {
            "has_check": board.is_check(),
            "is_checkmate": board.is_checkmate(),
            "is_stalemate": board.is_stalemate(),
            "has_en_passant": board.has_legal_en_passant(),
            "can_castle_kingside": board.has_kingside_castling_rights(board.turn),
            "can_castle_queenside": board.has_queenside_castling_rights(board.turn),
        }

        # Count attacked pieces
        attacked_pieces = self._count_attacked_pieces(board)
        features["attacked_pieces"] = attacked_pieces

        return features

    def _count_attacked_pieces(self, board: chess.Board) -> Dict:
        """
        Count pieces under attack for each side.

        Args:
            board: Chess board

        Returns:
            Dictionary with attack information
        """
        white_attacked = 0
        black_attacked = 0

        # Check each square
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is None:
                continue

            # Check if this piece is attacked by the opponent
            if piece.color == chess.WHITE:
                if board.is_attacked_by(chess.BLACK, square):
                    white_attacked += 1
            else:
                if board.is_attacked_by(chess.WHITE, square):
                    black_attacked += 1

        return {
            "white_pieces_attacked": white_attacked,
            "black_pieces_attacked": black_attacked,
        }

    def _determine_game_phase(self, board: chess.Board) -> str:
        """
        Determine the current game phase.

        Args:
            board: Chess board

        Returns:
            Game phase: "opening", "middlegame", or "endgame"
        """
        move_count = board.fullmove_number

        # Count major and minor pieces
        total_pieces = 0
        for piece_type in [chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]:
            total_pieces += len(board.pieces(piece_type, chess.WHITE))
            total_pieces += len(board.pieces(piece_type, chess.BLACK))

        # Simple heuristic
        if move_count < 10:
            return "opening"
        elif total_pieces <= 6:  # Few pieces left
            return "endgame"
        else:
            return "middlegame"

    def compare_positions(self, fen1: str, fen2: str) -> Dict:
        """
        Compare two chess positions.

        Args:
            fen1: First position (FEN)
            fen2: Second position (FEN)

        Returns:
            Dictionary with comparison metrics
        """
        eval1 = self.evaluate_position(fen1)
        eval2 = self.evaluate_position(fen2)

        return {
            "position1": eval1,
            "position2": eval2,
            "material_difference": (
                eval2["material_balance"] - eval1["material_balance"]
            ),
            "evaluation_difference": (
                eval2["engine_evaluation"]["score"] - eval1["engine_evaluation"]["score"]
                if eval1["engine_evaluation"]["score"] and eval2["engine_evaluation"]["score"]
                else None
            ),
        }

    def is_tactical_position(self, fen: str) -> bool:
        """
        Determine if a position is tactical (has forcing moves, threats, etc.)

        Args:
            fen: Position in FEN notation

        Returns:
            True if position appears tactical
        """
        board = chess.Board(fen)
        features = self._detect_tactical_features(board)

        # Consider position tactical if:
        # - There's a check
        # - Many pieces are under attack
        # - It's checkmate or stalemate
        is_tactical = (
            features["has_check"]
            or features["is_checkmate"]
            or features["attacked_pieces"]["white_pieces_attacked"] >= 3
            or features["attacked_pieces"]["black_pieces_attacked"] >= 3
        )

        return is_tactical
