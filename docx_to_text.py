import os
import sys
from docx2python import docx2python

def docx_to_text(docx_path: str) -> str:
    """
    Extracts text from a DOCX file using docx2python.
    Returns the path to the saved text file.
    """
    print(f"Extracting text from: {docx_path}")
    
    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.getcwd(), "test_output")
    os.makedirs(output_dir, exist_ok=True)
    
    # Create output filename
    base_filename = os.path.splitext(os.path.basename(docx_path))[0]
    output_file = os.path.join(output_dir, f"{base_filename}_extracted.txt")
    
    # Extract content using docx2python
    with docx2python(docx_path) as docx:
        # Get document metadata
        metadata = []
        if docx.properties and hasattr(docx.properties, 'core_properties'):
            props = docx.properties.core_properties
            if hasattr(props, 'title') and props.title:
                metadata.append(f"Title: {props.title}")
            if hasattr(props, 'creator') and props.creator:
                metadata.append(f"Author: {props.creator}")
            if hasattr(props, 'created') and props.created:
                metadata.append(f"Created: {props.created}")
            if hasattr(props, 'modified') and props.modified:
                metadata.append(f"Modified: {props.modified}")
        
        # Extract text from different document parts
        header_text = []
        for header in docx.header:
            for table in header:
                for row in table:
                    for cell in row:
                        for paragraph in cell:
                            if paragraph.strip():
                                header_text.append(paragraph)
        
        footer_text = []
        for footer in docx.footer:
            for table in footer:
                for row in table:
                    for cell in row:
                        for paragraph in cell:
                            if paragraph.strip():
                                footer_text.append(paragraph)
        
        body_text = []
        for table in docx.body:
            for row in table:
                for cell in row:
                    for paragraph in cell:
                        if paragraph.strip():
                            body_text.append(paragraph)
        
        footnotes_text = []
        for footnote in docx.footnotes:
            for table in footnote:
                for row in table:
                    for cell in row:
                        for paragraph in cell:
                            if paragraph.strip():
                                footnotes_text.append(paragraph)
                                
        endnotes_text = []
        for endnote in docx.endnotes:
            for table in endnote:
                for row in table:
                    for cell in row:
                        for paragraph in cell:
                            if paragraph.strip():
                                endnotes_text.append(paragraph)
        
        # Combine all sections with clear separation
        all_text_parts = []
        
        if metadata:
            all_text_parts.append("=== DOCUMENT METADATA ===")
            all_text_parts.extend(metadata)
            all_text_parts.append("")
        
        if header_text:
            all_text_parts.append("=== HEADERS ===")
            all_text_parts.extend(header_text)
            all_text_parts.append("")
        
        if body_text:
            all_text_parts.append("=== DOCUMENT BODY ===")
            all_text_parts.extend(body_text)
            all_text_parts.append("")
        
        if footer_text:
            all_text_parts.append("=== FOOTERS ===")
            all_text_parts.extend(footer_text)
            all_text_parts.append("")
            
        if footnotes_text:
            all_text_parts.append("=== FOOTNOTES ===")
            all_text_parts.extend(footnotes_text)
            all_text_parts.append("")
            
        if endnotes_text:
            all_text_parts.append("=== ENDNOTES ===")
            all_text_parts.extend(endnotes_text)
            all_text_parts.append("")
            
        if docx.comments:
            all_text_parts.append("=== COMMENTS ===")
            for ref_text, author, date, comment_text in docx.comments:
                all_text_parts.append(f"Comment by {author} on {date}:")
                all_text_parts.append(f"Referenced text: \"{ref_text}\"")
                all_text_parts.append(f"Comment: {comment_text}")
                all_text_parts.append("")
            
        # Join all parts into a single string
        full_text = "\n".join(all_text_parts)
        
        # Save to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(full_text)
    
    print(f"Text extraction complete. Output saved to: {output_file}")
    
    # Print preview
    preview_length = min(1000, len(full_text))
    print("\nPreview of extracted text:")
    print("-" * 50)
    print(full_text[:preview_length] + ("..." if len(full_text) > preview_length else ""))
    print("-" * 50)
    
    return output_file, full_text

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <path_to_docx>")
        sys.exit(1)
    
    docx_path = sys.argv[1]
    
    if not os.path.exists(docx_path):
        print(f"Error: File not found - {docx_path}")
        sys.exit(1)
        
    if not docx_path.lower().endswith('.docx'):
        print(f"Warning: File may not be a DOCX file - {docx_path}")
    
    output_file, _ = docx_to_text(docx_path)
    print(f"Text extraction complete. Output saved to: {output_file}")
    
    # Print preview of the file
    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            preview = f.read(1000)
        print("\nPreview of output:")
        print("-" * 50)
        print(preview + ("..." if len(preview) >= 1000 else ""))
        print("-" * 50)
    except:
        pass 