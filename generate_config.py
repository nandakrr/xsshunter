#!/usr/bin/env python
import binascii
import yaml
import os

nginx_template = """
server {
    # Redirect HTTP to www
    listen 80;
    server_name fakedomain.com;
    location / {
        rewrite ^/(.*)$ https://www.fakedomain.com/$1 permanent;
    }
}

server {
    # Redirect payloads to HTTPS
    listen 80;
    server_name *.fakedomain.com;
    proxy_set_header X-Forwarded-For $remote_addr;

    return 307 https://$host$request_uri;
    client_max_body_size 500M; # In case we have an extra large payload capture 
}

server {
    # Redirect HTTPS to www
    listen 443;
    ssl on;
    ssl_certificate /etc/nginx/ssl/fakedomain.com.crt; # Wildcard SSL certificate
    ssl_certificate_key /etc/nginx/ssl/fakedomain.com.key; # Wildcard SSL certificate key

    server_name fakedomain.com;
    location / {
        rewrite ^/(.*)$ https://www.fakedomain.com/$1 permanent;
    }
}

server {
    # API proxy
    listen 443;
    ssl on;
    ssl_certificate /etc/nginx/ssl/fakedomain.com.crt; # Wildcard SSL certificate
    ssl_certificate_key /etc/nginx/ssl/fakedomain.com.key; # Wildcard SSL certificate key

    server_name *.fakedomain.com;
    access_log /var/log/nginx/fakedomain.com.vhost.access.log;
    error_log /var/log/nginx/fakedomain.com.vhost.error.log;

    client_max_body_size 500M;

    location / {
        proxy_pass  http://localhost:8888;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $remote_addr;
    }
}

server {
    # Redirect api to HTTPS
    listen 80;
    server_name api.fakedomain.com; # Subdomain for API server
    proxy_set_header X-Forwarded-For $remote_addr;

    return 307 https://api.fakedomain.com$request_uri;
    client_max_body_size 500M; # In case we have an extra large payload capture 
}

server {
   # Redirect www to HTTPS
   listen 80;
   server_name www.fakedomain.com;
   location / {
       rewrite ^/(.*)$ https://www.fakedomain.com/$1 permanent;
   }
}

server {
   # GUI proxy
   listen 443;
   server_name www.fakedomain.com;
   client_max_body_size 500M;
   ssl on;
   ssl_certificate /etc/nginx/ssl/fakedomain.com.crt; # Wildcard SSL certificate
   ssl_certificate_key /etc/nginx/ssl/fakedomain.com.key; # Wildcard SSL certificate key


   location / {
       proxy_pass  http://localhost:1234;
       proxy_set_header Host $host;
   }
}
"""


settings = {
    "email_from": "you@example.com",
    "mailgun_api_key": "your_mailgun_api_key",
    "mailgun_sending_domain": "your_mailgun_sending_domain",
    "domain": "x.nksec.tech",
    "abuse_email": "abuse@example.com",
    "cookie_secret": "",
    "postgreql_username": "your_postgres_user",
    "postgreql_password": "your_postgres_password",
    "postgres_db": "your_postgres_db",
}

settings["cookie_secret"] = binascii.hexlify(os.urandom(50))

yaml_config = yaml.dump(settings, default_flow_style=False)
file_handler = open("config.yaml", "w")
file_handler.write(yaml_config)
file_handler.close()

file_handler = open("default", "w")
file_handler.write(nginx_template)
file_handler.close()
