"""
Output Builder - Implements IOutputBuilder interface.
Single Responsibility: ONLY saves text to .tex file.
"""

from pathlib import Path
from core.interfaces import IOutputBuilder


class LaTeXBuilder(IOutputBuilder):
    """Service for building LaTeX output files."""
    
    def build_output(self, content: str, output_path: str) -> str:
        """
        Build LaTeX output file from content.
        
        Args:
            content: LaTeX code to save
            output_path: Path where .tex file should be saved
            
        Returns:
            Path to the created .tex file
        """
        path = Path(output_path)
        
        # Ensure directory exists
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Ensure .tex extension
        if path.suffix != '.tex':
            path = path.with_suffix('.tex')
        
        # Write content to file
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return str(path)


