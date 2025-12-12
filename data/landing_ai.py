import os
import json
from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter
from landingai_ade import LandingAIADE
import time

# Define your page ranges for each PDF
PAGE_RANGES = {
    # "AbbVie.pdf": (60, 66),
    # "Accenture.pdf": (75, 90),
    # "Adobe.pdf": (54, 60),
    # "American_Tower_Corporation.pdf": (95, 102),
    # "AstraZeneca.pdf": (143, 147),
    # "Bristol_Myers_Squibb.pdf": (45, 39),
    # "Cisco_Systems.pdf": (70, 78),
    # "Colgate_Palmolive.pdf": (202, 276),
    # "Comcast.pdf": (60, 69),
    # "IFCI.pdf": (96, 100),
    # "Infosys.pdf": (195, 205),
    # "JD.com.pdf": (19, 31),
    # "LARSEN_&_TOUBRO.pdf": (455, 462),
    # "Merck_&_Co..pdf": (77, 80),
    # "Mitsui_Fudosan.pdf": (62, 63),
    # "Netflix.pdf": (39, 46),
    # "Novartis.pdf": (129, 133),
    # "Nvidia.pdf": (144, 148),
    # "PepsiCo.pdf": (73, 78),
    # "Shriram_Properties.pdf": (62, 64),
    # "Spencers.pdf": (149, 153),
    # "The_Walt_Disney_Company.pdf": (77, 81),
    # "Unilever.pdf": (145, 148),
    # "Titan.pdf": (367, 371),
    # "Vodafone Group.pdf": (190, 198),
    # "Warner_Bros._Discovery.pdf": (70, 74),
    # "Aditya_Birla.pdf": (242, 247),
    # "Bisleri.pdf": (37, 40),
    # "ChinaMobile.pdf": (94, 101),
    # "DHL.pdf": (151, 155),
    # "FedEx.pdf": (81, 86),
    # "Gopal_Snacks.pdf": (75, 76),
    # "Hapag_Lloyd.pdf": (304, 311),
    # "HnM.pdf": (62, 67),
    # "Huawei.pdf": (99, 101),
    # "Lenovo.pdf": (5, 11),
    # "Mastek.pdf": (96, 98),
    # "Morgan_Stanley.pdf": (78, 81),
    # "Nippon_Express.pdf": (3, 11),
    # "NovoNordisk.pdf": (102, 105),
    # "Philips.pdf": (88, 92),
    # "RajRatanOutperform.pdf": (134, 138),
    # "Rane_Holdings_Limited.pdf": (105, 108),
    # "Reliance.pdf": (84, 87),
    # "Resolute.pdf": (206, 210),
    # "TCI_Express.pdf": (220, 226),
    # "United_Breweries_Limited.pdf": (59, 61),
    # "VRL_Logistics.pdf": (158, 161),
    # "AmericanTourister.pdf": (42, 56),
    # "Calvin_Klein.pdf": (80, 84),
    # "Aimtron.pdf": (64, 65),
}

INPUT_PDFS_PATH = "/home/friday_code/Desktop/Web Scrap - Finalyze/data/"
OUTPUT_DIR = "/home/friday_code/Desktop/Web Scrap - Finalyze/data/"

# Create output directory if it doesn't exist
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)


def extract_pdf_pages(pdf_path, start_page, end_page):
    """
    Extract specific pages from a PDF and save to a temporary file
    
    Args:
        pdf_path: Full path to the PDF
        start_page: Starting page number (1-indexed)
        end_page: Ending page number (1-indexed, inclusive)
    
    Returns:
        Path to the temporary extracted PDF
    """
    try:
        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        
        total_pages = len(reader.pages)
        
        # Handle case where end_page < start_page (swap them)
        if end_page < start_page:
            start_page, end_page = end_page, start_page
        
        # Validate page range
        start_page = max(1, start_page)
        end_page = min(total_pages, end_page)
        
        print(f"  Total pages: {total_pages}, Extracting pages {start_page}-{end_page}")
        
        # Extract pages (convert to 0-indexed)
        for page_num in range(start_page - 1, end_page):
            writer.add_page(reader.pages[page_num])
        
        # Save to temporary file
        temp_pdf_path = pdf_path.replace(".pdf", "_temp.pdf")
        with open(temp_pdf_path, "wb") as temp_file:
            writer.write(temp_file)
        
        return temp_pdf_path
    
    except Exception as e:
        print(f"  ✗ Error extracting pages from PDF: {e}")
        return None


def parse_with_landingai(pdf_path):
    """
    Parse PDF using LandingAI ADE API
    
    Args:
        pdf_path: Path to the PDF file
    
    Returns:
        Markdown text from the PDF
    """
    try:
        client = LandingAIADE()
        
        # Parse with page splitting to better handle content
        response = client.parse(
            document=Path(pdf_path),
            model="dpt-2-latest"
        )
        
        # Handle response - check if it has markdown attribute
        if hasattr(response, 'markdown'):
            return response.markdown
        elif hasattr(response, 'as_markdown'):
            return response.as_markdown()
        else:
            # Fallback: handle response object
            return str(response)
    
    except Exception as e:
        print(f"  ✗ Error parsing PDF with LandingAI: {e}")
        return None


def process_pdf(pdf_filename, input_dir, output_dir, page_ranges):
    """
    Main function to process a single PDF
    
    Args:
        pdf_filename: Name of the PDF file
        input_dir: Directory containing input PDFs
        output_dir: Directory to save output markdown files
        page_ranges: Dictionary mapping filenames to (start_page, end_page) tuples
    """
    pdf_path = os.path.join(input_dir, pdf_filename)
    
    # Check if file exists
    if not os.path.exists(pdf_path):
        print(f"✗ File not found: {pdf_path}")
        return
    
    # Get page range for this PDF
    if pdf_filename not in page_ranges:
        print(f"✗ No page range defined for {pdf_filename}")
        return
    
    start_page, end_page = page_ranges[pdf_filename]
    
    print(f"\n📄 Processing: {pdf_filename}")
    print(f"  Page range: {start_page}-{end_page}")
    
    # Step 1: Extract specified pages
    temp_pdf_path = extract_pdf_pages(pdf_path, start_page, end_page)
    if not temp_pdf_path:
        return
    
    # Step 2: Parse with LandingAI
    print(f"  🔄 Parsing with LandingAI ADE API...")
    markdown_content = parse_with_landingai(temp_pdf_path)
    
    if not markdown_content:
        return
    
    # Step 3: Save to markdown file
    output_filename = pdf_filename.replace(".pdf", ".md")
    output_path = os.path.join(output_dir, output_filename)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    
    print(f"  ✅ Saved: {output_path}")
    
    # Cleanup temporary PDF
    try:
        os.remove(temp_pdf_path)
    except:
        pass
    
    # Add delay to avoid rate limiting
    time.sleep(1)


def main():
    """Main execution function"""
    print("=" * 60)
    print("PDF Text Extraction using LandingAI ADE API")
    print("=" * 60)
    
    # Process all PDFs in the input directory
    pdf_files = [f for f in os.listdir(INPUT_PDFS_PATH) if f.lower().endswith(".pdf")]
    
    if not pdf_files:
        print("❌ No PDF files found in the input directory!")
        return
    
    print(f"\nFound {len(pdf_files)} PDF files to process\n")
    
    successful = 0
    failed = 0
    
    for pdf_filename in sorted(pdf_files):
        try:
            process_pdf(pdf_filename, INPUT_PDFS_PATH, OUTPUT_DIR, PAGE_RANGES)
            successful += 1
        except Exception as e:
            print(f"❌ Failed to process {pdf_filename}: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Processing Complete!")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print("=" * 60)


if __name__ == "__main__":
    main()
