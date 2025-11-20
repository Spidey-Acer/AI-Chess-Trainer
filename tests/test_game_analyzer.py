"""
Tests for GameAnalyzer class
"""

import pytest
from src.core.game_analyzer import GameAnalyzer, MistakeType


class TestGameAnalyzer:
    """Test cases for GameAnalyzer"""

    def test_initialization(self):
        """Test analyzer initialization"""
        analyzer = GameAnalyzer()
        assert analyzer is not None

    def test_classify_move(self):
        """Test move classification"""
        analyzer = GameAnalyzer()

        # Test blunder
        assert analyzer.classify_move(350) == MistakeType.BLUNDER

        # Test mistake
        assert analyzer.classify_move(150) == MistakeType.MISTAKE

        # Test inaccuracy
        assert analyzer.classify_move(75) == MistakeType.INACCURACY

        # Test good move
        assert analyzer.classify_move(20) == MistakeType.GOOD

        # Test excellent move
        assert analyzer.classify_move(-75) == MistakeType.EXCELLENT

    def test_player_statistics_calculation(self):
        """Test statistics calculation for a player"""
        analyzer = GameAnalyzer()

        # Mock player moves
        player_moves = [
            {"mistake_type": "blunder", "eval_loss": 300, "is_best_move": False},
            {"mistake_type": "good", "eval_loss": 10, "is_best_move": True},
            {"mistake_type": "mistake", "eval_loss": 120, "is_best_move": False},
            {"mistake_type": "excellent", "eval_loss": -50, "is_best_move": True},
        ]

        stats = analyzer._player_statistics(player_moves)

        assert stats["total_moves"] == 4
        assert stats["blunders"] == 1
        assert stats["mistakes"] == 1
        assert stats["best_moves"] == 2
