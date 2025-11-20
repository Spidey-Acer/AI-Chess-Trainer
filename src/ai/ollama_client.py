"""
Ollama Client - Free local LLM integration
"""

import requests
from typing import Optional, Dict
import os


class OllamaClient:
    """
    Client for Ollama - run LLMs locally for free.

    Installation:
        curl -fsSL https://ollama.com/install.sh | sh
        ollama pull llama3.2:3b
    """

    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = "llama3.2:3b",
        temperature: float = 0.7,
    ):
        """
        Initialize Ollama client.

        Args:
            base_url: Ollama server URL
            model: Model name (e.g., 'llama3.2:3b', 'mistral:7b')
            temperature: Creativity (0.0-1.0)
        """
        self.base_url = base_url
        self.model = model
        self.temperature = temperature

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generate text from prompt.

        Args:
            prompt: User prompt
            system_prompt: Optional system instructions

        Returns:
            Generated text
        """
        try:
            # Build the full prompt
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"

            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": full_prompt,
                    "temperature": self.temperature,
                    "stream": False,
                },
                timeout=60,
            )

            response.raise_for_status()
            result = response.json()

            return result.get("response", "")

        except requests.exceptions.ConnectionError:
            return (
                "❌ Error: Ollama is not running.\n\n"
                "To fix:\n"
                "1. Install Ollama: curl -fsSL https://ollama.com/install.sh | sh\n"
                "2. Start Ollama: ollama serve\n"
                "3. Download model: ollama pull llama3.2:3b"
            )
        except Exception as e:
            return f"Error generating response: {str(e)}"

    def chat(self, messages: list) -> str:
        """
        Chat with the model (multi-turn conversation).

        Args:
            messages: List of message dicts with 'role' and 'content'

        Returns:
            Generated response
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": self.temperature,
                    "stream": False,
                },
                timeout=60,
            )

            response.raise_for_status()
            result = response.json()

            return result.get("message", {}).get("content", "")

        except Exception as e:
            return f"Error in chat: {str(e)}"

    def is_available(self) -> bool:
        """
        Check if Ollama is running and model is available.

        Returns:
            True if ready to use
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            response.raise_for_status()

            models = response.json().get("models", [])
            model_names = [m.get("name") for m in models]

            return self.model in model_names

        except Exception:
            return False

    def list_models(self) -> list:
        """
        List available models.

        Returns:
            List of model names
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            response.raise_for_status()

            models = response.json().get("models", [])
            return [m.get("name") for m in models]

        except Exception:
            return []

    def pull_model(self, model_name: str) -> bool:
        """
        Download a model.

        Args:
            model_name: Name of model to download

        Returns:
            True if successful
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/pull",
                json={"name": model_name},
                timeout=600,  # 10 minutes for download
            )

            response.raise_for_status()
            return True

        except Exception as e:
            print(f"Error pulling model: {e}")
            return False


class KidFriendlyPrompts:
    """
    Pre-made prompts optimized for teaching kids chess.
    """

    @staticmethod
    def explain_position(age_group: str = "7-12") -> str:
        """Get system prompt for position explanations."""
        if age_group == "7-12":
            return (
                "You are a friendly chess teacher for kids age 7-12. "
                "Use simple words, short sentences, and be very encouraging. "
                "Use emojis occasionally to make it fun. "
                "Never use complex chess notation - explain everything clearly. "
                "Keep explanations under 100 words."
            )
        else:  # 13-17
            return (
                "You are a knowledgeable chess coach for teenagers. "
                "Be clear and educational, but you can use proper chess terminology. "
                "Be encouraging and explain the 'why' behind moves. "
                "Keep explanations concise but thorough."
            )

    @staticmethod
    def explain_mistake(age_group: str = "7-12") -> str:
        """Get system prompt for mistake explanations."""
        if age_group == "7-12":
            return (
                "You are a kind chess teacher helping a child learn from their mistakes. "
                "Be very encouraging and positive - mistakes are how we learn! "
                "Explain what went wrong in simple terms, and what they could do better next time. "
                "Use examples and analogies that kids understand. "
                "Always end with encouragement."
            )
        else:
            return (
                "You are a chess coach analyzing a student's mistake. "
                "Be constructive and educational. Explain what went wrong and why. "
                "Suggest better alternatives and the reasoning behind them. "
                "Help them understand the pattern to avoid it in the future."
            )

    @staticmethod
    def motivational_feedback() -> str:
        """Get system prompt for motivational messages."""
        return (
            "You are an encouraging chess coach. "
            "Give short, motivational feedback that makes kids excited about chess. "
            "Celebrate their progress and encourage them to keep learning. "
            "Be enthusiastic and positive!"
        )


def test_ollama_setup():
    """
    Test if Ollama is set up correctly.

    Returns:
        Dict with setup status
    """
    client = OllamaClient()

    status = {
        "ollama_running": False,
        "model_available": False,
        "models": [],
        "ready": False,
    }

    # Check if Ollama is running
    try:
        response = requests.get(f"{client.base_url}/api/tags", timeout=5)
        status["ollama_running"] = response.status_code == 200
    except Exception:
        pass

    if status["ollama_running"]:
        # Check available models
        status["models"] = client.list_models()
        status["model_available"] = client.model in status["models"]
        status["ready"] = status["model_available"]

    return status


if __name__ == "__main__":
    # Quick test
    print("Testing Ollama setup...")
    status = test_ollama_setup()

    print(f"\n📊 Status:")
    print(f"  Ollama running: {'✅' if status['ollama_running'] else '❌'}")
    print(f"  Model available: {'✅' if status['model_available'] else '❌'}")
    print(f"  Models installed: {', '.join(status['models']) if status['models'] else 'None'}")
    print(f"  Ready to use: {'✅' if status['ready'] else '❌'}")

    if status["ready"]:
        print("\n🎉 Great! Testing generation...")
        client = OllamaClient()
        response = client.generate(
            "Explain in one sentence what chess is to a 10 year old.",
            system_prompt=KidFriendlyPrompts.explain_position("7-12")
        )
        print(f"\nTest response: {response}")
    else:
        print("\n⚠️  Setup needed:")
        if not status["ollama_running"]:
            print("  1. Install Ollama: curl -fsSL https://ollama.com/install.sh | sh")
            print("  2. Start Ollama: ollama serve")
        if not status["model_available"]:
            print("  3. Download model: ollama pull llama3.2:3b")
