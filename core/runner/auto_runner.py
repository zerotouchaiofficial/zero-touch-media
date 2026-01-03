import sys
import subprocess
import os

def main():
    root = os.path.abspath(os.getcwd())
    script = os.path.join(root, "generate_short.py")

    print("▶ Repo root:", root)
    print("▶ Running:", script)

    if not os.path.exists(script):
        raise FileNotFoundError(f"generate_short.py not found at {script}")

    result = subprocess.run(
        [sys.executable, script],
        stdout=sys.stdout,
        stderr=sys.stderr
    )

    if result.returncode != 0:
        raise RuntimeError("Video generation failed")

if __name__ == "__main__":
    main()
