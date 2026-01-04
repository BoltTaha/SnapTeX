"""
Factory Pattern - ModelFactory for creating LLM provider instances.
"""

from services.gemini_service import GeminiService
from core.interfaces import ICodeGenerator


class ModelFactory:
    """Factory for creating LLM provider instances."""
    
    @staticmethod
    def get_model(model_type: str) -> ICodeGenerator:
        """
        Get appropriate LLM provider instance.
        
        Args:
            model_type: Type of model ("gemini-flash", "gemini-pro", etc.)
            
        Returns:
            Instance of ICodeGenerator implementation
            
        Raises:
            ValueError: If model_type is not supported
        """
        model_type = model_type.lower()
        
        if model_type in ["gemini-flash", "gemini-1.5-flash"]:
            return GeminiService(model_name="gemini-1.5-flash")
        elif model_type in ["gemini-pro", "gemini-1.5-pro"]:
            return GeminiService(model_name="gemini-1.5-pro")
        # Future: Add GPT-4, Claude, etc.
        # elif model_type == "gpt-4o":
        #     return GPT4Service()
        else:
            raise ValueError(f"Unsupported model type: {model_type}")


