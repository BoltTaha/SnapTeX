# SnapTeX - PDF/Image to LaTeX Converter

Convert PDFs and images (JPEG, PNG) to LaTeX code using AI-powered Gemini models.

## Features

- ✅ **Bulk Processing**: Convert entire PDFs at once (all pages in parallel)
- ✅ **Flexible Input**: Support for PDF, single images, and batch images
- ✅ **AI-Powered**: Intelligent context repair and error correction
- ✅ **Parallel Processing**: Fast conversion using multi-threading
- ✅ **Clean Output**: Structured LaTeX code ready for compilation
- ✅ **SOLID Principles**: Production-ready architecture

## Architecture

This project follows **SOLID Principles** and implements **Design Patterns**:

- **SOLID Principles**: Single Responsibility, Open/Closed, Dependency Inversion
- **Design Patterns**: Factory, Strategy, Facade
- **Modular Structure**: Core interfaces, services, facade, and UI layers

## Installation

### Prerequisites

1. **Python 3.8+**
2. **TeX Live** (for LaTeX compilation)
3. **Poppler** (for PDF to image conversion)

### Step 1: Install Poppler (Required)

#### Windows:

1. Download Poppler from: https://github.com/oschwartz10612/poppler-windows/releases
2. Extract the ZIP file to a location (e.g., `C:\poppler`)
3. Add Poppler's `bin` folder to your system PATH:
   - Open System Properties → Environment Variables
   - Edit "Path" variable
   - Add: `C:\poppler\Library\bin` (or your extraction path)
4. Verify installation:
   ```bash
   pdftoppm -h
   ```

#### Linux:

```bash
sudo apt-get install poppler-utils
```

#### macOS:

```bash
brew install poppler
```

#### Streamlit Cloud:

Create a `packages.txt` file (already included) with:
```
poppler-utils
```

### Step 2: Install TeX Live

#### Windows:

1. Download TeX Live installer from: https://www.tug.org/texlive/
2. Run the installer and follow instructions
3. Verify installation:
   ```bash
   pdflatex --version
   ```

#### Linux:

```bash
sudo apt-get install texlive-full
```

#### macOS:

```bash
brew install --cask mactex
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Get your Gemini API key from: https://makersuite.google.com/app/apikey

3. Add your API key to `.env`:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

## Usage

### Run the Application

```bash
streamlit run ui/streamlit_app.py
```

Or use the main entry point:

```bash
python main.py
```

### Using the UI

1. **Upload Files**:
   - Upload a PDF file for multi-page conversion
   - Upload a single image (JPEG/PNG) for quick conversion
   - Upload multiple images for batch processing

2. **Select Model**: Choose between Gemini Flash (faster) or Pro (more accurate)

3. **Convert**: Click "Convert to LaTeX" button

4. **Download**: Download the generated LaTeX code and compiled PDF

## Project Structure

```
SnapTeX/
├── core/
│   ├── interfaces.py      # Abstract base classes (SOLID)
│   ├── factories.py       # Factory Pattern
│   └── strategies.py      # Strategy Pattern
├── services/
│   ├── gemini_service.py  # Gemini API integration
│   ├── pdf_processor.py   # Image loading (PDF/images)
│   ├── output_builder.py  # LaTeX file creation
│   └── latex_compiler.py  # LaTeX to PDF compilation
├── facade/
│   └── converter_facade.py  # Facade Pattern
├── ui/
│   └── streamlit_app.py   # Streamlit UI
├── main.py                # Entry point
├── requirements.txt       # Python dependencies
├── packages.txt          # System dependencies (Streamlit Cloud)
└── README.md            # This file
```

## Technical Details

### Parallel Processing

- PDF pages and batch images are processed in parallel (4 threads)
- Results are automatically sorted to maintain correct order
- Single images are processed sequentially (no parallelization needed)

### Context Loss Handling (MVP)

Since pages/images are processed in parallel, context between them is lost. The MVP solution includes a prompt instruction to handle incomplete sentences at page boundaries.

### Ordering Fix

Threads finish asynchronously, so results are sorted by page/image number before final output to ensure correct order.

## Troubleshooting

### Poppler Not Found

- **Windows**: Ensure Poppler's `bin` folder is in your PATH
- **Streamlit Cloud**: Ensure `packages.txt` contains `poppler-utils`
- Verify: Run `pdftoppm -h` in terminal

### TeX Live Not Found

- Ensure TeX Live is installed and `pdflatex` is in PATH
- Verify: Run `pdflatex --version` in terminal

### API Key Error

- Ensure `.env` file exists with `GEMINI_API_KEY` set
- Get API key from: https://makersuite.google.com/app/apikey

## License

Copyright (c) 2026 SnapTeX
All Rights Reserved.

NOTICE: All information contained herein is, and remains the property of SnapTeX.
The intellectual and technical concepts contained herein are proprietary to SnapTeX
and are protected by trade secret or copyright law. Dissemination of this information
or reproduction of this material is strictly forbidden unless prior written permission
is obtained from SnapTeX.
## Contributing



