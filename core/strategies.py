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
        Generic approach - works for any LaTeX content.
        
        Args:
            content: LaTeX content to analyze
            
        Returns:
            Command definitions string (empty if no commands needed)
        """
        import re
        
        # Find all command usages (e.g., \commandname, \classname, \method, etc.)
        # Pattern: \commandname{ or \commandname  or \commandname\n
        command_pattern = r'\\(\w+)(?=\{| |\n|$)'
        commands_used = set(re.findall(command_pattern, content))
        
        # Known LaTeX commands that don't need definition
        standard_commands = {
            'documentclass', 'usepackage', 'begin', 'end', 'document',
            'item', 'textbf', 'textit', 'emph', 'texttt', 'textsc',
            'section', 'subsection', 'subsubsection', 'paragraph',
            'caption', 'label', 'ref', 'cite', 'input', 'include',
            'includegraphics', 'tikz', 'node', 'draw', 'fill', 'path',
            'coordinate', 'tikzpicture', 'pgfpicture', 'pgfsetcolor',
            'pgfusepath', 'pgfpath', 'pgfpoint', 'pgfkeys',
            'newcommand', 'renewcommand', 'def', 'newcommand', 
            'providecommand', 'DeclareRobustCommand',
            'math', 'text', 'mbox', 'fbox', 'makebox',
            'centering', 'raggedright', 'raggedleft',
            'hspace', 'vspace', 'hfill', 'vfill',
            'newline', 'linebreak', 'newpage', 'clearpage',
            'par', 'vskip', 'hskip', 'rule',
            'addcontentsline', 'tableofcontents', 'listoffigures', 'listoftables',
            'title', 'author', 'date', 'maketitle',
            'pagestyle', 'thispagestyle', 'pagenumbering',
            'footnote', 'marginpar', 'footnotemark', 'footnotetext',
            'equation', 'eqnarray', 'align', 'gather', 'multline',
            'frac', 'sqrt', 'sum', 'int', 'prod', 'lim',
            'left', 'right', 'big', 'Big', 'bigg', 'Bigg',
            'overbrace', 'underbrace', 'overline', 'underline',
            'matrix', 'pmatrix', 'bmatrix', 'vmatrix', 'Vmatrix',
            'cases', 'array', 'eqnarray', 'split',
            'table', 'tabular', 'array', 'longtable',
            'figure', 'minipage', 'parbox',
            'verb', 'verbatim', 'lstlisting',
            'url', 'href', 'nolinkurl',
            'color', 'textcolor', 'colorbox', 'fcolorbox',
            'makeatletter', 'makeatother',
            'ifthenelse', 'whiledo',
            'newcounter', 'setcounter', 'addtocounter', 'stepcounter',
            'newlength', 'setlength', 'addtolength',
            'newsavebox', 'savebox', 'usebox',
            'newenvironment', 'renewenvironment',
            'newcommand', 'renewcommand',
            'providecommand', 'DeclareRobustCommand',
            'hyphenation', 'sloppy', 'fussy',
            'the', 'value', 'arabic', 'roman', 'Roman', 'alph', 'Alph',
            'addtocontents', 'addcontentsline',
            'appendix', 'appendixpage',
            'index', 'glossary', 'nomenclature',
            'makeindex', 'makeglossary',
            'bibliography', 'bibliographystyle',
            'cite', 'citep', 'citet', 'citeauthor', 'citeyear',
            'addbibresource', 'printbibliography',
            'index', 'glossary', 'nomenclature',
            'makeindex', 'makeglossary',
            'pagestyle', 'thispagestyle', 'pagenumbering',
            'fancyhead', 'fancyfoot', 'fancypagestyle',
            'hypersetup', 'urlstyle', 'urldef',
            'captionof', 'caption', 'label', 'ref', 'pageref',
            'includegraphics', 'graphicspath',
            'tikzset', 'pgfkeys', 'pgfqkeys',
            'draw', 'fill', 'shade', 'clip', 'scope',
            'node', 'coordinate', 'path', 'pgfpath', 'pgfusepath',
            'pgfpoint', 'pgfsetlinewidth', 'pgfsetdash',
            'pgfsetcolor', 'pgfsetfillcolor',
            'pgfsetarrows', 'pgfsetarrowoptions',
            'pgfsetroundcap', 'pgfsetroundjoin',
            'pgfsetmiterlimit', 'pgfsetlinejoin',
            'pgfsetcapbutt', 'pgfsetcapround', 'pgfsetcaprect',
            'pgfsetlinewidth', 'pgfsetdash',
            'pgfsetfillcolor', 'pgfsetcolor',
            'pgfsetarrows', 'pgfsetarrowoptions',
            'pgfsetroundcap', 'pgfsetroundjoin',
            'pgfsetmiterlimit', 'pgfsetlinejoin',
            'pgfsetcapbutt', 'pgfsetcapround', 'pgfsetcaprect',
            'nodepart', 'anchor', 'above', 'below', 'left', 'right',
            'above left', 'above right', 'below left', 'below right',
            'anchor', 'label', 'pin', 'edge', 'child', 'parent',
            'foreach', 'let', 'pgfmathparse', 'pgfmathresult',
            'pgfmathtruncatemacro', 'pgfmathsetmacro',
            'pgfmathsetlength', 'pgfmathsetcount',
            'pgfmathdeclaredim', 'pgfmathsetdim',
            'pgfmathadd', 'pgfmathsubtract', 'pgfmathmultiply',
            'pgfmathdivide', 'pgfmathmod', 'pgfmathpower',
            'pgfmathsqrt', 'pgfmathabs', 'pgfmathround',
            'pgfmathfloor', 'pgfmathceil', 'pgfmathint',
            'pgfmathsetseed', 'pgfmathrandom',
            'pgfmathrandominteger', 'pgfmathrandomuniform',
            'pgfmathrandomnormal', 'pgfmathrandomsign',
            'pgfmathrandomint', 'pgfmathrandomuniformint',
            'pgfmathrandomnormalint', 'pgfmathrandomsignint',
            'pgfmathdeclarefunction', 'pgfmathdeclarefunction*',
            'pgfmathparse', 'pgfmathresult', 'pgfmathtruncatemacro',
            'pgfmathsetmacro', 'pgfmathsetlength', 'pgfmathsetcount',
            'pgfmathdeclaredim', 'pgfmathsetdim',
            'pgfmathadd', 'pgfmathsubtract', 'pgfmathmultiply',
            'pgfmathdivide', 'pgfmathmod', 'pgfmathpower',
            'pgfmathsqrt', 'pgfmathabs', 'pgfmathround',
            'pgfmathfloor', 'pgfmathceil', 'pgfmathint',
            'pgfmathsetseed', 'pgfmathrandom',
            'pgfmathrandominteger', 'pgfmathrandomuniform',
            'pgfmathrandomnormal', 'pgfmathrandomsign',
            'pgfmathrandomint', 'pgfmathrandomuniformint',
            'pgfmathrandomnormalint', 'pgfmathrandomsignint',
            'pgfmathdeclarefunction', 'pgfmathdeclarefunction*',
        }
        
        # Filter out standard commands
        undefined_commands = commands_used - standard_commands
        
        if not undefined_commands:
            return ""
        
        # Generate command definitions
        definitions = ["% Auto-generated command definitions"]
        for cmd in sorted(undefined_commands):
            # Simple default: just pass through with text formatting
            # User can customize if needed
            definitions.append(f"\\newcommand{{\\{cmd}}}[1]{{#1}}")
        
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


