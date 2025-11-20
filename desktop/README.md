# AI Chess Trainer - Desktop App

Offline desktop application for AI Chess Trainer, built with Electron and Python.

## Overview

This desktop application provides a user-friendly interface for the AI Chess Trainer, combining:
- **Electron** - Cross-platform desktop framework
- **Python Flask** - Backend API for chess analysis
- **Stockfish** - Chess engine for position evaluation
- **Ollama** - Free local AI for explanations

## Architecture

```
Desktop App
├── Electron Main Process (main.js)
│   ├── Window Management
│   ├── Python Backend Launcher
│   └── IPC Communication
├── Preload Script (preload.js)
│   └── Secure API Bridge
├── Renderer Process (HTML/JS/React)
│   └── User Interface
└── Python Backend (Flask API)
    ├── Chess Engine (Stockfish)
    ├── Game Analyzer
    ├── AI Integration (Ollama)
    └── Database (SQLite)
```

## Current Status

**✅ Completed (Week 1 - Backend & Shell):**
- [x] Python Flask API with all endpoints
- [x] Bundled resource detection utilities
- [x] Electron project structure
- [x] Main process with Python backend management
- [x] Preload script for security
- [x] Basic HTML renderer with status checks
- [x] Package configuration for building

**🚧 In Progress:**
- [ ] React frontend with chess board
- [ ] Full UI components
- [ ] Bundling and packaging

**📋 Planned:**
- [ ] Ollama integration
- [ ] Desktop installers (Windows/Mac/Linux)
- [ ] Auto-updater
- [ ] Full offline mode

## Development Setup

### Prerequisites

1. **Node.js** (v18 or higher)
2. **Python 3.10+**
3. **Stockfish** chess engine
4. **Git**

### Installation

1. **Install Python dependencies:**
   ```bash
   cd /home/user/AI-Chess-Trainer
   pip install -r requirements.txt
   ```

2. **Install Electron dependencies:**
   ```bash
   cd desktop
   npm install
   ```

3. **Configure environment:**
   Create a `.env` file in the project root:
   ```env
   STOCKFISH_PATH=/usr/games/stockfish
   AI_PROVIDER=ollama
   AI_MODEL=llama3.2:3b
   ```

### Running in Development

1. **Start the desktop app:**
   ```bash
   cd desktop
   npm start
   ```

   This will:
   - Start the Python Flask backend on port 5000
   - Launch the Electron window
   - Load the renderer interface

2. **Debug mode:**
   ```bash
   npm run dev
   ```

   Opens DevTools automatically for debugging.

## API Endpoints

The Python backend provides these REST endpoints:

### Health & Status
- `GET /api/health` - Backend health check

### Position Analysis
- `POST /api/analyze/position` - Analyze a single position
  ```json
  {
    "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    "depth": 20
  }
  ```

### Game Analysis
- `POST /api/analyze/game` - Analyze complete game
  ```json
  {
    "pgn": "1. e4 e5 2. Nf3 ...",
    "depth": 20,
    "generate_feedback": true
  }
  ```

### Training
- `POST /api/train/position` - Get training position
- `POST /api/train/check-move` - Check user's move

### Game Management
- `GET /api/games` - List all games
- `GET /api/games/:id` - Get specific game
- `POST /api/import/pgn` - Import PGN file

### Statistics
- `GET /api/stats` - Get user statistics

## Project Structure

```
desktop/
├── main.js              # Electron main process
├── preload.js           # Security bridge
├── package.json         # Dependencies and build config
├── renderer/            # Frontend files
│   └── index.html       # Current: Simple HTML
│   └── src/             # Future: React app
├── assets/              # Icons and images
│   ├── icon.ico         # Windows icon
│   ├── icon.icns        # macOS icon
│   └── icon.png         # Linux icon
├── build/               # Build resources
└── dist/                # Build output
```

## Building for Production

### Package for Current Platform

```bash
npm run build
```

### Package for All Platforms

```bash
npm run build:all
```

This creates installers in `desktop/dist/`:
- **Windows:** `.exe` installer
- **macOS:** `.dmg` disk image
- **Linux:** `.AppImage` and `.deb` packages

## Testing the App

1. **Check backend status:**
   - Click "Refresh Status" button
   - All three indicators should show green "Ready/Running"

2. **Test analysis:**
   - Click "Test Analysis" button
   - Should show analysis of starting position

3. **Open PGN file:**
   - Use File menu (when implemented)
   - Or drag & drop PGN file (when implemented)

## Configuration

The app uses `electron-store` for persistent settings:

```javascript
// Get setting
const depth = await window.electronAPI.getSetting('analysis_depth', 20);

// Set setting
await window.electronAPI.setSetting('analysis_depth', 25);
```

Settings are stored in:
- **Windows:** `%APPDATA%/ai-chess-trainer-desktop/`
- **macOS:** `~/Library/Application Support/ai-chess-trainer-desktop/`
- **Linux:** `~/.config/ai-chess-trainer-desktop/`

## Next Steps

### Week 2: React Frontend
- Set up React with react-chessboard
- Create chess board component
- Create analysis panel
- Create game list
- Create training mode
- Create statistics dashboard

### Week 3: Bundling & Ollama
- Bundle Python backend with PyInstaller
- Integrate Ollama for offline AI
- Create installers for all platforms
- Add auto-update functionality

### Week 4: Polish
- Add splash screen
- Add keyboard shortcuts
- Add drag & drop support
- Improve error handling
- User testing and bug fixes

## Troubleshooting

### Python backend won't start

1. Check Python is installed: `python3 --version`
2. Check dependencies: `pip list | grep -E "flask|chess|stockfish"`
3. Check Stockfish path in `.env`
4. Look at console logs in DevTools

### Port 5000 already in use

Change the port in `main.js`:
```javascript
const PYTHON_API_PORT = 5001; // Use different port
```

### Window doesn't open

1. Check DevTools console (Ctrl+Shift+I)
2. Try development mode: `npm run dev`
3. Check for errors in terminal

## Contributing

This is part of the AI Chess Trainer project. See the main README for contribution guidelines.

## License

MIT License - See LICENSE file for details.
