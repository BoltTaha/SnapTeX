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
        
        # Flash Models (Map old 1.5 and generic names to 2.5)
        if model_type in ["gemini-flash", "gemini-1.5-flash", "gemini-2.5-flash", "gemini-flash-latest"]:
            return GeminiService(model_name="gemini-2.5-flash")
        # Pro Models (Map old 1.5 and generic names to 2.5)
        elif model_type in ["gemini-pro", "gemini-1.5-pro", "gemini-2.5-pro", "gemini-pro-latest"]:
            return GeminiService(model_name="gemini-2.5-pro")
        # Future: Add GPT-4, Claude, etc.
        # elif model_type == "gpt-4o":
        #     return GPT4Service()
        else:
            raise ValueError(f"Unsupported model type: {model_type}")


