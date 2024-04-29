#!/usr/bin/env python3


import requests

# Configuration
api_token = 'cgWFsKRlzvp7Kz7BIKxTDo_fo5FQToVOGAxxSVtG'
zone_id = '856c63bfe1539773778d91e0a67e1cc3'  # Can be found in the Cloudflare dashboard
record_name = 'sonway.org'
record_type = 'A'  # Typically 'A' for IPv4 or 'AAAA' for IPv6

headers = {
    'Authorization': f'Bearer {api_token}',
    'Content-Type': 'application/json',
}

def get_external_ip():
    response = requests.get('https://api.ipify.org')
    return response.text

def get_dns_record():
    url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records'
    params = {'name': record_name, 'type': record_type}
    response = requests.get(url, headers=headers, params=params)
    return response.json()['result'][0]

def update_dns_record(ip, record_id):
    url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}'
    data = {'type': record_type, 'name': record_name, 'content': ip}
    response = requests.put(url, headers=headers, json=data)
    return response.json()

def main():
    current_ip = get_external_ip()
    dns_record = get_dns_record()
    if dns_record['content'] != current_ip:
        result = update_dns_record(current_ip, dns_record['id'])
        if result['success']:
            print(f'DNS record updated to {current_ip}')
        else:
            print('Failed to update DNS record')

if __name__ == '__main__':
    main()

