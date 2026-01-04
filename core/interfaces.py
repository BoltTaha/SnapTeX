"""
Abstract base classes (interfaces) for SOLID principles compliance.
Following Dependency Inversion Principle (DIP).
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class ICodeGenerator(ABC):
    """Abstract interface for LLM providers (Gemini, GPT-4, Claude, etc.)."""
    
    @abstractmethod
    def generate_code(self, image_path: str) -> str:
        """
        Generate LaTeX code from an image.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Generated LaTeX code as string
        """
        pass


class IImageLoader(ABC):
    """Abstract interface for image loading (PDF, single images, batch images)."""
    
    @abstractmethod
    def load_images(self, source: str | List[str]) -> List[Dict[str, Any]]:
        """
        Load images from source (PDF, single image, or batch of images).
        
        Args:
            source: File path (str) for PDF/single image, or list of paths for batch images
            
        Returns:
            List of dictionaries with 'path' and 'index' keys
        """
        pass


class IOutputBuilder(ABC):
    """Abstract interface for output generation (LaTeX, Markdown, etc.)."""
    
    @abstractmethod
    def build_output(self, content: str, output_path: str) -> str:
        """
        Build output file from content.
        
        Args:
            content: Content to write (LaTeX code, Markdown, etc.)
            output_path: Path where output file should be saved
            
        Returns:
            Path to the created output file
        """
        pass


class IOutputStrategy(ABC):
    """Abstract interface for output format strategies."""
    
    @abstractmethod
    def format_output(self, content: str) -> str:
        """
        Format content according to strategy (LaTeX, Markdown, etc.).
        
        Args:
            content: Raw content to format
            
        Returns:
            Formatted content
        """
        pass

