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

1. Set up an Ubuntu server.
2. Once the server is deployed, you’ll need to login via SSH:
    1. Open a terminal on your local machine.
    2. Login using the IP address of the server:
    ```bash
    ssh username@your_server_ip
    ```
    •  If you’re using an SSH key:
    ```bash
    ssh -i /path/to/your/private_key username@your_server_ip
    ```
    •  If it’s your first login and no SSH key is set up, you may need the password you         provided during server creation.

3. Create a New User with Sudo Privileges:
   After logging in as root or an existing user, it’s recommended to create a new user with sudo privileges for security reasons.
   1. Add new user:
     ```bash
     adduser new_username
     ```
     Follow the prompts to set the user password and information.
   
   2. Grant the new user sudo privileges:
      ```bash
      usermod -aG sudo new_username
      ```
   3. Switch to the new user:
      ```bash
      su - new_username
      ```

### 2. Install Required Packages

```bash
apt update
apt install python3-venv python3-dev nginx curl pip
```

### 3. Create  Virtual Environment

```bash
python3 -m venv env
source env/bin/activate
```

### 4. Install Django and Other Requirements

```bash
pip install django gunicorn pillow
```

### 5. Clone the Project from GitHub

```bash
git clone https://github.com/carlosj1999/IP_Aggregator.git
```

### 6. Configure Django Settings

Replace 'your_server_ip_or_domain' with your actual server IP or domain
``` bash
sed -i "s/^ALLOWED_HOSTS = .*/ALLOWED_HOSTS = ['your_server_ip_or_domain', 'localhost']/" /your_username/IP_Agregator/ip_aggregator/settings.py
```

```python
ALLOWED_HOSTS = ['your_server_ip_or_domain', 'localhost']
```

### 7. Set Up Django Project

```bash
python manage.py collectstatic
```

### 8. Test Gunicorn

```bash
gunicorn --bind 0.0.0.0:8000 ip_aggregator.wsgi
```
If everything is correct:
```bash
deactivate
```

### 9. Create Gunicorn Systemd Socket and Service Files

Create and edit `/etc/systemd/system/gunicorn.socket`:

```bash
cat <<EOF | sudo tee /etc/systemd/system/gunicorn.socket
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
EOF
```

Create and edit `/etc/systemd/system/gunicorn.service`:

```bash
cat <<EOF | sudo tee /etc/systemd/system/gunicorn.service
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=your_username
Group=www-data
WorkingDirectory=/your_username/IP_Agregator/ip_aggregator
ExecStart=/your_username/env/bin/gunicorn \\
          --access-logfile - \\
          --workers 3 \\
          --bind unix:/run/gunicorn.sock \\
          ip_aggregator.wsgi:application

[Install]
WantedBy=multi-user.target
EOF
```

Notes:
1. Replace your_username with the actual username you’re using on the server.
2. Make sure the paths in WorkingDirectory and ExecStart are correct according to your setup.

### 10. Start and Enable Gunicorn Socket

```bash
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
```
Check the status of the process to find out whether it was able to start:
```bash
systemctl status gunicorn.socket
```
### 10.1. Testing Socket Activation
Currently, if you’ve only started the gunicorn.socket unit, the gunicorn.service will not be active yet since the socket has not yet received any connections. You can check this by typing:
```bash
systemctl status gunicorn
```
To test the socket activation mechanism, you can send a connection to the socket through curl by typing:
```bash
curl --unix-socket /run/gunicorn.sock localhost
```
You should receive the HTML output from your application in the terminal. This indicates that Gunicorn was started and was able to serve your Django application. You can verify that the Gunicorn service is running by typing:
```bash
systemctl status gunicorn
```

### 11. Configure Nginx

Create and edit `/etc/nginx/sites-available/ip_aggregator`:

```bash
cat <<EOF | sudo tee /etc/nginx/sites-available/ip_aggregator
server {
    listen 80;
    server_name your_server_ip_or_domain;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /your_username/IP_Aggregator/ip_aggregator;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
EOF
```

Notes:
1. Make sure the paths in location /static/ and server_name are correct according to your setup.

Enable the Nginx configuration:
```bash
ln -s /etc/nginx/sites-available/ip_aggregator /etc/nginx/sites-enabled
```
Test your Nginx configuration for syntax errors by typing:
```bash
nginx -t
```
```bash
systemctl restart nginx
```
Finally, you need to open up your firewall to normal traffic on port 80
```bash
ufw allow 'Nginx Full'
```

## Troubleshooting
For additional troubleshooting, the logs can help narrow down root causes. Check each of them in turn and look for messages indicating problem areas.

The following logs may be helpful:

Check the Nginx process logs by typing:` journalctl -u nginx`

Check the Nginx access logs by typing:` less /var/log/nginx/access.log`

Check the Nginx error logs by typing:` less /var/log/nginx/error.log`

Check the Gunicorn application logs by typing:` journalctl -u gunicorn`

Check the Gunicorn socket logs by typing:` journalctl -u gunicorn.socket`

#### Nginx Permission Denied Errors:

The primary place to look for more information is in Nginx’s error logs. Generally, this will tell you what conditions caused problems during the proxying event. Follow the Nginx error logs by typing:
```bash
tail -F /var/log/nginx/error.log
```
##### For (13: Permission denied), "GET /static/css/style.css HTTP/1.1":
Ensure that Nginx and Gunicorn have the necessary permissions to access your project files. Adjust permissions cautiously:
```bash
chmod o+rx /your_username
```
```bash
chmod o+rx /your_username/IP_Aggregator/ip_aggregator
```
```bash
chmod -R o+rx /your_username/IP_Aggregator/ip_aggregator/static
```
```bash
sudo chown -R www-data:www-data /your_username/IP_Aggregator/ip_aggregator/static
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
