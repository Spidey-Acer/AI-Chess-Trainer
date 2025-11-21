# Deployment Guide

Guide for packaging and deploying AI Chess Trainer.

## Overview

AI Chess Trainer can be deployed as:
1. **Desktop App** (Electron) - Recommended for end users
2. **CLI Tool** (Python) - For developers and power users
3. **Web App** (Future) - Browser-based version

---

## Desktop App Deployment

### Prerequisites

**Development Machine**:
- Node.js 18+
- Python 3.10+
- PyInstaller
- Platform-specific tools (see below)

### Step 1: Prepare Python Backend

```bash
# Install PyInstaller
pip install pyinstaller

# Create standalone executable
pyinstaller server.spec --clean

# Output: dist/chess-trainer-server/
```

**Platform-Specific**:

**Windows**:
```bash
# Ensure Visual C++ Redistributable installed
# Bundle .exe with dependencies
pyinstaller server.spec --onedir
```

**macOS**:
```bash
# Sign and notarize (optional)
codesign --deep --force --verify --verbose --sign "Developer ID" dist/chess-trainer-server
```

**Linux**:
```bash
# Include system libraries if needed
pyinstaller server.spec --hidden-import=_cffi_backend
```

### Step 2: Build React Frontend

```bash
cd desktop/renderer-app

# Production build
npm run build

# Output: build/ (169KB gzipped)
```

### Step 3: Package Electron App

```bash
cd desktop

# Build for current platform
npm run build

# Build for all platforms
npm run build:all

# Build specific platform
npm run build:win    # Windows
npm run build:mac    # macOS
npm run build:linux  # Linux
```

**Output Locations**:
- `desktop/dist/` - Installers
- Windows: `.exe` installer
- macOS: `.dmg` disk image
- Linux: `.AppImage` and `.deb`

### Step 4: Test Installer

```bash
# Install on test machine
# Run application
# Verify all features work
# Check for errors in logs
```

---

## CLI Tool Deployment

### Option 1: pip Install (Recommended)

```bash
# Create distribution
python setup.py sdist bdist_wheel

# Upload to PyPI (requires account)
pip install twine
twine upload dist/*

# Users install with:
pip install ai-chess-trainer
```

### Option 2: Direct Install

```bash
# Clone and install
git clone https://github.com/Spidey-Acer/AI-Chess-Trainer.git
cd AI-Chess-Trainer
pip install -e .
```

### Option 3: Standalone Executable

```bash
# Bundle with PyInstaller
pyinstaller --onefile src/ui/cli.py

# Distribute single executable
# Output: dist/cli (or cli.exe on Windows)
```

---

## Docker Deployment (Future)

### Dockerfile

```dockerfile
FROM python:3.10-slim

# Install Stockfish
RUN apt-get update && apt-get install -y stockfish

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY src/ /app/src/
COPY data/ /app/data/

WORKDIR /app

# Run API server
CMD ["python", "-m", "src.api.server"]
```

### Docker Compose

```yaml
version: '3.8'
services:
  chess-trainer:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/data
    environment:
      - STOCKFISH_PATH=/usr/games/stockfish
```

---

## Platform-Specific Instructions

### Windows

**Building**:
```bash
# Install Visual Studio Build Tools
# Required for native modules

# Build
npm run build:win
```

**Installer**: NSIS (Nullsoft Scriptable Install System)
- One-click or custom install
- Desktop shortcut
- Start menu entry
- Uninstaller

**Requirements**:
- Windows 10+
- 4GB RAM
- 8GB disk space

### macOS

**Building**:
```bash
# Install Xcode Command Line Tools
xcode-select --install

# Build
npm run build:mac
```

**Installer**: DMG (Disk Image)
- Drag and drop to Applications
- Code signing (optional but recommended)
- Notarization for Gatekeeper

**Requirements**:
- macOS 10.13+
- 4GB RAM
- 8GB disk space

**Code Signing**:
```bash
# Sign app
codesign --deep --force --verify --verbose \
  --sign "Developer ID Application: Your Name" \
  dist/mac/AI Chess Trainer.app

# Verify
codesign --verify --deep --strict --verbose=2 \
  dist/mac/AI Chess Trainer.app
```

### Linux

**Building**:
```bash
# Install dependencies
sudo apt-get install -y rpm

# Build
npm run build:linux
```

**Formats**:
- **AppImage**: Self-contained, no installation
- **deb**: For Debian/Ubuntu
- **rpm**: For Fedora/RedHat (future)

**Requirements**:
- Ubuntu 18.04+ or equivalent
- 4GB RAM
- 8GB disk space

**AppImage**:
- Single file
- No installation needed
- `chmod +x AI-Chess-Trainer.AppImage`
- `./AI-Chess-Trainer.AppImage`

---

## Distribution

### GitHub Releases

```bash
# Create release
git tag v0.3.0
git push origin v0.3.0

# Upload installers to GitHub Releases
# Include:
# - Windows .exe
# - macOS .dmg
# - Linux .AppImage and .deb
# - SHA256 checksums
# - Release notes (from CHANGELOG.md)
```

### Auto-Updates

Using electron-updater:

```javascript
// main.js
const { autoUpdater } = require('electron-updater');

app.on('ready', () => {
  autoUpdater.checkForUpdatesAndNotify();
});
```

**Configuration** (package.json):
```json
{
  "publish": {
    "provider": "github",
    "owner": "Spidey-Acer",
    "repo": "AI-Chess-Trainer"
  }
}
```

---

## CI/CD Pipeline (Future)

### GitHub Actions

```yaml
name: Build and Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '18'
      
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          cd desktop && npm install
      
      - name: Build
        run: |
          cd desktop
          npm run build
      
      - name: Upload artifacts
        uses: actions/upload-artifact@v2
        with:
          name: installer-${{ matrix.os }}
          path: desktop/dist/*
```

---

## Bundling Considerations

### Size Optimization

**Python**:
- Use `--exclude-module` for unused packages
- Remove development dependencies
- Compress with UPX

**Electron**:
- Use asar archives
- Exclude dev dependencies
- Compress assets

**Total Size**:
- Base app: ~200MB
- With Ollama model: ~3-8GB

### Security

1. **Code Signing**: Sign all executables
2. **Checksums**: Provide SHA256 hashes
3. **HTTPS**: Use HTTPS for updates
4. **Sandboxing**: Enable Electron sandbox
5. **CSP**: Content Security Policy

### Performance

1. **Lazy Loading**: Load components on demand
2. **Caching**: Cache API responses
3. **Worker Threads**: Use for heavy computations
4. **Compression**: Gzip assets

---

## Post-Deployment

### Monitoring

- Error tracking (Sentry)
- Usage analytics (optional, privacy-respecting)
- Crash reports
- Performance metrics

### User Feedback

- GitHub Issues
- In-app feedback form
- User surveys
- Community forum

### Updates

- Semantic versioning
- Changelog in each release
- Auto-update mechanism
- Backwards compatibility

---

## Troubleshooting Deployment

### Build Fails

```bash
# Clear cache
rm -rf desktop/dist/ desktop/node_modules/
cd desktop && npm install

# Clean Python build
rm -rf dist/ build/ *.spec
```

### Large Bundle Size

- Check included files in package.json
- Exclude unnecessary dependencies
- Use webpack-bundle-analyzer

### Platform-Specific Issues

- Test on actual target platform
- Check architecture (x64, arm64)
- Verify system dependencies

---

## Checklist

Before release:

- [ ] All tests passing
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version numbers incremented
- [ ] Python backend bundled
- [ ] React app built
- [ ] Electron app packaged
- [ ] Tested on all platforms
- [ ] Code signed (Mac/Windows)
- [ ] Checksums generated
- [ ] Release notes written
- [ ] GitHub release created
- [ ] Announcement posted

---

See also:
- [electron-builder docs](https://www.electron.build/)
- [PyInstaller manual](https://pyinstaller.org/en/stable/)
- [GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github)
