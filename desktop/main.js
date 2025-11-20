/**
 * Electron Main Process
 *
 * Manages the application lifecycle, window creation, and Python backend process.
 */

const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
const Store = require('electron-store');
const axios = require('axios');

// Initialize persistent store for settings
const store = new Store();

// Global references
let mainWindow = null;
let pythonProcess = null;
let pythonReady = false;

// Configuration
const PYTHON_API_PORT = 5000;
const PYTHON_API_URL = `http://127.0.0.1:${PYTHON_API_PORT}`;
const isDevelopment = process.env.NODE_ENV === 'development' || process.argv.includes('--debug');

/**
 * Get the path to Python backend executable.
 * In development, runs the Python script directly.
 * In production, uses the bundled executable.
 */
function getPythonPath() {
  if (isDevelopment) {
    // Development mode - run Python script directly
    const pythonScript = path.join(__dirname, '..', 'src', 'api', 'server.py');
    return {
      command: 'python3',
      args: [pythonScript],
      cwd: path.join(__dirname, '..')
    };
  } else {
    // Production mode - use bundled executable
    const resourcesPath = process.resourcesPath;

    if (process.platform === 'win32') {
      return {
        command: path.join(resourcesPath, 'python', 'server.exe'),
        args: [],
        cwd: resourcesPath
      };
    } else {
      return {
        command: path.join(resourcesPath, 'python', 'server'),
        args: [],
        cwd: resourcesPath
      };
    }
  }
}

/**
 * Start the Python backend server.
 */
function startPythonBackend() {
  return new Promise((resolve, reject) => {
    const pythonConfig = getPythonPath();

    console.log('Starting Python backend...');
    console.log('Command:', pythonConfig.command);
    console.log('Args:', pythonConfig.args);
    console.log('CWD:', pythonConfig.cwd);

    // Set environment variables for Python process
    const env = {
      ...process.env,
      API_HOST: '127.0.0.1',
      API_PORT: String(PYTHON_API_PORT),
      DEBUG: isDevelopment ? 'true' : 'false'
    };

    // Spawn Python process
    pythonProcess = spawn(pythonConfig.command, pythonConfig.args, {
      cwd: pythonConfig.cwd,
      env: env
    });

    // Handle stdout
    pythonProcess.stdout.on('data', (data) => {
      const message = data.toString().trim();
      console.log('[Python]', message);

      // Check if server is ready
      if (message.includes('Running on') || message.includes('Started')) {
        pythonReady = true;
        resolve();
      }
    });

    // Handle stderr
    pythonProcess.stderr.on('data', (data) => {
      const message = data.toString().trim();
      console.error('[Python Error]', message);
    });

    // Handle process exit
    pythonProcess.on('exit', (code, signal) => {
      console.log(`Python process exited with code ${code} and signal ${signal}`);
      pythonReady = false;

      if (code !== 0 && mainWindow) {
        dialog.showErrorBox(
          'Backend Error',
          `The chess analysis backend stopped unexpectedly. Please restart the application.`
        );
      }
    });

    // Handle process error
    pythonProcess.on('error', (error) => {
      console.error('Failed to start Python process:', error);
      pythonReady = false;
      reject(error);
    });

    // Timeout fallback - assume ready after 3 seconds if no confirmation
    setTimeout(() => {
      if (!pythonReady) {
        // Try to ping the API
        checkPythonAPI()
          .then(() => {
            pythonReady = true;
            resolve();
          })
          .catch(() => {
            console.warn('Python backend might not be ready, but continuing...');
            resolve(); // Resolve anyway to allow app to start
          });
      }
    }, 3000);
  });
}

/**
 * Check if Python API is responding.
 */
async function checkPythonAPI() {
  try {
    const response = await axios.get(`${PYTHON_API_URL}/api/health`, {
      timeout: 2000
    });
    return response.data.status === 'ok';
  } catch (error) {
    return false;
  }
}

/**
 * Stop the Python backend server.
 */
function stopPythonBackend() {
  if (pythonProcess) {
    console.log('Stopping Python backend...');
    pythonProcess.kill();
    pythonProcess = null;
    pythonReady = false;
  }
}

/**
 * Create the main application window.
 */
function createMainWindow() {
  // Get window bounds from store or use defaults
  const windowBounds = store.get('windowBounds', {
    width: 1200,
    height: 800
  });

  mainWindow = new BrowserWindow({
    ...windowBounds,
    minWidth: 800,
    minHeight: 600,
    title: 'AI Chess Trainer',
    backgroundColor: '#1e1e1e',
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    },
    show: false // Don't show until ready-to-show
  });

  // Load the app
  if (isDevelopment) {
    // In development, load from React dev server if running
    mainWindow.loadURL('http://localhost:3000').catch(() => {
      // Fallback to React build if dev server not running
      mainWindow.loadFile(path.join(__dirname, 'renderer-app', 'build', 'index.html'));
    });
    mainWindow.webContents.openDevTools();
  } else {
    // In production, load React build
    mainWindow.loadFile(path.join(__dirname, 'renderer-app', 'build', 'index.html'));
  }

  // Show window when ready
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
  });

  // Save window bounds on resize/move
  mainWindow.on('resize', () => {
    store.set('windowBounds', mainWindow.getBounds());
  });

  mainWindow.on('move', () => {
    store.set('windowBounds', mainWindow.getBounds());
  });

  // Clean up on close
  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

/**
 * Show splash/loading screen while backend starts.
 */
function createSplashWindow() {
  const splash = new BrowserWindow({
    width: 400,
    height: 300,
    transparent: true,
    frame: false,
    alwaysOnTop: true,
    webPreferences: {
      nodeIntegration: false
    }
  });

  // Create simple splash HTML
  const splashHTML = `
    <!DOCTYPE html>
    <html>
      <head>
        <style>
          body {
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            color: white;
            text-align: center;
          }
          .splash {
            padding: 40px;
          }
          h1 {
            font-size: 32px;
            margin: 0 0 20px 0;
          }
          .spinner {
            border: 4px solid rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            border-top: 4px solid white;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
          }
          @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
        </style>
      </head>
      <body>
        <div class="splash">
          <h1>♟️ AI Chess Trainer</h1>
          <div class="spinner"></div>
          <p>Starting chess engine...</p>
        </div>
      </body>
    </html>
  `;

  splash.loadURL(`data:text/html;charset=utf-8,${encodeURIComponent(splashHTML)}`);

  return splash;
}

// App lifecycle handlers

app.whenReady().then(async () => {
  // Show splash screen
  const splash = createSplashWindow();

  try {
    // Start Python backend
    await startPythonBackend();

    // Wait a bit to ensure backend is fully ready
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Create main window
    createMainWindow();

    // Close splash after main window is shown
    if (mainWindow) {
      mainWindow.once('ready-to-show', () => {
        setTimeout(() => {
          splash.close();
        }, 500);
      });
    }
  } catch (error) {
    console.error('Failed to start backend:', error);
    splash.close();

    dialog.showErrorBox(
      'Startup Error',
      `Failed to start the chess analysis backend:\n\n${error.message}\n\nPlease check that Python and required dependencies are installed.`
    );

    app.quit();
  }
});

app.on('window-all-closed', () => {
  // On macOS, apps typically stay open until explicitly quit
  if (process.platform !== 'darwin') {
    stopPythonBackend();
    app.quit();
  }
});

app.on('activate', () => {
  // On macOS, recreate window when dock icon is clicked
  if (BrowserWindow.getAllWindows().length === 0) {
    createMainWindow();
  }
});

app.on('before-quit', () => {
  stopPythonBackend();
});

// IPC Handlers

ipcMain.handle('get-api-url', () => {
  return PYTHON_API_URL;
});

ipcMain.handle('check-backend', async () => {
  return await checkPythonAPI();
});

ipcMain.handle('get-setting', (event, key, defaultValue) => {
  return store.get(key, defaultValue);
});

ipcMain.handle('set-setting', (event, key, value) => {
  store.set(key, value);
  return true;
});

ipcMain.handle('open-file-dialog', async () => {
  const result = await dialog.showOpenDialog(mainWindow, {
    properties: ['openFile'],
    filters: [
      { name: 'Chess Games', extensions: ['pgn'] },
      { name: 'All Files', extensions: ['*'] }
    ]
  });

  if (!result.canceled && result.filePaths.length > 0) {
    const filePath = result.filePaths[0];
    const content = fs.readFileSync(filePath, 'utf8');
    return { path: filePath, content };
  }

  return null;
});

ipcMain.handle('save-file-dialog', async (event, content, defaultName = 'game.pgn') => {
  const result = await dialog.showSaveDialog(mainWindow, {
    defaultPath: defaultName,
    filters: [
      { name: 'Chess Games', extensions: ['pgn'] },
      { name: 'All Files', extensions: ['*'] }
    ]
  });

  if (!result.canceled && result.filePath) {
    fs.writeFileSync(result.filePath, content, 'utf8');
    return result.filePath;
  }

  return null;
});

// Log unhandled errors
process.on('uncaughtException', (error) => {
  console.error('Uncaught exception:', error);
});

process.on('unhandledRejection', (error) => {
  console.error('Unhandled rejection:', error);
});
