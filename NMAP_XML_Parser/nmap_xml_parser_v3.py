#!/usr/bin/env python3

import xml.etree.ElementTree as etree
import os
import csv
import argparse
import logging
from collections import Counter
from time import sleep, strftime
from tqdm import tqdm

# Setup logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def get_xml_root(xml):
    """Parses an xml file and returns the root element."""
    try:
        tree = etree.parse(xml)
    except Exception as error:
        logging.error(f"The XML may not be well-formed. Error: {error}")
        exit(1)
    return tree.getroot()

def get_host_data(root):
    """Extracts live hosts and their open port details from the Nmap XML."""
    host_data = []
    hosts = root.findall('host')
    for host in tqdm(hosts, desc="Parsing hosts", unit="host"):
        if not host.find('status').attrib['state'] == 'up':
            continue

        ip_address = host.find('address').attrib['addr']
        try:
            host_name = host.find('hostnames').find('hostname').attrib['name']
        except (AttributeError, IndexError):
            host_name = ''
        try:
            os_name = host.find('os').find('osmatch').attrib['name']
        except (AttributeError, IndexError):
            os_name = ''

        ports = host.find('ports').findall('port')
        for port in ports:
            if not port.find('state').attrib['state'] == 'open':
                continue

            proto = port.attrib['protocol']
            port_id = port.attrib['portid']
            service_data = port.find('service')
            service = service_data.attrib.get('name', 'unknown') if service_data is not None else 'unknown'
            product = service_data.attrib.get('product', '') if service_data is not None else ''
            servicefp = service_data.attrib.get('servicefp', '') if service_data is not None else ''

            scripts = port.findall('script')
            script_entries = []
            for script in scripts:
                script_entries.append((script.attrib.get('id', ''), script.attrib.get('output', '')))

            if not script_entries:
                script_entries = [('', '')]

            for script_id, script_output in script_entries:
                port_data = [
                    '', ip_address, '', '', '', port_id, service, host_name,
                    os_name, proto, product, servicefp, script_id, script_output
                ]
                host_data.append(port_data)

    return host_data

def parse_to_csv(data, csv_name):
    """Writes parsed data to CSV with headers and sorted IPs."""
    sorted_data = sorted(data, key=lambda x: tuple(map(int, x[1].split('.'))))
    ip_sort_values = {ip: i + 1 for i, (_, ip, *_) in enumerate(sorted_data)}

    os.makedirs(os.path.dirname(csv_name), exist_ok=True) if '/' in csv_name else None
    with open(csv_name, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        headers = [
            'Sort', 'IP', 'Technology', 'Finding', 'Notes',
            'Port', 'Service', 'Host', 'OS', 'Proto', 'Product',
            'Service FP', 'NSE Script ID', 'NSE Script Output'
        ]
        writer.writerow(headers)

        for row in sorted_data:
            row[0] = ip_sort_values[row[1]]
            writer.writerow(row)

    logging.info(f"[+] CSV file written to: {csv_name}")
    print(f"\n🔍 Summary: {len(set(row[1] for row in sorted_data))} hosts | {len(sorted_data)} port entries\n")

def main():
    """Main driver."""
    for filename in args.filename:
        if not os.path.exists(filename):
            logging.error(f"File {filename} not found or inaccessible.")
            continue

        if not args.skip_entity_check:
            with open(filename) as f:
                if '<!entity' in f.read().lower():
                    logging.warning(f"XML entity detected in {filename}, skipping. Use --skip_entity_check to override.")
                    continue

        root = get_xml_root(filename)
        data = get_host_data(root)
        if not data:
            logging.warning("No live hosts found in scan.")
            continue

        csv_name = args.csv or f"scan_output_{strftime('%Y%m%d_%H%M%S')}.csv"
        parse_to_csv(data, csv_name)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="📊 Nmap XML Parser → CSV Report Tool")
    parser.add_argument("-s", "--skip_entity_check", action="store_true", help="Skip the check for XML entities")
    parser.add_argument("-csv", "--csv", nargs='?', const='', help="Output CSV file (default uses timestamp)")
    parser.add_argument("-f", "--filename", nargs='+', help="Path(s) to Nmap XML scan file(s)")
    args = parser.parse_args()

    if not args.filename:
        parser.print_help()
        logging.error("Please specify at least one XML scan file with -f")
        exit(1)

    main()
