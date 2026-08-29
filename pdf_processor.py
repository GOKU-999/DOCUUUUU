"""
PDF Processing Utilities for DocuBot
"""

import PyPDF2
import io
import pypdf

def extract_text_from_pdf(pdf_file):
    """
    Extract text from a PDF file
    
    Args:
        pdf_file: Uploaded PDF file object
        
    Returns:
        str: Extracted text from the PDF
    """
    try:
        # Read the PDF file
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        # Check if PDF has pages
        if len(pdf_reader.pages) == 0:
            return ""
        
        # Extract text from all pages
        extracted_text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"
        
        return extracted_text.strip()
        
    except Exception as e:
        print(f"Error extracting text from PDF: {str(e)}")
        return ""

def get_pdf_metadata(pdf_file):
    """
    Extract metadata from PDF file
    
    Args:
        pdf_file: Uploaded PDF file object
        
    Returns:
        dict: PDF metadata
    """
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        metadata = pdf_reader.metadata
        return {
            "pages": len(pdf_reader.pages),
            "title": metadata.title if metadata and metadata.title else "Unknown",
            "author": metadata.author if metadata and metadata.author else "Unknown",
            "creator": metadata.creator if metadata and metadata.creator else "Unknown"
        }
    except Exception as e:
        return {"error": str(e)}

def validate_pdf(pdf_file):
    """
    Validate if the PDF is readable and contains text
    
    Args:
        pdf_file: Uploaded PDF file object
        
    Returns:
        tuple: (is_valid, message)
    """
    try:
        # Check if file is PDF
        if not pdf_file.name.lower().endswith('.pdf'):
            return False, "File must be a PDF"
        
        # Try to read the PDF
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        # Check if PDF is encrypted
        if pdf_reader.is_encrypted:
            return False, "PDF is encrypted. Please provide an unencrypted PDF."
        
        # Check if PDF has pages
        if len(pdf_reader.pages) == 0:
            return False, "PDF has no pages."
        
        # Try to extract text from first page to check if it's selectable
        first_page = pdf_reader.pages[0]
        text = first_page.extract_text()
        if not text or len(text.strip()) < 10:
            return False, "PDF appears to be scanned or image-based. Please use a PDF with selectable text."
        
        return True, "PDF is valid and ready for processing."
        
    except Exception as e:
        return False, f"Error validating PDF: {str(e)}"
