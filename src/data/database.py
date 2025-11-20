"""
Database - SQLite database for storing analysis and progress
"""

import sqlite3
import json
from typing import Dict, List, Optional
from datetime import datetime
import os


class Database:
    """
    Manages SQLite database for storing game analyses and user progress.
    """

    def __init__(self, db_path: str = "./data/chess_trainer.db"):
        """
        Initialize database connection.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.connection = None
        self._init_database()

    def connect(self):
        """Establish database connection."""
        if not self.connection:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row

    def close(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

    def _init_database(self):
        """Initialize database tables."""
        self.connect()

        # Create tables
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                white_player TEXT,
                black_player TEXT,
                result TEXT,
                date TEXT,
                pgn_path TEXT,
                analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS game_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_id INTEGER,
                player TEXT,
                accuracy REAL,
                blunders INTEGER,
                mistakes INTEGER,
                inaccuracies INTEGER,
                avg_centipawn_loss REAL,
                analysis_data TEXT,
                FOREIGN KEY (game_id) REFERENCES games(id)
            )
        """)

        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS training_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_type TEXT,
                positions_count INTEGER,
                correct_count INTEGER,
                started_at TIMESTAMP,
                completed_at TIMESTAMP
            )
        """)

        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS user_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_name TEXT,
                metric_value REAL,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        self.connection.commit()

    def save_game_analysis(
        self,
        metadata: Dict,
        white_stats: Dict,
        black_stats: Dict,
        full_analysis: Dict,
        pgn_path: Optional[str] = None,
    ) -> int:
        """
        Save game analysis to database.

        Args:
            metadata: Game metadata
            white_stats: White player statistics
            black_stats: Black player statistics
            full_analysis: Complete analysis dictionary
            pgn_path: Optional path to PGN file

        Returns:
            Game ID
        """
        self.connect()

        # Insert game record
        cursor = self.connection.execute("""
            INSERT INTO games (white_player, black_player, result, date, pgn_path)
            VALUES (?, ?, ?, ?, ?)
        """, (
            metadata.get("white", "Unknown"),
            metadata.get("black", "Unknown"),
            metadata.get("result", "*"),
            metadata.get("date", datetime.now().strftime("%Y-%m-%d")),
            pgn_path,
        ))

        game_id = cursor.lastrowid

        # Insert white player analysis
        self.connection.execute("""
            INSERT INTO game_analysis
            (game_id, player, accuracy, blunders, mistakes, inaccuracies,
             avg_centipawn_loss, analysis_data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            game_id,
            "white",
            white_stats.get("accuracy", 0),
            white_stats.get("blunders", 0),
            white_stats.get("mistakes", 0),
            white_stats.get("inaccuracies", 0),
            white_stats.get("average_centipawn_loss", 0),
            json.dumps(white_stats),
        ))

        # Insert black player analysis
        self.connection.execute("""
            INSERT INTO game_analysis
            (game_id, player, accuracy, blunders, mistakes, inaccuracies,
             avg_centipawn_loss, analysis_data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            game_id,
            "black",
            black_stats.get("accuracy", 0),
            black_stats.get("blunders", 0),
            black_stats.get("mistakes", 0),
            black_stats.get("inaccuracies", 0),
            black_stats.get("average_centipawn_loss", 0),
            json.dumps(black_stats),
        ))

        self.connection.commit()
        return game_id

    def get_game_history(self, player_name: Optional[str] = None, limit: int = 10) -> List[Dict]:
        """
        Get game history.

        Args:
            player_name: Filter by player name (optional)
            limit: Maximum number of games to return

        Returns:
            List of game dictionaries
        """
        self.connect()

        if player_name:
            query = """
                SELECT * FROM games
                WHERE white_player = ? OR black_player = ?
                ORDER BY analyzed_at DESC
                LIMIT ?
            """
            cursor = self.connection.execute(query, (player_name, player_name, limit))
        else:
            query = """
                SELECT * FROM games
                ORDER BY analyzed_at DESC
                LIMIT ?
            """
            cursor = self.connection.execute(query, (limit,))

        return [dict(row) for row in cursor.fetchall()]

    def get_player_statistics(self, player_name: str) -> Dict:
        """
        Get aggregated statistics for a player.

        Args:
            player_name: Player name

        Returns:
            Dictionary with statistics
        """
        self.connect()

        query = """
            SELECT
                COUNT(*) as games_count,
                AVG(accuracy) as avg_accuracy,
                SUM(blunders) as total_blunders,
                SUM(mistakes) as total_mistakes,
                SUM(inaccuracies) as total_inaccuracies,
                AVG(avg_centipawn_loss) as avg_acpl
            FROM game_analysis ga
            JOIN games g ON ga.game_id = g.id
            WHERE (g.white_player = ? AND ga.player = 'white')
               OR (g.black_player = ? AND ga.player = 'black')
        """

        cursor = self.connection.execute(query, (player_name, player_name))
        row = cursor.fetchone()

        if row:
            return dict(row)
        else:
            return {}

    def save_training_session(
        self,
        session_type: str,
        positions_count: int,
        correct_count: int,
        started_at: datetime,
        completed_at: datetime,
    ) -> int:
        """
        Save training session results.

        Args:
            session_type: Type of training session
            positions_count: Number of positions practiced
            correct_count: Number solved correctly
            started_at: Session start time
            completed_at: Session end time

        Returns:
            Session ID
        """
        self.connect()

        cursor = self.connection.execute("""
            INSERT INTO training_sessions
            (session_type, positions_count, correct_count, started_at, completed_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            session_type,
            positions_count,
            correct_count,
            started_at.isoformat(),
            completed_at.isoformat(),
        ))

        self.connection.commit()
        return cursor.lastrowid

    def record_progress(self, metric_name: str, metric_value: float) -> None:
        """
        Record a progress metric.

        Args:
            metric_name: Name of the metric
            metric_value: Value of the metric
        """
        self.connect()

        self.connection.execute("""
            INSERT INTO user_progress (metric_name, metric_value)
            VALUES (?, ?)
        """, (metric_name, metric_value))

        self.connection.commit()

    def get_progress_trend(self, metric_name: str, days: int = 30) -> List[Dict]:
        """
        Get progress trend for a metric.

        Args:
            metric_name: Metric to track
            days: Number of days to look back

        Returns:
            List of progress records
        """
        self.connect()

        query = """
            SELECT metric_value, recorded_at
            FROM user_progress
            WHERE metric_name = ?
              AND recorded_at >= datetime('now', '-' || ? || ' days')
            ORDER BY recorded_at
        """

        cursor = self.connection.execute(query, (metric_name, days))
        return [dict(row) for row in cursor.fetchall()]
