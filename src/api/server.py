"""Flask REST API server for AI Chess Trainer Desktop App.

This server provides HTTP endpoints for the Electron frontend to communicate
with the Python chess analysis backend.
"""

import os
import sys
import logging
from typing import Dict, Any, Optional
from pathlib import Path

from flask import Flask, jsonify, request
from flask_cors import CORS
import chess
import chess.pgn
from io import StringIO

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.chess_engine import ChessEngine
from src.core.game_analyzer import GameAnalyzer
from src.ai.trainer import ChessTrainer
from src.data.game_manager import GameManager
from src.data.database import Database

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for Electron renderer

# Global instances (will be initialized on startup)
engine: Optional[ChessEngine] = None
database: Optional[Database] = None
game_manager: Optional[GameManager] = None


def initialize_services():
    """Initialize chess engine, database, and other services."""
    global engine, database, game_manager

    logger.info("Initializing services...")

    try:
        # Initialize chess engine
        engine = ChessEngine()
        logger.info(f"Chess engine initialized at: {engine.engine_path}")

        # Initialize database
        database = Database()
        logger.info("Database initialized")

        # Initialize game manager
        game_manager = GameManager()
        logger.info("Game manager initialized")

        logger.info("All services initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize services: {e}", exc_info=True)
        return False


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'ok',
        'services': {
            'engine': engine is not None,
            'database': database is not None,
            'game_manager': game_manager is not None
        }
    })


@app.route('/api/analyze/position', methods=['POST'])
def analyze_position():
    """Analyze a chess position.

    Request body:
        {
            "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            "depth": 20  // optional, default from config
        }

    Response:
        {
            "fen": "...",
            "score": 50,  // centipawns
            "best_move": "e2e4",
            "evaluation": "equal/winning/losing",
            "depth": 20
        }
    """
    try:
        data = request.json
        fen = data.get('fen')
        depth = data.get('depth')

        if not fen:
            return jsonify({'error': 'FEN position required'}), 400

        # Analyze position
        with ChessEngine() as eng:
            result = eng.analyze_position(fen, depth)

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error analyzing position: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/analyze/game', methods=['POST'])
def analyze_game():
    """Analyze a complete game.

    Request body:
        {
            "pgn": "1. e4 e5 2. Nf3 Nc6 ...",
            "depth": 20,  // optional
            "generate_feedback": true  // optional, use AI for explanations
        }

    Response:
        {
            "white_player": "Player 1",
            "black_player": "Player 2",
            "result": "1-0",
            "total_moves": 40,
            "white_stats": {
                "accuracy": 95.5,
                "blunders": 0,
                "mistakes": 1,
                "inaccuracies": 3,
                "avg_cp_loss": 25.3
            },
            "black_stats": { ... },
            "move_analysis": [
                {
                    "move_number": 1,
                    "move": "e4",
                    "score_before": 0,
                    "score_after": 50,
                    "classification": "good",
                    "best_move": "e4",
                    "explanation": "..."  // if generate_feedback=true
                },
                ...
            ]
        }
    """
    try:
        data = request.json
        pgn_text = data.get('pgn')
        depth = data.get('depth')
        generate_feedback = data.get('generate_feedback', False)

        if not pgn_text:
            return jsonify({'error': 'PGN required'}), 400

        # Parse PGN
        pgn_io = StringIO(pgn_text)
        game = chess.pgn.read_game(pgn_io)

        if not game:
            return jsonify({'error': 'Invalid PGN format'}), 400

        # Analyze game
        with ChessEngine(depth=depth) as eng:
            analyzer = GameAnalyzer(eng)
            analysis = analyzer.analyze_game(game)

        # Get game metadata
        white_player = game.headers.get('White', 'Unknown')
        black_player = game.headers.get('Black', 'Unknown')
        result = game.headers.get('Result', '*')

        # Calculate statistics
        stats = analyzer.get_statistics(analysis)

        # Format response
        response = {
            'white_player': white_player,
            'black_player': black_player,
            'result': result,
            'total_moves': len(analysis['moves']),
            'white_stats': stats['white'],
            'black_stats': stats['black'],
            'move_analysis': analysis['moves']
        }

        # Generate AI feedback if requested
        if generate_feedback:
            try:
                trainer = ChessTrainer()
                feedback = trainer.generate_game_feedback(game, analysis)
                response['ai_feedback'] = feedback
            except Exception as e:
                logger.warning(f"Failed to generate AI feedback: {e}")
                response['ai_feedback'] = None

        return jsonify(response)

    except Exception as e:
        logger.error(f"Error analyzing game: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/train/position', methods=['POST'])
def train_position():
    """Get a training position for the user.

    Request body:
        {
            "difficulty": "beginner|intermediate|advanced",
            "focus": "tactics|endgame|opening|general"
        }

    Response:
        {
            "fen": "...",
            "objective": "Find the best move for White",
            "hint": "Look for a tactical combination",
            "difficulty": "intermediate"
        }
    """
    try:
        data = request.json
        difficulty = data.get('difficulty', 'intermediate')
        focus = data.get('focus', 'general')

        trainer = ChessTrainer()
        position = trainer.get_training_position(difficulty, focus)

        return jsonify(position)

    except Exception as e:
        logger.error(f"Error getting training position: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/train/check-move', methods=['POST'])
def check_move():
    """Check if a move is the best move in a training position.

    Request body:
        {
            "fen": "...",
            "move": "e2e4"
        }

    Response:
        {
            "correct": true,
            "score_loss": 0,
            "best_move": "e2e4",
            "explanation": "Excellent! This is the best move.",
            "alternative_moves": ["d2d4", "Nf3"]
        }
    """
    try:
        data = request.json
        fen = data.get('fen')
        move = data.get('move')

        if not fen or not move:
            return jsonify({'error': 'FEN and move required'}), 400

        with ChessEngine() as eng:
            result = eng.evaluate_move(fen, move)

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error checking move: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/games', methods=['GET'])
def list_games():
    """List all analyzed games.

    Query params:
        ?limit=10&offset=0

    Response:
        {
            "games": [
                {
                    "id": 1,
                    "white_player": "...",
                    "black_player": "...",
                    "date": "2025-01-20",
                    "result": "1-0",
                    "white_accuracy": 95.5,
                    "black_accuracy": 92.1
                },
                ...
            ],
            "total": 100
        }
    """
    try:
        limit = int(request.args.get('limit', 10))
        offset = int(request.args.get('offset', 0))

        games = database.get_games(limit=limit, offset=offset)
        total = database.count_games()

        return jsonify({
            'games': games,
            'total': total
        })

    except Exception as e:
        logger.error(f"Error listing games: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/games/<int:game_id>', methods=['GET'])
def get_game(game_id: int):
    """Get a specific game by ID.

    Response:
        {
            "id": 1,
            "pgn": "...",
            "white_player": "...",
            "black_player": "...",
            "analysis": { ... }
        }
    """
    try:
        game = database.get_game(game_id)

        if not game:
            return jsonify({'error': 'Game not found'}), 404

        return jsonify(game)

    except Exception as e:
        logger.error(f"Error getting game: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get overall user statistics.

    Response:
        {
            "total_games": 150,
            "avg_accuracy": 92.5,
            "total_blunders": 45,
            "total_mistakes": 120,
            "improvement_trend": [
                {"date": "2025-01-01", "accuracy": 85.0},
                {"date": "2025-01-07", "accuracy": 88.5},
                ...
            ],
            "opening_performance": {
                "e4": {"games": 50, "accuracy": 94.2},
                "d4": {"games": 30, "accuracy": 91.5},
                ...
            }
        }
    """
    try:
        stats = database.get_user_statistics()
        return jsonify(stats)

    except Exception as e:
        logger.error(f"Error getting stats: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/import/pgn', methods=['POST'])
def import_pgn():
    """Import a PGN file or text.

    Request body:
        {
            "pgn": "1. e4 e5 ...",
            "analyze": true  // optional, analyze immediately
        }

    Response:
        {
            "game_id": 123,
            "imported": true,
            "analysis": { ... }  // if analyze=true
        }
    """
    try:
        data = request.json
        pgn_text = data.get('pgn')
        should_analyze = data.get('analyze', False)

        if not pgn_text:
            return jsonify({'error': 'PGN required'}), 400

        # Parse and save game
        pgn_io = StringIO(pgn_text)
        game = chess.pgn.read_game(pgn_io)

        if not game:
            return jsonify({'error': 'Invalid PGN format'}), 400

        # Save to database
        game_id = database.save_game(game)

        response = {
            'game_id': game_id,
            'imported': True
        }

        # Analyze if requested
        if should_analyze:
            with ChessEngine() as eng:
                analyzer = GameAnalyzer(eng)
                analysis = analyzer.analyze_game(game)
                database.save_analysis(game_id, analysis)
                response['analysis'] = analysis

        return jsonify(response)

    except Exception as e:
        logger.error(f"Error importing PGN: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/ollama/status', methods=['GET'])
def ollama_status():
    """Get Ollama status."""
    try:
        from src.api.ollama_manager import OllamaManager
        manager = OllamaManager()

        return jsonify({
            'running': manager.is_running(),
            'models': manager.list_models() if manager.is_running() else []
        })
    except Exception as e:
        logger.error(f"Error checking Ollama status: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/ollama/pull', methods=['POST'])
def ollama_pull():
    """Pull an Ollama model."""
    try:
        data = request.json
        model_name = data.get('model')

        if not model_name:
            return jsonify({'error': 'Model name required'}), 400

        from src.api.ollama_manager import OllamaManager
        manager = OllamaManager()

        if not manager.is_running():
            return jsonify({'error': 'Ollama is not running'}), 503

        success = manager.pull_model(model_name)
        return jsonify({'success': success})
    except Exception as e:
        logger.error(f"Error pulling model: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal error: {error}", exc_info=True)
    return jsonify({'error': 'Internal server error'}), 500


def main():
    """Run the Flask server."""
    # Initialize services
    if not initialize_services():
        logger.error("Failed to initialize services. Exiting.")
        sys.exit(1)

    # Get configuration
    host = os.getenv('API_HOST', '127.0.0.1')
    port = int(os.getenv('API_PORT', 5000))
    debug = os.getenv('DEBUG', 'false').lower() == 'true'

    logger.info(f"Starting Flask server on {host}:{port}")
    logger.info(f"Debug mode: {debug}")

    # Run server
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    main()
