# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Collect all submodules
hiddenimports = [
    'flask',
    'flask_cors',
    'chess',
    'chess.engine',
    'chess.pgn',
    'sqlalchemy',
    'sqlalchemy.orm',
    'sqlalchemy.ext.declarative',
    'pandas',
    'numpy',
    'anthropic',
    'requests',
    'yaml',
    'dotenv',
    'tqdm',
    'dateutil',
    'cffi',
    '_cffi_backend',
]

# Data files to include
datas = [
    ('src', 'src'),
    ('data/sample_games', 'data/sample_games'),
    ('.env.example', '.'),
]

# Binaries to include
# NOTE: Before building, download Stockfish from https://stockfishchess.org/download/
# and place the binary in engines/ directory:
#   - Windows: engines/stockfish.exe
#   - macOS/Linux: engines/stockfish
#
# Example binaries configuration:
# binaries = [
#     ('engines/stockfish.exe', 'engines') if os.name == 'nt' else ('engines/stockfish', 'engines'),
# ]
binaries = []

# Try to include Stockfish if available
if os.path.exists('engines'):
    import glob
    stockfish_files = glob.glob('engines/stockfish*')
    for sf in stockfish_files:
        binaries.append((sf, 'engines'))
        print(f"Including Stockfish binary: {sf}")

a = Analysis(
    ['src/api/server.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='chess-trainer-server',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # Keep console for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='chess-trainer-server',
)
