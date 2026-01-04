"""
Strategy Pattern - Output format strategies.
"""

from abc import ABC, abstractmethod
from core.interfaces import IOutputStrategy


class OutputStrategy(ABC):
    """Abstract base class for output strategies."""
    
    @abstractmethod
    def format_output(self, content: str) -> str:
        """Format content according to strategy."""
        pass


class LaTeXStrategy(OutputStrategy):
    """Strategy for LaTeX output format."""
    
    def format_output(self, content: str) -> str:
        """
        Format content as LaTeX.
        
        Args:
            content: Raw LaTeX content
            
        Returns:
            Formatted LaTeX document
        """
        # Wrap content in basic LaTeX document structure if not already wrapped
        if not content.strip().startswith("\\documentclass"):
            latex_doc = f"""\\documentclass{{article}}
\\usepackage{{amsmath}}
\\usepackage{{amssymb}}
\\usepackage{{graphicx}}
\\begin{{document}}

{content}

\\end{{document}}"""
            return latex_doc
        
        return content


class MarkdownStrategy(OutputStrategy):
    """Strategy for Markdown output format (future extension)."""
    
    def format_output(self, content: str) -> str:
        """Format content as Markdown."""
        # Future implementation
        return content


class PlainTextStrategy(OutputStrategy):
    """Strategy for plain text output format (future extension)."""
    
    def format_output(self, content: str) -> str:
        """Format content as plain text."""
        # Future implementation
        return content


