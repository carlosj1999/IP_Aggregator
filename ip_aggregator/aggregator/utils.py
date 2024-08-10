# aggregator/utils.py
"""
from ipaddress import ip_network, ip_address, summarize_address_range
import ipaddress

def aggregate_ip_addresses(ip_addresses, output_format, why_blocked=None, asn_code=None):
    # Split the input into lines and remove any empty lines
    ip_list = [line.strip() for line in ip_addresses.split('\n') if line.strip()]
    
    # Convert IP addresses and ranges to networks
    networks = []
    for ip in ip_list:
        try:
            if '-' in ip:
                start, end = ip.split('-')
                networks.extend(summarize_address_range(ip_address(start.strip()), ip_address(end.strip())))
            elif '/' in ip:
                networks.append(ip_network(ip, strict=False))
            else:
                networks.append(ip_network(ip + '/32', strict=False))
        except ValueError:
            # Skip invalid IP addresses
            continue
    
    # Sort networks to ensure consistent output
    networks.sort(key=lambda x: x.network_address)
    
    # Format the output based on the selected format
    if output_format == 'cidr':
        result = [str(net) for net in networks]
    elif output_format == 'mask':
        result = [f"{net.network_address}/{net.netmask}" for net in networks]
    elif output_format == 'range':
        result = [f"{net.network_address}-{net.broadcast_address}" for net in networks]
    elif output_format == 'b-n':
        result = [f"{net.network_address}-{net.broadcast_address}" for net in networks]
    elif output_format == 'hta':
        result = [f"deny from {net.network_address}/{net.netmask}" for net in networks]
    elif output_format == 'zbb':
        result = [f"{net.network_address}/{net.prefixlen}" for net in networks]
    
    # Add why_blocked and asn_code if provided
    if why_blocked:
        result = [f"{line} # {why_blocked}" for line in result]
    if asn_code:
        result = [f"{line} # AS{asn_code}" for line in result]
    
    return '\n'.join(result)"""
    
    

from ipaddress import ip_network, ip_address, summarize_address_range, collapse_addresses
import re

# Regex Definitions
IP4_OCTET = r"(?:[\d]{1,3})"
IP4_DOT = r"\."
IP4_MASK = r"(?:\/[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}|\/3[0-2]|\/[1-2][\d]|\/[\d])?"
IP4_ADDRESS = IP4_OCTET + IP4_DOT + IP4_OCTET + IP4_DOT + IP4_OCTET + IP4_DOT + IP4_OCTET

IP4_NETWORK = re.compile(IP4_ADDRESS + IP4_MASK + r"(?=[\D])", re.ASCII)
IP4_RANGE = re.compile(r"(" + IP4_ADDRESS + r")[-]?", re.ASCII)

# IP Network Constants
IP4_ALIASES = {
    "A": [ip_network("10.0.0.0/8")],
    "B": [ip_network("172.16.0.0/12")],
    "C": [ip_network("192.168.0.0/16")],
}

def clean_input(ip_addresses):
    # Replace commas with newlines
    cleaned = ip_addresses.replace(',', '\n')
    # Split on whitespace and join with newlines
    cleaned = '\n'.join(cleaned.split())
    # Remove any empty lines
    cleaned = '\n'.join(line for line in cleaned.split('\n') if line.strip())
    return cleaned



def aggregate_ip_addresses(ip_addresses, output_format='cidr', why_blocked=None, asn_code=None):
    # Clean the input data
    cleaned_ip_addresses = clean_input(ip_addresses)
    
    # Split the cleaned input into lines
    ip_list = cleaned_ip_addresses.split('\n')
    
    # Split the input into lines and remove any empty lines
    #ip_list = [line.strip() for line in ip_addresses.split('\n') if line.strip()]
    
    # Convert IP addresses and ranges to networks
    networks = []
    for ip in ip_list:
        try:
            if ip in IP4_ALIASES:
                networks.extend(IP4_ALIASES[ip])
            elif '-' in ip:
                range_match = IP4_RANGE.findall(ip)
                if len(range_match) == 2:
                    start, end = range_match
                    networks.extend(summarize_address_range(ip_address(start), ip_address(end)))
            elif IP4_NETWORK.match(ip):
                networks.append(ip_network(ip, strict=False))
            else:
                networks.append(ip_network(ip + '/32', strict=False))
        except ValueError:
            # Skip invalid IP addresses
            print(f"Warning: Invalid IP address or range: {ip}")
            continue

    # Aggregate networks
    aggregated_networks = list(collapse_addresses(networks))

    # Sort networks to ensure consistent output
    aggregated_networks.sort(key=lambda x: x.network_address)

    # Format the output based on the selected format
    if output_format == 'cidr':
        result = [str(net) for net in aggregated_networks]
    elif output_format == 'mask':
        result = [f"{net.network_address}/{net.netmask}" for net in aggregated_networks]
    elif output_format == 'range':
        result = [f"{net.network_address}-{net.broadcast_address}" for net in aggregated_networks]
    elif output_format == 'b-n':
        result = [f"{net.network_address}-{net.broadcast_address}" for net in aggregated_networks]
    elif output_format == 'hta':
        result = [f"deny from {net.network_address}/{net.netmask}" for net in aggregated_networks]
    elif output_format == 'zbb':
        result = [f"{net.network_address}/{net.prefixlen}" for net in aggregated_networks]
    else:
        raise ValueError(f"Unsupported output format: {output_format}")

    # Add why_blocked and asn_code if provided
    if why_blocked:
        result = [f"{line} # {why_blocked}" for line in result]
    if asn_code:
        result = [f"{line} # AS{asn_code}" for line in result]

    return '\n'.join(result)

# Example usage
if __name__ == "__main__":
    ip_list = """
    192.168.1.0/24
    10.0.0.0/8
    172.16.0.0-172.31.255.255
    A
    192.168.2.1
    """
    print(aggregate_ip_addresses(ip_list, output_format='cidr'))
    
