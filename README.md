# Audit Report Data Analysis Workflow

![GitHub repo size](https://img.shields.io/github/repo-size/phuchungbhutia/audit-report-viewer)
![GitHub stars](https://img.shields.io/github/stars/phuchungbhutia/audit-report-viewer?style=social)
![GitHub forks](https://img.shields.io/github/forks/phuchungbhutia/audit-report-viewer?style=social)

---

## Project Description

This project enables easy upload, conversion, and interactive viewing of audit reports submitted in DOCX or PDF formats.

**Key features:**

- Automated conversion of DOCX/PDF audit reports to Markdown files via a GitHub Actions workflow using Python.
- Extraction and counting of observations within reports.
- Standardization of unit names using a reference CSV.
- Auto-renaming of files with meaningful metadata.
- JSON manifest (`files.json`) generation to track all processed reports.
- Interactive frontend hosted on GitHub Pages with:
  - Search and filter functionality
  - Sorting by audit year or unit name
  - Dynamic Markdown rendering for rich, readable report previews
  - Responsive and clean UI design

---

## GitHub Statistics

- Repo size: ![repo size](https://img.shields.io/github/repo-size/phuchungbhutia/audit-report-viewer)
- Stars: ![stars](https://img.shields.io/github/stars/phuchungbhutia/audit-report-viewer?style=social)
- Forks: ![forks](https://img.shields.io/github/forks/phuchungbhutia/audit-report-viewer?style=social)

---

## Folder Structure

```

/

├── .github/

│   └── workflows/

│       └── convert-and-generate-files.yml  # GitHub Actions workflow

├── css/

│   └── style.css                           # CSS styling

├── data/

│   └── *.md                               # Converted Markdown audit reports

├── input_files/

│   └── *.docx, *.pdf                      # Original upload files

├── js/

│   └── app.js                            # Frontend JS

├── convert_files.py                      # Python conversion script

├── files.json                           # Manifest JSON with metadata

├── index.html                          # Frontend HTML

├── LICENSE

├── README.md

├── CONTRIBUTING.md

├── ISSUE_TEMPLATE.md

└── PULL_REQUEST_TEMPLATE.md

```

---

## How to Use

### Upload & Convert Reports

1. Add DOCX or PDF audit report files to the `input_files/` folder.
2. Push changes to GitHub. This triggers the GitHub Actions workflow:
   - Converts files to Markdown.
   - Extracts metadata and counts observations.
   - Saves Markdown files under `data/`.
   - Updates `files.json` manifest.
3. After workflow completion, the frontend on GitHub Pages will update automatically.

### Viewing Reports

- Open the GitHub Pages URL:`https://phuchungbhutia.github.io/audit-report-viewer/`
- Use the search box to filter reports by unit name or audit year.
- Sort reports by year or unit using the dropdown.
- Click any report to view the full Markdown-rendered content on the right.

---

## GitHub Pages Setup

1. Navigate to **Settings** → **Pages** in your GitHub repository.
2. Select the branch (`main` or `master`) and root folder `/` as the source.
3. Save and wait a few minutes for the site to publish.
4. Your site URL will look like:
   `https://phuchungbhutia.github.io/audit-report-viewer/`

---

## Development & Contribution

### Running Locally

- Install Python dependencies:

  ```bash
  pip install python-docx pymupdf markdownify
  ```

```

* Run the conversion script manually:
  ```bash
  python convert_files.py
```

* Use a simple HTTP server to serve the frontend locally for testing:
  ```bash
  python -m http.server 8000
  ```
* Open `http://localhost:8000` in your browser.

### Contribution Guidelines

* Fork the repo and create a new branch for your feature or fix.
* Ensure any Python or JS code you add is well-commented.
* Update/add tests if applicable.
* Open a pull request with a clear description of your changes.

### Issue Reporting

* Use the issue template to report bugs or request features.
* Provide detailed steps to reproduce issues.

---

## License

This project is licensed under the MIT License. See [LICENSE](https://chatgpt.com/c/LICENSE) for details.

---

## Contact

Created and maintained by [PB](https://github.com/phuchungbhutia).

Feel free to open issues or PRs!
