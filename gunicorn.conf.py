import os

# Bind to 0.0.0.0 and the dynamic port provided by Render (defaults to 10000)
bind = f"0.0.0.0:{os.environ.get('PORT', '10000')}"

# Number of worker processes to handle customer traffic
workers = 4

# Timeout settings to prevent connection hanging
timeout = 120
