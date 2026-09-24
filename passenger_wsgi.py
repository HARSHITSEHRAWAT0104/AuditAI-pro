"""
GoDaddy cPanel Entrypoint (Phusion Passenger WSGI adapter)
Enables FastAPI (ASGI) to run natively on GoDaddy Linux cPanel hosting.
"""

import sys
import os

# Add current directory to Python path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from server import app
from a2wsgi import ASGIMiddleware

# Passenger looks for a WSGI callable named 'application'
application = ASGIMiddleware(app)
