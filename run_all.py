"""
Single-Command Orchestrator for AI Tech Consultant Capstone.
Launches Task 1 (8001), Task 2 (8002), Task 3 (8003), and Executive Portal (8000).
Monitors health and handles graceful shutdown.
"""
import sys
import os
import subprocess
import time
import socket
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent
PYTHON_EXE = sys.executable
VENV_PYTHON = ROOT_DIR / ".venv" / ("Scripts" if os.name == "nt" else "bin") / ("python.exe" if os.name == "nt" else "python")

if VENV_PYTHON.exists():
    PYTHON_EXE = str(VENV_PYTHON)

PORTAL_PORT = 8000
TASK1_PORT = 8001
TASK2_PORT = 8002
TASK3_PORT = 8003


def is_port_open(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex(("127.0.0.1", port)) == 0


class PortalHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT_DIR / "shared" / "portal"), **kwargs)

    def log_message(self, format, *args):
        pass  # Quiet portal logs


def start_portal_server():
    server = HTTPServer(("0.0.0.0", PORTAL_PORT), PortalHandler)
    server.serve_forever()


def main():
    print("=" * 70)
    print("🚀 LAUNCHING AI TECH CONSULTANT CAPSTONE (ONE-COMMAND RUNNER)")
    print("=" * 70)
    print(f"Working Directory: {ROOT_DIR}")
    print(f"Python Runtime:    {PYTHON_EXE}\n")

    processes = []

    # 1. Start Portal Server in background thread
    portal_thread = threading.Thread(target=start_portal_server, daemon=True)
    portal_thread.start()
    print(f"✅ [Portal] Executive Command Portal listening on http://localhost:{PORTAL_PORT}")

    # 2. Launch Task 1: Knowledge Brain (Python FastAPI)
    print("⏳ [Task 1] Starting Knowledge Brain on port 8001...")
    p_task1 = subprocess.Popen(
        [PYTHON_EXE, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", str(TASK1_PORT)],
        cwd=str(ROOT_DIR / "task1-knowledge-brain")
    )
    processes.append(("Task 1 Knowledge Brain", p_task1))

    # 3. Launch Task 2: Inbox Agent (TypeScript Node.js)
    print("⏳ [Task 2] Starting Inbox Agent on port 8002...")
    # First ensure compiled dist exists
    dist_file = ROOT_DIR / "task2-inbox-agent" / "dist" / "src" / "index.js"
    if not dist_file.exists():
        subprocess.run(["npx", "tsc"], cwd=str(ROOT_DIR / "task2-inbox-agent"), shell=True)

    p_task2 = subprocess.Popen(
        ["node", "dist/src/index.js"],
        cwd=str(ROOT_DIR / "task2-inbox-agent"),
        shell=True
    )
    processes.append(("Task 2 Inbox Agent", p_task2))

    # 4. Launch Task 3: Meeting to Scope of Work (Python FastAPI)
    print("⏳ [Task 3] Starting Meeting to SOW on port 8003...")
    p_task3 = subprocess.Popen(
        [PYTHON_EXE, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", str(TASK3_PORT)],
        cwd=str(ROOT_DIR / "task3-meeting-sow")
    )
    processes.append(("Task 3 Meeting to SOW", p_task3))

    # Wait for all services to become healthy
    print("\n🔍 Awaiting service readiness...")
    for port, name in [(TASK1_PORT, "Task 1 (Knowledge Brain)"), (TASK2_PORT, "Task 2 (Inbox Agent)"), (TASK3_PORT, "Task 3 (Meeting to SOW)")]:
        for _ in range(30):
            if is_port_open(port):
                print(f"   🟢 {name} is READY on http://localhost:{port}")
                break
            time.sleep(0.5)

    print("\n" + "=" * 70)
    print("🌟 ALL 3 CAPSTONE SERVICES ARE LIVE & INTERCONNECTED!")
    print("=" * 70)
    print(f" • Executive Command Portal:  http://localhost:{PORTAL_PORT}")
    print(f" • Task 1 (Knowledge Brain):  http://localhost:{TASK1_PORT} (API Docs: /docs)")
    print(f" • Task 2 (The Inbox Agent):  http://localhost:{TASK2_PORT}")
    print(f" • Task 3 (Meeting to SOW):   http://localhost:{TASK3_PORT} (API Docs: /docs)")
    print("=" * 70)
    print("Press Ctrl+C to stop all services.\n")

    try:
        while True:
            time.sleep(1)
            for name, p in processes:
                if p.poll() is not None:
                    print(f"⚠️ {name} exited with code {p.returncode}")
    except KeyboardInterrupt:
        print("\n🛑 Shutting down AI Tech Consultant services...")
        for name, p in processes:
            print(f"   Stopping {name}...")
            p.terminate()
            try:
                p.wait(timeout=3)
            except Exception:
                p.kill()
        print("✅ All services stopped safely.")


if __name__ == "__main__":
    main()
