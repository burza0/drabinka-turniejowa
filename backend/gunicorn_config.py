# Gunicorn configuration for WERSJA 30.3 (StartLineScanner skonsolidowany)
import os

# Server socket
bind = f"0.0.0.0:{os.environ.get('PORT', 5000)}"
backlog = 2048

# Worker processes
workers = 2  # Optymalne dla wersji 30.3
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 2

# Restart workers after this many requests to prevent memory leaks
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Process naming
proc_name = "skatecross-api-v30.3"

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Application preloading
preload_app = True

# Worker recycling
max_worker_memory = 200  # MB

def when_ready(server):
    server.log.info("Server ready - WERSJA 30.3 (StartLineScanner skonsolidowany)")

def worker_int(worker):
    worker.log.info("Worker received INT or QUIT signal")

def pre_fork(server, worker):
    server.log.info(f"Worker spawned (pid: {worker.pid})")

def post_fork(server, worker):
    server.log.info(f"Worker started (pid: {worker.pid})") 