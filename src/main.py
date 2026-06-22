import argparse
import ipaddress
import os
import requests
import sys
from cloudflare import Cloudflare
from datetime import datetime

from dotenv import load_dotenv
# from dotenv import dotenv_values
from pathlib import Path


PUBLIC_IP_SITES = ["http://checkip.amazonaws.com","https://ident.me", "https://api.ipify.org" ]


def get_public_ip():
    for site in PUBLIC_IP_SITES:
        r = requests.get(site)
        if r.status_code == 200:
            ip = r.text.strip()
            if validate_ip(ip):
                return ip
    return None


def validate_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def update_dns_record(client, record, new_ip):
    try:
        client.dns.records.update(
            dns_record_id=record.id,
            zone_id=ZONE_ID,
            name=record.name,
            content=new_ip,
            ttl=record.ttl,
            type=record.type,
            proxied=record.proxied
        )
        success = True
    except Exception as e:
        print(f"Error updating DNS record: {e}")
        success = False
    return success   


def get_dns_records(client, zone_id):
    r = client.dns.records.list(
        zone_id=zone_id
    )
    if r.success:
        return r.result
    else:
        return None


if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent
    load_dotenv()
    # config = dotenv_values(BASE_DIR / '.env')

    # Argument parsing
    # Validate that API_TOKEN and ZONE_ID are provided either via command-line arguments or environment variables
    # Values from command-line arguments take precedence over environment variables
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--token",
                    required=False,
                    type=str,
                    help="Cloudflare API TOKEN")
    parser.add_argument("-z", "--zone",
                    required=False,
                    type=str,
                    help="Cloudflare ZONE ID",
                    )
    parser.add_argument("-l", "--logging",
                    required=False,
                    help="logging level",
                    type=int,
                    choices=[0,1,2]
                    )    
    parser.add_argument("-f", "--file",
                    required=False,
                    help="log file path",
                    type=str
                    )    
    args = parser.parse_args()
    if args.token:
        API_TOKEN = args.token
    else:
        API_TOKEN = os.getenv("API_TOKEN")  # config.get('API_TOKEN')

    if args.zone:
        ZONE_ID = args.zone
    else:
        ZONE_ID = os.getenv("ZONE_ID")  # config.get('ZONE_ID')

    if not API_TOKEN or not ZONE_ID:
        sys.exit("Error: API_TOKEN and ZONE_ID must be provided either as command-line arguments or in the .env file.")

    if args.logging:
        LOGGING = args.logging
    else:
        LOGGING = os.getenv("LOGGING")  # int(config["LOGGING"])

    if args.file:
        LOG_FILE = args.file
    else:
        LOG_FILE = os.getenv("LOG_FILE")  # config.get('LOG_FILE')
    try:
        LOGGING = int(LOGGING)
    except ValueError:
        print("Invalid LOGGING value. Defaulting to 0 (no logging).")
        LOGGING = 0
    now = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    print(f"{now} running...")
    current_ip = get_public_ip()
    logs = [now,]
    if current_ip is not None:
        logs.append(f"Current IP: {current_ip}")
        print(f"Current IP: {current_ip}")
        client = Cloudflare(api_token=API_TOKEN)
        dns_records = get_dns_records(client, ZONE_ID)
        if dns_records is not None:  # Check if records exist
            for record in dns_records:  # Loop through each record
                if validate_ip(record.content) and record.content != current_ip:  # Check if the record IP is different from the current IP
                    if update_dns_record(client=client, record=record, new_ip=current_ip):
                        t=f"{record.name} was updated from {record.content} to {current_ip}"
                        print(t)
                        logs.append(t)
                    else:
                        t = f"Failed to update {record.name} IP address."
                        print(t)
                        logs.append(t)
        else:
            t = "No DNS records found for the specified zone."
            print(t)
            logs.append("No DNS records found for the specified zone.")
    else:
        t = "Unable to retrieve public IP address."
        print(t)
        logs.append(t)
    if LOGGING > 0:
        logs.append("-----")
        if LOG_FILE:
            LOG_FILE = Path(LOG_FILE)
        else:
            LOG_FILE = BASE_DIR / 'logs.txt'
        if ((len(logs) > 3) and (LOGGING == 2)) or (LOGGING == 1):
            # sauver log si logging == 2 et update OU erreur (len(logs) > 3), ou si always logging (logging == 1)
            try:
                print(f"Writing logs to {LOG_FILE}")
                with open(LOG_FILE, 'a') as log_file:
                    for log in logs:
                        log_file.write(f"{log}\n")
            except (PermissionError, OSError):
                print("Error writing to log file. Please check the file path and permissions.")
