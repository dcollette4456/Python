------------------------parser9.py----------10JUL2025----------------------

## 🔐 Purpose

This script **scans a folder full of `.xlsx` files**, looks for sheets named "Consolidated*", and extracts two types of IOCs:
- **Email senders** (potential phishing sources)
- **URLs** (malicious or suspicious URLs)

It then **validates and refangs** the URLs (i.e. restores obfuscated versions), and **exports the cleaned and verified IOCs to two CSV files.**

---

## 🧠 Key Functional Breakdown

### 🔍 Regex Validation
- `URL_REGEX` checks if a URL has the proper format.
- `EMAIL_REGEX` verifies email addresses.

### 🛠 Refang Logic
- `refang_url()` fixes obfuscated IOCs like:
  - `hxxp` → `http`
  - `[.]` → `.`
  - Removes brackets `[...]` around any character (e.g. `[c]` → `c`)

### 🧹 Extracting IOCs
- For each file:
  - Loads the workbook using `openpyxl`.
  - Ignores sheets unless they start with `"Consolidated"`.
  - Extracts non-null **Email_Sender** and **FE_URL** values.
  - Filters and stores only those that pass validation.

### 📁 Folder Parsing
- Walks through a folder recursively.
- If a file ends in `.xlsx`, it’s processed.
- Final results saved as:
  - `combined_IOC_SENDER_EMAIL.csv`
  - `combined_IOC_URLs.csv`

### 🚀 Execution
- The script expects to be run like:
  ```bash
  python3 xlsx_combiner.py ./path/to/xlsx/folder
  ```
- If the user doesn't pass the folder path, it prints usage guidance and exits.



-------------parser4.py -------------------


🧪 IOC Extraction Tool for Threat Intel Analysts Version 4 (changes listed below)

This script automates the extraction of email senders and refanged URLs from .xlsx files used in threat intelligence reporting. It’s tailored for analysts working with consolidated IOC collections, especially those formatted with columns like Email_Sender and FE_URL.

✅ Key Features 📥 Parses multiple Excel files across subdirectories

🧠 Refangs defanged URLs (e.g., hxxp[:]//malicious[.]site)

🌐 Validates well-formed URLs using regex

📧 Extracts and deduplicates sender addresses

📊 Outputs results as clean CSVs per file (e.g., parsed_.csv)

🔄 How It Works Walks through a target folder and locates .xlsx files

For sheets that begin with "consolidated":

Extracts unique Email_Sender values

Refangs and validates URLs from FE_URL

Aligns extracted values side by side and saves as CSV

🛠 Usage bash python3 xlsx_per_file_parser.py <folder_path> Example: python3 xlsx_per_file_parser.py ./ioc_uploads/

Each valid file will produce a corresponding CSV with structured indicators.

🚧 Requirements Python 3.7+

pandas

openpyxl
