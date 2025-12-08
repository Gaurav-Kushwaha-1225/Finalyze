#!/usr/bin/env python3
"""
Combine chunked company report folders into a single report folder.

Behavior:
- Detect folders with names like "Company_chunk_000", "Company_chunk_001", ...
- For each company base name, merge their `structuredData.json` files:
  - Concatenate `elements` arrays
  - Concatenate `filePaths` arrays, updating paths to point to new `tables/` filenames
  - Preserve other top-level fields from the first chunk
- Copy table files from chunk folders into the combined `Company/ tables/` folder and rename them to avoid collisions.
- Output the merged `structuredData.json` into the combined folder.

Usage:
    python3 combine_chunks.py

"""
import os
import json
import shutil
from collections import defaultdict

DATA_DIR = os.path.dirname(__file__)  # data/ folder


def find_chunk_folders(data_dir):
    """Return a mapping base_name -> list of chunk folder paths (sorted)."""
    entries = os.listdir(data_dir)
    chunks = defaultdict(list)

    for name in entries:
        path = os.path.join(data_dir, name)
        if not os.path.isdir(path):
            continue
        # look for the pattern _chunk_
        if "_chunk_" in name:
            base = name.split("_chunk_")[0]
            chunks[base].append(path)
    # sort chunk paths by chunk index if possible
    for base, paths in chunks.items():
        def key(p):
            # try to parse trailing chunk number
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


def combine_company(base_name, chunk_paths):
    print(f"\nCombining {base_name}: {len(chunk_paths)} chunks")
    combined_dir = os.path.join(DATA_DIR, base_name)
    combined_tables_dir = os.path.join(combined_dir, "tables")
    ensure_dir(combined_tables_dir)

    combined = None
    next_table_index = 0
    new_filepaths = []

    for chunk_path in chunk_paths:
        sd = load_structured(chunk_path)
        if sd is None:
            print(f"  - Warning: no structuredData.json in {chunk_path}")
            continue
        if combined is None:
            # start with a shallow copy of the first structuredData
            combined = dict(sd)
            # we'll rebuild elements and filePaths
            combined["elements"] = []
            combined["filePaths"] = []
        # merge elements
        elements = sd.get("elements", [])
        # If elements contain references to file paths, their Path values may need updating later.
        combined["elements"].extend(elements)

        # merge filePaths and copy table files
        fps = sd.get("filePaths", [])
        for fp in fps:
            # only handle table files (paths that include /tables/)
            if "/tables/" in fp:
                filename = os.path.basename(fp)
                src_table = os.path.join(chunk_path, "tables", filename)
                if not os.path.exists(src_table):
                    # sometimes tables might be nested differently; try basename in any tables folder
                    found = None
                    for root, _, files in os.walk(chunk_path):
                        if "tables" in root and filename in files:
                            found = os.path.join(root, filename)
                            break
                    if not found:
                        print(f"  - Warning: table file {filename} not found in {chunk_path}")
                        continue
                    src_table = found
                # create a unique name for target to avoid collisions
                tgt_name = f"{base_name}_table_{next_table_index:04d}_{filename}"
                tgt_path = os.path.join(combined_tables_dir, tgt_name)
                shutil.copy2(src_table, tgt_path)
                # update file path to point to the combined tables folder
                new_fp = os.path.join("tables", tgt_name)
                combined["filePaths"].append(new_fp)
                new_filepaths.append(new_fp)
                next_table_index += 1
            else:
                # keep other filePaths (figures etc.) but try to copy if present
                src = os.path.join(chunk_path, os.path.basename(fp))
                if os.path.exists(src):
                    tgt_name = f"{base_name}_{os.path.basename(fp)}"
                    tgt_path = os.path.join(combined_dir, tgt_name)
                    shutil.copy2(src, tgt_path)
                    combined["filePaths"].append(tgt_name)
                else:
                    # keep as-is
                    combined["filePaths"].append(fp)

    if combined is None:
        print(f"  - No structured data found for {base_name}, skipping")
        return

    # Optionally deduplicate elements by some key; for now keep order
    # Write combined structuredData.json
    out_path = os.path.join(combined_dir, "structuredData.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(combined, f, ensure_ascii=False, indent=2)

    print(f"  ✓ Wrote combined structuredData.json with {len(combined.get('elements', []))} elements and {len(combined.get('filePaths', []))} filePaths")
    print(f"  ✓ Tables copied: {len(new_filepaths)} -> {combined_tables_dir}")


if __name__ == '__main__':
    chunks = find_chunk_folders(DATA_DIR)
    if not chunks:
        print("No chunk folders found in data/ (look for folders with '_chunk_')")
        raise SystemExit(0)

    for base, paths in chunks.items():
        combine_company(base, paths)

    print("\nDone.")
