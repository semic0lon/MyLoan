import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app
from waitress import serve

print("Starting Waitress...", flush=True)

serve(app, host="0.0.0.0", port=5000)