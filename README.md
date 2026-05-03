# Universal File Parser (UFP) 🚀

A high-performance VS Code extension designed for seamless file parsing and visualization. UFP handles everything from standard CSVs to complex binary formats like **Avro** and **Parquet**, providing a unified view for developers.

---

## 🏗️ Project Status: Phase 1–5 Complete
*   **Phases 1-2: Foundation & Detection**: Implemented a robust project scaffold with signature-based (magic-number) file type identification.
*   **Phases 3-4: Parsing & Cleaning**: Developed strategy-based parsers for CSV, JSON, Avro, Parquet, and XLSX. Includes an automated **DataCleaner** that handles `snake_case` normalization and flattens nested structures (e.g., Avro records) into flat columns.
*   **Phase 5: Visualizations**: Integrated a theme-aware VS Code Webview dashboard that displays data previews and file statistics.

---

## 🚦 Getting Started

### Prerequisites
*   **Python 3.11+**: If you are on macOS, ensure `xz` is installed via Homebrew (`brew install xz`) before installing Python to avoid `lzma` errors.
*   **Docker & Docker Compose**: Recommended for a consistent, isolated development environment.
*   **Node.js**: Required for compiling the VS Code extension bridge.

### Local Setup
1.  **Environment Configuration**:
    ```bash
    git clone [https://github.com/Arshdeepdubey/UniversalFileParser.git](https://github.com/Arshdeepdubey/UniversalFileParser.git)
    python -m venv .venv
    source .venv/bin/activate
    ```
2.  **Dependency Installation**:
    *Note: We strictly use `numpy<2` to maintain binary compatibility with Pandas and PyArrow.*
    ```bash
    pip install "numpy<2" -r requirements.txt
    npm install
    ```
3.  **Generate Binary Assets**:
    Generate the necessary `.avro` and `.json` files for testing:
    ```bash
    python scripts/generate_test_data.py
    ```

### Docker Usage
To verify the entire pipeline (including binary dependencies like `liblzma`) in a production-like environment:
```bash
docker-compose up --build -d
docker exec -it universalfileparser-ufp-parser-1 pytest tests/