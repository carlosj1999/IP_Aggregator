# IP Aggregator

IP Aggregator is a powerful Python utility built with Django, designed to streamline the aggregation, formatting, and management of IP addresses and networks. It's ideal for integration into web applications requiring efficient IP address handling.

## Features

- Aggregate IP addresses and ranges into optimal network representations.
- Support for various input formats, including CIDR, IP ranges, and special aliases (A, B, C classes).
- Multiple output formats: CIDR, netmask, IP range, and more.
- Optional tagging with 'why blocked' reasons and ASN codes.
- Built-in input cleaning and validation.
- Efficient network collapsing for optimal aggregation.

## Deployment Guide(Ubuntu)

Follow these steps to deploy the IP Aggregator project on a new Ubuntu server:

### 1. Initial Server Setup

1. Set up a  Ubuntu server.
2. Create a non-root user with sudo privileges.
3. Set up a firewall (UFW).

### 2. Install Required Packages

```bash
sudo apt update
sudo apt install python3-venv python3-dev libpq-dev postgresql postgresql-contrib nginx curl
```

### 3. Create Project Directory and Virtual Environment

```bash
mkdir ~/ip_aggregator
cd ~/ip_aggregator
python3 -m venv env
source env/bin/activate
```

### 4. Install Django and Other Requirements

```bash
pip install django gunicorn psycopg2-binary pillow
```

### 5. Clone the Project from GitHub

```bash
git clone https://github.com/your_username/IP_Aggregator.git .
```

### 6. Configure Django Settings

Edit `~/ip_aggregator/myproject/settings.py`:

```python
ALLOWED_HOSTS = ['your_server_ip_or_domain', 'localhost']

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATICFILES_DIRS = [ os.path.join(BASE_DIR,'static') ]
```

### 7. Set Up Django Project

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```

### 8. Test Gunicorn

```bash
gunicorn --bind 0.0.0.0:8000 myproject.wsgi
```

### 9. Create Gunicorn Systemd Socket and Service Files

Create and edit `/etc/systemd/system/gunicorn.socket`:

```ini
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

Create and edit `/etc/systemd/system/gunicorn.service`:

```ini
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=your_username
Group=www-data
WorkingDirectory=/home/your_username/ip_aggregator
ExecStart=/home/your_username/ip_aggregator/env/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          myproject.wsgi:application

[Install]
WantedBy=multi-user.target
```

### 10. Start and Enable Gunicorn Socket

```bash
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
```

### 11. Configure Nginx

Create and edit `/etc/nginx/sites-available/ip_aggregator`:

```nginx
server {
    listen 80;
    server_name your_server_ip_or_domain;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/your_username/ip_aggregator;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

Enable the Nginx configuration:

```bash
sudo ln -s /etc/nginx/sites-available/ip_aggregator /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

### 12. Configure Firewall

```bash
sudo ufw allow 'Nginx Full'
```

## Usage

Once deployed, you can access the IP Aggregator application through your server's IP address or domain name.

For local development:

```bash
cd ip_aggregator
python manage.py runserver
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License
This version is streamlined for clarity, with consistent formatting and concise instructions. Be sure to replace placeholders with your specific information, and add any additional sections that might be relevant to your project.
