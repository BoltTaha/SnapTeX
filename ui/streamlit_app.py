"""
Streamlit UI for SnapTeX.
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import streamlit as st
import os
from typing import List
from facade.converter_facade import ConverterFacade


def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="SnapTeX - PDF/Image to LaTeX Converter",
        page_icon="📄",
        layout="wide"
    )
    
    st.title("📄 SnapTeX")
    st.markdown("### Convert PDFs and Images to LaTeX Code")
    st.markdown("Upload a PDF, single image, or multiple images to convert them to LaTeX format.")
    
    # Sidebar for settings
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Model selection (Factory Pattern)
        model_type = st.selectbox(
            "Select Model",
            ["gemini-2.5-flash", "gemini-2.5-pro"],
            index=0,
            help="Gemini 2.5 is the latest stable version (2026). Flash is faster, Pro is more accurate."
        )
        
        st.markdown("---")
        st.markdown("### 📋 Supported Formats")
        st.markdown("- **PDF**: Multi-page documents")
        st.markdown("- **Images**: JPEG, PNG")
        st.markdown("- **Batch**: Multiple images at once")
    
    # File uploader
    st.header("📤 Upload Files")
    
    uploaded_files = st.file_uploader(
        "Choose files to convert",
        type=["pdf", "jpg", "jpeg", "png"],
        accept_multiple_files=True,
        help="Upload PDF files or images (JPEG/PNG). You can upload multiple images for batch processing."
    )
    
    if uploaded_files:
        # Determine file type
        if len(uploaded_files) == 1 and uploaded_files[0].type == "application/pdf":
            file_type = "PDF"
            st.info(f"📄 PDF file detected: {uploaded_files[0].name}")
        elif len(uploaded_files) == 1:
            file_type = "Single Image"
            st.info(f"🖼️ Image file detected: {uploaded_files[0].name}")
        else:
            file_type = "Batch Images"
            st.info(f"🖼️ {len(uploaded_files)} images detected for batch processing")
        
        # Save uploaded files temporarily
        temp_dir = Path("temp_uploads")
        temp_dir.mkdir(exist_ok=True)
        
        saved_paths = []
        for uploaded_file in uploaded_files:
            file_path = temp_dir / uploaded_file.name
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            saved_paths.append(str(file_path))
        
        # Convert to single path or list
        if file_type == "PDF":
            file_input = saved_paths[0]
        elif file_type == "Single Image":
            file_input = saved_paths[0]
        else:
            file_input = saved_paths
        
        # Process button
        if st.button("🚀 Convert to LaTeX", type="primary", use_container_width=True):
            try:
                # Initialize facade
                converter = ConverterFacade(model_type=model_type)
                
                # Progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Show processing status
                if file_type == "PDF":
                    status_text.info("📄 Processing PDF pages in parallel...")
                elif file_type == "Single Image":
                    status_text.info("🖼️ Processing image...")
                else:
                    status_text.info(f"🖼️ Processing {len(uploaded_files)} images in parallel...")
                
                # Convert
                with st.spinner("Converting..."):
                    latex_path, pdf_path = converter.convert(file_input)
                
                progress_bar.progress(100)
                
                # Check if PDF compilation succeeded
                pdf_available = pdf_path is not None and Path(pdf_path).exists()
                
                if pdf_available:
                    status_text.success("✅ Conversion completed! LaTeX and PDF ready.")
                else:
                    status_text.warning("⚠️ LaTeX generated, but PDF compilation failed (TeX Live not installed).")
                    with st.expander("📝 How to Install TeX Live (for PDF generation)", expanded=False):
                        st.markdown("""
                        **Windows:**
                        1. Download TeX Live installer from: https://www.tug.org/texlive/
                        2. Run the installer and follow instructions
                        3. Verify: Run `pdflatex --version` in terminal
                        
                        **Alternative (Smaller):** Install MiKTeX (smaller, easier):
                        1. Download from: https://miktex.org/download
                        2. Install and restart the app
                        
                        You can still download the LaTeX file and compile it manually!
                        """)
                
                # Display results
                st.header("📥 Download Results")
                
                if pdf_available:
                    col1, col2 = st.columns(2)
                else:
                    col1 = st.container()
                
                with col1:
                    st.subheader("LaTeX Source Code")
                    with open(latex_path, "r", encoding="utf-8") as f:
                        latex_content = f.read()
                    
                    st.download_button(
                        label="📄 Download .tex File",
                        data=latex_content,
                        file_name=Path(latex_path).name,
                        mime="text/plain",
                        use_container_width=True
                    )
                    
                    # Show preview
                    with st.expander("Preview LaTeX Code"):
                        st.code(latex_content, language="latex")
                
                if pdf_available:
                    with col2:
                        st.subheader("Compiled PDF")
                        with open(pdf_path, "rb") as f:
                            pdf_content = f.read()
                        
                        st.download_button(
                            label="📕 Download PDF",
                            data=pdf_content,
                            file_name=Path(pdf_path).name,
                            mime="application/pdf",
                            use_container_width=True
                        )
                
                # Cleanup temp files
                try:
                    import shutil
                    # Delete uploaded files
                    if temp_dir.exists():
                        shutil.rmtree(temp_dir)
                    # Delete extracted images from PDF processing
                    temp_images_dir = Path("temp_images")
                    if temp_images_dir.exists():
                        shutil.rmtree(temp_images_dir)
                except:
                    pass
                
            except Exception as e:
                st.error(f"❌ Error during conversion: {str(e)}")
                st.exception(e)
    
    else:
        # Show instructions
        st.info("👆 Please upload files to get started!")
        
        with st.expander("ℹ️ How to use"):
            st.markdown("""
            ### Usage Instructions:
            
            1. **Upload Files**: 
               - Upload a PDF file for multi-page conversion
               - Upload a single image (JPEG/PNG) for quick conversion
               - Upload multiple images for batch processing
            
            2. **Select Model**: Choose between Gemini 2.5 Flash (faster) or 2.5 Pro (more accurate)
            
            3. **Convert**: Click the "Convert to LaTeX" button
            
            4. **Download**: Download the generated LaTeX code and compiled PDF
            
            ### Features:
            - ✅ Bulk processing (entire PDF at once)
            - ✅ Parallel processing for speed
            - ✅ AI-powered context repair
            - ✅ Clean, structured LaTeX output
            """)
    
    # Footer
    st.markdown("---")
    st.markdown("**SnapTeX** - Intelligent PDF/Image to LaTeX Converter")


if __name__ == "__main__":
    main()


