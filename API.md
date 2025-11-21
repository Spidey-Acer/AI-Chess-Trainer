# API Reference

REST API documentation for AI Chess Trainer backend.

**Base URL**: `http://127.0.0.1:5000` (development)

**Content-Type**: `application/json`

---

## Health & Status

### `GET /api/health`

Health check endpoint.

**Response**:
```json
{
  "status": "ok",
  "services": {
    "engine": true,
    "database": true,
    "game_manager": true
  }
}
```

---

## Position Analysis

### `POST /api/analyze/position`

Analyze a single chess position.

**Request**:
```json
{
  "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
  "depth": 20
}
```

**Response**:
```json
{
  "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
  "score": 50,
  "best_move": "e2e4",
  "evaluation": "equal",
  "depth": 20
}
```

---

## Game Analysis

### `POST /api/analyze/game`

Analyze a complete chess game.

**Request**:
```json
{
  "pgn": "1. e4 e5 2. Nf3 Nc6 ...",
  "depth": 20,
  "generate_feedback": false
}
```

**Response**:
```json
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
  "black_stats": {...},
  "move_analysis": [...]
}
```

---

## Training

### `POST /api/train/position`

Get a training position.

**Request**:
```json
{
  "difficulty": "intermediate",
  "focus": "general"
}
```

**Response**:
```json
{
  "fen": "...",
  "objective": "Find the best move for White",
  "hint": "Look for a tactical combination",
  "difficulty": "intermediate"
}
```

### `POST /api/train/check-move`

Check if a move is correct.

**Request**:
```json
{
  "fen": "...",
  "move": "e2e4"
}
```

**Response**:
```json
{
  "correct": true,
  "score_loss": 0,
  "best_move": "e2e4",
  "explanation": "Excellent!",
  "alternative_moves": ["d2d4", "Nf3"]
}
```

---

## Game Management

### `GET /api/games`

List all analyzed games.

**Query Parameters**:
- `limit` (default: 10)
- `offset` (default: 0)

**Response**:
```json
{
  "games": [...],
  "total": 100
}
```

### `GET /api/games/:id`

Get specific game by ID.

### `POST /api/import/pgn`

Import a PGN game.

**Request**:
```json
{
  "pgn": "1. e4 e5...",
  "analyze": false
}
```

---

## Statistics

### `GET /api/stats`

Get user statistics.

**Response**:
```json
{
  "total_games": 150,
  "avg_accuracy": 92.5,
  "total_blunders": 45,
  "total_mistakes": 120,
  "improvement_trend": [...],
  "opening_performance": {...}
}
```

---

## Ollama Integration

### `GET /api/ollama/status`

Check Ollama status.

**Response**:
```json
{
  "running": true,
  "models": [...]
}
```

### `POST /api/ollama/pull`

Download an Ollama model.

**Request**:
```json
{
  "model": "llama3.2:3b"
}
```

---

## Error Responses

All endpoints may return error responses:

```json
{
  "error": "Error description"
}
```

**HTTP Status Codes**:
- `200` - Success
- `400` - Bad Request
- `404` - Not Found
- `500` - Internal Server Error
- `503` - Service Unavailable

---

See [src/api/server.py](src/api/server.py) for implementation details.
