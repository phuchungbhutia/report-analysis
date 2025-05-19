import os
import re
import json
import csv
import fitz  # PyMuPDF
import docx
import markdownify

INPUT_DIR = "input_files"
OUTPUT_DIR = "data"
LOCALBODIES_CSV = "localbodies.csv"
MANIFEST_FILE = "files.json"

# --- Load and normalize local body names from CSV ---
def load_localbodies(csv_path):
    mapping = {}
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            # Assuming CSV: variant_name, normalized_name
            if len(row) >= 2:
                variant, normalized = row[0].strip().lower(), row[1].strip()
                mapping[variant] = normalized
    return mapping

# --- Normalize unit name ---
def normalize_unit_name(raw_name, mapping):
    raw_lower = raw_name.strip().lower()
    return mapping.get(raw_lower, raw_name.strip())

# --- Extract text from DOCX ---
def extract_text_docx(filepath):
    doc = docx.Document(filepath)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return "\n".join(full_text)

# --- Extract text from PDF ---
def extract_text_pdf(filepath):
    doc = fitz.open(filepath)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# --- Identify observations count ---
def count_observations(text):
    # Simple heuristic:
    # Count occurrences of headings like "Audit Findings", "Observations", "Paras", "Paragraphs"
    # Assuming headings are followed by some content
    
    # Pattern to match common observation headings (case insensitive)
    pattern = re.compile(r'(audit findings|observations|paras|paragraphs)', re.IGNORECASE)
    
    # Split by lines and count how many lines match the pattern as headings
    count = 0
    lines = text.splitlines()
    for line in lines:
        if pattern.search(line.strip()):
            count += 1
    # If none found, fallback to counting occurrences of "Observation" keyword in text
    if count == 0:
        count = len(re.findall(r'observation', text, re.IGNORECASE))
    return count

# --- Extract audit year ---
def extract_year(text):
    # Look for 4 digit year, e.g. 2019, 2020, 2021 etc.
    years = re.findall(r'20\d{2}', text)
    if years:
        # Return the most common or first year found
        return years[0]
    return "unknown"

# --- Extract unit name ---
def extract_unit_name(text):
    # Heuristic to find unit name - try first few lines for known names or patterns
    # This part is tricky and may need customization
    # For now, look for a line starting with "Unit:", "Local Body:", or "Name:"
    for line in text.splitlines()[:20]:
        if ':' in line:
            key, val = line.split(':', 1)
            key = key.strip().lower()
            if key in ('unit', 'local body', 'localbody', 'name'):
                return val.strip()
    # Fallback: take first non-empty line
    for line in text.splitlines():
        if line.strip():
            return line.strip()
    return "unknown_unit"

# --- Convert plain text to markdown (basic) ---
def text_to_markdown(text):
    # If text is plain text, just return it (or optionally convert some markup)
    # If HTML is present, use markdownify
    # Here, we assume text is plain, return as-is
    # You can enhance this later if needed
    return text

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Load local bodies mapping
    localbody_map = load_localbodies(LOCALBODIES_CSV)

    manifest = []
    
    for filename in os.listdir(INPUT_DIR):
        filepath = os.path.join(INPUT_DIR, filename)
        ext = filename.lower().split('.')[-1]

        print(f"Processing file: {filename}")

        try:
            if ext == "docx":
                text = extract_text_docx(filepath)
            elif ext == "pdf":
                text = extract_text_pdf(filepath)
            else:
                print(f"Skipping unsupported file type: {filename}")
                continue

            # Extract info
            unit_raw = extract_unit_name(text)
            unit_norm = normalize_unit_name(unit_raw, localbody_map)

            audit_year = extract_year(text)
            obs_count = count_observations(text)

            md_content = text_to_markdown(text)

            # Build output filename
            safe_unit = re.sub(r'[^a-zA-Z0-9_-]', '_', unit_norm.lower())
            safe_year = audit_year if audit_year != "unknown" else "unknownyear"
            out_filename = f"{safe_unit}-{safe_year}-{obs_count}.md"
            out_filepath = os.path.join(OUTPUT_DIR, out_filename)

            # Save markdown file
            with open(out_filepath, "w", encoding="utf-8") as f:
                f.write(md_content)

            manifest.append({
                "filename": out_filename,
                "unit_name": unit_norm,
                "audit_year": audit_year,
                "observations_count": obs_count
            })

            print(f"Saved: {out_filename}")

        except Exception as e:
            print(f"Error processing {filename}: {e}")

    # Save manifest JSON
    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"Manifest saved to {MANIFEST_FILE}")

if __name__ == "__main__":
    main()
