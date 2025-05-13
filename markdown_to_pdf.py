#!/usr/bin/env python3
import sys
import os
import markdown
import tempfile
from weasyprint import HTML, CSS
from bs4 import BeautifulSoup

def markdown_to_pdf(markdown_file, output_file=None, custom_css=None):
    """
    Convert a Markdown file to PDF with proper formatting.
    
    Args:
        markdown_file (str): Path to the markdown file
        output_file (str, optional): Path to output PDF file. If None, uses the same name with .pdf extension
        custom_css (str, optional): Path to custom CSS file for styling
        
    Returns:
        str: Path to the created PDF file
    """
    # Get the output filename if not provided
    if output_file is None:
        base_name = os.path.splitext(markdown_file)[0]
        output_file = f"{base_name}.pdf"
    
    # Get base directory for any relative links
    base_dir = os.path.dirname(os.path.abspath(markdown_file))
    
    # Read markdown content
    with open(markdown_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert markdown to HTML with extensions for better formatting
    html_content = markdown.markdown(
        md_content, 
        extensions=[
            'markdown.extensions.fenced_code',
            'markdown.extensions.tables',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            'markdown.extensions.attr_list',
            'markdown.extensions.extra',
            'markdown.extensions.nl2br',
        ]
    )
    
    # Process checkboxes [x] and [ ] which are not handled by standard markdown
    html_content = html_content.replace('[ ]', '☐').replace('[x]', '☑').replace('[X]', '☑')
    
    # Parse the HTML with BeautifulSoup to add more structure
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Fix checkboxes in HTML
    for p in soup.find_all('p'):
        if '☐' in p.text or '☑' in p.text:
            p['class'] = p.get('class', []) + ['checkbox-item']
    
    # Create a complete HTML document with styling
    html_template = f"""<!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>SOP Review Report</title>
        <style>
            @page {{
                size: letter;
                margin: 1in;
            }}
            body {{
                font-family: Arial, Helvetica, sans-serif;
                font-size: 11pt;
                line-height: 1.4;
                color: #333;
            }}
            h1, h2, h3, h4, h5, h6 {{
                margin-top: 1.2em;
                margin-bottom: 0.6em;
                color: #000;
            }}
            h1 {{ font-size: 18pt; }}
            h2 {{ font-size: 16pt; }}
            h3 {{ font-size: 14pt; color: #333366; }}
            h4 {{ font-size: 12pt; }}
            p {{ margin: 0.5em 0; }}
            ul, ol {{ 
                margin: 0.5em 0;
                padding-left: 1.5em;
            }}
            li {{ 
                margin-bottom: 0.25em; 
                padding-left: 0.5em;
            }}
            li p {{ margin: 0; }}
            code {{
                font-family: monospace;
                background-color: #f5f5f5;
                padding: 0.1em 0.3em;
                border-radius: 3px;
                font-size: 0.9em;
            }}
            pre {{
                background-color: #f5f5f5;
                padding: 0.5em;
                border-radius: 3px;
                overflow-x: auto;
            }}
            pre code {{ background-color: transparent; padding: 0; }}
            blockquote {{
                margin: 1em 0;
                padding: 0 1em;
                border-left: 3px solid #ccc;
                color: #666;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 1em 0;
            }}
            th, td {{
                padding: 0.5em;
                border: 1px solid #ddd;
                text-align: left;
            }}
            th {{ background-color: #f5f5f5; }}
            strong {{ font-weight: bold; }}
            em {{ font-style: italic; }}
            .checkbox-item {{
                position: relative;
                padding-left: 1.5em;
                margin: 0.3em 0;
            }}
            .checkbox-item::before {{
                position: absolute;
                left: 0;
                top: 0.2em;
                width: 1em;
                height: 1em;
            }}
            a {{ color: #0066cc; }}
            hr {{ 
                border: none;
                border-top: 1px solid #ddd; 
                margin: 1.5em 0;
            }}
        </style>
    </head>
    <body>
        {soup.prettify()}
    </body>
    </html>"""
    
    # Add custom CSS if provided
    if custom_css and os.path.exists(custom_css):
        with open(custom_css, 'r', encoding='utf-8') as f:
            custom_css_content = f.read()
            html_template = html_template.replace(
                '</style>', 
                f"{custom_css_content}\n</style>"
            )
    
    # Create a temporary HTML file
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False, mode='w', encoding='utf-8') as tmp_file:
        tmp_html_path = tmp_file.name
        tmp_file.write(html_template)
    
    try:
        # Convert HTML to PDF
        HTML(filename=tmp_html_path).write_pdf(
            output_file,
            stylesheets=[
                CSS(string='@page { size: letter; margin: 1in; }')
            ]
        )
        print(f"Successfully created PDF: {output_file}")
        return output_file
    finally:
        # Clean up the temporary file
        if os.path.exists(tmp_html_path):
            os.unlink(tmp_html_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python markdown_to_pdf.py <markdown_file> [output_pdf_file] [custom_css_file]")
        sys.exit(1)
    
    markdown_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    custom_css = sys.argv[3] if len(sys.argv) > 3 else None
    
    markdown_to_pdf(markdown_file, output_file, custom_css) 