"""
LaTeX Compiler - Compiles .tex files to PDF.
Single Responsibility: ONLY compiles .tex to PDF.
"""

import subprocess
import os
from pathlib import Path
from typing import Optional


class LaTeXCompiler:
    """Service for compiling LaTeX files to PDF."""
    
    def __init__(self):
        """Initialize LaTeX compiler."""
        self.pdflatex_cmd = "pdflatex"
    
    def compile(self, tex_path: str, output_dir: Optional[str] = None) -> str:
        """
        Compile .tex file to PDF using pdflatex.
        
        Args:
            tex_path: Path to .tex file
            output_dir: Optional output directory (defaults to same as .tex file)
            
        Returns:
            Path to compiled PDF file
            
        Raises:
            Exception: If compilation fails
        """
        tex_file = Path(tex_path)
        
        if not tex_file.exists():
            raise FileNotFoundError(f"LaTeX file not found: {tex_path}")
        
        if tex_file.suffix != '.tex':
            raise ValueError(f"File must have .tex extension: {tex_path}")
        
        # Set output directory
        if output_dir:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            work_dir = str(output_path)
        else:
            work_dir = str(tex_file.parent)
        
        # Compile LaTeX
        try:
            # Run pdflatex (twice for references)
            # Use absolute path for tex file
            tex_abs_path = str(tex_file.resolve())
            cmd = [
                self.pdflatex_cmd,
                "-interaction=nonstopmode",
                "-output-directory", work_dir,
                tex_abs_path
            ]
            
            # First compilation (run from tex file directory to find includes)
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(tex_file.parent)
            )
            
            # Second compilation for references
            subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(tex_file.parent)
            )
            
            # Check if PDF was created
            # pdflatex creates PDF in output-directory with the same name as input
            pdf_path = Path(work_dir) / f"{tex_file.stem}.pdf"
            
            if not pdf_path.exists():
                # Try in current directory as fallback
                pdf_path = tex_file.parent / f"{tex_file.stem}.pdf"
            
            if not pdf_path.exists():
                error_msg = result.stderr if result.stderr else result.stdout
                raise Exception(f"PDF compilation failed. LaTeX output: {error_msg}")
            
            # Clean up auxiliary files
            self._cleanup_auxiliary_files(work_dir, tex_file.stem)
            
            return str(pdf_path)
            
        except FileNotFoundError:
            raise Exception("pdflatex not found. Please install TeX Live.")
        except Exception as e:
            raise Exception(f"LaTeX compilation failed: {str(e)}")
    
    def _cleanup_auxiliary_files(self, work_dir: str, base_name: str):
        """
        Clean up auxiliary files created during compilation.
        
        Args:
            work_dir: Working directory
            base_name: Base name of the LaTeX file
        """
        aux_extensions = ['.aux', '.log', '.out', '.toc', '.lof', '.lot']
        
        for ext in aux_extensions:
            aux_file = Path(work_dir) / f"{base_name}{ext}"
            if aux_file.exists():
                try:
                    aux_file.unlink()
                except:
                    pass  # Ignore cleanup errors

