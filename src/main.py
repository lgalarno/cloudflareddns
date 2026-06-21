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


def main():
    print("Hello from cloudflareddns!")

def get_ip():
    r = requests.get("http://checkip.amazonaws.com")
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
    current_ip = get_ip()
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Current IP: {current_ip}")
    client = Cloudflare(api_token=API_TOKEN)
    dns_records = get_dns_records(client, ZONE_ID)
    if dns_records is not None:  # Check if records exist
        for record in dns_records:  # Loop through each record
            if validate_ip(record.content) and record.content != current_ip:  # Check if the record IP is different from the current IP
                if update_dns_record(client=client, record=record, new_ip=current_ip):
                    print(f"{record.name} was updated from {record.content} to {current_ip}")
                else:
                    print(f"Failed to update {record.name} IP address.")
    else:
        print("No DNS records found for the specified zone.")
        