import os
import sys
import subprocess
import time
import webbrowser

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(root_dir, "backend")
    frontend_dir = os.path.join(root_dir, "frontend")
    python_exe = sys.executable

    print("======================================================================")
    print("      🏦 BANKSECURE API GUARD - ALL-IN-ONE PLATFORM LAUNCHER")
    print("======================================================================")
    print()

    # 1. Database Seed
    print("[1/3] Initializing Database & Security Test Suite...")
    subprocess.run([python_exe, "-m", "app.seed"], cwd=backend_dir, check=True)
    print("[OK] Database Seeded.")
    print()

    # 2. Launch Backend
    print("[2/3] Launching FastAPI Backend on http://localhost:8000 ...")
    backend_process = subprocess.Popen(
        [python_exe, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"],
        cwd=backend_dir
    )
    time.sleep(2)
    print("[OK] Backend Server Online.")
    print()

    # 3. Launch Frontend
    print("[3/3] Launching Vite React Dashboard on http://localhost:3000 ...")
    npm_cmd = os.path.join(r"C:\Program Files\nodejs", "npm.cmd")
    if not os.path.exists(npm_cmd):
        npm_cmd = "npm"

    frontend_process = subprocess.Popen(
        [npm_cmd, "run", "dev"],
        cwd=frontend_dir,
        env={**os.environ, "PATH": r"C:\Program Files\nodejs;" + os.environ.get("PATH", "")}
    )
    time.sleep(2)
    print("[OK] Frontend Server Online.")
    print()

    print("======================================================================")
    print(" 🚀 BANKSECURE API GUARD IS READY!")
    print(" 🌐 Web Dashboard: http://localhost:3000")
    print(" ⚙️ API Swagger Docs: http://localhost:8000/docs")
    print("======================================================================")

    webbrowser.open("http://localhost:3000")

    try:
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("\nShutting down BankSecure servers...")
        backend_process.terminate()
        frontend_process.terminate()

if __name__ == "__main__":
    main()
