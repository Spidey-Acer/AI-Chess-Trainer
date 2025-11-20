"""Ollama model manager for desktop app."""

import subprocess
import requests
import logging
import os
from pathlib import Path
from typing import Optional, List, Dict

logger = logging.getLogger(__name__)


class OllamaManager:
    """Manages Ollama installation and models."""

    def __init__(self, ollama_url: str = "http://localhost:11434"):
        self.ollama_url = ollama_url
        self.ollama_process = None

    def is_running(self) -> bool:
        """Check if Ollama is running."""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=2)
            return response.status_code == 200
        except Exception:
            return False

    def start_ollama(self, ollama_path: Optional[str] = None) -> bool:
        """Start Ollama server."""
        if self.is_running():
            logger.info("Ollama is already running")
            return True

        try:
            # Try to find Ollama binary
            if not ollama_path:
                ollama_path = self._find_ollama()

            if not ollama_path:
                logger.error("Ollama binary not found")
                return False

            # Start Ollama server
            self.ollama_process = subprocess.Popen(
                [ollama_path, "serve"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            logger.info(f"Started Ollama server (PID: {self.ollama_process.pid})")
            return True

        except Exception as e:
            logger.error(f"Failed to start Ollama: {e}")
            return False

    def stop_ollama(self):
        """Stop Ollama server."""
        if self.ollama_process:
            self.ollama_process.terminate()
            self.ollama_process.wait(timeout=5)
            self.ollama_process = None
            logger.info("Stopped Ollama server")

    def list_models(self) -> List[Dict]:
        """List installed models."""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data.get('models', [])
            return []
        except Exception as e:
            logger.error(f"Failed to list models: {e}")
            return []

    def has_model(self, model_name: str) -> bool:
        """Check if a model is installed."""
        models = self.list_models()
        return any(model['name'].startswith(model_name) for model in models)

    def pull_model(self, model_name: str) -> bool:
        """Download a model."""
        try:
            logger.info(f"Pulling model: {model_name}")
            response = requests.post(
                f"{self.ollama_url}/api/pull",
                json={"name": model_name},
                stream=True,
                timeout=600
            )

            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        logger.info(line.decode('utf-8'))
                return True
            return False

        except Exception as e:
            logger.error(f"Failed to pull model: {e}")
            return False

    def delete_model(self, model_name: str) -> bool:
        """Delete a model."""
        try:
            response = requests.delete(
                f"{self.ollama_url}/api/delete",
                json={"name": model_name},
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Failed to delete model: {e}")
            return False

    def generate(self, model: str, prompt: str) -> Optional[str]:
        """Generate text with a model."""
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60
            )

            if response.status_code == 200:
                return response.json().get('response')
            return None

        except Exception as e:
            logger.error(f"Failed to generate: {e}")
            return None

    def _find_ollama(self) -> Optional[str]:
        """Find Ollama binary in system paths."""
        # Check common installation paths
        paths = [
            '/usr/local/bin/ollama',
            '/usr/bin/ollama',
            '/opt/homebrew/bin/ollama',
            'C:\\Program Files\\Ollama\\ollama.exe',
            'C:\\ollama\\ollama.exe',
        ]

        for path in paths:
            if os.path.exists(path):
                return path

        # Try to find in PATH
        try:
            result = subprocess.run(
                ['which', 'ollama'] if os.name != 'nt' else ['where', 'ollama'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception:
            pass

        return None
