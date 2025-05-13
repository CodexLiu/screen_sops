import os
import sys
import concurrent.futures
from docx import Document
from call import ask_openrouter
from docx_to_text import docx_to_text
from prompts.review_prompt import review_prompt
import markdown
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT, WD_LINE_SPACING
from docx.oxml.ns import qn
import html
from bs4 import BeautifulSoup
import re
from markdown_to_pdf import markdown_to_pdf

def read_sop_template():
    """Read the SOP template from the file"""
    with open("prompts/sop_template.txt", "r") as f:
        return f.read()

def process_sop(sop_path, output_dir="output", debug=False):
    """Process a single SOP document"""
    try:
        # Extract filename without extension for the output file
        filename = os.path.basename(sop_path)
        base_filename = os.path.splitext(filename)[0]
        
        print(f"Processing: {filename}")
        
        # Extract text from DOCX using docx_to_text function
        print(f"Extracting text from: {filename}")
        _, sop_text = docx_to_text(sop_path)
        
        # Get the SOP template
        sop_template = read_sop_template()
        
        # Format the prompt with the template and actual SOP text
        formatted_prompt = review_prompt.format(
            sop_template=sop_template,
            sop=sop_text  # Use the actual extracted text instead of placeholder
        )
        
        # Print the formatted payload for debugging
        if debug:
            print("\n=== PROMPT BEING SENT TO API ===")
            print("SOP Template (first 100 chars):", sop_template[:100] + "...")
            print("SOP Text (first 100 chars):", sop_text[:100] + "...")
            print("Formatted Prompt (first 500 chars):", formatted_prompt[:500] + "...")
            print("=== (Truncated for readability) ===\n")
        
        # Make the API call with the text prompt only (no DOCX attachment)
        print(f"Sending to API for review: {filename}")
        review_result = ask_openrouter(formatted_prompt)
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Save markdown output
        markdown_path = os.path.join(output_dir, f"{base_filename}_review.md")
        with open(markdown_path, "w", encoding='utf-8') as f:
            f.write(review_result)
        print(f"Markdown saved to: {markdown_path}")
        
        # Convert markdown to PDF (instead of DOCX)
        pdf_path = os.path.join(output_dir, f"{base_filename}_review.pdf")
        markdown_to_pdf(markdown_path, pdf_path)
        print(f"PDF saved to: {pdf_path}")
        
        return (sop_path, pdf_path)
    except Exception as e:
        print(f"Error processing {sop_path}: {str(e)}")
        return (sop_path, None)

def process_all_sops(docs_dir="docs", output_dir="output", max_workers=4, debug=False):
    """Walk through the docs directory and process all docx files in parallel"""
    # Find all docx files
    sop_files = []
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.docx'):
                sop_path = os.path.join(root, file)
                sop_files.append(sop_path)
    
    # Process files in parallel
    processed_files = []
    total_files = len(sop_files)
    print(f"Found {total_files} docx files to process")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Process files in parallel using ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_sop = {
            executor.submit(process_sop, sop_path, output_dir, debug): sop_path 
            for sop_path in sop_files
        }
        
        # Process as they complete
        for i, future in enumerate(concurrent.futures.as_completed(future_to_sop), 1):
            sop_path = future_to_sop[future]
            try:
                result = future.result()
                if result[1]:  # If output path is not None
                    processed_files.append(result)
                print(f"Progress: {i}/{total_files} - Completed {os.path.basename(sop_path)}")
            except Exception as e:
                print(f"Error processing {sop_path}: {str(e)}")
    
    print(f"\nProcessing complete. Successfully processed {len(processed_files)} out of {total_files} files.")
    return processed_files

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Process SOP files in parallel")
    parser.add_argument("--docs_dir", default="docs", help="Directory containing the SOP documents")
    parser.add_argument("--output_dir", default="output", help="Directory to store the output files")
    parser.add_argument("--max_workers", type=int, default=64, help="Maximum number of parallel workers")
    parser.add_argument("--debug", action="store_true", help="Enable debug output to see the prompt being sent")
    
    args = parser.parse_args()
    
    process_all_sops(args.docs_dir, args.output_dir, args.max_workers, args.debug) 