
import subprocess, sys, os
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
os.makedirs(ROOT/'index', exist_ok=True)
subprocess.check_call([sys.executable, str(ROOT/'app'/'build_index.py')])
print('Index built.')
