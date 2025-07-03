🧪 IOC Extraction Tool for Threat Intel Analysts Version 1-4 (changes listed below)

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
