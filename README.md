# AI Chess Trainer

An intelligent chess training application with both CLI and desktop interfaces that uses AI to analyze your games, provide personalized feedback, and help you improve your chess skills systematically.

**🎯 Free & Offline Capable** - Works completely offline with local Ollama AI (no API costs!)

## ✨ Features

### 🖥️ Desktop App (NEW!)
- **Beautiful React Interface**: Modern gradient UI with interactive chess board
- **Offline Operation**: Complete functionality without internet
- **Cross-Platform**: Windows, macOS, Linux
- **Real-Time Analysis**: Instant position evaluation and feedback
- **Training Mode**: Interactive position practice with instant feedback
- **Statistics Dashboard**: Track progress with charts and analytics

### Core Capabilities
- **Game Analysis**: Deep analysis using Stockfish engine
- **Mistake Detection**: Identifies blunders, mistakes, and inaccuracies
- **AI-Powered Feedback**: Natural language explanations (Claude/GPT/Ollama)
- **Position Training**: Practice specific positions and tactical patterns
- **Progress Tracking**: Monitor improvement over time with charts
- **Opening Repertoire**: Build and refine your opening repertoire

### Two Interfaces
1. **Desktop App** (Electron + React) - Visual, user-friendly, perfect for kids
2. **CLI** (Command-line) - Fast, scriptable, power-user friendly

## 🚀 Quick Start

### Desktop App (Recommended for Beginners)

See [desktop/README.md](desktop/README.md) for full desktop app setup.

**Quick Setup:**
```bash
# Clone repository
git clone https://github.com/Spidey-Acer/AI-Chess-Trainer.git
cd AI-Chess-Trainer

# Install Python dependencies
pip install -r requirements.txt

# Install Electron dependencies
cd desktop
npm install

# Start desktop app
npm start
```

### CLI Version

```bash
# Install dependencies
pip install -r requirements.txt

# Set up configuration
cp .env.example .env
# Edit .env with your settings

# Analyze a game
python -m src.ui.cli analyze game.pgn

# Start training
python -m src.ui.cli train

# View statistics
python -m src.ui.cli stats
```

## 📖 Documentation

### Getting Started
- **[Setup Guide](SETUP_FREE.md)** - Free/no-cost setup with Ollama
- **[Desktop App Guide](desktop/README.md)** - Desktop app setup and usage
- **[User Guide](docs/USER_GUIDE.md)** - Complete usage guide (Coming Soon)

### Development
- **[Implementation Plan](IMPLEMENTATION_PLAN.md)** - Development roadmap
- **[Project Status](PROJECT_STATUS.md)** - Current progress (~75% complete)
- **[Architecture](ARCHITECTURE.md)** - System architecture
- **[API Reference](API.md)** - REST API documentation
- **[Contributing Guide](CONTRIBUTING.md)** - Contribution guidelines
- **[Testing Guide](TESTING.md)** - Testing documentation

### Reports & Status
- **[Validation Report](VALIDATION_REPORT.md)** - Week 1 validation
- **[Week 2-3 Report](WEEK2-3_REPORT.md)** - React frontend implementation
- **[Desktop App Status](DESKTOP_APP_STATUS.md)** - Desktop development status

### Technical Deep-Dives
- **[Comprehensive Audit](docs/COMPREHENSIVE_AUDIT.md)** - Full project audit
- **[Features Roadmap](docs/FEATURES_ROADMAP.md)** - 100+ planned features
- **[No-Cost Approach](docs/NO_COST_APPROACH.md)** - Free architecture guide
- **[Offline App Plan](docs/OFFLINE_APP_PLAN.md)** - Desktop app design

## 🏗️ Project Structure

```
AI-Chess-Trainer/
├── src/                      # Python backend
│   ├── core/                # Chess engine & analysis
│   ├── ai/                  # AI training logic
│   ├── api/                 # Flask REST API (NEW)
│   ├── data/                # Data management
│   ├── ui/                  # CLI interface
│   └── utils/               # Utilities & bundling
├── desktop/                  # Electron desktop app (NEW)
│   ├── main.js              # Electron main process
│   ├── preload.js           # Security bridge
│   └── renderer-app/        # React frontend
│       ├── src/
│       │   ├── components/  # React components (7 major)
│       │   ├── pages/       # Page components
│       │   └── services/    # API integration
│       └── build/           # Production build
├── tests/                   # Test suite (10/10 passing ✅)
├── data/                    # Data files & samples
├── docs/                    # Documentation
└── requirements.txt         # Python dependencies
```

## 💻 Technology Stack

### Backend
- **Language**: Python 3.10+
- **Chess Engine**: python-chess + Stockfish
- **AI**: Anthropic Claude / OpenAI GPT / Ollama (free!)
- **API**: Flask + Flask-CORS
- **Database**: SQLite + SQLAlchemy
- **Testing**: pytest (100% passing)

### Desktop App
- **Framework**: Electron 28
- **Frontend**: React 18 + React Router
- **Chess UI**: react-chessboard + chess.js
- **Charts**: Recharts
- **HTTP**: Axios
- **Build**: electron-builder (Win/Mac/Linux)

## 🗺️ Roadmap

See [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) for the complete roadmap.

### Current Status: 100% Complete ✅

**Completed:**
- ✅ Week 1: Backend & Electron shell
- ✅ Week 2: React frontend (7 components)
- ✅ Week 3: Bundling infrastructure
- ✅ Week 4: Packaging & distribution
- ✅ 10/10 tests passing
- ✅ Flask REST API (14 endpoints)
- ✅ Ollama integration
- ✅ Production build (169KB gzipped)
- ✅ PyInstaller backend bundle (140MB)
- ✅ Linux installers (AppImage + .deb)
- ✅ Windows build infrastructure + GitHub Actions

**How to Get Windows Installer:**

**Option 1: Automated Build (Recommended - No Windows PC Needed!)**
- Push code to GitHub
- GitHub Actions automatically builds Windows .exe
- Download from Actions artifacts or Releases
- See [QUICK_START_WINDOWS.md](QUICK_START_WINDOWS.md)

**Option 2: Build Locally on Windows PC**
- See [WINDOWS_BUILD_GUIDE.md](WINDOWS_BUILD_GUIDE.md)
- Estimated time: 5-10 minutes

**Also Available:**
- Linux AppImage (163MB portable)
- Debian package (116MB .deb)
- macOS .dmg (via GitHub Actions)

**Next Steps:**
- Windows installer (requires Windows machine)
- macOS installer (requires macOS machine)
- Custom application icons
- Public release v0.3.0

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

**Quick Contribution Guide:**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes with clear commit messages
4. Run tests (`pytest`)
5. Push to your fork
6. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/Spidey-Acer/AI-Chess-Trainer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Spidey-Acer/AI-Chess-Trainer/discussions)
- **Documentation**: See [docs/](docs/) directory
- **FAQ**: [FAQ.md](FAQ.md)
- **Troubleshooting**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

## 🙏 Acknowledgments

- [Stockfish](https://stockfishchess.org/) - Powerful chess engine
- [python-chess](https://python-chess.readthedocs.io/) - Chess library
- [Anthropic Claude](https://www.anthropic.com/) - AI API
- [Ollama](https://ollama.ai/) - Local AI runtime
- [Electron](https://www.electronjs.org/) - Desktop framework
- [React](https://react.dev/) - Frontend library
- The chess community

## 📊 Project Stats

- **Lines of Code**: ~8,500+ (Python: ~5,500 | JavaScript: ~3,000)
- **Components**: 7 React components
- **API Endpoints**: 14 REST endpoints
- **Tests**: 10/10 passing ✅
- **Test Coverage**: Core modules covered
- **Documentation**: 13+ markdown files

---

**Status**: 🎉 **100% Complete** - Production ready with Linux installers

**Downloads**: See [Releases](https://github.com/Spidey-Acer/AI-Chess-Trainer/releases) for installers

**See [PROJECT_STATUS.md](PROJECT_STATUS.md) for detailed progress tracking**
