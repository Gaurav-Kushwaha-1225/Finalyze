from pathlib import Path
from landingai_ade import LandingAIADE
import pymupdf  # pip install pymupdf
import json
import os
import time
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PDFExtractor:
    """Production-ready PDF extractor for large documents (100+ pages)"""
    
    def __init__(self, pages_per_chunk=80, delay_between_requests=10):
        """Initialize extractor"""
        self.client = LandingAIADE()
        self.pages_per_chunk = pages_per_chunk
        self.failed_chunks = []
        self.delay_between_requests = delay_between_requests

    def split_pdf_into_chunks(self, pdf_path: str) -> list:
        """Split large PDF into smaller chunks to avoid 100-page limit"""
        try:
            pdf_doc = pymupdf.open(pdf_path)
            total_pages = len(pdf_doc)
            chunks = []
            
            logger.info(f"Total pages: {total_pages}")
            
            # Split into chunks
            for start_page in range(0, total_pages, self.pages_per_chunk):
                end_page = min(start_page + self.pages_per_chunk, total_pages)
                
                # Create chunk PDF
                chunk_pdf = pymupdf.open()
                chunk_pdf.insert_pdf(pdf_doc, from_page=start_page, to_page=end_page - 1)
                
                chunk_path = f"temp_chunk_{start_page:04d}_{end_page:04d}.pdf"
                chunk_pdf.save(chunk_path)
                chunk_pdf.close()
                
                chunks.append({
                    "path": chunk_path,
                    "start_page": start_page + 1,
                    "end_page": end_page,
                    "chunk_id": len(chunks)
                })
                
                logger.info(f"Created chunk: pages {start_page + 1}-{end_page}")
            
            pdf_doc.close()
            return chunks
            
        except Exception as e:
            logger.error(f"Error splitting PDF: {e}")
            raise
    
    def process_chunk(self, chunk_info: dict, retry_count: int = 3) -> dict:
        """Process single chunk with retry logic"""
        chunk_id = chunk_info["chunk_id"]
        
        for attempt in range(retry_count):
            try:
                logger.info(
                    f"Processing chunk {chunk_id} (pages {chunk_info['start_page']}-{chunk_info['end_page']}) "
                    f"[attempt {attempt + 1}/{retry_count}]"
                )
                
                # Parse chunk
                response = self.client.parse(
                    document=Path(chunk_info["path"]),
                    model="dpt-2-latest"
                )
                
                result = {
                    "status": "success",
                    "chunk_id": chunk_id,
                    "start_page": chunk_info["start_page"],
                    "end_page": chunk_info["end_page"],
                    "markdown": response.markdown,
                    "chunks_count": len(response.chunks),
                    "duration_ms": response.metadata.duration_ms if hasattr(response.metadata, 'duration_ms') else None
                }
                
                logger.info(f"✅ Chunk {chunk_id} complete")
                return result
                
            except Exception as e:
                logger.warning(f"⚠️ Chunk {chunk_id} attempt {attempt + 1} failed: {e}")
                if attempt < retry_count - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff (wait 1s, 2s, 4s)
                    continue
        
        logger.error(f"❌ Chunk {chunk_id} failed after {retry_count} attempts")
        self.failed_chunks.append(chunk_info)
        
        return {
            "status": "failed",
            "chunk_id": chunk_id,
            "start_page": chunk_info["start_page"],
            "end_page": chunk_info["end_page"],
            "error": f"Failed after {retry_count} attempts"
        }
    
    def extract_large_pdf(self, pdf_path: str, output_dir: str = ".") -> str:
        """Main extraction method for large PDFs"""
        
        pdf_path = Path(pdf_path)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Starting extraction: {pdf_path.name}")
        start_time = time.time()
        
        # Step 1: Split PDF
        try:
            chunks = self.split_pdf_into_chunks(str(pdf_path))
        except Exception as e:
            logger.error(f"Failed to split PDF: {e}")
            return None
        
        logger.info(f"Split into {len(chunks)} chunks")
        
        # Step 2: Process each chunk
        results = []
        for i, chunk_info in enumerate(chunks, 1):
            result = self.process_chunk(chunk_info)
            results.append(result)
            time.sleep(self.delay_between_requests)

            progress = (i / len(chunks)) * 100
            logger.info(f"Progress: {progress:.1f}% ({i}/{len(chunks)})")
        
        # Step 3: Combine results
        combined_markdown = ""
        processing_stats = []
        
        for result in sorted(results, key=lambda x: x["chunk_id"]):
            if result["status"] == "success":
                # Add page separator
                combined_markdown += (
                    f"\n---\n"
                    f"## Pages {result['start_page']}-{result['end_page']}\n"
                    f"---\n"
                    f"{result['markdown']}"
                )
                
                processing_stats.append({
                    "chunk": result["chunk_id"],
                    "pages": f"{result['start_page']}-{result['end_page']}",
                    "status": "success",
                    "chunks": result["chunks_count"],
                    "duration_ms": result["duration_ms"]
                })
            else:
                logger.warning(f"Skipping failed chunk {result['chunk_id']}")
                processing_stats.append({
                    "chunk": result["chunk_id"],
                    "status": "failed",
                    "error": result.get("error")
                })
        
        # Step 4: Save outputs
        output_file = output_dir / f"{pdf_path.stem}.md"
        output_file.write_text(combined_markdown, encoding="utf-8")
        logger.info(f"✅ Combined markdown saved: {output_file}")
        
        # Save metadata
        metadata = {
            "source_pdf": pdf_path.name,
            "total_pages": sum(r['end_page'] - r['start_page'] + 1 for r in chunks),
            "total_chunks": len(chunks),
            "successful_chunks": len([r for r in results if r["status"] == "success"]),
            "failed_chunks": len(self.failed_chunks),
            "total_processing_time_seconds": time.time() - start_time,
            "output_file": output_file.name,
            "output_size_chars": len(combined_markdown),
            "chunk_details": processing_stats
        }
        
        metadata_file = output_dir / f"{pdf_path.stem}_metadata.json"
        metadata_file.write_text(json.dumps(metadata, indent=2))
        logger.info(f"✅ Metadata saved: {metadata_file}")
        
        # Cleanup temporary chunk files
        for chunk_info in chunks:
            try:
                Path(chunk_info["path"]).unlink()
            except:
                pass
        logger.info("✅ Temporary chunk files cleaned up")
        
        # Report results
        print("\n" + "="*70)
        print("✅ EXTRACTION COMPLETE")
        print("="*70)
        print(f"File: {pdf_path.name}")
        print(f"Total Pages: {metadata['total_pages']}")
        print(f"Output: {output_file.name}")
        print(f"Size: {len(combined_markdown):,} characters")
        print(f"Time: {metadata['total_processing_time_seconds']:.2f} seconds")
        print(f"Status: {metadata['successful_chunks']}/{metadata['total_chunks']} chunks ✅")
        print("="*70)
        
        return str(output_file)


def process_all_pdfs(input_dir: str, output_dir: str, pages_per_chunk: int = 80):
    """Process all PDFs in a directory"""
    
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Find all PDFs
    pdf_files = list(input_path.glob("*.pdf"))
    
    if not pdf_files:
        logger.error(f"No PDF files found in {input_dir}")
        return
    
    logger.info(f"Found {len(pdf_files)} PDF files to process")
    
    # Initialize extractor
    extractor = PDFExtractor(pages_per_chunk=pages_per_chunk)
    
    # Process each PDF
    results = []
    for i, pdf_file in enumerate(pdf_files, 1):
        try:
            print(f"\n[{i}/{len(pdf_files)}] Processing: {pdf_file.name}")
            
            output_file = extractor.extract_large_pdf(
                pdf_path=str(pdf_file),
                output_dir=str(output_path)
            )
            
            results.append({
                "file": pdf_file.name,
                "status": "success",
                "output": output_file
            })

            time.sleep(20)
            
        except Exception as e:
            logger.error(f"❌ Failed to process {pdf_file.name}: {e}")
            results.append({
                "file": pdf_file.name,
                "status": "failed",
                "error": str(e)
            })
    
    # Save summary
    summary_file = output_path / "extraction_summary.json"
    summary_file.write_text(json.dumps(results, indent=2))
    logger.info(f"\n✅ Summary saved: {summary_file}")
    
    # Print summary
    print("\n" + "="*70)
    print("ALL PROCESSING COMPLETE")
    print("="*70)
    successful = len([r for r in results if r["status"] == "success"])
    failed = len([r for r in results if r["status"] == "failed"])
    print(f"Total Files: {len(pdf_files)}")
    print(f"Successful: {successful} ✅")
    print(f"Failed: {failed} ❌")
    print(f"Summary: {summary_file}")
    print("="*70)


# ============================================
# MAIN EXECUTION
# ============================================

if __name__ == "__main__":
    # Set your paths here
    INPUT_PDFS_PATH = "/home/friday_code/Desktop/Web Scrap - Finalyze/data/"
    OUTPUT_DIR = "/home/friday_code/Desktop/Web Scrap - Finalyze/data/extracted/"
    
    # Process all PDFs in the directory
    process_all_pdfs(
        input_dir=INPUT_PDFS_PATH,
        output_dir=OUTPUT_DIR,
        pages_per_chunk=80,  # Process 80 pages at a time (safe for 100-page limit)
    )
