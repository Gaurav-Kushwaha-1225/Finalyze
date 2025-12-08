from adobe.pdfservices.operation.auth.service_principal_credentials import ServicePrincipalCredentials
from adobe.pdfservices.operation.pdfjobs.params.extract_pdf.extract_pdf_params import ExtractPDFParams
from adobe.pdfservices.operation.pdfjobs.params.extract_pdf.extract_element_type import ExtractElementType
from adobe.pdfservices.operation.pdfjobs.jobs.extract_pdf_job import ExtractPDFJob
from adobe.pdfservices.operation.pdf_services import PDFServices
from adobe.pdfservices.operation.pdf_services_media_type import PDFServicesMediaType
from adobe.pdfservices.operation.io.cloud_asset import CloudAsset
from adobe.pdfservices.operation.io.stream_asset import StreamAsset
from adobe.pdfservices.operation.pdfjobs.result.extract_pdf_result import ExtractPDFResult
import zipfile
import json
import os
from PyPDF2 import PdfReader, PdfWriter


CREDENTIALS_FILE_PATH = "/home/friday_code/Desktop/Web Scrap - Finalyze/PDFServicesSDK-PythonSamples/pdfservices-api-credentials.json"
INPUT_PDFS_PATH = "/home/friday_code/Desktop/Web Scrap - Finalyze/data/"  # Your 10-K, annual report, etc.
OUTPUT_ZIP_PATH = "/home/friday_code/Desktop/Web Scrap - Finalyze/data/"
OUTPUT_DIR = "/home/friday_code/Desktop/Web Scrap - Finalyze/data/"


def main(INPUT_PDF_PATH):
    if "LARSEN" in INPUT_PDF_PATH:
        return
    # skip pdfs whose extraction are done, whose folders are in data/
    existing_folders = os.listdir(OUTPUT_DIR)
    pdf_name = os.path.basename(INPUT_PDF_PATH).replace(".pdf", "")
    if pdf_name in existing_folders:
        print(f"✓ Skipping {INPUT_PDF_PATH}, already extracted.")
        return

    # If a PDF is large, split into chunks and process each chunk
    def split_pdf_if_needed(pdf_path, max_pages=350):
        """Check if PDF exceeds page limit and split if needed"""
        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)
        
        if total_pages <= max_pages:
            return [pdf_path]  # No need to split
        
        print(f"⚠️  {os.path.basename(pdf_path)} has {total_pages} pages (limit: {max_pages})")
        print(f"📌 Splitting into chunks...")
        
        chunks_dir = os.path.dirname(pdf_path) + "/chunks"
        os.makedirs(chunks_dir, exist_ok=True)
        
        chunk_files = []
        for i in range(0, total_pages, max_pages):
            writer = PdfWriter()
            chunk_num = i // max_pages
            
            for page_num in range(i, min(i + max_pages, total_pages)):
                writer.add_page(reader.pages[page_num])
            
            chunk_filename = f"{os.path.basename(pdf_path).replace('.pdf', '')}_chunk_{chunk_num:03d}.pdf"
            chunk_path = os.path.join(chunks_dir, chunk_filename)
            
            with open(chunk_path, "wb") as f:
                writer.write(f)
            
            chunk_files.append(chunk_path)
            print(f"  ✓ Chunk {chunk_num}: {len(writer.pages)} pages → {chunk_filename}")
        
        return chunk_files

    # Split if needed and process each resulting file
    pdf_files_to_process = split_pdf_if_needed(INPUT_PDF_PATH, max_pages=350)

    for pdf_path in pdf_files_to_process:
        try:
            # 1. Build credentials
            credentials = ServicePrincipalCredentials(
                client_id="4df8576e7f2c4838947e3dfacb1f0dd8",
                client_secret="p8e-8EywBPesIOE2dWgjsca9yz0cEOvHNN-z"
            )

            # 2. Create PDFServices client
            pdf_services = PDFServices(credentials=credentials)

            # 3. Upload PDF
            with open(pdf_path, "rb") as f:
                input_asset = pdf_services.upload(
                    input_stream=f,
                    mime_type=PDFServicesMediaType.PDF
                )

            # 4. Define extraction: TEXT + TABLES + FIGURES
            # For financial reports: TEXT (narrative) + TABLES (balance sheet, P&L, CF)
            extract_params = ExtractPDFParams(
                elements_to_extract=[
                    ExtractElementType.TEXT,      # Headings, section labels, notes
                    ExtractElementType.TABLES,    # Balance Sheet, Income Statement, Cash Flow
                    # ExtractElementType.IMAGES    # Optional: charts, graphs
                ]
            )

            # 5. Create and submit extract job
            extract_job = ExtractPDFJob(
                input_asset=input_asset,
                extract_pdf_params=extract_params
            )

            location = pdf_services.submit(extract_job)
            # The SDK expects the Result class to be passed directly. ExtractPDFJob does not expose
            pdf_services_response = pdf_services.get_job_result(location, ExtractPDFResult)

            # 6. Download result ZIP
            result_asset: CloudAsset = pdf_services_response.get_result().get_resource()
            stream_asset: StreamAsset = pdf_services.get_content(result_asset)

            # FIXED: Extract filename and build paths correctly
            pdf_name = os.path.basename(pdf_path).replace(".pdf", "")
            zip_output_path = os.path.join(OUTPUT_ZIP_PATH, pdf_name + ".zip")
            with open(zip_output_path, "wb") as out:
                out.write(stream_asset.get_input_stream())

            print(f"✓ Extraction complete. Saved to: {zip_output_path}")

            # 7. Extract and organize the ZIP
            extract_folder = os.path.join(OUTPUT_DIR, pdf_name)
            os.makedirs(extract_folder, exist_ok=True)

            with zipfile.ZipFile(zip_output_path, "r") as zf:
                zf.extractall(extract_folder)

            print(f"✓ Extracted contents to: {extract_folder}")

            # 8. Read structuredData.json and analyze
            json_path = os.path.join(extract_folder, "structuredData.json")
            with open(json_path, "r") as f:
                data = json.load(f)

            # Show summary
            print("\n" + "=" * 60)
            print("EXTRACTION SUMMARY")
            print("=" * 60)

            elements = data.get("elements", [])
            print(f"\nTotal elements extracted: {len(elements)}")

            # Count element types
            type_counts = {}
            for el in elements:
                el_type = el.get("Type", "Unknown")
                type_counts[el_type] = type_counts.get(el_type, 0) + 1

            print("\nElement breakdown:")
            for el_type, count in sorted(type_counts.items()):
                print(f"  - {el_type}: {count}")

            # 9. Extract table information
            print("\n" + "-" * 60)
            print("TABLES FOUND:")
            print("-" * 60)

            file_paths = data.get("filePaths", [])
            table_files = [fp for fp in file_paths if "/tables/" in fp]

            if table_files:
                for i, table_path in enumerate(table_files, 1):
                    print(f"\n{i}. {os.path.basename(table_path)}")
                    print(f"   Location: {table_path}")

                    # Find corresponding element in JSON for metadata
                    for el in elements:
                        if el.get("Path") == f"/{table_path.split('/')[-1]}":
                            print(f"   Page: {el.get('Page', 'N/A')}")
                            if "Text" in el:
                                preview = el.get("Text", "")[:100]
                                print(f"   Preview: {preview}...")
                            break
            else:
                print("No tables found in extraction.")

            # 10. Extract text sections (balance sheet labels, headings)
            print("\n" + "-" * 60)
            print("TEXT SECTIONS (First 10):")
            print("-" * 60)

            text_elements = [el for el in elements if el.get("Type") in ["Paragraph", "Title", "Heading"]]
            for i, el in enumerate(text_elements[:10], 1):
                text = el.get("Text", "").strip()[:80]
                print(f"{i}. [{el.get('Type')}] {text}")

            print(f"\n✓ Analysis complete! Check '{extract_folder}' folder for:")
            print("   - structuredData.json (full metadata)")
            print("   - tables/ (CSV, XLSX, PNG files)")
            print("   - figures/ (extracted charts/images)")
        except Exception as e:
            print(f"✗ An error occurred: {e}")


if __name__ == "__main__":
    for INPUT_PDF_PATH in os.listdir(INPUT_PDFS_PATH):
        if INPUT_PDF_PATH.lower().endswith(".pdf"):
            print(f"\nProcessing file: {INPUT_PDF_PATH}")
            main(os.path.join(INPUT_PDFS_PATH, INPUT_PDF_PATH))
