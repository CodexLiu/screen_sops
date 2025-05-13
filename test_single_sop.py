#!/usr/bin/env python
import sys
import os
import json
from docx_to_text import docx_to_text
from prompts.review_prompt import review_prompt
from call import ask_openrouter
from markdown_to_pdf import markdown_to_pdf

def main():
    """
    Test script to convert a single DOCX file to text using docx2python
    and send the payload to Gemini API for review.
    """
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <path_to_docx_file>")
        sys.exit(1)
    
    # Get the DOCX file path
    docx_path = sys.argv[1]
    
    # Check if file exists
    if not os.path.exists(docx_path):
        print(f"Error: File not found - {docx_path}")
        sys.exit(1)
    
    # Check if it's a DOCX file
    if not docx_path.lower().endswith('.docx'):
        print(f"Warning: File may not be a DOCX file - {docx_path}")
    
    # Convert the file to text using docx2python
    print(f"Converting {docx_path} to text using docx2python...")
    output_file, extracted_text = docx_to_text(docx_path)
    
    # Load the SOP template
    template_path = os.path.join("prompts", "sop_template.txt")
    with open(template_path, 'r', encoding='utf-8') as f:
        sop_template = f.read()
    
    # Create a payload using the review_prompt template
    print("Creating prompt payload...")
    payload = review_prompt.format(
        sop_template=sop_template,
        sop=extracted_text
    )
    
    # Save the payload to a file
    base_filename = os.path.splitext(os.path.basename(docx_path))[0]
    payload_file = os.path.join("test_output", f"{base_filename}_payload.txt")
    
    with open(payload_file, 'w', encoding='utf-8') as f:
        f.write(payload)
    
    print(f"API payload saved to: {payload_file}")
    
    # Send the payload to Gemini API
    print("Sending payload to Gemini API (this may take a while)...")
    response = ask_openrouter(payload)
    
    # Save the response to a markdown file
    response_md_file = os.path.join("test_output", f"{base_filename}_review.md")
    with open(response_md_file, 'w', encoding='utf-8') as f:
        f.write(response)
    
    # Convert markdown to PDF
    print("Converting markdown response to PDF...")
    response_pdf_file = os.path.join("test_output", f"{base_filename}_review.pdf")
    markdown_to_pdf(response_md_file, response_pdf_file)
    
    print(f"\nText extraction complete! Text saved to: {output_file}")
    print(f"API payload saved to: {payload_file}")
    print(f"Gemini API response saved to: {response_md_file}")
    print(f"PDF report saved to: {response_pdf_file}")
    print(f"To view the extracted text, run: cat {output_file}")
    print(f"To view the payload, run: cat {payload_file}")
    print(f"To view the Gemini response, run: cat {response_md_file}")

if __name__ == "__main__":
    main() 