# Frequently Asked Questions

## General Questions

### What is AI Chess Trainer?

An intelligent chess training application that uses AI to analyze your games and help you improve.

### Is it free?

Yes! You can use it completely free with local Ollama AI. No API costs required.

### Do I need internet?

No. The desktop app works completely offline once installed.

### What platforms are supported?

- **Desktop**: Windows, macOS, Linux
- **CLI**: Any OS with Python 3.10+

---

## Installation

### How do I install it?

See [README.md](README.md#quick-start) for installation instructions.

### Do I need to install Stockfish separately?

Yes, Stockfish is required for chess analysis:
- **macOS**: `brew install stockfish`
- **Linux**: `apt-get install stockfish`
- **Windows**: Download from [stockfishchess.org](https://stockfishchess.org)

### Do I need an API key?

Only if you want to use Claude or GPT for feedback. Ollama (free) requires no API key.

---

## Usage

### How do I analyze a game?

**Desktop App**: Import PGN → Click "Analyze"
**CLI**: `python -m src.ui.cli analyze game.pgn`

### Can I use my own chess games?

Yes! Import PGN files from chess.com, lichess.org, or any chess platform.

### How accurate is the analysis?

Analysis uses Stockfish (top chess engine), so it's extremely accurate.

### What's the difference between blunder/mistake/inaccuracy?

- **Blunder**: Loss of 300+ centipawns (major error)
- **Mistake**: Loss of 100-300 centipawns
- **Inaccuracy**: Loss of 50-100 centipawns

---

## Technical

### Which AI models are supported?

- **Ollama** (free, local): llama3.2, mistral, etc.
- **Claude** (paid): claude-3-5-sonnet
- **OpenAI** (paid): gpt-4, gpt-3.5-turbo

### How much disk space do I need?

- Base app: ~200MB
- With Ollama + model: ~3-8GB total

### What's the minimum system requirements?

- **CPU**: 2+ cores
- **RAM**: 4GB (8GB recommended)
- **Disk**: 8GB free space
- **OS**: Windows 10+, macOS 10.13+, Ubuntu 18.04+

---

## Troubleshooting

### App won't start

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed solutions.

### Stockfish not found

Set the path in `.env`:
```env
STOCKFISH_PATH=/path/to/stockfish
```

### Backend not connecting

1. Check if Flask is running (port 5000)
2. Check firewall settings
3. Restart the app

---

## Features

### Can I train specific openings?

Yes, via training mode with opening focus.

### Does it track my progress?

Yes, the statistics page shows:
- Accuracy trends
- Mistake frequency
- Opening performance
- Improvement over time

### Can I export my analysis?

Currently, analysis is stored in the database. Export features coming soon.

---

## Development

### Can I contribute?

Yes! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Is the code open source?

Yes, MIT licensed. Fork away!

### How do I report bugs?

[Create an issue](https://github.com/Spidey-Acer/AI-Chess-Trainer/issues) on GitHub.

---

## Performance

### Why is analysis slow?

Analysis time depends on:
- Stockfish depth (higher = slower)
- Game length
- CPU speed

Adjust depth in settings for faster analysis.

### Does it work on older computers?

Yes, but analysis may be slower. Reduce depth for better performance.

---

## Privacy

### Is my data collected?

No. Everything runs locally. No data is sent anywhere except to AI APIs if you configure them.

### Where is my data stored?

- **Database**: `data/chess_trainer.db`
- **Settings**: Electron store (OS-specific)
- **Games**: `data/user_games/`

---

## Future Features

### What's planned?

See [docs/FEATURES_ROADMAP.md](docs/FEATURES_ROADMAP.md) for 100+ planned features.

### When will X feature be added?

Check [PROJECT_STATUS.md](PROJECT_STATUS.md) for current priorities.

---

## More Questions?

- **Issues**: [GitHub Issues](https://github.com/Spidey-Acer/AI-Chess-Trainer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Spidey-Acer/AI-Chess-Trainer/discussions)
- **Documentation**: [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)
