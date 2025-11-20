/**
 * Electron Preload Script
 *
 * This script runs in a sandboxed context with access to both Node.js APIs
 * and the DOM. It exposes a safe API to the renderer process.
 */

const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods to renderer process
contextBridge.exposeInMainWorld('electronAPI', {
  /**
   * Get the Python API URL.
   */
  getApiUrl: () => ipcRenderer.invoke('get-api-url'),

  /**
   * Check if the backend is ready.
   */
  checkBackend: () => ipcRenderer.invoke('check-backend'),

  /**
   * Get a setting value.
   * @param {string} key - Setting key
   * @param {any} defaultValue - Default value if not found
   */
  getSetting: (key, defaultValue) => ipcRenderer.invoke('get-setting', key, defaultValue),

  /**
   * Set a setting value.
   * @param {string} key - Setting key
   * @param {any} value - Setting value
   */
  setSetting: (key, value) => ipcRenderer.invoke('set-setting', key, value),

  /**
   * Open a file dialog to select a PGN file.
   * @returns {Promise<{path: string, content: string} | null>}
   */
  openFileDialog: () => ipcRenderer.invoke('open-file-dialog'),

  /**
   * Open a save file dialog.
   * @param {string} content - File content to save
   * @param {string} defaultName - Default file name
   * @returns {Promise<string | null>} - Saved file path or null if canceled
   */
  saveFileDialog: (content, defaultName) => ipcRenderer.invoke('save-file-dialog', content, defaultName),

  /**
   * Get platform information.
   */
  platform: process.platform,

  /**
   * Get app version.
   */
  version: process.env.npm_package_version || '0.3.0'
});

// Log when preload is loaded
console.log('Preload script loaded successfully');
