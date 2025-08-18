# Use a Python base image for your application, which is more efficient
FROM python:3.11-slim

# Setup virtual display and other dependencies
RUN apt-get update && \
    apt-get install -y \
    xvfb \
    xterm \
    fluxbox \
	 # X testing
	 mesa-utils \
	 x11-utils \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/rtc-rd/

# Copy project dependencies and install them
COPY requirements.prod.txt ./
RUN pip install --no-cache-dir -r requirements.prod.txt

# Copy application source code
COPY src .
COPY docker/entrypoint.sh .

# Make the startup script executable
RUN chmod +x entrypoint.sh

# Expose the port your application will run on
EXPOSE 8000

CMD ["./entrypoint.sh"]
