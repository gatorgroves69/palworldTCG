"""`python -m analysis results/<run>/` (re)writes report.md for a run."""
import sys
from pathlib import Path

from .report import write_report

if __name__ == "__main__":
    for d in sys.argv[1:] or ["."]:
        print(write_report(Path(d)))
