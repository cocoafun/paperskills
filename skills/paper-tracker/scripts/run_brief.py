#!/usr/bin/env python3
"""Run the paper-tracker retrieval pipeline for a brief."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def run_command(command: list[str]) -> dict:
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    return json.loads(result.stdout)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--brief", required=True)
    parser.add_argument("--rows-per-source", type=int, default=25)
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    retrieve_script = script_dir / "retrieve_candidates.py"
    postprocess_script = script_dir / "postprocess_papers.py"

    raw = run_command(
        [
            sys.executable,
            str(retrieve_script),
            "--brief",
            args.brief,
            "--rows-per-source",
            str(args.rows_per_source),
        ]
    )

    with tempfile.NamedTemporaryFile("w+", suffix=".json", delete=False) as handle:
        json.dump(raw, handle, ensure_ascii=False, indent=2)
        handle.flush()
        postprocessed = run_command(
            [
                sys.executable,
                str(postprocess_script),
                "--input",
                handle.name,
                *(["--limit", str(args.limit)] if args.limit is not None else []),
            ]
        )

    json.dump(postprocessed, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
