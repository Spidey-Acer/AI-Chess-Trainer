# Changelog

All notable changes to AI Chess Trainer will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### In Progress - CI/CD Infrastructure
- GitHub Actions workflows for automated builds
- Windows builds via GitHub Actions (no Windows PC needed)
- Multi-platform builds (Win/Mac/Linux) via cloud

### Future Enhancements
- Custom application icons
- Auto-updater integration
- Code signing for macOS/Windows

## [0.3.0] - 2025-11-22 (Week 4 Complete - 100%)

### Added - CI/CD & Windows Infrastructure
- **GitHub Actions Workflows**: Automated building for all platforms
  - `build-windows.yml`: Windows-only builds (triggered on push)
  - `build-all-platforms.yml`: Win/Mac/Linux builds (triggered on tags)
- **Windows Build Guide**: Comprehensive WINDOWS_BUILD_GUIDE.md
- **Quick Start Guide**: QUICK_START_WINDOWS.md for fast Windows builds
- **Automated Releases**: Auto-create releases with installers on git tags
- **Artifact Uploads**: Build artifacts saved for 30 days
- **Windows Configuration**: NSIS installer settings in package.json

### Added - Packaging & Distribution
- **PyInstaller Bundling**: Complete Python backend bundling (140MB)
- **Linux AppImage**: Portable executable (163MB) for all Linux distros
- **Debian Package**: .deb installer (116MB) for Ubuntu/Debian
- **Electron Packaging**: Full desktop app packaging infrastructure
- **Build Scripts**: Automated build process for all platforms
- **Bundling Docs**: engines/README.md and models/README.md

### Changed
- **server.spec**: Added cffi/cryptography dependencies, Stockfish auto-detection
- **package.json**: Added author email, homepage, Linux maintainer metadata
- **PyInstaller Config**: Improved hidden imports, data file inclusion

### Fixed
- PyInstaller cryptography/cffi module errors
- electron-builder metadata validation errors
- Resource path configuration for bundled Python backend

### Documentation
- **WEEK4_REPORT.md**: Complete Week 4 implementation report
- **DEPLOYMENT.md**: Updated with packaging instructions
- **PROJECT_STATUS.md**: Updated to 100% complete

### Testing
- ✅ Bundled Python backend tested successfully
- ✅ Flask server starts in bundled form
- ✅ All dependencies properly included
- ✅ Database and chess engine initialization working

## [0.3.0] - 2025-01-20 (Week 2-3 Complete)

### Added
- **Desktop App**: Complete Electron application with React frontend
- **React Components**: 7 major components (ChessBoard, AnalysisPanel, GameList, TrainingMode, StatsDisplay, AnalyzePage, App)
- **React Router**: Navigation with sidebar menu
- **Professional UI**: Gradient purple theme, smooth animations
- **Charts**: Recharts integration for statistics
- **Ollama Integration**: OllamaManager class for local AI
- **API Endpoints**: 2 new Ollama endpoints (/status, /pull)
- **Bundling Infrastructure**: PyInstaller spec and electron-builder config
- **Production Build**: React app builds to 169KB gzipped

### Changed
- Updated Electron main.js to load React build
- Enhanced API.js with proper Electron API URL detection
- Improved package.json with correct file paths

### Fixed
- pandas-stubs version compatibility issue
- API service initialization timing

### Documentation
- Created WEEK2-3_REPORT.md (comprehensive implementation report)
- Updated desktop/README.md with full setup instructions

## [0.2.0] - 2025-01-18 (Week 1 Complete)

### Added
- **Flask REST API**: Complete backend with 12 endpoints
- **Electron Shell**: Main process, preload script, basic HTML renderer
- **Resource Detection**: Cross-platform path resolution for Stockfish/Ollama
- **Sample Games**: 3 PGN files for testing
- **.env Configuration**: Stockfish path and API settings
- **Build Configuration**: electron-builder setup for Win/Mac/Linux

### Changed
- Updated requirements.txt with Flask and flask-cors
- Modified requirements-dev.txt (pandas-stubs version fix)

### Fixed
- Stockfish path detection on Ubuntu (/usr/games vs /usr/local/bin)
- Test suite integration (all 10/10 passing)

### Documentation
- Created desktop/README.md
- Created DESKTOP_APP_STATUS.md
- Created VALIDATION_REPORT.md

## [0.1.0] - 2025-01-15 (Foundation Complete)

### Added
- **Core Engine**: ChessEngine class with Stockfish UCI integration (382 lines)
- **Game Analyzer**: Move-by-move analysis with mistake classification (388 lines)
- **Position Evaluator**: Detailed position evaluation (234 lines)
- **AI Integration**: Multi-provider LLM support (323 lines)
- **Ollama Client**: Free local AI integration (266 lines)
- **Feedback Generator**: Natural language explanations (322 lines)
- **Trainer**: Interactive training mode (221 lines)
- **Game Manager**: PGN/FEN handling (160 lines)
- **Database**: SQLite with 4 tables (253 lines)
- **CLI**: Click-based command-line interface (275 lines)
- **Testing**: pytest framework with 10 tests
- **Configuration**: setup.py, requirements.txt, .env.example
- **Documentation**: Comprehensive docs (7 markdown files)

### Implementation Details
- Python 3.10+ with type hints throughout
- Stockfish integration via python-chess
- SQLAlchemy ORM for database
- Click + Rich for beautiful CLI
- pytest for testing (100% passing)

### Documentation
- Created README.md
- Created IMPLEMENTATION_PLAN.md
- Created PROJECT_STATUS.md
- Created SETUP_FREE.md
- Created docs/COMPREHENSIVE_AUDIT.md
- Created docs/FEATURES_ROADMAP.md
- Created docs/NO_COST_APPROACH.md
- Created docs/OFFLINE_APP_PLAN.md

## [0.0.1] - 2025-01-12 (Initial Setup)

### Added
- Project structure
- Git repository initialization
- License (MIT)
- .gitignore
- Basic file structure

---

## Version History Summary

- **0.3.0**: Desktop app with React UI (~75% complete)
- **0.2.0**: Electron shell + Flask API (Week 1)
- **0.1.0**: Python backend foundation
- **0.0.1**: Initial project setup

## Contributors

- Primary Developer: AI Chess Trainer Team
- Contributors: See GitHub contributors

## Links

- [GitHub Repository](https://github.com/Spidey-Acer/AI-Chess-Trainer)
- [Issue Tracker](https://github.com/Spidey-Acer/AI-Chess-Trainer/issues)
- [Roadmap](IMPLEMENTATION_PLAN.md)
- [Project Status](PROJECT_STATUS.md)
