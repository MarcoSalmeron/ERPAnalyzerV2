import sys
import pathlib
import uvicorn

# Ensure root project path is on sys.path so imports like agents.* and common.* resolve.
"""ROOT_DIR = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
"""
if __name__ == "__main__":
    uvicorn.run("analyzer_services.app.main:services", host="0.0.0.0", port=8000)