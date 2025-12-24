#!/usr/bin/env python3
"""Run all tests across all chapters."""
import subprocess
import sys


def main():
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-v", "--tb=short"],
        cwd=__file__.rsplit("/", 1)[0] or ".",
    )
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
