# IP_Aggregator
IP Aggregator is a robust Python utility designed to simplify the process of aggregating, formatting, and managing IP addresses and networks.  It's built as part of a Django project, making it easy to integrate into web applications.

## Features

- Aggregate IP addresses and ranges into optimal network representations
- Support for various input formats including CIDR, IP ranges, and special aliases (A, B, C classes)
- Multiple output formats: CIDR, netmask, IP range, and more
- Optional tagging with 'why blocked' reasons and ASN codes
- Built-in input cleaning and validation
- Efficient network collapsing for optimal aggregation

## Usage
> [!TIP]
> Just run on the terminal:

```$ cd ip_aggregator```

```$ python manage.py runserver```

The main functionality is provided by the `aggregate_ip_addresses` function in `aggregator/utils.py`. Here's a basic example:

```python
from aggregator.utils import aggregate_ip_addresses

ip_list = """
192.168.1.0/24
10.0.0.0/8
172.16.0.0-172.31.255.255
A
192.168.2.1
"""

result = aggregate_ip_addresses(ip_list, output_format='cidr')
print(result)
