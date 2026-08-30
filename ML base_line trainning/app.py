import sys
from pathlib import Path

app_dir = Path(__file__).resolve().parent / "ML base_line trainning"
sys.path.insert(0, str(app_dir))

app_file = app_dir / "app.py"
with open(app_file, "r", encoding="utf-8") as f:
    code = f.read()

exec(code, {"__file__": str(app_file), "__name__": "__main__"})
