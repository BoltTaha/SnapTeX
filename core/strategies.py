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
        
        # Dynamically detect undefined commands and define them
        # This makes it generic - works for any LaTeX content
        command_definitions = self._detect_and_define_commands(cleaned_content)
        
        latex_doc = f"""\\documentclass{{article}}
\\usepackage{{amsmath}}
\\usepackage{{amssymb}}
\\usepackage{{graphicx}}"""
        
        if uses_tikz:
            latex_doc += "\n\\usepackage{tikz}\n\\usetikzlibrary{shapes.multipart,arrows,positioning}"
        
        if command_definitions:
            latex_doc += f"\n{command_definitions}"
        
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
            
            # Fix common typos: \class name -> \classname (remove space)
            line = line.replace('\\class name{', '\\classname{')
            line = line.replace('\\class name ', '\\classname ')
            line = line.replace('\\class name\n', '\\classname\n')
            
            # Add all other lines to body
            body_lines.append(line)
        
        return '\n'.join(body_lines)
    
    def _detect_and_define_commands(self, content: str) -> str:
        """
        Dynamically detect undefined commands in LaTeX content and define them.
        Generic approach - works for any LaTeX content, automatically adapts.
        Uses \\providecommand so it won't redefine existing commands.
        
        Args:
            content: LaTeX content to analyze
            
        Returns:
            Command definitions string (empty if no commands needed)
        """
        import re
        
        # Find all command usages (e.g., \commandname, \classname, \method, etc.)
        # Pattern: \commandname{ or \commandname  or \commandname\n
        command_pattern = r'\\(\w+)(?=\{| |\n|$|\\|,|\.|;|:|\]|\)|!)'
        commands_used = set(re.findall(command_pattern, content))
        
        # Very basic commands that we know are standard (avoid redefining these)
        # Using providecommand makes this safer, but we filter these anyway
        basic_commands = {
            'documentclass', 'usepackage', 'begin', 'end', 'document',
            'item', 'textbf', 'textit', 'emph', 'textsc', 'textmd',
            'section', 'subsection', 'subsubsection', 'paragraph',
            'caption', 'label', 'ref', 'cite', 'input', 'include',
            'includegraphics', 'tikz', 'node', 'draw', 'fill', 'path',
            'coordinate', 'tikzpicture', 'nodepart',
            'newcommand', 'renewcommand', 'providecommand',
            'math', 'text', 'mbox', 'fbox',
            'centering', 'hspace', 'vspace',
            'newline', 'linebreak', 'newpage', 'clearpage',
            'par', 'rule', 'title', 'author', 'date', 'maketitle',
            'footnote', 'equation', 'align', 'gather',
            'frac', 'sqrt', 'sum', 'int', 'prod', 'lim',
            'left', 'right', 'big', 'Big', 'bigg', 'Bigg',
            'matrix', 'pmatrix', 'bmatrix', 'table', 'tabular',
            'figure', 'verb', 'verbatim', 'color', 'textcolor',
            'makeatletter', 'makeatother',
        }
        
        # Filter out basic commands (use providecommand so it won't redefine anyway)
        custom_commands = commands_used - basic_commands
        
        if not custom_commands:
            return ""
        
        # Generate command definitions using \providecommand (safer - won't redefine existing)
        definitions = ["% Auto-generated command definitions (generic)"]
        for cmd in sorted(custom_commands):
            # Use providecommand - only defines if not already defined
            definitions.append(f"\\providecommand{{\\{cmd}}}[1]{{#1}}")
        
        return "\n".join(definitions)


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


