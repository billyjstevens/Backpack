#!/usr/bin/env python3

import requests

# Configuration
api_token = '$CF-DNS_EDIT-TOKEN'  # Your Cloudflare API token
zone_id = '$CF-ZONE-ID'  # Your Cloudflare Zone ID (found in the Cloudflare dashboard)
record_name = '@'  # The DNS record name to update
record_type = 'A'  # DNS record type ('A' for IPv4 or 'AAAA' for IPv6)

# Headers for the Cloudflare API requests
headers = {
    'Authorization': f'Bearer {api_token}',
    'Content-Type': 'application/json',
}

def get_external_ip():
    """
    Retrieves the current external IP address.
    
    Returns:
        str: The external IP address.
    """
    response = requests.get('https://api.ipify.org')
    return response.text

def get_dns_record():
    """
    Retrieves the DNS record information from Cloudflare.
    
    Returns:
        dict: The DNS record information.
    """
    url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records'
    params = {'name': record_name, 'type': record_type}
    response = requests.get(url, headers=headers, params=params)
    return response.json()['result'][0]

def update_dns_record(ip, record_id):
    """
    Updates the DNS record on Cloudflare with the new IP address.
    
    Args:
        ip (str): The new IP address.
        record_id (str): The ID of the DNS record to update.
        
    Returns:
        dict: The response from the Cloudflare API.
    """
    url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}'
    data = {'type': record_type, 'name': record_name, 'content': ip}
    response = requests.put(url, headers=headers, json=data)
    return response.json()

def main():
    """
    Main function to update the DNS record if the IP address has changed.
    """
    # Get the current external IP address
    current_ip = get_external_ip()
    
    # Get the existing DNS record from Cloudflare
    dns_record = get_dns_record()
    
    # Check if the current IP is different from the DNS record IP
    if dns_record['content'] != current_ip:
        # Update the DNS record with the new IP address
        result = update_dns_record(current_ip, dns_record['id'])
        
        # Print the result of the update
        if result['success']:
            print(f'DNS record updated to {current_ip}')
        else:
            print('Failed to update DNS record')

# Entry point of the script
if __name__ == '__main__':
    main()
