#!/usr/bin/env python3
"""
Combine chunked company report folders into a single report folder.

Fixed version: Properly updates JSON element Path references to new table files.
"""
import os
import json
import shutil
from collections import defaultdict
import re


DATA_DIR = os.path.dirname(__file__)  # data/ folder


def find_chunk_folders(data_dir):
    """Return a mapping base_name -> list of chunk folder paths (sorted)."""
    entries = os.listdir(data_dir)
    chunks = defaultdict(list)

    for name in entries:
        path = os.path.join(data_dir, name)
        if not os.path.isdir(path):
            continue
        if "_chunk_" in name:
            base = name.split("_chunk_")[0]
            chunks[base].append(path)
    
    for base, paths in chunks.items():
        def key(p):
            try:
                idx = int(os.path.basename(p).split("_chunk_")[-1])
                return idx
            except Exception:
                return 0
        chunks[base] = sorted(paths, key=key)
    return chunks


def load_structured(path):
    p = os.path.join(path, "structuredData.json")
    if not os.path.exists(p):
        return None
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def get_table_files(chunk_path):
    """Find all table files (CSV, XLSX, PNG) in chunk"""
    tables_dir = os.path.join(chunk_path, "tables")
    if not os.path.exists(tables_dir):
        return []
    
    table_files = []
    for ext in ["*.csv", "*.xlsx", "*.png"]:
        table_files.extend(glob.glob(os.path.join(tables_dir, ext)))
    return table_files


def combine_company(base_name, chunk_paths):
    print(f"\n🔄 Combining {base_name}: {len(chunk_paths)} chunks")
    
    combined_dir = os.path.join(DATA_DIR, base_name)
    combined_tables_dir = os.path.join(combined_dir, "tables")
    ensure_dir(combined_tables_dir)
    
    combined = None
    table_mapping = {}  # old_path -> new_path
    next_table_index = 0
    
    # Step 1: Process all chunks
    for i, chunk_path in enumerate(chunk_paths):
        print(f"  Processing chunk {i+1}/{len(chunk_paths)}: {os.path.basename(chunk_path)}")
        sd = load_structured(chunk_path)
        if sd is None:
            print(f"    ⚠️  No structuredData.json in {chunk_path}")
            continue
            
        if combined is None:
            # Initialize with first chunk's metadata
            combined = dict(sd)
            combined["elements"] = []
            combined["filePaths"] = []
        
        # Step 2: Copy ALL table files (CSV, XLSX, PNG)
        tables_dir = os.path.join(chunk_path, "tables")
        if os.path.exists(tables_dir):
            for filename in os.listdir(tables_dir):
                if filename.lower().endswith(('.csv', '.xlsx', '.png')):
                    src_table = os.path.join(tables_dir, filename)
                    # Create unique name: company_table_XXXX_originalname.ext
                    tgt_name = f"{base_name}_table_{next_table_index:04d}_{filename}"
                    tgt_path = os.path.join(combined_tables_dir, tgt_name)
                    shutil.copy2(src_table, tgt_path)
                    
                    # Map old path → new path
                    old_relative_path = f"tables/{filename}"
                    new_relative_path = f"tables/{tgt_name}"
                    table_mapping[old_relative_path] = new_relative_path
                    
                    print(f"    📊 Copied table: {filename} → {tgt_name}")
                    next_table_index += 1
        
        # Step 3: Merge elements (we'll fix paths later)
        elements = sd.get("elements", [])
        combined["elements"].extend(elements)
    
    if combined is None:
        print(f"  ❌ No data found for {base_name}")
        return
    
    # Step 4: CRITICAL FIX - Update all Path references in elements
    print(f"\n  🔧 Fixing {len(combined['elements'])} element paths...")
    fixed_elements = 0
    for element in combined["elements"]:
        if "Path" in element:
            old_path = element["Path"]
            # Fix table references
            for old_table_path, new_table_path in table_mapping.items():
                if old_path == old_table_path or old_table_path in old_path:
                    element["Path"] = new_table_path
                    fixed_elements += 1
                    break
    
    print(f"    ✓ Fixed {fixed_elements} table path references")
    
    # Step 5: Update filePaths array
    combined["filePaths"] = list(table_mapping.values())
    
    # Step 6: Save combined JSON
    out_path = os.path.join(combined_dir, "structuredData.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(combined, f, ensure_ascii=False, indent=2)
    
    print(f"  ✅ Combined: {len(combined['elements'])} elements, {len(table_mapping)} tables")
    print(f"  📁 Output: {combined_dir}/")
    print(f"  📊 Tables: {combined_tables_dir}/ ({next_table_index} total)")


if __name__ == '__main__':
    import glob  # Add this import for get_table_files
    
    chunks = find_chunk_folders(DATA_DIR)
    if not chunks:
        print("❌ No chunk folders found (look for '_chunk_' folders)")
        print("Example: LARSEN_&_TOUBRO_chunk_000/, LARSEN_&_TOUBRO_chunk_001/")
        raise SystemExit(1)
    
    print(f"Found {len(chunks)} companies with chunks:")
    for base, paths in chunks.items():
        print(f"  - {base}: {len(paths)} chunks")
    
    total_tables = 0
    for base, paths in chunks.items():
        combine_company(base, paths)
        total_tables += len([f for p in paths for f in get_table_files(p)])
    
    print(f"\n🎉 Done! Combined {len(chunks)} companies, {total_tables} total tables.")
