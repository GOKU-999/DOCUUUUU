"""
PDF Processing Utilities for DocuBot
Handles text extraction from PDF files
"""

import PyPDF2
import io
from typing import Optional

def extract_text_from_pdf(pdf_file) -> Optional[str]:
    """
    Extract text content from uploaded PDF file
    
    Args:
        pdf_file: Uploaded file object from Streamlit
        
    Returns:
        Extracted text as string, or None if extraction fails
    """
    try:
        # Create PDF reader object
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file.getvalue()))
        
        # Extract text from all pages
        extracted_text = []
        total_pages = len(pdf_reader.pages)
        
        for page_num, page in enumerate(pdf_reader.pages, 1):
            try:
                page_text = page.extract_text()
                if page_text and page_text.strip():
                    extracted_text.append(f"--- Page {page_num} ---\n{page_text}")
            except Exception as e:
                print(f"Error extracting page {page_num}: {str(e)}")
                continue
        
        if not extracted_text:
            return None
            
        # Combine all pages
        full_text = "\n\n".join(extracted_text)
        
        # Clean up text
        full_text = clean_text(full_text)
        
        return full_text
        
    except Exception as e:
        print(f"PDF extraction error: {str(e)}")
        return None

def clean_text(text: str) -> str:
    """
    Clean extracted text by removing extra whitespace and formatting issues
    
    Args:
        text: Raw extracted text
        
    Returns:
        Cleaned text
    """
    # Remove excessive newlines
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # Join with single newlines
    cleaned = '\n'.join(lines)
    
    # Remove multiple spaces
    import re
    cleaned = re.sub(r' +', ' ', cleaned)
    
    return cleaned

def get_text_statistics(text: str) -> dict:
    """
    Get statistics about extracted text
    
    Args:
        text: Extracted text content
        
    Returns:
        Dictionary with text statistics
    """
    words = text.split()
    return {
        'characters': len(text),
        'words': len(words),
        'pages': text.count('--- Page') if '--- Page' in text else 1,
        'paragraphs': text.count('\n\n')
    }
