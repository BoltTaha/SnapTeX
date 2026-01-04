# SnapTeX

> **Turn Chaos into Code.** Instantly convert handwritten notes, equations, and diagrams into clean, compilable LaTeX & PDF documents using AI.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red?style=for-the-badge&logo=streamlit)](https://streamlit.io/)
[![Gemini AI](https://img.shields.io/badge/AI-Gemini%202.5-purple?style=for-the-badge)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-Proprietary-orange?style=for-the-badge)](LICENSE)

---

## What is SnapTeX?

**SnapTeX** is an intelligent digitization tool designed for students and researchers. Unlike standard OCR tools that just copy text, SnapTeX **understands context**. It takes your messy handwritten notes (PDFs or Images) and transforms them into professional, structured **LaTeX code**.

Whether it's a complex **UML Class Diagram**, a messy **Calculus equation**, or a full page of text, SnapTeX digitizes it in seconds.

### Key Features

- **Bulk Processing Engine:** Upload an entire 50-page PDF notebook, and SnapTeX processes all pages in parallel using multi-threading.
- **Intelligent Correction:** AI automatically fixes handwriting errors (e.g., correcting "Pythogoras" to "Pythagoras") and closes unclosed brackets in math equations.
- **Diagram to Code:** Converts hand-drawn sketches (Flowcharts, UML) directly into **TikZ** code.
- **High-Speed Architecture:** Built with a parallel processing pipeline that respects API rate limits while maximizing throughput.
- **Session Isolation:** Fully supports multiple concurrent users with isolated temporary storage (no file collisions).
- **Multiple Input Formats:** Supports PDF files, single images (JPEG, PNG), or batch image processing.
- **LaTeX & PDF Output:** Generates both `.tex` source code and compiled `.pdf` files.

---

## Engineering & Architecture

SnapTeX is built with **Scalability** and **Maintainability** in mind, strictly following **SOLID Principles** and standard **Design Patterns**:

| Pattern | Implementation | Purpose |
| :--- | :--- | :--- |
| **Facade Pattern** | `ConverterFacade` | Hides the complexity of image loading, AI processing, and PDF compilation behind a single interface. |
| **Factory Pattern** | `ModelFactory` | Allows instant switching between AI models (Gemini Flash vs. Pro) without changing core logic. |
| **Strategy Pattern** | `LaTeXStrategy` | Enables easy extension to other output formats (Markdown, HTML) in the future. |
| **SRP (SOLID)** | `Service Layer` | Each service (PDF Processing, API Call, File Saving) handles exactly one responsibility. |
| **DIP (SOLID)** | `Interfaces` | High-level modules depend on abstractions (ICodeGenerator, IImageLoader), not concrete implementations. |

### Project Structure

```
SnapTeX/
├── core/                      # Core abstractions and patterns
│   ├── interfaces.py          # Abstract base classes (ICodeGenerator, IImageLoader, etc.)
│   ├── factories.py           # Factory Pattern (ModelFactory)
│   └── strategies.py          # Strategy Pattern (LaTeXStrategy)
├── services/                  # Service layer (SRP compliance)
│   ├── gemini_service.py      # Gemini API integration
│   ├── pdf_processor.py       # Image loading from PDF/images
│   ├── output_builder.py      # LaTeX file generation
│   └── latex_compiler.py      # PDF compilation
├── facade/                    # Facade Pattern
│   └── converter_facade.py    # High-level conversion interface
├── ui/                        # User interface
│   └── streamlit_app.py       # Streamlit web application
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── packages.txt               # System dependencies (for Streamlit Cloud)
└── README.md                  # This file
```

---

## Installation Guide

### Prerequisites

Before running, ensure you have these installed on your system:

1. **Python 3.8+**
2. **Poppler** (Required for processing PDFs)
3. **TeX Live / MiKTeX** (Required for generating compiled PDFs - optional, LaTeX code works without it)

### Step 1: Clone & Setup

```bash
# Clone the repository
git clone https://github.com/BoltTaha/SnapTeX.git
cd SnapTeX

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### Step 2: System Dependencies

#### Windows Users

**1. Install Poppler:**
- Download from [Poppler Releases](https://github.com/oschwartz10612/poppler-windows/releases)
- Extract the zip file to a location like `C:\Program Files\poppler`
- Add the `bin` folder (e.g., `C:\Program Files\poppler\bin`) to your System **PATH**
- Restart your terminal/IDE after adding to PATH
- Verify: Run `pdftoppm -h` in terminal (should show help text)

**2. Install LaTeX (Optional - for PDF compilation):**
- Download and install [MiKTeX](https://miktex.org/download) (Recommended for Windows)
- Or install [TeX Live](https://www.tug.org/texlive/)
- Restart your terminal after installation
- Verify: Run `pdflatex --version` in terminal

#### Linux Users

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install poppler-utils texlive-full

# Verify Poppler
pdftoppm -h

# Verify LaTeX
pdflatex --version
```

#### macOS Users

```bash
# Using Homebrew
brew install poppler mactex

# Verify Poppler
pdftoppm -h

# Verify LaTeX
pdflatex --version
```

### Step 3: API Key Configuration

1. **Get your free API Key:**
   - Visit [Google AI Studio](https://aistudio.google.com/)
   - Sign in with your Google account
   - Click "Get API Key" and create a new key

2. **Configure the API Key:**
   - Create a `.env` file in the root directory:
   ```bash
   # Copy the example file (if available)
   cp .env.example .env
   ```

   - Open `.env` and add your key:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   ```

   - **Important:** Never commit the `.env` file to version control (it's already in `.gitignore`)

---

## How to Run

Launch the application with one command:

```bash
streamlit run ui/streamlit_app.py
```

The application will start and open in your browser at `http://localhost:8501`.

### Usage Instructions

1. **Upload Files:**
   - Drag & drop your PDF file, single image (JPEG, PNG), or multiple images
   - Supported formats: PDF, JPEG, PNG

2. **Convert:**
   - Click the "Convert to LaTeX" button
   - Wait for processing (progress will be shown)

3. **Download:**
   - Download the `.tex` source code file
   - Download the compiled `.pdf` file (if TeX Live/MiKTeX is installed)

---

## Troubleshooting

### Error: `Poppler is not installed or not in PATH`

**Solution:**
- Ensure Poppler is installed (see Installation Guide)
- Verify the `bin` folder is added to your System PATH
- Restart your terminal/IDE after adding to PATH
- Test with: `pdftoppm -h` (should show help text)

### Error: `pdflatex not found. Please install TeX Live.`

**Solution:**
- You can still download the `.tex` file! This error just means SnapTeX couldn't compile the PDF locally
- Install TeX Live or MiKTeX (see Installation Guide)
- Verify: Run `pdflatex --version` in terminal
- Or compile manually: Use online LaTeX editors like [Overleaf](https://www.overleaf.com/)

### Error: `429 Too Many Requests`

**Solution:**
- SnapTeX has a built-in rate limiter and retry mechanism
- The free API tier has rate limits
- Wait for a minute and try again
- Consider upgrading to a paid API tier for higher limits

### Error: `GEMINI_API_KEY not found in environment variables`

**Solution:**
- Ensure you created a `.env` file in the root directory
- Check that the `.env` file contains: `GEMINI_API_KEY=your_key_here`
- Verify there are no spaces around the `=` sign
- Restart the application after creating/editing `.env`

### LaTeX Compilation Errors

**Solution:**
- Most LaTeX errors are handled automatically by SnapTeX
- If compilation fails, download the `.tex` file and compile manually
- Common issues:
  - Missing packages (usually auto-handled)
  - Complex diagrams may need manual tweaking
  - Use online LaTeX editors for debugging

---

## Features in Detail

### Bulk Processing
Process entire PDFs with multiple pages simultaneously. SnapTeX uses parallel processing to handle multiple pages concurrently, significantly reducing processing time.

### Intelligent Context Repair
The AI model doesn't just transcribe - it understands context and fixes common errors:
- Spelling corrections (handwriting errors)
- Mathematical notation fixes
- Structural improvements

### Diagram Recognition
Advanced support for:
- UML Class Diagrams (converted to TikZ)
- Flowcharts and diagrams
- Mathematical equations and formulas
- Tables and structured data

### Session Management
Each user session has isolated temporary storage, preventing file collisions in multi-user environments. Temp files are automatically cleaned up after processing.

---

## Technology Stack

- **Frontend:** Streamlit (Python web framework)
- **AI/ML:** Google Gemini 2.5 (Flash & Pro models)
- **PDF Processing:** pdf2image, Poppler
- **Image Processing:** Pillow (PIL)
- **LaTeX Compilation:** TeX Live / MiKTeX
- **Language:** Python 3.8+

---

## License

**© 2026 SnapTeX. All Rights Reserved.**

This project is proprietary software. Unauthorized copying, modification, distribution, or use of this source code is strictly prohibited.

---

## Author

Built with ❤️ by a CS Student @ FAST

---

## Contributing

This is a proprietary project. Contributions are not currently accepted. However, suggestions and feedback are welcome!

---

## Changelog

### Version 1.0.0 (2026)
- Initial release
- Support for PDF, single images, and batch image processing
- Gemini 2.5 Flash & Pro model integration
- Parallel processing with rate limiting
- Session-based temp file management
- LaTeX compilation support
- Streamlit web interface

---

**Happy Converting!**
