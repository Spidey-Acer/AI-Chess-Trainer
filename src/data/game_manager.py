"""
Game Manager - Handles PGN/FEN operations and game storage
"""

import os
from typing import List, Optional, Dict
import chess.pgn
from io import StringIO


class GameManager:
    """
    Manages chess games, PGN files, and game storage.
    """

    def __init__(self, data_directory: str = "./data/sample_games"):
        """
        Initialize game manager.

        Args:
            data_directory: Directory for storing game files
        """
        self.data_directory = data_directory
        os.makedirs(data_directory, exist_ok=True)

    def load_pgn(self, file_path: str) -> chess.pgn.Game:
        """
        Load a game from PGN file.

        Args:
            file_path: Path to PGN file

        Returns:
            chess.pgn.Game object
        """
        with open(file_path, "r") as pgn_file:
            game = chess.pgn.read_game(pgn_file)

        if not game:
            raise ValueError(f"No valid game found in {file_path}")

        return game

    def load_pgn_string(self, pgn_string: str) -> chess.pgn.Game:
        """
        Load a game from PGN string.

        Args:
            pgn_string: PGN notation as string

        Returns:
            chess.pgn.Game object
        """
        pgn_io = StringIO(pgn_string)
        game = chess.pgn.read_game(pgn_io)

        if not game:
            raise ValueError("No valid game found in PGN string")

        return game

    def save_pgn(self, game: chess.pgn.Game, file_path: str) -> None:
        """
        Save a game to PGN file.

        Args:
            game: chess.pgn.Game object
            file_path: Path to save file
        """
        with open(file_path, "w") as pgn_file:
            exporter = chess.pgn.FileExporter(pgn_file)
            game.accept(exporter)

    def create_game_from_moves(
        self,
        moves: List[str],
        metadata: Optional[Dict] = None,
    ) -> chess.pgn.Game:
        """
        Create a game object from a list of moves.

        Args:
            moves: List of moves in UCI notation
            metadata: Optional game metadata (headers)

        Returns:
            chess.pgn.Game object
        """
        game = chess.pgn.Game()

        # Set metadata
        if metadata:
            for key, value in metadata.items():
                game.headers[key] = value

        # Add moves
        node = game
        board = chess.Board()

        for move_uci in moves:
            move = chess.Move.from_uci(move_uci)
            if move not in board.legal_moves:
                raise ValueError(f"Illegal move: {move_uci}")

            node = node.add_variation(move)
            board.push(move)

        return game

    def list_games(self, directory: Optional[str] = None) -> List[str]:
        """
        List all PGN files in a directory.

        Args:
            directory: Directory to search (defaults to data_directory)

        Returns:
            List of PGN file paths
        """
        search_dir = directory or self.data_directory
        pgn_files = []

        for root, dirs, files in os.walk(search_dir):
            for file in files:
                if file.endswith(".pgn"):
                    pgn_files.append(os.path.join(root, file))

        return sorted(pgn_files)

    def get_game_info(self, file_path: str) -> Dict:
        """
        Get metadata from a PGN file without full analysis.

        Args:
            file_path: Path to PGN file

        Returns:
            Dictionary with game metadata
        """
        game = self.load_pgn(file_path)

        return {
            "event": game.headers.get("Event", "Unknown"),
            "site": game.headers.get("Site", "Unknown"),
            "date": game.headers.get("Date", "Unknown"),
            "round": game.headers.get("Round", "?"),
            "white": game.headers.get("White", "Unknown"),
            "black": game.headers.get("Black", "Unknown"),
            "result": game.headers.get("Result", "*"),
            "white_elo": game.headers.get("WhiteElo", "?"),
            "black_elo": game.headers.get("BlackElo", "?"),
            "eco": game.headers.get("ECO", "?"),
            "opening": game.headers.get("Opening", "Unknown"),
        }

    def extract_moves(self, game: chess.pgn.Game) -> List[str]:
        """
        Extract all moves from a game in UCI notation.

        Args:
            game: chess.pgn.Game object

        Returns:
            List of moves in UCI notation
        """
        return [move.uci() for move in game.mainline_moves()]

    def validate_fen(self, fen: str) -> bool:
        """
        Validate a FEN string.

        Args:
            fen: FEN notation string

        Returns:
            True if valid
        """
        try:
            chess.Board(fen)
            return True
        except ValueError:
            return False
