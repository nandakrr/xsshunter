# Use a base image with the desired OS
FROM ubuntu:latest

# Set noninteractive mode to prevent tzdata prompts during build
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && \
    apt-get install -y nginx postgresql postgresql-contrib git tmux python3-venv python3-dev libpq-dev libffi-dev

# Set up PostgreSQL
USER postgres
RUN service postgresql start && \
    psql -c "CREATE USER xsshunter WITH PASSWORD 'xsshunter';" && \
    psql -c "CREATE DATABASE xsshunter;" && \
    service postgresql stop

# Switch back to root user
USER root

# Clone xsshunter repository
RUN git clone https://github.com/nandakrr/xsshunter.git && \
    cd xsshunter && \
    python3 generate_config.py && \
    mv default /etc/nginx/sites-enabled/default && \
    service nginx restart

# Set up API server
RUN cd xsshunter/api/ && \
    python3 -m venv env && \
    . env/bin/activate && \
    pip3 install -r requirements.txt

# Set up GUI server
RUN cd xsshunter/gui/ && \
    python3 -m venv env && \
    . env/bin/activate && \
    pip3 install -r requirements.txt

# Expose necessary ports
EXPOSE 80
EXPOSE 5000

# Start the services
CMD ["tmux", "new-session", "-d", "bash", "-c", "cd /xsshunter/api && . env/bin/activate && python3 apiserver.py; bash"] && \
    ["tmux", "new-session", "-d", "bash", "-c", "cd /xsshunter/gui && . env/bin/activate && python3 guiserver.py; bash"]
