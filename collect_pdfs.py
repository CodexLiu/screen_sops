#!/usr/bin/env python3
import os
import shutil
import sys
import glob

def collect_pdfs(source_folder="output", dest_folder="collected_pdfs"):
    """
    Collect all PDF files from the source folder and copy them to the destination folder.
    
    Args:
        source_folder (str): Folder containing PDF files to collect
        dest_folder (str): Destination folder where PDFs will be copied
    """
    # Create destination folder if it doesn't exist
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
        print(f"Created destination folder: {dest_folder}")
    
    # Find all PDF files
    pdf_pattern = os.path.join(source_folder, "*.pdf")
    pdf_files = glob.glob(pdf_pattern)
    
    if not pdf_files:
        print(f"No PDF files found in {source_folder}")
        return
    
    # Copy files to destination
    for pdf_file in pdf_files:
        filename = os.path.basename(pdf_file)
        dest_path = os.path.join(dest_folder, filename)
        shutil.copy2(pdf_file, dest_path)
        print(f"Copied: {filename}")
    
    print(f"\nSuccessfully copied {len(pdf_files)} PDF files to {dest_folder}")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        source_folder = sys.argv[1]
        dest_folder = sys.argv[2]
        collect_pdfs(source_folder, dest_folder)
    elif len(sys.argv) > 1:
        source_folder = sys.argv[1]
        collect_pdfs(source_folder)
    else:
        collect_pdfs() 