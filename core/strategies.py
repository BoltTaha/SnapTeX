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
        # Clean up content - remove problematic packages and commands
        cleaned_content = self._clean_latex_content(content)
        
        # Always wrap in document structure (cleaned_content is body only)
        # Check if TikZ is needed (tikzpicture or tikz in content)
        uses_tikz = 'tikzpicture' in cleaned_content.lower() or '\\tikz' in cleaned_content or 'nodepart' in cleaned_content.lower()
        
        # Define common commands that might be used in diagrams
        common_commands = ""
        if uses_tikz and ('\\method' in cleaned_content or '\\attribute' in cleaned_content or '\\classname' in cleaned_content):
            common_commands = """% Define common UML diagram commands
\\newcommand{\\classname}[1]{\\textbf{#1}}
\\newcommand{\\attribute}[1]{\\textit{#1}}
\\newcommand{\\method}[1]{\\textit{#1}}"""
        
        latex_doc = f"""\\documentclass{{article}}
\\usepackage{{amsmath}}
\\usepackage{{amssymb}}
\\usepackage{{graphicx}}"""
        
        if uses_tikz:
            latex_doc += "\n\\usepackage{tikz}\n\\usetikzlibrary{shapes.multipart,arrows,positioning}"
        
        if common_commands:
            latex_doc += f"\n{common_commands}"
        
        latex_doc += f"""
\\begin{{document}}

{cleaned_content}

\\end{{document}}"""
        return latex_doc
    
    def _clean_latex_content(self, content: str) -> str:
        """
        Clean LaTeX content by removing problematic packages and commands.
        Separates preamble from body content.
        
        Args:
            content: Raw LaTeX content
            
        Returns:
            Cleaned LaTeX content (body only, no preamble)
        """
        lines = content.split('\n')
        body_lines = []
        
        for line in lines:
            # Skip documentclass, usepackage, usetikzlibrary, and other preamble commands
            if any(cmd in line.lower() for cmd in ['\\documentclass', '\\usepackage', '\\usetikzlibrary', '\\newcommand', '\\newcommand']):
                continue  # Skip preamble commands - we add them separately in format_output
            
            # Skip begin/end document if present (we add our own)
            if '\\begin{document}' in line.lower() or '\\end{document}' in line.lower():
                continue
            
            # Remove problematic commands that require missing packages
            if any(cmd in line for cmd in ['\\fancyhead', '\\hypersetup']):
                continue
            
            # Add all other lines to body
            body_lines.append(line)
        
        return '\n'.join(body_lines)


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


