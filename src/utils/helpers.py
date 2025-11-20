"""
Helper utility functions
"""

from typing import Optional
import chess


def format_move(move: chess.Move, board: Optional[chess.Board] = None) -> str:
    """
    Format a move in algebraic notation.

    Args:
        move: Chess move
        board: Optional board for SAN notation

    Returns:
        Formatted move string
    """
    if board:
        return board.san(move)
    else:
        return move.uci()


def format_score(score_cp: Optional[int]) -> str:
    """
    Format an evaluation score in a human-readable way.

    Args:
        score_cp: Score in centipawns

    Returns:
        Formatted score string
    """
    if score_cp is None:
        return "N/A"

    if abs(score_cp) >= 10000:
        # Mate score
        mate_in = (10000 - abs(score_cp)) // 2
        return f"M{mate_in}" if score_cp > 0 else f"-M{mate_in}"

    # Regular score in pawns
    score_pawns = score_cp / 100
    return f"{score_pawns:+.2f}"


def parse_time(time_str: str) -> int:
    """
    Parse time string to seconds.

    Args:
        time_str: Time string (e.g., "5m", "30s", "1h30m")

    Returns:
        Time in seconds
    """
    total_seconds = 0

    # Parse hours
    if "h" in time_str:
        hours, time_str = time_str.split("h")
        total_seconds += int(hours) * 3600

    # Parse minutes
    if "m" in time_str:
        minutes, time_str = time_str.split("m")
        total_seconds += int(minutes) * 60

    # Parse seconds
    if "s" in time_str:
        seconds = time_str.replace("s", "")
        if seconds:
            total_seconds += int(seconds)

    return total_seconds or 300  # Default 5 minutes


def centipawns_to_win_probability(cp: int) -> float:
    """
    Convert centipawn evaluation to win probability.

    Uses a logistic function based on chess statistics.

    Args:
        cp: Centipawns

    Returns:
        Win probability (0.0 to 1.0)
    """
    import math
    return 1 / (1 + math.exp(-cp / 400))


def get_piece_value(piece_type: int) -> int:
    """
    Get standard piece value.

    Args:
        piece_type: Chess piece type

    Returns:
        Value in centipawns (pawns = 100)
    """
    values = {
        chess.PAWN: 100,
        chess.KNIGHT: 320,
        chess.BISHOP: 330,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 0,
    }
    return values.get(piece_type, 0)
