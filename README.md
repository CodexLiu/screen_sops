# SOP Reviewer

A tool for automatically reviewing Standard Operating Procedures (SOPs) for scientific reproducibility and compliance with template standards.

## Overview

This project automatically analyzes scientific SOPs in DOCX format against a standard template, evaluating:

- Template compliance
- Experimental reproducibility
- Clarity and usability
- Documentation requirements

The tool places special emphasis on verifying detailed measurement procedures and equipment specifications to ensure experimental reproducibility.

## Installation

### Prerequisites

- Python 3.10+
- pip (Python package manager)

### Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd screen_sops
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```
   cp example.env .env
   ```
   Edit the `.env` file and add your OpenRouter API key.

### API Key Requirements

This tool uses the OpenRouter API to access language models for SOP reviews. You'll need:

1. An account on [OpenRouter](https://openrouter.ai/)
2. An API key from your account
3. Add this key to your `.env` file:
   ```
   OPENROUTER_API_KEY=your_api_key_here
   ```

### Main Dependencies

The system relies on several Python libraries including:
- `python-docx` and `docx2python` for DOCX file parsing
- `weasyprint` for PDF generation
- `openai` for API client functionality
- `markdown` for markdown processing
- `beautifulsoup4` for HTML parsing

All dependencies are listed in the requirements.txt file.

## Usage

The project offers two main modes of operation:

### 1. Process a Single SOP

Use this mode to test the system with a single SOP file:

```
python test_single_sop.py path/to/your/sop.docx
```

This will:
- Extract text from the DOCX file
- Compare it against the SOP template
- Generate a review in the `test_output` directory as both markdown and PDF

### 2. Process Multiple SOPs

Use this mode to batch process all SOPs in a directory:

```
python process_sops.py --docs_dir=docs --output_dir=output --max_workers=4
```

Options:
- `--docs_dir`: Directory containing SOP DOCX files (default: "docs")
- `--output_dir`: Directory for output reviews (default: "output")
- `--max_workers`: Maximum number of parallel processing workers (default: 64)
- `--debug`: Enable debug output to see the prompt being sent to the API

## Output

For each processed SOP, the system generates:
- A markdown file containing the detailed review
- A PDF version of the review report

Reviews focus on:
1. Template compliance analysis
2. Experimental reproducibility assessment (with detailed focus on measurement tools and containers)
3. Clarity and usability review
4. Documentation requirements

## Project Structure

```
screen_sops/
├── call.py                  # API integration with OpenRouter
├── collect_pdfs.py          # Utility for collecting PDFs
├── docx_to_text.py          # DOCX file text extraction
├── markdown_to_pdf.py       # Markdown to PDF conversion
├── process_sops.py          # Batch processing of SOPs
├── test_single_sop.py       # Single SOP processing for testing
├── docs/                    # Directory for SOP documents
├── output/                  # Directory for output reviews
├── prompts/                 # Contains review prompts and templates
│   ├── review_prompt.py     # The review prompt template
│   └── sop_template.txt     # The standard SOP template for comparison
└── test_output/             # Directory for test outputs
```

## Notes for Scientific Users

This tool is specifically designed to check for proper scientific documentation, with special emphasis on:

- Explicit identification of laboratory containers (beakers, Erlenmeyer flasks, etc.)
- Precise identification of measurement instruments
- Detailed specification of equipment and measurement precision
- Proper documentation of experimental procedures

## License

[License information] 