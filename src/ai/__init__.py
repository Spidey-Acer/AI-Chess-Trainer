"""
AI-powered training and feedback modules
"""

from .trainer import ChessTrainer
from .feedback_generator import FeedbackGenerator
from .llm_integration import LLMIntegration

__all__ = ["ChessTrainer", "FeedbackGenerator", "LLMIntegration"]
