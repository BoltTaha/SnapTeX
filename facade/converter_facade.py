"""
Facade Pattern - ConverterFacade hides complexity from user.
"""

import os
import time
from typing import List, Dict, Any, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from core.factories import ModelFactory
from core.strategies import LaTeXStrategy
from services.pdf_processor import ImageLoader
from services.output_builder import LaTeXBuilder
from services.latex_compiler import LaTeXCompiler
from core.interfaces import ICodeGenerator, IImageLoader, IOutputBuilder


class ConverterFacade:
    """Facade for converting PDF/images to LaTeX/PDF."""
    
    def __init__(self, model_type: str = "gemini-flash", max_workers: int = 4, session_id: str = "default"):
        """
        Initialize converter facade.
        
        Args:
            model_type: Type of model to use (default: "gemini-flash")
            max_workers: Maximum number of parallel workers (default: 4)
            session_id: Unique session ID for temp folder isolation (default: "default")
        """
        self.model: ICodeGenerator = ModelFactory.get_model(model_type)
        self.image_loader: IImageLoader = ImageLoader(session_id=session_id)
        self.output_builder: IOutputBuilder = LaTeXBuilder()
        self.latex_compiler = LaTeXCompiler()
        self.strategy = LaTeXStrategy()
        self.max_workers = max_workers
        # Unique output directory per session to prevent file collisions
        self.output_dir = Path(f"output_{session_id}")
        self.output_dir.mkdir(exist_ok=True)
    
    def convert(self, file_path: str | List[str], output_format: str = "latex", progress_callback=None) -> Tuple[str, Optional[str]]:
        """
        Convert PDF/images to LaTeX and compiled PDF.
        
        Args:
            file_path: Path to PDF/single image, or list of image paths for batch
            output_format: Output format (default: "latex")
            
        Returns:
            Tuple of (latex_file_path, pdf_file_path)
        """
        # Load images
        image_data = self.image_loader.load_images(file_path)
        
        # Process images (parallel for multiple, single for one)
        if len(image_data) > 1:
            results = self._process_parallel(image_data, progress_callback)
            # Final progress update
            if progress_callback:
                progress_callback(1.0)
        else:
            results = self._process_single(image_data[0])
            results = [results]
            # Single item progress
            if progress_callback:
                progress_callback(1.0)
        
        # ⚠️ CRITICAL: Sort results by index to maintain correct order
        # Threads finish asynchronously - Page 2 might finish before Page 1
        if len(results) > 1:
            # Determine sort key based on type
            if results[0].get('type') == 'pdf_page':
                results.sort(key=lambda x: x.get('page_num', 0) or 0)
            elif results[0].get('type') in ['batch_image', 'single_image']:
                results.sort(key=lambda x: x.get('image_index', 0) or 0)
        
        # Combine all LaTeX code
        latex_contents = []
        for result in results:
            latex_contents.append(result['latex_code'])
        
        combined_latex = "\n\n".join(latex_contents)
        
        # Format using strategy
        formatted_latex = self.strategy.format_output(combined_latex)
        
        # Build output file using session-specific output directory
        # Determine output filename
        if isinstance(file_path, list):
            base_name = "batch_output"
        else:
            base_name = Path(file_path).stem
        
        latex_file_path = self.output_builder.build_output(
            formatted_latex,
            str(self.output_dir / f"{base_name}.tex")
        )
        
        # Compile to PDF (optional - may fail if TeX Live not installed)
        pdf_file_path = None
        try:
            pdf_file_path = self.latex_compiler.compile(latex_file_path)
        except Exception as e:
            # PDF compilation failed, but LaTeX file is still available
            pdf_file_path = None
            print(f"Warning: PDF compilation failed: {str(e)}")
        
        return (latex_file_path, pdf_file_path)
    
    def _process_single(self, image_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a single image.
        
        Args:
            image_data: Dictionary with image path and metadata
            
        Returns:
            Dictionary with LaTeX code and metadata
        """
        image_path = image_data['path']
        index = image_data['index']
        img_type = image_data['type']
        
        # Generate LaTeX code
        latex_code = self.model.generate_code(image_path)
        
        return {
            'latex_code': latex_code,
            'page_num': index if img_type == 'pdf_page' else None,
            'image_index': index if img_type != 'pdf_page' else None,
            'type': img_type
        }
    
    def _process_parallel(self, image_data_list: List[Dict[str, Any]], progress_callback=None) -> List[Dict[str, Any]]:
        """
        Process multiple images in parallel.
        
        Args:
            image_data_list: List of dictionaries with image paths and metadata
            
        Returns:
            List of dictionaries with LaTeX code and metadata
        """
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks with delay to avoid rate limiting
            future_to_data = {}
            for img_data in image_data_list:
                # Submit task
                future = executor.submit(self._process_single, img_data)
                future_to_data[future] = img_data
                
                # Add delay between submissions to avoid rate limit bombing
                # This spaces out requests so they don't hit API simultaneously
                time.sleep(1.5)
            
            # Collect results as they complete
            for future in as_completed(future_to_data):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    # Log error but continue with other images
                    img_data = future_to_data[future]
                    print(f"Error processing {img_data['path']}: {str(e)}")
                    # Add error result to maintain indexing
                    results.append({
                        'latex_code': f"% Error processing image: {str(e)}",
                        'page_num': img_data.get('index') if img_data.get('type') == 'pdf_page' else None,
                        'image_index': img_data.get('index') if img_data.get('type') != 'pdf_page' else None,
                        'type': img_data.get('type', 'unknown')
                    })
        
        return results

