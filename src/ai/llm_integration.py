"""
LLM Integration - Interface to Claude/GPT/Ollama for natural language explanations
"""

import os
from typing import Optional, Dict, List
from dotenv import load_dotenv

load_dotenv()


class LLMIntegration:
    """
    Integration with Large Language Models for generating chess explanations.
    Supports: Anthropic Claude, OpenAI GPT, and Ollama (free, local).
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        provider: str = "ollama",  # Changed default to free option
    ):
        """
        Initialize LLM integration.

        Args:
            api_key: API key for LLM service (not needed for Ollama)
            model: Model to use (defaults to env variable)
            provider: "ollama" (free), "anthropic", or "openai"
        """
        self.provider = provider
        self.api_key = api_key or self._get_api_key() if provider != "ollama" else None

        # Set default model based on provider
        if provider == "ollama":
            self.model = model or os.getenv("AI_MODEL", "llama3.2:3b")
        else:
            self.model = model or os.getenv("AI_MODEL", "claude-3-5-sonnet-20241022")

        self.client = None
        self._initialize_client()

    def _get_api_key(self) -> str:
        """Get API key from environment."""
        if self.provider == "ollama":
            return None  # Ollama doesn't need API key
        elif self.provider == "anthropic":
            key = os.getenv("ANTHROPIC_API_KEY")
            if not key:
                raise ValueError("ANTHROPIC_API_KEY not set in environment")
        else:
            key = os.getenv("OPENAI_API_KEY")
            if not key:
                raise ValueError("OPENAI_API_KEY not set in environment")
        return key

    def _initialize_client(self):
        """Initialize the LLM client."""
        if self.provider == "ollama":
            try:
                from .ollama_client import OllamaClient
                self.client = OllamaClient(model=self.model)
            except ImportError:
                raise ImportError(
                    "ollama_client not found. Make sure ollama_client.py is in the ai module."
                )
        elif self.provider == "anthropic":
            try:
                from anthropic import Anthropic
                self.client = Anthropic(api_key=self.api_key)
            except ImportError:
                raise ImportError(
                    "anthropic package not installed. Run: pip install anthropic"
                )
        else:  # openai
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
            except ImportError:
                raise ImportError(
                    "openai package not installed. Run: pip install openai"
                )

    def explain_position(
        self,
        fen: str,
        evaluation: Dict,
        context: Optional[str] = None,
    ) -> str:
        """
        Generate a natural language explanation of a chess position.

        Args:
            fen: Position in FEN notation
            evaluation: Position evaluation dictionary
            context: Optional additional context

        Returns:
            Natural language explanation
        """
        prompt = self._build_position_prompt(fen, evaluation, context)
        return self._generate_response(prompt)

    def explain_mistake(
        self,
        move_analysis: Dict,
        player_level: str = "intermediate",
    ) -> str:
        """
        Explain why a move was a mistake and suggest improvements.

        Args:
            move_analysis: Move analysis dictionary from GameAnalyzer
            player_level: "beginner", "intermediate", "advanced"

        Returns:
            Natural language explanation of the mistake
        """
        prompt = self._build_mistake_prompt(move_analysis, player_level)
        return self._generate_response(prompt)

    def generate_study_plan(
        self,
        weaknesses: List[str],
        strengths: List[str],
        goals: Optional[str] = None,
    ) -> str:
        """
        Generate a personalized study plan based on player analysis.

        Args:
            weaknesses: List of identified weaknesses
            strengths: List of identified strengths
            goals: Optional player goals

        Returns:
            Personalized study plan
        """
        prompt = f"""
You are an expert chess coach. Based on the following player analysis, create a personalized
study plan to help them improve.

Weaknesses:
{chr(10).join(f'- {w}' for w in weaknesses)}

Strengths:
{chr(10).join(f'- {s}' for s in strengths)}

{f'Player Goals: {goals}' if goals else ''}

Provide a structured 4-week study plan with:
1. Focus areas for each week
2. Specific exercises and resources
3. Time allocation recommendations
4. Progress checkpoints

Keep the plan practical and achievable.
"""
        return self._generate_response(prompt)

    def explain_tactical_pattern(
        self,
        pattern_name: str,
        fen: str,
        solution: Optional[str] = None,
    ) -> str:
        """
        Explain a tactical pattern found in a position.

        Args:
            pattern_name: Name of the tactical pattern (e.g., "pin", "fork")
            fen: Position demonstrating the pattern
            solution: Optional solution moves

        Returns:
            Explanation of the tactical pattern
        """
        prompt = f"""
Explain the chess tactical pattern "{pattern_name}" found in this position.

Position (FEN): {fen}

{f'Solution: {solution}' if solution else ''}

Provide:
1. Clear definition of the {pattern_name} pattern
2. How to recognize it in this position
3. How to exploit it
4. How to avoid falling victim to it

Keep the explanation clear and educational.
"""
        return self._generate_response(prompt)

    def _build_position_prompt(
        self,
        fen: str,
        evaluation: Dict,
        context: Optional[str] = None,
    ) -> str:
        """Build prompt for position explanation."""
        score = evaluation.get("engine_evaluation", {}).get("score", "unclear")
        phase = evaluation.get("game_phase", "unknown")
        material_balance = evaluation.get("material_balance", 0)

        prompt = f"""
Analyze and explain this chess position in clear, educational language.

Position (FEN): {fen}
Engine Evaluation: {score} centipawns
Game Phase: {phase}
Material Balance: {'+' if material_balance > 0 else ''}{material_balance} for {'white' if material_balance > 0 else 'black'}

{f'Context: {context}' if context else ''}

Provide:
1. Overall assessment of the position
2. Key features and imbalances
3. Plans for both sides
4. Most important considerations

Keep it concise and instructive.
"""
        return prompt

    def _build_mistake_prompt(
        self,
        move_analysis: Dict,
        player_level: str,
    ) -> str:
        """Build prompt for mistake explanation."""
        move = move_analysis["move_played"]
        best = move_analysis["best_move"]
        loss = move_analysis["eval_loss"]
        mistake_type = move_analysis["mistake_type"]

        level_context = {
            "beginner": "Use simple language and focus on basic concepts.",
            "intermediate": "Assume knowledge of basic tactics and strategy.",
            "advanced": "Provide deep positional and tactical insights.",
        }

        prompt = f"""
Explain this chess mistake to a {player_level} player.

Move Played: {move}
Best Move: {best}
Evaluation Loss: {loss} centipawns
Mistake Type: {mistake_type}
Position (FEN): {move_analysis.get('fen_before', '')}

{level_context.get(player_level, '')}

Explain:
1. Why the played move was a {mistake_type}
2. What the best move accomplishes
3. The key difference between them
4. How to recognize this pattern in future games

Be encouraging and educational.
"""
        return prompt

    def _generate_response(self, prompt: str) -> str:
        """
        Generate response from LLM.

        Args:
            prompt: The prompt to send

        Returns:
            LLM response text
        """
        try:
            if self.provider == "ollama":
                # Ollama local generation
                from .ollama_client import KidFriendlyPrompts
                system_prompt = KidFriendlyPrompts.explain_position("7-12")
                return self.client.generate(prompt, system_prompt=system_prompt)

            elif self.provider == "anthropic":
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=int(os.getenv("AI_MAX_TOKENS", "1024")),
                    temperature=float(os.getenv("AI_TEMPERATURE", "0.7")),
                    messages=[{"role": "user", "content": prompt}],
                )
                return response.content[0].text

            else:  # OpenAI
                response = self.client.chat.completions.create(
                    model=self.model,
                    max_tokens=int(os.getenv("AI_MAX_TOKENS", "1024")),
                    temperature=float(os.getenv("AI_TEMPERATURE", "0.7")),
                    messages=[{"role": "user", "content": prompt}],
                )
                return response.choices[0].message.content

        except Exception as e:
            return f"Error generating explanation: {str(e)}"

    def summarize_game(self, game_analysis: Dict) -> str:
        """
        Generate a summary of a complete game analysis.

        Args:
            game_analysis: Complete game analysis dictionary

        Returns:
            Game summary with key insights
        """
        white = game_analysis["metadata"]["white"]
        black = game_analysis["metadata"]["black"]
        result = game_analysis["metadata"]["result"]

        white_stats = game_analysis["statistics"]["white"]
        black_stats = game_analysis["statistics"]["black"]

        prompt = f"""
Summarize this chess game analysis:

Game: {white} vs {black}
Result: {result}

White Statistics:
- Accuracy: {white_stats['accuracy']}%
- Blunders: {white_stats['blunders']}
- Mistakes: {white_stats['mistakes']}
- Average Centipawn Loss: {white_stats['average_centipawn_loss']:.1f}

Black Statistics:
- Accuracy: {black_stats['accuracy']}%
- Blunders: {black_stats['blunders']}
- Mistakes: {black_stats['mistakes']}
- Average Centipawn Loss: {black_stats['average_centipawn_loss']:.1f}

Provide:
1. Overall game summary
2. Key turning points
3. Main takeaways for each player
4. Suggestions for improvement

Keep it concise and actionable.
"""
        return self._generate_response(prompt)
