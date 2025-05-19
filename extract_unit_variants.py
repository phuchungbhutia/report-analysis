import os
import re
import csv
import fitz  # PyMuPDF
import docx

INPUT_DIR = "input_files"
OUTPUT_CSV = "unit_variants.csv"

def extract_text_docx(filepath):
    doc = docx.Document(filepath)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return "\n".join(full_text)

def extract_text_pdf(filepath):
    doc = fitz.open(filepath)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_unit_name_candidates(text):
    # Heuristic: look in first 20 lines for "Unit:", "Local Body:", "Name:" keys
    candidates = []
    lines = text.splitlines()[:20]
    for line in lines:
        if ':' in line:
            key, val = line.split(':', 1)
            key = key.strip().lower()
            if key in ('unit', 'local body', 'localbody', 'name'):
                candidates.append(val.strip())
    # If no key found, fallback to first non-empty line
    if not candidates:
        for line in text.splitlines():
            if line.strip():
                candidates.append(line.strip())
                break
    return candidates

def main():
    variants_set = set()

    for filename in os.listdir(INPUT_DIR):
        filepath = os.path.join(INPUT_DIR, filename)
        ext = filename.lower().split('.')[-1]

        try:
            if ext == "docx":
                text = extract_text_docx(filepath)
            elif ext == "pdf":
                text = extract_text_pdf(filepath)
            else:
                continue

            candidates = extract_unit_name_candidates(text)
            for c in candidates:
                variants_set.add(c.strip())

        except Exception as e:
            print(f"Error processing {filename}: {e}")

    # Save unique variants to CSV (one column: variant_name)
    with open(OUTPUT_CSV, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["variant_name"])
        for variant in sorted(variants_set):
            writer.writerow([variant])

    print(f"Extracted {len(variants_set)} unique unit name variants.")
    print(f"Saved to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
