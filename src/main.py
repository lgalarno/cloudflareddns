from datetime import datetime
import ipaddress
import requests
from cloudflare import Cloudflare
from pathlib import Path

from dotenv import dotenv_values


BASE_DIR = Path(__file__).resolve().parent
config = dotenv_values(BASE_DIR / '.env')
API_TOKEN = config.get('API_TOKEN')
ZONE_ID = config.get('ZONE_ID')
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
    #print(r)
    if r.success:
        return r.result
    else:
        return None


if __name__ == "__main__":
    logging = int(config["LOGGING"])
    current_ip = get_public_ip()
    now = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    logs = [now,]
    if current_ip is not None:
        logs.append(f"Current IP: {current_ip}")
        client = Cloudflare(api_token=API_TOKEN)
        dns_records = get_dns_records(client, ZONE_ID)
        if dns_records is not None:  # Check if records exist
            for record in dns_records:  # Loop through each record
                if validate_ip(record.content) and record.content != current_ip:  # Check if the record IP is different from the current IP
                    if update_dns_record(client=client, record=record, new_ip=current_ip):
                        logs.append(f"{record.name} was updated from {record.content} to {current_ip}")
                    else:
                        logs.append(f"Failed to update {record.name} IP address.")
        else:
            logs.append("No DNS records found for the specified zone.")
    else:
        logs.append("Unable to retrieve public IP address.")
    if logging > 0:
        logs.append("-----")
        LOG_FILE = config.get('LOG_FILE')
        if LOG_FILE:
            LOG_FILE = Path(LOG_FILE)
        else:
            LOG_FILE = BASE_DIR / 'logs.txt'
        if ((len(logs) > 3) and (logging == 2)) or (logging == 1):
            # sauver log si logging == 2 et update OU erreur (len(logs) > 3), ou si always logging (logging == 1)
            with open(LOG_FILE, 'a') as log_file:
                for log in logs:
                    log_file.write(f"{log}\n")
