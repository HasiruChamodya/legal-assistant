# slpc_pdf_extractor.py

"""
Sri Lankan Penal Code (SLPC) PDF Extractor

This script extracts sections from the Sri Lankan Penal Code PDF and converts them
into structured JSON format for vector database ingestion.

Usage:
1. Place your SLPC PDF in the data/ directory
2. Update the PDF_PATH variable below
3. Run: python slpc_pdf_extractor.py
4. Output will be saved as slpc.json

Note: You may need to adjust regex patterns based on your PDF's formatting.
"""

import json
import re
import os
from typing import List, Dict
import pdfplumber


# Configuration
PDF_PATH = "data/penal_code.pdf"  # Update this path to your SLPC PDF location
OUTPUT_PATH = "slpc.json"


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract all text from PDF file.
    
    Args:
        pdf_path (str): Path to the PDF file.
    
    Returns:
        str: Extracted text from all pages.
    """
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        print(f"✅ Successfully extracted text from {len(pdf.pages)} pages")
    except Exception as e:
        print(f"❌ Error extracting PDF: {e}")
        raise
    return text


def parse_slpc_sections(text: str) -> List[Dict]:
    """
    Parse SLPC sections from extracted text using regex patterns.
    
    This function uses regex patterns to identify chapters and sections.
    You may need to adjust these patterns based on your PDF's formatting.
    
    Args:
        text (str): Raw text extracted from PDF.
    
    Returns:
        List[Dict]: List of structured section dictionaries.
    """
    sections = []
    
    # Regex patterns - ADJUST THESE based on your PDF format
    # Example patterns for different possible formats:
    
    # Pattern 1: "CHAPTER XVI" or "CHAPTER 16" or "Chapter XVI"
    chapter_pattern = r'(?:CHAPTER|Chapter)\s+([IVXLCDM]+|\d+)[:\s]*([^\n]+)'
    
    # Pattern 2: "Section 365" or "§365" or "365."
    section_pattern = r'(?:Section|§)\s*(\d+)[:\.\s]*([^\n]+)'
    
    # Alternative section pattern if the PDF uses just numbers
    # section_pattern = r'^(\d+)\.\s+([^\n]+)'
    
    current_chapter = "Unknown"
    current_chapter_num = 0
    
    # Split text into lines for processing
    lines = text.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Try to match chapter
        chapter_match = re.match(chapter_pattern, line, re.IGNORECASE)
        if chapter_match:
            current_chapter_num = chapter_match.group(1)
            current_chapter = chapter_match.group(2).strip()
            print(f"Found Chapter {current_chapter_num}: {current_chapter}")
            i += 1
            continue
        
        # Try to match section
        section_match = re.match(section_pattern, line, re.IGNORECASE)
        if section_match:
            section_num = int(section_match.group(1))
            section_title = section_match.group(2).strip()
            
            # Extract section description (next few lines)
            section_desc = ""
            j = i + 1
            # Collect lines until we hit another section or chapter
            while j < len(lines):
                next_line = lines[j].strip()
                if re.match(chapter_pattern, next_line, re.IGNORECASE) or \
                   re.match(section_pattern, next_line, re.IGNORECASE):
                    break
                if next_line:  # Only add non-empty lines
                    section_desc += next_line + " "
                j += 1
            
            section_desc = section_desc.strip()
            
            # Only add if we have meaningful content
            if section_desc:
                sections.append({
                    "chapter": current_chapter_num,
                    "chapter_title": current_chapter,
                    "Section": section_num,
                    "section_title": section_title,
                    "section_desc": section_desc
                })
                print(f"  Extracted Section {section_num}: {section_title[:50]}...")
            
            i = j
            continue
        
        i += 1
    
    return sections


def save_to_json(data: List[Dict], output_path: str):
    """
    Save extracted sections to JSON file.
    
    Args:
        data (List[Dict]): Extracted sections data.
        output_path (str): Path to save JSON file.
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ Successfully saved {len(data)} sections to {output_path}")
    except Exception as e:
        print(f"❌ Error saving JSON: {e}")
        raise


def preview_sections(sections: List[Dict], num_sections: int = 3):
    """
    Display a preview of extracted sections for verification.
    
    Args:
        sections (List[Dict]): Extracted sections.
        num_sections (int): Number of sections to preview.
    """
    print("\n" + "="*80)
    print("PREVIEW OF EXTRACTED SECTIONS")
    print("="*80)
    
    for i, section in enumerate(sections[:num_sections]):
        print(f"\nSection {i+1}:")
        print(f"  Chapter: {section['chapter']} - {section['chapter_title']}")
        print(f"  Section: {section['Section']}")
        print(f"  Title: {section['section_title']}")
        print(f"  Description: {section['section_desc'][:200]}...")
    
    print("\n" + "="*80)
    print(f"Total sections extracted: {len(sections)}")
    print("="*80)


def main():
    """
    Main execution function.
    """
    print("🔍 Sri Lankan Penal Code PDF Extractor")
    print("-" * 50)
    
    # Check if PDF exists
    if not os.path.exists(PDF_PATH):
        print(f"❌ PDF file not found at: {PDF_PATH}")
        print("\n📝 Instructions:")
        print("1. Create a 'data/' directory if it doesn't exist")
        print("2. Place your SLPC PDF in the data/ directory")
        print("3. Update the PDF_PATH variable in this script")
        return
    
    # Extract text from PDF
    print(f"\n📄 Reading PDF: {PDF_PATH}")
    text = extract_text_from_pdf(PDF_PATH)
    
    # Parse sections
    print("\n🔍 Parsing sections...")
    sections = parse_slpc_sections(text)
    
    if not sections:
        print("\n⚠️  No sections found!")
        print("\n💡 Troubleshooting tips:")
        print("1. Check if the PDF text extraction is working correctly")
        print("2. Adjust the regex patterns in parse_slpc_sections() function")
        print("3. Review the PDF structure and formatting")
        print("\nHere's a sample of the extracted text (first 500 chars):")
        print("-" * 50)
        print(text[:500])
        print("-" * 50)
        return
    
    # Preview extracted sections
    preview_sections(sections)
    
    # Save to JSON
    print(f"\n💾 Saving to {OUTPUT_PATH}...")
    save_to_json(sections, OUTPUT_PATH)
    
    print("\n✅ Extraction complete!")
    print("\n📋 Next steps:")
    print("1. Review the generated slpc.json file")
    print("2. If sections look incorrect, adjust regex patterns in this script")
    print("3. Once satisfied, run: python slpc_vectordb_builder.py")


if __name__ == "__main__":
    main()
