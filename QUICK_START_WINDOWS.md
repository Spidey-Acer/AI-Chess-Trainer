# Quick Start - Get Windows Installer

## Fastest Way: Use GitHub Actions (No Windows PC Needed!)

### Step 1: Push to GitHub

The code is already configured. Just push and GitHub will build automatically:

```bash
git push origin claude/revamp-and-document-project-01BhXmNqrQdPrY34A67AkKE1
```

### Step 2: GitHub Builds Automatically

GitHub Actions will:
- ✅ Build Python backend with PyInstaller
- ✅ Build React frontend
- ✅ Package Electron app
- ✅ Create Windows .exe installer with NSIS
- ✅ Takes ~10-15 minutes

### Step 3: Download the Installer

**Option A: From Actions (Immediate)**
1. Go to: https://github.com/Spidey-Acer/AI-Chess-Trainer/actions
2. Click the latest workflow run
3. Scroll to "Artifacts"
4. Download "windows-installer"
5. Extract and you'll have: `AI Chess Trainer Setup 0.3.0.exe`

**Option B: Create a Release (For Distribution)**
1. Create a git tag: `git tag v0.3.0 && git push origin v0.3.0`
2. GitHub Actions builds all platforms
3. Automatic release created at: https://github.com/Spidey-Acer/AI-Chess-Trainer/releases
4. Installer available for download

---

## Alternative: Build on Windows PC

If you have a Windows computer:

### Quick Build (5 minutes)

```powershell
# 1. Clone and setup
git clone https://github.com/Spidey-Acer/AI-Chess-Trainer.git
cd AI-Chess-Trainer

# 2. Install dependencies and build
pip install -r requirements.txt pyinstaller
pyinstaller server.spec --clean

# 3. Build desktop app
cd desktop\renderer-app
npm install && npm run build
cd ..

# 4. Create Windows installer
npm install
npm run build:win

# Done! Installer is at: desktop\dist\AI Chess Trainer Setup 0.3.0.exe
```

See [WINDOWS_BUILD_GUIDE.md](WINDOWS_BUILD_GUIDE.md) for detailed instructions.

---

## What You Get

### Windows Installer Features

✅ **Full NSIS Installer** (~130-150MB)
- Professional setup wizard
- Choose installation directory
- Desktop shortcut
- Start menu entry
- Clean uninstaller

✅ **Everything Included**
- Python backend (Flask API)
- Stockfish chess engine support
- React UI with 7 components
- Offline AI ready (Ollama)
- Sample games
- Complete documentation

✅ **No Dependencies Required**
- Bundled Python runtime
- Bundled Node.js/Electron
- Works on fresh Windows install

---

## Recommended: Use GitHub Actions

**Why?**
- ✅ No Windows PC needed
- ✅ Consistent builds
- ✅ Automated process
- ✅ Free for public repos
- ✅ Builds all platforms (Win/Mac/Linux)

**Just push to GitHub and download!**

---

## Current Build Status

Check: https://github.com/Spidey-Acer/AI-Chess-Trainer/actions

All builds configured and ready to run automatically.
