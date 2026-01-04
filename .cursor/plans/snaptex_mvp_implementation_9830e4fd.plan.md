---
name: SnapTeX MVP Implementation
overview: Build a complete SnapTeX MVP that converts PDF pages (with equations/images) to LaTeX using Gemini AI, following SOLID principles with a modular architecture. The system will process single PDFs, extract pages as images, send them to Gemini API, compile LaTeX, and provide both LaTeX and PDF downloads via Streamlit UI.
todos: []
---

# SnapTeX MVP Implementation Plan

## Architecture Overview

The project follows **SOLID Principles** and implements **Design Patterns** for a production-ready, maintainable codebase:

```
SnapTeX/
├── core/
│   ├── __init__.py
│   ├── interfaces.py          # Abstract base classes (ICodeGenerator, IImageLoader, IOutputBuilder)
│   ├── factories.py           # Factory Pattern (ModelFactory for LLM providers)
│   └── strategies.py          # Strategy Pattern (OutputStrategy: LaTeX, Markdown, etc.)
├── services/
│   ├── __init__.py
│   ├── gemini_service.py      # GeminiService implementing ICodeGenerator (SRP: Only API calls)
│   ├── pdf_processor.py       # ImageLoader: Only PDF to images (SRP: Only image loading)
│   ├── latex_compiler.py      # LaTeXBuilder: Only .tex to PDF compilation
│   └── output_builder.py      # OutputBuilder: Only text to .tex file saving
├── facade/
│   ├── __init__.py
│   └── converter_facade.py    # Facade Pattern: Hides complexity from user
├── ui/
│   ├── __init__.py
│   └── streamlit_app.py       # Main Streamlit UI
├── main.py                    # Entry point
├── requirements.txt           # Dependencies (no versions per user preference)
├── .env.example              # Template for API key
└── README.md                 # Documentation
```

## SOLID Principles Implementation

### S - Single Responsibility Principle (SRP)

Each class has **one and only one** responsibility:

- **ImageLoader** (`pdf_processor.py`): **ONLY** loads images from PDF (PDF to images conversion)
- **GeminiClient** (`gemini_service.py`): **ONLY** communicates with API (no image loading, no file saving)
- **LaTeXBuilder** (`output_builder.py`): **ONLY** saves text to `.tex` file (no API calls, no compilation)
- **LaTeXCompiler** (`latex_compiler.py`): **ONLY** compiles `.tex` to PDF (no text generation)

**Anti-pattern to avoid:** Don't put image loading + API call + file saving all in `main.py` - this violates SRP.

### O - Open/Closed Principle (OCP)

Code should be **Open for Extension, Closed for Modification**.

**Implementation:** Common `ICodeGenerator` interface (in `core/interfaces.py`). If a new model (GPT-4, Claude) arrives, we don't edit existing `GeminiService` code. We simply add a new class `GPT4Service` that implements `ICodeGenerator`.

**Extension Example:**

- Today: `GeminiService` implements `ICodeGenerator`
- Tomorrow: Add `GPT4Service` implements `ICodeGenerator`
- Main code remains unchanged - uses interface, not concrete classes

### D - Dependency Inversion Principle (DIP)

High-level code should not depend on low-level code. Both should depend on abstractions.

**Implementation:** Main logic (`converter_facade.py`) calls `ICodeGenerator` interface, not `GeminiService` directly. Whether it's Gemini, Claude, or GPT-4 behind the interface - main code doesn't care.

**Structure:**

- High-level: `ConverterFacade` → depends on `ICodeGenerator` (interface)
- Low-level: `GeminiService` → implements `ICodeGenerator` (interface)

## Design Patterns

### 1. Factory Pattern (Creational)

**Purpose:** Create LLM provider instances without exposing creation logic.

**Implementation:** `core/factories.py` - `ModelFactory` class

```python
model = ModelFactory.get_model("gemini-fylash")  # Returns GeminiService
# OR
model = ModelFactory.get_model("gpt-4o")       # Returns GPT4Service (future)
```

**Why:** User selects model type, Factory returns appropriate instance. Easy to add new models without changing client code.

### 2. Strategy Pattern (Behavioral)

**Purpose:** Switch output formats at runtime (LaTeX, Markdown, Summary, etc.).

**Implementation:** `core/strategies.py` - `OutputStrategy` interface with implementations:

- `LaTeXStrategy` - Generates `.tex` file
- `MarkdownStrategy` - Generates `.md` file (future extension)
- `PlainTextStrategy` - Generates `.txt` file (future extension)

**Why:** User requirement changes (sometimes LaTeX, sometimes Markdown). Switch strategy at runtime without modifying core logic.

### 3. Facade Pattern (Structural)

**Purpose:** Hide complex subsystem operations behind a simple interface.

**Implementation:** `facade/converter_facade.py` - `ConverterFacade` class

**User sees:** `converter.convert(pdf_path)` → Magic happens → Get LaTeX/PDF

**Behind the scenes (hidden):**

1. Image loading (PDF → images)
2. Image cleaning/preprocessing
3. API calls (parallel processing)
4. Error correction
5. LaTeX generation
6. File saving
7. PDF compilation

**Why:** User doesn't need to know about ImageLoader, GeminiClient, LaTeXBuilder, etc. Just call `convert()` and get results.

## Competition Analysis & Strategy

### Competitive Advantages

1. **Bulk Processing (Killer Feature)**

   - Mathpix: Requires 100 screenshots for 100 pages
   - SnapTeX: Upload entire PDF → Process all pages in parallel → Download complete `.tex` file
   - **Target:** Students with multi-page assignments

2. **Intelligent Context Repair**

   - Competitors (Mathpix): OCR only - replicates errors (e.g., "Pythogoras" → "Pythogoras")
   - SnapTeX: AI-powered correction (e.g., "Pythogoras" → "Pythagoras")
   - **Positioning:** "Intelligent Digitizer" not just OCR

3. **Structured Output**

   - ChatGPT Plus: Output in chat, poor formatting
   - SnapTeX: Clean, structured `.tex` files ready for compilation
   - **Value:** Professional, editable LaTeX code

4. **Flexible Input Formats**

   - Most tools: Only PDF or only single images
   - SnapTeX: Accepts PDF (bulk processing), single images (JPEG, PNG), or batch of images (parallel processing)
   - **Value:** One tool for all use cases:
     - Quick single equation (single image)
     - Multiple equations at once (batch images)
     - Entire document (PDF with all pages)

### Future Monetization (Not in MVP)

- Price localization (Easypaisa/JazzCash integration)
- Volume pricing ("Rs. 50 per assignment")
- Note: MVP focuses on core functionality first

## Implementation Steps

### 1. Project Structure & Core Interfaces

**Files to create:**

- `core/__init__.py` - Package initialization
- `core/interfaces.py` - Abstract base classes for SOLID compliance

**Key interfaces (DIP compliance):**

- `ICodeGenerator` - Abstract class for LLM providers (Gemini, GPT-4, Claude)
- `IImageLoader` - Abstract class for image loading (PDF, other sources)
- `IOutputBuilder` - Abstract class for output generation (LaTeX, Markdown)
- `IOutputStrategy` - Abstract class for output format strategies

**Files:**

- `core/factories.py` - `ModelFactory` (Factory Pattern)
- `core/strategies.py` - `LaTeXStrategy`, `MarkdownStrategy` (Strategy Pattern)

### 2. Service Layer Implementation (SRP Compliance)

#### 2.1 Gemini Service (GeminiClient)

**File:** `services/gemini_service.py`

- `GeminiService` class implementing `ICodeGenerator` interface
- **SRP:** **ONLY** communicates with Gemini API (no image loading, no file saving)
- Takes image path, sends to Gemini 1.5 Flash API
- Returns text/LaTeX code (no file operations)
- Retry mechanism for API failures (exponential backoff)
- Error handling and logging
- API key loaded from `.env` file

**⚠️ Context Loss Handling (MVP):**

- Since parallel processing means pages are processed independently, context between pages is lost
- **MVP Solution:** Add to prompt: *"If a sentence seems incomplete at the start or end, just transcribe it as is."*
- This handles cases where sentences are split across pages (e.g., "The gradient descent algorithm is..." on Page 1, "...used to minimize the loss function." on Page 2)
- **Future Enhancement:** Sequential processing with context passing (not for MVP)

**Dependencies:** `google-generativeai`, `python-dotenv`

**OCP Example:** If GPT-4 is needed, create `GPT4Service` implementing `ICodeGenerator` - no changes to `GeminiService`

#### 2.2 Image Loader (PDF, Single Image & Batch Images Processing)

**File:** `services/pdf_processor.py`

- `ImageLoader` class implementing `IImageLoader` interface
- **SRP:** **ONLY** loads images from PDF, single image files, or batch of images (no API calls, no file saving)
- **Triple Support:**
  - **PDF:** Convert PDF pages to images using `pdf2image` (Poppler dependency)
  - **Single Image:** Accept single JPEG, PNG, or other image formats directly
  - **Batch Images:** Accept multiple image files (JPEG, PNG) in a list/array
- Auto-detect file type (PDF vs. single image vs. batch images) and handle accordingly
- Returns list of image paths:
  - PDF → List of all page images
  - Single image → List with one path
  - Batch images → List of all image paths
- Memory-efficient image handling
- Validate image formats (JPEG, PNG supported)
- Handle mixed formats in batch (all JPEG, all PNG, or mixed JPEG+PNG)

**Dependencies:** `pdf2image`, `Pillow`

**⚠️ Critical System Dependency - Poppler:**

- `pdf2image` requires **Poppler** (system-level software, not a Python package)
- **Windows Development:** Download Poppler, add `bin` folder to system PATH
- **Streamlit Cloud Deployment:** Create `packages.txt` with `poppler-utils`
- **Installation Instructions:** Must be documented in README.md

**File Type Detection:**

- Check file extension or MIME type
- PDF → Extract pages as images (requires Poppler)
- Single JPEG/PNG → Use directly (validate format)
- Multiple images → Process all, validate each format

#### 2.3 Output Builder (LaTeX File Creation)

**File:** `services/output_builder.py`

- `LaTeXBuilder` class implementing `IOutputBuilder` interface
- **SRP:** **ONLY** saves text to `.tex` file (no API calls, no compilation)
- Takes text/LaTeX code, saves to `.tex` file
- Returns file path

**Dependencies:** Built-in `io`, `pathlib`

#### 2.4 LaTeX Compiler

**File:** `services/latex_compiler.py`

- `LaTeXCompiler` class
- **SRP:** **ONLY** compiles `.tex` to PDF (no text generation, no file saving)
- Compile `.tex` files to PDF using TeX Live (`pdflatex` command)
- Handle compilation errors gracefully
- Clean up auxiliary files after compilation
- Return compiled PDF path

**Note:** Requires TeX Live installation on system

### 3. Factory Pattern Implementation

**File:** `core/factories.py`

- `ModelFactory` class (Factory Pattern)
- `get_model(model_type: str)` method
- Returns appropriate `ICodeGenerator` implementation:
  - `"gemini-flash"` → `GeminiService`
  - `"gemini-pro"` → `GeminiService` (with different config)
  - Future: `"gpt-4o"` → `GPT4Service`

**Why:** Centralized model creation, easy to extend without changing client code

### 4. Strategy Pattern Implementation

**File:** `core/strategies.py`

- `OutputStrategy` abstract base class
- Implementations:
  - `LaTeXStrategy` - Generates `.tex` file (MVP)
  - Future: `MarkdownStrategy` - Generates `.md` file
  - Future: `PlainTextStrategy` - Generates `.txt` file

**Why:** Switch output format at runtime without modifying core logic

### 5. Facade Pattern Implementation

**File:** `facade/converter_facade.py`

- `ConverterFacade` class (Facade Pattern)
- Public method: `convert(file_path: str | list[str], output_format: str = "latex")` → Returns LaTeX code and PDF
- **Unified Interface:** Accepts PDF files, single images (JPEG, PNG), or batch of images
- Auto-detects file type and processes accordingly:
  - **PDF:** Extracts all pages, processes in parallel (4 threads)
  - **Single Image (JPEG/PNG):** Processes directly (no extraction, single API call)
  - **Batch Images (list of JPEG/PNG):** Processes all images in parallel (4 threads, similar to PDF pages)
- Hides complex operations:

  1. Image loading (ImageLoader - handles PDF, single images, and batch images)
  2. Parallel processing with ThreadPoolExecutor (4 threads):

     - Multi-page PDFs → Parallel page processing
     - Batch images → Parallel image processing
     - Single image → No parallelization needed

  1. **⚠️ Ordering Fix (Critical):** Sort results by page/image number before output

     - Threads finish asynchronously (Page 2 might finish before Page 1)
     - **Solution:** `results.sort(key=lambda x: x['page_num'])` or `results.sort(key=lambda x: x['image_index'])`
     - Ensures correct order in final LaTeX/PDF output

  1. API calls (GeminiService via ModelFactory)
  2. Output generation (LaTeXBuilder via Strategy)
  3. PDF compilation (LaTeXCompiler)

**Why:** User calls one method with any file type (PDF, single image, or batch images), gets complete result. Complexity hidden.

**DIP Example:** Facade depends on `ICodeGenerator`, `IImageLoader`, `IOutputBuilder` (interfaces), not concrete classes

### 6. Streamlit UI

**File:** `ui/streamlit_app.py`

- Modern, clean UI with drag-and-drop file uploader
- **Multi-format Support:** Accepts PDF files, single images (JPEG, PNG), or batch of images
- **Batch Upload:** Allow multiple image files to be selected/uploaded at once
- File type validation and user-friendly error messages for unsupported formats
- Progress bar during processing:
  - **PDF:** Shows parallel processing status for each page
  - **Single Image:** Shows single processing status
  - **Batch Images:** Shows parallel processing status for each image (similar to PDF pages)
- Display processing status:
  - PDF → Page-by-page status
  - Single image → Single status
  - Batch images → Image-by-image status with count (e.g., "Processing image 3 of 10")
- Model selection dropdown (Factory Pattern usage)
- Output format selection (Strategy Pattern usage)
- Download buttons for:
  - LaTeX source code (`.tex` file)
  - Compiled PDF
- Error messages and success notifications
- Responsive design

**UI → Facade:** UI only interacts with `ConverterFacade`, not individual services. Facade handles PDF, single images, and batch images seamlessly.

**File:** `main.py` - Entry point that runs Streamlit app

### 7. Configuration & Dependencies

**Files:**

- `requirements.txt` - All Python dependencies (no version numbers)
- `packages.txt` - System dependencies for Streamlit Cloud deployment (contains `poppler-utils`)
- `.env.example` - Template showing required environment variables
- `README.md` - Setup instructions, usage guide, architecture documentation

**⚠️ Poppler Installation Requirements:**

- **Windows Development:** Download Poppler, extract, add `bin` folder to system PATH
- **Streamlit Cloud:** Create `packages.txt` with `poppler-utils` (required for pdf2image)
- **Documentation:** README.md must include step-by-step Poppler installation instructions

## Key Technical Decisions

1. **API Key Management:** Environment variables via `.env` file (user preference, never hardcoded)
2. **LaTeX Compiler:** TeX Live (`pdflatex` command)
3. **Processing:** 

   - **PDF:** Single PDF at a time, but pages processed in parallel (4 threads via ThreadPoolExecutor)
   - **Single Images:** JPEG/PNG files processed directly (single API call, no parallelization needed)
   - **Batch Images:** Multiple images processed in parallel (4 threads via ThreadPoolExecutor, similar to PDF pages)

4. **Error Handling:** Retry mechanism for API calls (exponential backoff), graceful error messages in UI
5. **Memory Management:** Process pages in batches if needed for large PDFs
6. **Architecture:** SOLID principles + Design Patterns for maintainability and extensibility
7. **Dependency Injection:** High-level code (Facade) depends on interfaces (ICodeGenerator, IImageLoader), not concrete classes
8. **⚠️ Parallel Processing Ordering:** Results must be sorted by page/image number after parallel processing to maintain correct order
9. **⚠️ Poppler Installation:** Required system dependency for `pdf2image` - must be installed separately (Windows: add to PATH, Cloud: packages.txt)
10. **⚠️ Context Loss (MVP):** Parallel processing loses context between pages - handled via prompt instruction for incomplete sentences

## Dependencies Summary

**Python Dependencies:**

- `streamlit` - UI framework
- `google-generativeai` - Gemini API client
- `pdf2image` - PDF to images conversion
- `Pillow` - Image processing
- `python-dotenv` - Environment variable management
- `concurrent.futures` - Parallel processing (built-in)

**System Dependencies:**

- **TeX Live** (for LaTeX compilation via `pdflatex`)
- **⚠️ Poppler** (REQUIRED for `pdf2image` library):
  - **Windows:** Download from Poppler website, extract, add `bin` folder to system PATH
  - **Streamlit Cloud:** Add `poppler-utils` to `packages.txt` file
  - **Verification:** Run `pdftoppm -h` in terminal to confirm installation
  - **Note:** This is NOT a Python package - must be installed separately at system level

## Architecture Flow Diagram

```
User (Streamlit UI)
    ↓
Upload: PDF, Single Image (JPEG/PNG), or Batch Images
    ↓
ConverterFacade (Facade Pattern)
    ↓
ImageLoader (implements IImageLoader)
    ├─→ PDF → Extract pages as images
    ├─→ Single Image (JPEG/PNG) → Use directly
    └─→ Batch Images → Process all images
    ↓
ModelFactory (Factory Pattern) → GeminiService (implements ICodeGenerator)
    ↓
    ├─→ PDF: ThreadPoolExecutor → Parallel API Calls (4 threads)
    ├─→ Single Image: Single API Call
    └─→ Batch Images: ThreadPoolExecutor → Parallel API Calls (4 threads)
    ↓
LaTeXStrategy (Strategy Pattern) → LaTeXBuilder (implements IOutputBuilder)
    ↓
LaTeXCompiler → PDF Generation
    ↓
Download (LaTeX .tex + Compiled PDF)
```

**Key Points:**

- All dependencies flow through interfaces (DIP)
- Facade hides complexity from UI
- Factory creates appropriate model instance
- Strategy allows output format switching
- Each service has single responsibility (SRP)

## Testing Strategy

1. Unit tests for each service class (SRP makes testing easier)
2. Integration testing with sample PDFs
3. Error handling tests (invalid API key, missing TeX Live, etc.)
4. Pattern tests (Factory creates correct instances, Strategy switches correctly)
5. Facade tests (end-to-end conversion flow)

## Interview Readiness Points

When explaining to examiner/investor:

1. **SOLID Principles:**

   - **SRP:** Each class does one thing (ImageLoader only loads, GeminiClient only calls API)
   - **OCP:** Add GPT-4 by creating new class, no modification to existing code
   - **DIP:** High-level code depends on interfaces, not concrete classes

2. **Design Patterns:**

   - **Factory:** Model selection without exposing creation logic
   - **Strategy:** Output format switching at runtime
   - **Facade:** Simple interface hiding complex subsystem

3. **Competitive Advantages:**

   - Bulk processing (entire PDF vs. screenshot-by-screenshot)
   - AI-powered context repair (intelligent correction, not just OCR)
   - Structured output (clean LaTeX code, not chat messages)

This plan implements your 5-day strategy with production-ready architecture following SOLID principles and Design Patterns.

## Implementation Todos (Day-by-Day Breakdown)

### Day 1: Architecture & Setup (Foundation)

- [ ] Create project directory structure (core/, services/, facade/, ui/)
- [ ] Create all `__init__.py` files for packages
- [ ] Implement `core/interfaces.py` with abstract base classes (ICodeGenerator, IImageLoader, IOutputBuilder, IOutputStrategy)
- [ ] Create `requirements.txt` (dependencies without versions)
- [ ] Create `packages.txt` for Streamlit Cloud (contains `poppler-utils`)
- [ ] Create `.env.example` template
- [ ] **⚠️ Install Poppler (System Dependency):**
  - Windows: Download Poppler, extract, add `bin` folder to system PATH
  - Verify installation: `pdftoppm -h` should work in terminal
  - Document installation steps in README.md

### Day 2: Core Services & Patterns (Backend Logic)

- [ ] Implement `services/gemini_service.py` (GeminiService implementing ICodeGenerator - SRP: only API calls)
- [ ] Implement `services/pdf_processor.py` (ImageLoader implementing IImageLoader - SRP: only image loading)
  - Support PDF extraction, single image handling (JPEG, PNG), and batch images
  - Auto-detect file type (PDF, single image, or batch) and process accordingly
  - Handle mixed image formats in batch (JPEG + PNG together)
- [ ] Implement `services/output_builder.py` (LaTeXBuilder implementing IOutputBuilder - SRP: only file saving)
- [ ] Implement `services/latex_compiler.py` (LaTeXCompiler - SRP: only compilation)
- [ ] Implement `core/factories.py` (ModelFactory - Factory Pattern)
- [ ] Implement `core/strategies.py` (LaTeXStrategy - Strategy Pattern)

### Day 3: Facade & Integration (Assembly Line)

- [ ] Implement `facade/converter_facade.py` (ConverterFacade - Facade Pattern)
  - Accept PDF, single image files (JPEG, PNG), or batch of images (list)
  - Auto-detect file type and route accordingly
- [ ] Integrate parallel processing with ThreadPoolExecutor (4 threads)
  - PDF pages → Parallel processing
  - Batch images → Parallel processing
  - Single image → No parallelization
- [ ] **⚠️ Implement Ordering Fix (Critical):**
  - Sort results by page/image number after parallel processing
  - Use: `results.sort(key=lambda x: x['page_num'])` for PDFs
  - Use: `results.sort(key=lambda x: x['image_index'])` for batch images
  - Ensures correct order in final output (Page 2 won't appear before Page 1)
- [ ] **⚠️ Add Context Loss Handling to Gemini Prompt:**
  - Add instruction: "If a sentence seems incomplete at the start or end, just transcribe it as is."
  - Handles cases where sentences are split across pages in parallel processing
- [ ] Wire all components together (Facade → Factory → Services → Strategies)
- [ ] Test end-to-end flow with sample PDF, single images (JPEG, PNG), and batch images

### Day 4: Frontend UI (Streamlit)

- [ ] Implement `ui/streamlit_app.py` with modern, clean UI
- [ ] Add drag-and-drop file uploader (accepts PDF, JPEG, PNG, or multiple images)
- [ ] Add batch image upload support (allow multiple image files selection)
- [ ] Add file type validation and user-friendly error messages
- [ ] Add progress bar for processing:
  - PDF → Parallel processing status (page-by-page)
  - Single image → Single status
  - Batch images → Parallel processing status (image-by-image with count)
- [ ] Add model selection dropdown (Factory Pattern usage)
- [ ] Add output format selection (Strategy Pattern usage)
- [ ] Add download buttons (LaTeX .tex and compiled PDF)
- [ ] Create `main.py` entry point

### Day 5: Testing & Polish (Final Touches)

- [ ] Test error handling (invalid API key, missing TeX Live, unsupported file formats, etc.)
- [ ] Test with PDF, single images (JPEG, PNG), and batch images (multiple JPEG/PNG)
- [ ] Test batch processing with mixed formats (JPEG + PNG together)
- [ ] **⚠️ Test Ordering Fix:** Verify that multi-page PDFs and batch images maintain correct order in output
- [ ] **⚠️ Test Context Loss Handling:** Verify that incomplete sentences at page boundaries are handled correctly
- [ ] Add logging and error messages
- [ ] Create README.md with setup instructions:
  - PDF, single image, and batch image support
  - **Poppler installation steps (Windows and Streamlit Cloud)**
  - TeX Live installation requirements
  - Environment variable setup (.env file)
- [ ] Code review for SOLID principles compliance
- [ ] Add docstrings and comments
- [ ] Final integration testing (PDF, single image, and batch image workflows)