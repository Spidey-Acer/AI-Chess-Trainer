# Windows Build Guide - AI Chess Trainer

## Current Situation

**Building Windows installers requires a Windows machine.** While the build infrastructure is complete and ready, creating a proper Windows .exe installer with NSIS cannot be done reliably from this Linux environment without complex wine setup.

---

## Quick Start (On Windows PC)

### Prerequisites

1. **Windows 10/11** (64-bit)
2. **Node.js** 18+ ([Download](https://nodejs.org/))
3. **Python** 3.11+ ([Download](https://www.python.org/downloads/))
4. **Git** ([Download](https://git-scm.com/))

### Build Steps

```powershell
# 1. Clone the repository
git clone https://github.com/Spidey-Acer/AI-Chess-Trainer.git
cd AI-Chess-Trainer

# 2. Install Python dependencies
pip install -r requirements.txt
pip install pyinstaller

# 3. Bundle Python backend
pyinstaller server.spec --clean

# 4. Build React frontend
cd desktop\renderer-app
npm install
npm run build
cd ..

# 5. Install desktop dependencies
npm install

# 6. Build Windows installer
npm run build:win

# Output will be in: desktop\dist\
# - AI Chess Trainer Setup 0.3.0.exe (installer)
# - win-unpacked\ (portable folder)
```

---

## What You'll Get

### Windows Installer (NSIS)
**File**: `AI Chess Trainer Setup 0.3.0.exe`
- Full installer with setup wizard
- Customizable installation directory
- Desktop shortcut creation
- Start menu shortcuts
- Uninstaller included
- Estimated size: ~130-150MB

### Unpacked Build
**Folder**: `win-unpacked\`
- Portable version (no installation needed)
- Can be zipped and distributed
- Just run `AI Chess Trainer.exe`
- Estimated size: ~400MB uncompressed

---

## Build Configuration (Already Set Up)

### package.json - Windows Config

```json
"win": {
  "target": [
    {
      "target": "nsis",
      "arch": ["x64"]
    }
  ],
  "icon": "assets/icon.ico",
  "signingHashAlgorithms": ["sha256"],
  "signDlls": false
}
```

### NSIS Installer Options

```json
"nsis": {
  "oneClick": false,
  "allowToChangeInstallationDirectory": true,
  "createDesktopShortcut": true,
  "createStartMenuShortcut": true
}
```

**Features**:
- Not one-click (users can choose install location)
- Desktop shortcut
- Start menu shortcut
- Proper uninstaller

---

## Bundled Components

### What's Included in the Installer

1. **Electron App** (~180MB)
   - React frontend (built)
   - Electron shell
   - Node.js runtime

2. **Python Backend** (~140MB)
   - Flask API server
   - Chess analysis engine
   - SQLite database
   - All dependencies

3. **Resources**
   - Sample PGN games
   - Documentation
   - Configuration files

**Total Installer Size**: ~130MB (compressed with NSIS)
**Installed Size**: ~400MB

---

## Optional: Add Custom Icon

### Create Windows Icon

1. Create or find a 256x256 PNG icon
2. Convert to .ico format (use https://convertio.co/png-ico/)
3. Save as `desktop/assets/icon.ico`
4. Rebuild: `npm run build:win`

**Recommended sizes in .ico**:
- 256x256 (main)
- 128x128
- 64x64
- 48x48
- 32x32
- 16x16

---

## Optional: Download Stockfish

### Include Stockfish Engine

**Download**:
https://stockfishchess.org/download/

**Windows Version**: `stockfish-windows-x86-64-avx2.zip`

**Installation**:
1. Download and extract
2. Rename executable to `stockfish.exe`
3. Place in `engines/` folder in project root
4. Rebuild with PyInstaller: `pyinstaller server.spec --clean`

**Note**: If not included, users can:
- Install Stockfish separately
- Set `STOCKFISH_PATH` environment variable
- Place stockfish.exe in system PATH

---

## Troubleshooting

### Build Fails with "Python not found"

**Solution**:
```powershell
# Make sure Python is in PATH
python --version

# Reinstall with "Add to PATH" checked
# Or manually add Python to PATH
```

### Build Fails with "npm not found"

**Solution**:
```powershell
# Verify Node.js installation
node --version
npm --version

# Restart terminal after Node.js installation
```

### PyInstaller Fails

**Common Issues**:
```powershell
# Missing dependencies
pip install pyinstaller --upgrade

# Antivirus blocking
# - Add exception for PyInstaller
# - Add exception for dist/ folder

# Permission errors
# - Run terminal as Administrator
```

### Electron Builder Fails

**Solutions**:
```powershell
# Clear cache
cd desktop
npm cache clean --force
rm -rf node_modules
npm install

# Try again
npm run build:win
```

### Installer Size Too Large

The installer is large because it includes:
- Full Python runtime
- Electron (Chromium engine)
- Node.js runtime
- All dependencies

**This is normal** for Electron desktop apps.

---

## Alternative Build Methods

### Method 1: GitHub Actions (CI/CD)

Create `.github/workflows/build.yml`:

```yaml
name: Build Windows Installer

on:
  push:
    tags:
      - 'v*'

jobs:
  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pyinstaller

      - name: Bundle Python backend
        run: pyinstaller server.spec --clean

      - name: Build React app
        run: |
          cd desktop/renderer-app
          npm install
          npm run build

      - name: Build Windows installer
        run: |
          cd desktop
          npm install
          npm run build:win

      - name: Upload artifact
        uses: actions/upload-artifact@v3
        with:
          name: windows-installer
          path: desktop/dist/*.exe
```

**Benefits**:
- Automated builds
- No need for local Windows PC
- Free for public repos

### Method 2: Virtual Machine

**Tools**:
- VirtualBox (free)
- VMware Workstation
- Windows 10 Dev VM (free from Microsoft)

**Steps**:
1. Install Windows in VM
2. Follow "Quick Start" guide above
3. Copy installer out of VM

### Method 3: Cloud Build Service

**Options**:
- AppVeyor (Windows CI)
- CircleCI (Windows executors)
- Azure Pipelines

---

## Distribution

### Option 1: GitHub Releases

```bash
# Create release on GitHub
# Upload AI Chess Trainer Setup 0.3.0.exe
# Users download and run
```

### Option 2: Direct Download

Host the .exe on:
- GitHub Releases (recommended)
- Your own server
- Cloud storage (Google Drive, Dropbox)

### Option 3: Microsoft Store (Advanced)

**Requirements**:
- Microsoft Developer account ($19 one-time)
- App certification
- Code signing certificate

---

## Code Signing (Optional but Recommended)

### Why Code Sign?

**Without signing**:
- Windows SmartScreen warning
- "Unknown publisher"
- Users must click "Run anyway"

**With signing**:
- No warnings
- Shows your company name
- Builds trust

### How to Sign

**Option 1: Buy Certificate** ($300-400/year)
- DigiCert
- Sectigo
- GlobalSign

**Option 2: Free Signing (Limited)**
- Self-signed certificate (still shows warning)
- Not recommended for distribution

**Signing Command**:
```powershell
# With certificate
npm run build:win -- --win --x64 \
  --cscLink="path/to/cert.pfx" \
  --cscKeyPassword="password"
```

---

## Testing the Installer

### Before Distribution

**Test on clean Windows VM**:
1. ✅ Installer runs without errors
2. ✅ Application launches
3. ✅ Python backend starts automatically
4. ✅ Chess analysis works
5. ✅ Database created successfully
6. ✅ Uninstaller works properly

**Test scenarios**:
- Fresh Windows 10 installation
- Fresh Windows 11 installation
- No Python installed
- No Node.js installed
- Antivirus enabled

---

## What's Already Done

✅ **PyInstaller configuration** (`server.spec`)
✅ **Electron builder configuration** (`desktop/package.json`)
✅ **NSIS installer settings**
✅ **Windows build script** (`npm run build:win`)
✅ **Python backend bundling**
✅ **React frontend built**
✅ **All dependencies configured**

**What you need**: Windows PC to run the build command

---

## Next Steps

### Immediate

1. **Get access to Windows PC** (or VM, or CI/CD)
2. **Run build commands** (see Quick Start)
3. **Test installer** on clean Windows
4. **Upload to GitHub Releases**

### Optional Enhancements

1. **Custom icon** (create icon.ico)
2. **Stockfish bundling** (download and include)
3. **Code signing** (buy certificate)
4. **Auto-updates** (configure electron-updater)
5. **Crash reporting** (Sentry, etc.)

---

## Support

**Build Issues**: Check troubleshooting section above
**Windows-specific bugs**: Test on clean Windows install
**Installer problems**: Check electron-builder docs

**Documentation**:
- electron-builder: https://www.electron.build/
- PyInstaller: https://pyinstaller.org/
- NSIS: https://nsis.sourceforge.io/

---

## Summary

**Current Status**:
- ✅ All build infrastructure ready
- ✅ Configuration complete
- ✅ Python backend bundled and tested
- ✅ React frontend built
- ⚠️ **Needs Windows PC to create .exe installer**

**Estimated build time on Windows PC**: 5-10 minutes

**Alternative**: Use GitHub Actions for automated builds (no Windows PC needed)

---

**Ready to build?** Go to a Windows PC and run:
```powershell
git clone https://github.com/Spidey-Acer/AI-Chess-Trainer.git
cd AI-Chess-Trainer
pip install -r requirements.txt pyinstaller
pyinstaller server.spec --clean
cd desktop\renderer-app
npm install && npm run build
cd ..
npm install && npm run build:win
```

**Output**: `desktop\dist\AI Chess Trainer Setup 0.3.0.exe` 🎉
