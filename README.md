# Book HTML Converter

This repository contains several book projects in Markdown format and tools to convert them to HTML.

## Book Directory Structure

Each book project follows this general structure:

```
book_name/
├── README.md                 # Introduction or overview of the book
├── 01_chapter_name.md        # Chapter files with numeric prefixes
├── 02_chapter_name.md
├── 03_chapter_name.md
└── ...
```

Some books may have chapters in a subdirectory:

```
book_name/
├── README.md
└── chapters/
    ├── 01_chapter_name.md
    ├── 02_chapter_name.md
    └── ...
```

## Available Books

1. **agentic_ai_modern_data_architecture** - Agentic AI with Modern Enterprise Data Architecture for Airline Companies
2. **agentic_ai_transformation** - Guide to Agentic AI Transformation
3. **cx_agentic_ai_digital_workforce** - Customer Experience with Agentic AI Digital Workforce
4. **cx_enterprise_data_architecture** - Customer Experience Enterprise Data Architecture
5. **enterprise_data_architecture** - Enterprise Data Architecture

## Converting Books to HTML

### Using the Unified Converter Script

The recommended way to convert any book to HTML is using the `convert_book_to_html.py` script:

```bash
python convert_book_to_html.py <book_directory> [options]
```

#### Parameters:

- `book_directory`: Path to the book directory containing Markdown files
- `-o, --output-dir`: (Optional) Directory to save the HTML output file (defaults to "output" directory)
- `-v, --version`: (Optional) Version string to include in the HTML title (default: v1.0)

#### Examples:

Convert the agentic AI book with default settings:
```bash
python convert_book_to_html.py agentic_ai_modern_data_architecture
```

Convert with custom version number:
```bash
python convert_book_to_html.py agentic_ai_modern_data_architecture -v v2.1
```

Specify a custom output directory:
```bash
python convert_book_to_html.py agentic_ai_modern_data_architecture -o /path/to/output
```

### Features

- **Automatic Table of Contents** - Creates a clickable table of contents based on chapter files
- **Mermaid Diagram Support** - Properly renders Mermaid diagrams found in Markdown files
- **Responsive Design** - HTML output is styled to work well on different screen sizes
- **Code Highlighting** - Properly formats code blocks
- **Clean Navigation** - Chapters are clearly separated with navigation anchors

## HTML Output

The HTML output includes:
- Responsive styling for better readability
- Proper rendering of Mermaid diagrams
- Table of contents with links to each chapter
- Code syntax highlighting
- Clean, professional formatting

The output file will be saved to the specified output directory (or the default "output" directory) with a filename based on the book directory name and version.

## Requirements

- Python 3.6 or higher
- Markdown package (`pip install markdown`)


