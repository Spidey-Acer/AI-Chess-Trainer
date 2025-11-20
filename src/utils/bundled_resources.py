"""Utilities for detecting bundled resources in packaged applications.

When the app is packaged with PyInstaller or similar tools, resources like
Stockfish and Ollama need to be found in the bundle directory rather than
the system paths.
"""

import os
import sys
import platform
from pathlib import Path
from typing import Optional


def get_base_path() -> Path:
    """Get the base path for the application.

    Returns:
        Path: Base directory of the application (bundle or source)
    """
    if getattr(sys, 'frozen', False):
        # Running in a PyInstaller bundle
        if hasattr(sys, '_MEIPASS'):
            # PyInstaller >= 2.1 (temp folder extraction)
            return Path(sys._MEIPASS)
        else:
            # PyInstaller < 2.1 or other packagers
            return Path(sys.executable).parent
    else:
        # Running in normal Python environment
        # Go up from src/utils to project root
        return Path(__file__).parent.parent.parent


def get_stockfish_path() -> str:
    """Get the path to Stockfish engine.

    Looks for bundled Stockfish first, then falls back to system paths.

    Returns:
        str: Path to Stockfish executable

    Raises:
        FileNotFoundError: If Stockfish is not found
    """
    base_path = get_base_path()
    system = platform.system()

    # Determine executable name
    if system == 'Windows':
        exe_name = 'stockfish.exe'
    else:
        exe_name = 'stockfish'

    # Check bundled location first
    bundled_paths = [
        base_path / 'engines' / exe_name,  # In bundle
        base_path / 'resources' / 'engines' / exe_name,  # Alternative location
    ]

    for path in bundled_paths:
        if path.exists():
            return str(path)

    # Check environment variable
    env_path = os.getenv('STOCKFISH_PATH')
    if env_path and os.path.exists(env_path):
        return env_path

    # Check system paths
    system_paths = {
        'Windows': [
            r'C:\Program Files\Stockfish\stockfish.exe',
            r'C:\stockfish\stockfish.exe',
        ],
        'Darwin': [  # macOS
            '/usr/local/bin/stockfish',
            '/opt/homebrew/bin/stockfish',
            '/usr/bin/stockfish',
        ],
        'Linux': [
            '/usr/games/stockfish',
            '/usr/local/bin/stockfish',
            '/usr/bin/stockfish',
        ]
    }

    for path in system_paths.get(system, []):
        if os.path.exists(path):
            return path

    # Not found anywhere
    raise FileNotFoundError(
        "Stockfish engine not found. Please install Stockfish or set STOCKFISH_PATH environment variable."
    )


def get_ollama_path() -> Optional[str]:
    """Get the path to Ollama binary.

    Looks for bundled Ollama first, then falls back to system paths.

    Returns:
        Optional[str]: Path to Ollama executable, or None if not found
    """
    base_path = get_base_path()
    system = platform.system()

    # Determine executable name
    if system == 'Windows':
        exe_name = 'ollama.exe'
    else:
        exe_name = 'ollama'

    # Check bundled location first
    bundled_paths = [
        base_path / 'ollama' / exe_name,  # In bundle
        base_path / 'resources' / 'ollama' / exe_name,  # Alternative location
    ]

    for path in bundled_paths:
        if path.exists():
            return str(path)

    # Check environment variable
    env_path = os.getenv('OLLAMA_PATH')
    if env_path and os.path.exists(env_path):
        return env_path

    # Check system paths
    system_paths = {
        'Windows': [
            r'C:\Program Files\Ollama\ollama.exe',
            r'C:\ollama\ollama.exe',
        ],
        'Darwin': [  # macOS
            '/usr/local/bin/ollama',
            '/opt/homebrew/bin/ollama',
        ],
        'Linux': [
            '/usr/local/bin/ollama',
            '/usr/bin/ollama',
        ]
    }

    for path in system_paths.get(system, []):
        if os.path.exists(path):
            return path

    # Not found
    return None


def get_models_directory() -> Path:
    """Get the directory for AI models.

    Returns:
        Path: Directory where AI models are stored
    """
    base_path = get_base_path()

    if getattr(sys, 'frozen', False):
        # In packaged app, use app data directory
        if system := platform.system():
            if system == 'Windows':
                app_data = Path(os.getenv('APPDATA', ''))
            elif system == 'Darwin':  # macOS
                app_data = Path.home() / 'Library' / 'Application Support'
            else:  # Linux
                app_data = Path.home() / '.local' / 'share'

            models_dir = app_data / 'AI Chess Trainer' / 'models'
        else:
            models_dir = base_path / 'models'
    else:
        # In development, use project directory
        models_dir = base_path / 'models'

    # Create directory if it doesn't exist
    models_dir.mkdir(parents=True, exist_ok=True)

    return models_dir


def get_database_path() -> Path:
    """Get the path to the user database.

    Returns:
        Path: Path to SQLite database file
    """
    base_path = get_base_path()

    if getattr(sys, 'frozen', False):
        # In packaged app, use app data directory
        if system := platform.system():
            if system == 'Windows':
                app_data = Path(os.getenv('APPDATA', ''))
            elif system == 'Darwin':  # macOS
                app_data = Path.home() / 'Library' / 'Application Support'
            else:  # Linux
                app_data = Path.home() / '.local' / 'share'

            db_dir = app_data / 'AI Chess Trainer'
        else:
            db_dir = base_path / 'data'
    else:
        # In development, use project directory
        db_dir = base_path / 'data'

    # Create directory if it doesn't exist
    db_dir.mkdir(parents=True, exist_ok=True)

    return db_dir / 'chess_trainer.db'


def get_user_games_directory() -> Path:
    """Get the directory for user's game files.

    Returns:
        Path: Directory where user games are stored
    """
    base_path = get_base_path()

    if getattr(sys, 'frozen', False):
        # In packaged app, use app data directory
        if system := platform.system():
            if system == 'Windows':
                app_data = Path(os.getenv('APPDATA', ''))
            elif system == 'Darwin':  # macOS
                app_data = Path.home() / 'Library' / 'Application Support'
            else:  # Linux
                app_data = Path.home() / '.local' / 'share'

            games_dir = app_data / 'AI Chess Trainer' / 'games'
        else:
            games_dir = base_path / 'data' / 'user_games'
    else:
        # In development, use project directory
        games_dir = base_path / 'data' / 'user_games'

    # Create directory if it doesn't exist
    games_dir.mkdir(parents=True, exist_ok=True)

    return games_dir


def is_packaged() -> bool:
    """Check if the application is running as a packaged app.

    Returns:
        bool: True if packaged, False if running from source
    """
    return getattr(sys, 'frozen', False)


def get_resource_path(relative_path: str) -> Path:
    """Get the absolute path to a resource file.

    Args:
        relative_path: Path relative to the application base

    Returns:
        Path: Absolute path to the resource
    """
    base_path = get_base_path()
    return base_path / relative_path


# Module-level convenience functions
def setup_environment():
    """Set up environment variables for bundled resources.

    Call this at application startup to ensure all paths are correctly set.
    """
    try:
        # Set Stockfish path
        stockfish_path = get_stockfish_path()
        os.environ['STOCKFISH_PATH'] = stockfish_path

        # Set Ollama path if available
        ollama_path = get_ollama_path()
        if ollama_path:
            os.environ['OLLAMA_PATH'] = ollama_path

        # Set database path
        db_path = get_database_path()
        os.environ['DATABASE_PATH'] = str(db_path)

        return True
    except Exception as e:
        print(f"Error setting up environment: {e}")
        return False
