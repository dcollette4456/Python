import pandas as pd
import os
import re
import sys

# ✅ Validation regex
URL_REGEX = re.compile(r"^(https?://)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/[^\s]*)?$")
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

def refang_url(url):
    if not isinstance(url, str):
        return None
    url = url.strip()
    url = url.replace("hxxp", "http")
    url = url.replace("[.]", ".")
    url = url.replace("[:]", ":")
    url = url.replace(" ", "")
    url = re.sub(r"\[(.)\]", r"\1", url)
    if not url.lower().startswith(("http://", "https://")):
        url = "http://" + url
    return url

def is_valid_url(url):
    if not isinstance(url, str):
        return False
    return bool(URL_REGEX.match(url.strip()))

def is_valid_email(email):
    if not isinstance(email, str):
        return False
    return bool(EMAIL_REGEX.match(email.strip()))

# 🔍 Collect everything here
combined_emails = []
combined_urls = []

def extract_independent(file_path):
    print(f"🔍 Parsing: {file_path}")
    try:
        excel = pd.read_excel(file_path, sheet_name=None, engine='openpyxl')
        for sheet_name, sheet in excel.items():
            if not sheet_name.lower().startswith("consolidated"):
                continue
            if "Email_Sender" in sheet.columns and "FE_URL" in sheet.columns:
                raw_emails = sheet["Email_Sender"].dropna().unique()
                for email in raw_emails:
                    email = email.strip()
                    if is_valid_email(email):
                        combined_emails.append({
                            "Tipper": os.path.basename(file_path),
                            "IOC_SENDER_EMAIL": email
                        })

                raw_urls = sheet["FE_URL"].dropna().unique()
                for url in raw_urls:
                    refanged = refang_url(url)
                    if is_valid_url(refanged):
                        combined_urls.append({
                            "Tipper": os.path.basename(file_path),
                            "IOC_URLs": refanged
                        })
    except Exception as e:
        print(f"❌ Failed to parse {file_path}: {e}")

def parse_folder(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".xlsx"):
                full_path = os.path.join(root, file)
                extract_independent(full_path)

    if combined_emails:
        df_emails = pd.DataFrame(combined_emails)
        df_emails.to_csv(os.path.join(folder_path, "combined_IOC_SENDER_EMAIL.csv"), index=False)
        print(f"✅ Emails saved: combined_IOC_SENDER_EMAIL.csv | 📧 {len(combined_emails)}")

    if combined_urls:
        df_urls = pd.DataFrame(combined_urls)
        df_urls.to_csv(os.path.join(folder_path, "combined_IOC_URLs.csv"), index=False)
        print(f"✅ URLs saved: combined_IOC_URLs.csv | 🌐 {len(combined_urls)}")

# 🚀 Run it
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 xlsx_combiner.py <folder_path>")
        sys.exit(1)

    target = sys.argv[1]
    if not os.path.isdir(target):
        print("❌ That’s not a folder.")
        sys.exit(1)

    parse_folder(target)
