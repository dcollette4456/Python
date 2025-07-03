🧾 What This Script Does
This Python script is a utility that parses Nmap scan results in XML format and transforms the data into a clean, structured CSV file. It extracts:

🟢 Only live ('up') hosts

🌐 IP addresses and hostnames

🛠️ Open ports, detected services, and product/version info

🧠 Basic OS detection (if provided by Nmap)

📜 Optional script output (from Nmap NSE scripts)

The end result is a report-friendly CSV that gives visibility into the scanned network—perfect for analysts, pentesters, or ops teams.

🛠️ Enhancements Added
These updates make the script more flexible, safer, and user-friendly:

✅ New Features
Progress indicator using tqdm to show scan parsing progress

Output directory and filename safety checks

Logging instead of print statements for cleaner verbosity control

Automatic CSV naming if none is specified (based on timestamp)

Summary stats after parsing: host count, unique ports, etc.

Better error handling and exit codes for scripting integration

💡 Quality-of-Life Improvements
Better command-line help formatting

Clear warnings for malformed XML or missing tags

Logs skipped hosts/ports for debugging

Extracts multiple script tags per port

CSV is opened in write mode by default to avoid appending clutter
