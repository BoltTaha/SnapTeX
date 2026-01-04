"""
PDF Processor - Implements IImageLoader interface.
Single Responsibility: ONLY loads images from PDF, single images, or batch images.
"""

import os
import time
from typing import List, Dict, Any
from pathlib import Path
from pdf2image import convert_from_path
from pdf2image.exceptions import PDFInfoNotInstalledError
from PIL import Image
from core.interfaces import IImageLoader


class ImageLoader(IImageLoader):
    """Service for loading images from PDF, single images, or batch images."""
    
    SUPPORTED_IMAGE_FORMATS = {'.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG'}
    
    def __init__(self, session_id: str = "default"):
        """
        Initialize ImageLoader.
        
        Args:
            session_id: Unique session ID for temp folder isolation (default: "default")
        """
        self.session_id = session_id
    
    def load_images(self, source: str | List[str]) -> List[Dict[str, Any]]:
        """
        Load images from source (PDF, single image, or batch of images).
        
        Args:
            source: File path (str) for PDF/single image, or list of paths for batch images
            
        Returns:
            List of dictionaries with 'path', 'index', and 'type' keys
        """
        if isinstance(source, list):
            # Batch images
            return self._load_batch_images(source)
        elif isinstance(source, str):
            # Check if it's a PDF or single image
            path = Path(source)
            if path.suffix.lower() == '.pdf':
                return self._load_pdf_images(source)
            else:
                return self._load_single_image(source)
        else:
            raise ValueError(f"Invalid source type: {type(source)}")
    
    def _load_pdf_images(self, pdf_path: str) -> List[Dict[str, Any]]:
        """
        Convert PDF pages to images.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            List of dictionaries with image paths and page numbers
        """
        try:
            # Convert PDF to images
            images = convert_from_path(pdf_path)
            
            # Save images temporarily with session-specific folder to avoid collisions
            pdf_name = Path(pdf_path).stem
            # Use session_id to match UI's temp folder structure
            temp_dir = Path(f"temp_images_{self.session_id}")
            temp_dir.mkdir(exist_ok=True)
            
            result = []
            for idx, image in enumerate(images, start=1):
                # Save image
                image_path = temp_dir / f"{pdf_name}_page_{idx}.png"
                image.save(image_path, "PNG")
                
                result.append({
                    'path': str(image_path),
                    'index': idx,
                    'type': 'pdf_page'
                })
            
            return result
            
        except PDFInfoNotInstalledError:
            # User-friendly error message for missing Poppler
            raise Exception("Poppler is not installed or not in PATH. Please install Poppler to process PDFs. See README.md for installation instructions.")
        except Exception as e:
            raise Exception(f"Failed to load PDF images: {str(e)}")
    
    def _load_single_image(self, image_path: str) -> List[Dict[str, Any]]:
        """
        Load a single image file.
        
        Args:
            image_path: Path to image file
            
        Returns:
            List with single dictionary containing image path
        """
        path = Path(image_path)
        
        # Validate format
        if path.suffix not in self.SUPPORTED_IMAGE_FORMATS:
            raise ValueError(f"Unsupported image format: {path.suffix}. Supported: {self.SUPPORTED_IMAGE_FORMATS}")
        
        # Validate file exists
        if not path.exists():
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        # Validate it's actually an image
        try:
            Image.open(image_path).verify()
        except Exception as e:
            raise ValueError(f"Invalid image file: {str(e)}")
        
        return [{
            'path': str(image_path),
            'index': 1,
            'type': 'single_image'
        }]
    
    def _load_batch_images(self, image_paths: List[str]) -> List[Dict[str, Any]]:
        """
        Load multiple image files.
        
        Args:
            image_paths: List of paths to image files
            
        Returns:
            List of dictionaries with image paths and indices
        """
        result = []
        
        for idx, image_path in enumerate(image_paths, start=1):
            path = Path(image_path)
            
            # Validate format
            if path.suffix not in self.SUPPORTED_IMAGE_FORMATS:
                raise ValueError(f"Unsupported image format in batch: {path.suffix}. Supported: {self.SUPPORTED_IMAGE_FORMATS}")
            
            # Validate file exists
            if not path.exists():
                raise FileNotFoundError(f"Image file not found: {image_path}")
            
            # Validate it's actually an image
            try:
                Image.open(image_path).verify()
            except Exception as e:
                raise ValueError(f"Invalid image file in batch: {str(e)}")
            
            result.append({
                'path': str(image_path),
                'index': idx,
                'type': 'batch_image'
            })
        
        return result


