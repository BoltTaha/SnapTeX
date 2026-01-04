"""
Gemini Service - Implements ICodeGenerator interface.
Single Responsibility: ONLY communicates with Gemini API.
"""

import os
import time
from typing import Optional
from dotenv import load_dotenv
import google.generativeai as genai
from core.interfaces import ICodeGenerator

# Load environment variables
load_dotenv()


class GeminiService(ICodeGenerator):
    """Service for generating LaTeX code using Gemini API."""
    
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        """
        Initialize Gemini service.
        
        Args:
            model_name: Name of the Gemini model to use
        """
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self.max_retries = 3
        self.retry_delay = 1  # Initial delay in seconds
        
    def generate_code(self, image_path: str) -> str:
        """
        Generate LaTeX code from an image using Gemini API.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Generated LaTeX code as string
            
        Raises:
            Exception: If API call fails after retries
        """
        # Context loss handling prompt (MVP solution)
        prompt = """Convert this image to LaTeX code. 

IMPORTANT RULES:
1. Use ONLY standard LaTeX packages: amsmath, amssymb, amsthm, geometry, graphicx
2. DO NOT use packages like: capt-of, fancyhdr, hyperref, or any other non-standard packages
3. Use basic LaTeX commands only (no custom packages)
4. If a sentence seems incomplete at the start or end, just transcribe it as is.
5. Return only the LaTeX code without any explanations, markdown formatting, or \\documentclass/\\begin{document} tags (just the content)."""
        
        for attempt in range(self.max_retries):
            try:
                # Load image
                import PIL.Image
                img = PIL.Image.open(image_path)
                
                # Generate content
                response = self.model.generate_content([prompt, img])
                
                # Extract LaTeX code
                latex_code = response.text.strip()
                
                # Remove markdown code blocks if present
                if latex_code.startswith("```"):
                    lines = latex_code.split("\n")
                    latex_code = "\n".join(lines[1:-1]) if len(lines) > 2 else latex_code
                    latex_code = latex_code.replace("```latex", "").replace("```", "").strip()
                
                # Free tier safe rakhne ke liye 2 second ka break (rate limiting)
                time.sleep(2)
                
                return latex_code
                
            except Exception as e:
                if attempt < self.max_retries - 1:
                    # Exponential backoff
                    delay = self.retry_delay * (2 ** attempt)
                    time.sleep(delay)
                    continue
                else:
                    raise Exception(f"Failed to generate code after {self.max_retries} attempts: {str(e)}")


