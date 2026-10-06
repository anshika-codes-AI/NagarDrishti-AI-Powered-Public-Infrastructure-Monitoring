import os
import sys

backend = r"A:\AI-Powered Public Infra Monitoring\backend"
sys.path.insert(0, backend)

# List db directory
db_dir = os.path.join(backend, "db")
print("db_dir:", db_dir)
print("Files:", os.listdir(db_dir))

# Try importing
from db.base import Base
print("Base imported successfully:", Base)
PYEOF