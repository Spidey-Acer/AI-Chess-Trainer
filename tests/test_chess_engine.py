"""
Tests for ChessEngine class
"""

import pytest
import chess
from src.core.chess_engine import ChessEngine


class TestChessEngine:
    """Test cases for ChessEngine"""

    @pytest.fixture
    def engine(self):
        """Create a ChessEngine instance for testing"""
        # Note: These tests will be skipped if Stockfish is not installed
        try:
            engine = ChessEngine()
            engine.start()
            yield engine
            engine.stop()
        except FileNotFoundError:
            pytest.skip("Stockfish not installed")

    def test_engine_initialization(self):
        """Test that engine can be initialized"""
        engine = ChessEngine()
        assert engine is not None
        assert engine.depth == 20

    def test_set_position(self, engine):
        """Test setting a position from FEN"""
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        engine.set_position(fen)
        assert engine.board.fen() == fen

    def test_analyze_starting_position(self, engine):
        """Test analysis of starting position"""
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        analysis = engine.analyze_position(fen, depth=10)

        assert "score" in analysis
        assert "best_move" in analysis
        assert analysis["fen"] == fen

    def test_legal_moves(self, engine):
        """Test getting legal moves"""
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        moves = engine.get_legal_moves(fen)

        assert len(moves) == 20  # Starting position has 20 legal moves
        assert "e2e4" in moves
        assert "d2d4" in moves

    def test_is_legal_move(self, engine):
        """Test move legality checking"""
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

        assert engine.is_legal_move("e2e4", fen) is True
        assert engine.is_legal_move("e2e5", fen) is False

    def test_evaluate_move(self, engine):
        """Test move evaluation"""
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        before, after = engine.evaluate_move("e2e4", fen)

        assert before is not None
        assert after is not None

    def test_context_manager(self):
        """Test using engine as context manager"""
        try:
            with ChessEngine() as engine:
                assert engine.engine is not None
                fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
                moves = engine.get_legal_moves(fen)
                assert len(moves) == 20
        except FileNotFoundError:
            pytest.skip("Stockfish not installed")
