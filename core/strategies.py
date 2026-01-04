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
        
        Args:
            content: Raw LaTeX content
            
        Returns:
            Cleaned LaTeX content
        """
        lines = content.split('\n')
        cleaned_lines = []
        
        # Allowed packages (standard, commonly available)
        allowed_packages = {
            'amsmath', 'amssymb', 'amsthm', 'graphicx', 'geometry', 
            'inputenc', 'fontenc', 'babel', 'xcolor', 'listings',
            'tikz', 'pgf', 'pgfplots', 'array', 'tabularx', 'booktabs'
        }
        
        for line in lines:
            # Remove problematic usepackage commands
            if '\\usepackage' in line.lower():
                # Check if it's an allowed package
                package_used = False
                for pkg in allowed_packages:
                    if pkg in line.lower():
                        cleaned_lines.append(line)
                        package_used = True
                        break
                # If not allowed package, skip this line
                if not package_used:
                    continue
            # Remove problematic commands that require missing packages (but allow captionof)
            elif any(cmd in line for cmd in ['\\fancyhead', '\\hypersetup']):
                # Skip lines with problematic commands (but allow \captionof)
                continue
            else:
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)


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


