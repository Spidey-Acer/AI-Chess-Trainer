# AI Chess Trainer

An intelligent chess training application that uses AI to analyze your games, provide personalized feedback, and help you improve your chess skills systematically.

## Features

### Core Capabilities
- **Game Analysis**: Deep analysis of your chess games using Stockfish engine
- **Mistake Detection**: Automatically identifies blunders, mistakes, and inaccuracies
- **AI-Powered Feedback**: Natural language explanations of positions using Claude AI
- **Position Training**: Practice specific positions and tactical patterns
- **Progress Tracking**: Monitor your improvement over time
- **Opening Repertoire**: Build and refine your opening repertoire

### Key Benefits
- Learn from your mistakes with clear explanations
- Identify patterns in your play (both good and bad)
- Get personalized training recommendations
- Track your progress with detailed analytics
- Understand the "why" behind moves, not just the "what"

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Spidey-Acer/AI-Chess-Trainer.git
cd AI-Chess-Trainer

# Install dependencies
pip install -r requirements.txt

# Set up configuration
cp .env.example .env
# Edit .env with your API keys and settings
```

### Basic Usage

```bash
# Analyze a game
python -m src.ui.cli analyze game.pgn

# Start interactive training session
python -m src.ui.cli train

# View your progress
python -m src.ui.cli stats
```

## Configuration

Create a `.env` file with the following:

```env
# AI API Configuration
ANTHROPIC_API_KEY=your_claude_api_key_here
# or
OPENAI_API_KEY=your_openai_api_key_here

# Chess Engine
STOCKFISH_PATH=/usr/local/bin/stockfish

# Analysis Settings
ANALYSIS_DEPTH=20
ANALYSIS_TIME_PER_MOVE=1.0

# Database
DATABASE_PATH=./data/chess_trainer.db
```

## Project Structure

```
AI-Chess-Trainer/
├── src/                    # Source code
│   ├── core/              # Chess engine and analysis
│   ├── ai/                # AI training logic
│   ├── data/              # Data management
│   ├── ui/                # User interfaces
│   └── utils/             # Utilities
├── tests/                 # Test suite
├── data/                  # Data files
├── config/                # Configuration files
├── docs/                  # Documentation
└── requirements.txt       # Python dependencies
```

## Documentation

- [Implementation Plan](IMPLEMENTATION_PLAN.md) - Detailed development roadmap
- [Project Status](PROJECT_STATUS.md) - Current implementation status
- [Architecture](docs/ARCHITECTURE.md) - Technical architecture details
- [User Guide](docs/USER_GUIDE.md) - Comprehensive user documentation
- [API Documentation](docs/API.md) - API reference

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_game_analyzer.py

# Run with coverage
pytest --cov=src tests/
```

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run linting
flake8 src/
black src/

# Type checking
mypy src/
```

## Technology Stack

- **Language**: Python 3.10+
- **Chess Engine**: python-chess + Stockfish
- **AI**: Anthropic Claude API / OpenAI GPT
- **CLI**: Click framework
- **Testing**: pytest
- **Data**: SQLite, pandas

## Roadmap

See [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) for the complete roadmap.

### Current Phase: Phase 1 - Foundation
- Setting up project structure
- Implementing chess engine integration
- Building basic analysis capabilities

### Next Steps
- Position trainer implementation
- AI-powered feedback generation
- Progress tracking system

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see LICENSE file for details

## Support

- Issues: [GitHub Issues](https://github.com/Spidey-Acer/AI-Chess-Trainer/issues)
- Discussions: [GitHub Discussions](https://github.com/Spidey-Acer/AI-Chess-Trainer/discussions)

## Acknowledgments

- Stockfish chess engine
- python-chess library
- Anthropic Claude AI
- The chess community

---

**Status**: 🚧 In Development - See [PROJECT_STATUS.md](PROJECT_STATUS.md) for current progress
