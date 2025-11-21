# Architecture

System architecture for AI Chess Trainer.

## Overview

AI Chess Trainer uses a modular architecture with Python backend and optional Electron/React frontend.

```
┌─────────────────────────────────────────┐
│         User Interfaces                  │
│  ┌─────────────┐    ┌─────────────────┐ │
│  │  CLI        │    │  Desktop App    │ │
│  │  (Click)    │    │  (Electron)     │ │
│  └─────────────┘    └─────────────────┘ │
└─────────────────────────────────────────┘
              ↓                 ↓
┌─────────────────────────────────────────┐
│         REST API Layer                   │
│  Flask + Flask-CORS (Port 5000)         │
│  14 Endpoints (analyze/train/stats)     │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│         Business Logic Layer             │
│  ┌─────────────────────────────────────┐ │
│  │   Chess Core (src/core/)            │ │
│  │   • ChessEngine (Stockfish)         │ │
│  │   • GameAnalyzer                    │ │
│  │   • PositionEvaluator               │ │
│  └─────────────────────────────────────┘ │
│  ┌─────────────────────────────────────┐ │
│  │   AI Integration (src/ai/)          │ │
│  │   • LLMIntegration                  │ │
│  │   • OllamaClient                    │ │
│  │   • FeedbackGenerator               │ │
│  │   • Trainer                         │ │
│  └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│         Data Layer                       │
│  ┌─────────────────────────────────────┐ │
│  │   GameManager (PGN/FEN)             │ │
│  │   Database (SQLite + SQLAlchemy)    │ │
│  │   • Games                           │ │
│  │   • Analysis                        │ │
│  │   • Sessions                        │ │
│  │   • Progress                        │ │
│  └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

## Backend Architecture

### Core Layer (`src/core/`)
- **ChessEngine**: Stockfish UCI integration
- **GameAnalyzer**: Move-by-move analysis
- **PositionEvaluator**: Position evaluation

### AI Layer (`src/ai/`)
- **LLMIntegration**: Multi-provider AI support
- **OllamaClient**: Local Ollama integration
- **FeedbackGenerator**: Natural language feedback
- **Trainer**: Training session management

### API Layer (`src/api/`)
- **server.py**: Flask REST API
- **ollama_manager.py**: Ollama process management

### Data Layer (`src/data/`)
- **Database**: SQLite with 4 tables
- **GameManager**: PGN/FEN handling

### Utils Layer (`src/utils/`)
- **bundled_resources.py**: Resource path detection

## Desktop App Architecture

```
┌─────────────────────────────────────────┐
│    Electron Main Process (main.js)      │
│  • Window Management                     │
│  • Python Backend Launcher               │
│  • IPC Handlers                          │
│  • File Dialogs                          │
└─────────────────────────────────────────┘
                   ↕ IPC
┌─────────────────────────────────────────┐
│  Electron Renderer (React App)          │
│  ┌─────────────────────────────────────┐ │
│  │  Components (7):                    │ │
│  │  • ChessBoard                       │ │
│  │  • AnalysisPanel                    │ │
│  │  • GameList                         │ │
│  │  • TrainingMode                     │ │
│  │  • StatsDisplay                     │ │
│  │  • AnalyzePage                      │ │
│  │  • App (Router)                     │ │
│  └─────────────────────────────────────┘ │
│  ┌─────────────────────────────────────┐ │
│  │  Services:                          │ │
│  │  • api.js (Axios)                   │ │
│  └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
                   ↓ HTTP
┌─────────────────────────────────────────┐
│    Python Backend (localhost:5000)       │
│    (see Backend Architecture above)      │
└─────────────────────────────────────────┘
```

## Data Flow

### Game Analysis Flow
1. User uploads PGN (UI or API)
2. GameManager parses PGN
3. GameAnalyzer evaluates each move with Stockfish
4. Mistakes classified (blunder/mistake/inaccuracy)
5. Optional AI feedback generated
6. Results saved to database
7. Statistics updated

### Training Flow
1. User selects difficulty/focus
2. Trainer generates position
3. User makes move
4. ChessEngine evaluates move
5. Instant feedback provided
6. Next position loaded

## Security

- Context isolation in Electron
- No node integration in renderer
- Preload script for secure IPC
- API CORS configured for localhost only
- Database uses SQLAlchemy (SQL injection protected)

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for packaging details.
