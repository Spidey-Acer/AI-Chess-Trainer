# Troubleshooting Guide

Common issues and solutions for AI Chess Trainer.

## Installation Issues

### Python Dependencies Won't Install

**Problem**: `pip install` fails

**Solutions**:
```bash
# Update pip
python -m pip install --upgrade pip

# Use virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt

# Install specific problematic package
pip install pandas==2.2.0
```

### Stockfish Not Found

**Problem**: `FileNotFoundError: Stockfish engine not found`

**Solutions**:
1. **Install Stockfish**:
   ```bash
   # macOS
   brew install stockfish
   
   # Linux
   sudo apt-get install stockfish
   
   # Windows
   # Download from https://stockfishchess.org
   ```

2. **Set path in .env**:
   ```env
   STOCKFISH_PATH=/usr/games/stockfish
   ```

3. **Verify installation**:
   ```bash
   which stockfish  # Linux/Mac
   where stockfish  # Windows
   ```

### Node Modules Won't Install

**Problem**: `npm install` fails in desktop folder

**Solutions**:
```bash
# Clear cache
npm cache clean --force

# Delete and reinstall
rm -rf node_modules package-lock.json
npm install

# Use specific Node version
nvm use 18
npm install
```

---

## Runtime Issues

### Backend Won't Start

**Problem**: Flask API doesn't start

**Solutions**:
1. **Check port availability**:
   ```bash
   lsof -i :5000  # Check if port in use
   ```

2. **Check Python path**:
   ```bash
   python -m src.api.server
   ```

3. **Check dependencies**:
   ```bash
   pip list | grep -E "flask|chess"
   ```

4. **Check logs**:
   ```bash
   # Enable debug mode
   export DEBUG=true
   python -m src.api.server
   ```

### Desktop App Won't Launch

**Problem**: Electron app crashes or won't open

**Solutions**:
1. **Check console output**:
   ```bash
   cd desktop
   npm start
   # Read error messages
   ```

2. **Rebuild React app**:
   ```bash
   cd desktop/renderer-app
   npm run build
   ```

3. **Check Python backend**:
   ```bash
   # Start backend manually first
   python -m src.api.server
   
   # Then start Electron
   cd desktop
   npm start
   ```

4. **Clear Electron cache**:
   ```bash
   rm -rf ~/Library/Application Support/ai-chess-trainer-desktop  # Mac
   rm -rf ~/.config/ai-chess-trainer-desktop  # Linux
   # Windows: Check AppData folder
   ```

### Analysis Not Working

**Problem**: Game analysis fails or produces errors

**Solutions**:
1. **Check PGN format**:
   - Valid chess notation
   - Proper headers
   - Complete game

2. **Reduce analysis depth**:
   ```env
   ANALYSIS_DEPTH=15  # Lower value = faster
   ```

3. **Check Stockfish process**:
   ```bash
   ps aux | grep stockfish
   ```

4. **Try simple position**:
   ```python
   from src.core.chess_engine import ChessEngine
   eng = ChessEngine()
   result = eng.analyze_position()
   print(result)
   ```

---

## API Issues

### Connection Refused

**Problem**: Frontend can't connect to backend

**Solutions**:
1. **Check backend is running**:
   ```bash
   curl http://127.0.0.1:5000/api/health
   ```

2. **Check firewall**:
   - Allow port 5000
   - Check localhost access

3. **Check CORS settings**:
   - Flask-CORS should be installed
   - Check server.py has CORS enabled

### 404 Errors

**Problem**: API endpoints return 404

**Solutions**:
1. **Check endpoint URL**:
   - Correct path: `/api/analyze/position`
   - Not: `/analyze/position`

2. **Check Flask routes**:
   ```python
   from src.api.server import app
   print(app.url_map)
   ```

---

## Database Issues

### Database Locked

**Problem**: `database is locked` error

**Solutions**:
```bash
# Close all connections
pkill -f chess_trainer

# Delete and recreate
rm data/chess_trainer.db
# Will be recreated on next run
```

### Missing Tables

**Problem**: Table doesn't exist

**Solutions**:
```python
# Recreate database
from src.data.database import Database
db = Database()
db.create_tables()
```

---

## Performance Issues

### Slow Analysis

**Problem**: Analysis takes too long

**Solutions**:
1. **Reduce depth**:
   ```env
   ANALYSIS_DEPTH=15  # Default is 20
   ```

2. **Limit moves**:
   - Only analyze critical positions
   - Use move filtering

3. **Check CPU usage**:
   ```bash
   top  # or htop
   ```

### High Memory Usage

**Problem**: App uses too much RAM

**Solutions**:
1. **Close unused apps**
2. **Reduce Stockfish threads**
3. **Analyze shorter games**
4. **Restart app periodically**

---

## Ollama Issues

### Ollama Not Running

**Problem**: AI feedback fails

**Solutions**:
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama
ollama serve

# Pull model
ollama pull llama3.2:3b
```

### Model Not Found

**Problem**: Specified model doesn't exist

**Solutions**:
```bash
# List installed models
ollama list

# Pull required model
ollama pull llama3.2:3b

# Update .env
echo "AI_MODEL=llama3.2:3b" >> .env
```

---

## Test Failures

### Tests Won't Run

**Problem**: pytest fails to start

**Solutions**:
```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Set PYTHONPATH
export PYTHONPATH="${PWD}:${PYTHONPATH}"

# Run with module syntax
python -m pytest tests/
```

### Specific Tests Fail

**Problem**: Some tests fail consistently

**Solutions**:
1. **Check Stockfish is installed**
2. **Check .env configuration**
3. **Run tests verbosely**:
   ```bash
   pytest -v tests/test_chess_engine.py
   ```

---

## Build/Packaging Issues

### Electron Build Fails

**Problem**: `npm run build` fails

**Solutions**:
```bash
# Clear cache
rm -rf dist/ desktop/dist/

# Rebuild from scratch
cd desktop/renderer-app
npm run build

cd ..
npm run build
```

### PyInstaller Fails

**Problem**: Python bundling fails

**Solutions**:
```bash
# Install PyInstaller
pip install pyinstaller

# Try manual build
pyinstaller server.spec --clean

# Check for missing modules
pyinstaller --onefile --collect-all flask src/api/server.py
```

---

## Platform-Specific Issues

### macOS: Permission Denied

**Problem**: Can't execute binary

**Solutions**:
```bash
# Make executable
chmod +x stockfish
chmod +x dist/chess-trainer-server

# Allow in System Preferences → Security & Privacy
```

### Windows: DLL Not Found

**Problem**: Missing .dll files

**Solutions**:
- Install Visual C++ Redistributable
- Check Python installation
- Use Windows Python from python.org

### Linux: Missing Dependencies

**Problem**: System library not found

**Solutions**:
```bash
# Install system dependencies
sudo apt-get install python3-dev libpq-dev

# Or use Flatpak/AppImage version
```

---

## Getting More Help

If none of these solutions work:

1. **Check logs**:
   - Console output
   - Error messages
   - Stack traces

2. **Search issues**:
   [GitHub Issues](https://github.com/Spidey-Acer/AI-Chess-Trainer/issues)

3. **Create new issue**:
   Include:
   - OS and version
   - Python version
   - Error message
   - Steps to reproduce

4. **Ask in discussions**:
   [GitHub Discussions](https://github.com/Spidey-Acer/AI-Chess-Trainer/discussions)

---

See also:
- [FAQ.md](FAQ.md) for common questions
- [TESTING.md](TESTING.md) for testing issues
- [CONTRIBUTING.md](CONTRIBUTING.md) for development setup
