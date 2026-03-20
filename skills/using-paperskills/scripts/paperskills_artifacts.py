#!/usr/bin/env python3

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def slugify(value: str) -> str:
    text = value.strip().lower()
    text = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", text)
    text = re.sub(r"-{2,}", "-", text).strip("-")
    return text or "task"


def write_json_if_missing(path: Path, payload: dict) -> None:
    if not path.exists():
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text_if_missing(path: Path, payload: str) -> None:
    if not path.exists():
        path.write_text(payload, encoding="utf-8")


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def stage_dir_name(index: int, stage: str) -> str:
    return f"{index:02d}-{stage}"


def ensure_stage_entry(manifest: dict, stage_name: str, stage_path: Path, index: int, status: str) -> None:
    stages = manifest.setdefault("stages", [])
    for stage in stages:
        if stage.get("name") == stage_name and stage.get("path") == str(stage_path):
            stage["status"] = status
            stage["updated_at"] = utc_now_iso()
            return

    stages.append(
        {
            "index": index,
            "name": stage_name,
            "path": str(stage_path),
            "status": status,
            "created_at": utc_now_iso(),
            "updated_at": utc_now_iso(),
        }
    )


def cmd_init(args: argparse.Namespace) -> int:
    root = Path(args.root)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    task_slug = slugify(args.task)
    run_id = args.run_id or f"{timestamp}-{task_slug}"
    run_dir = root / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "stages").mkdir(exist_ok=True)

    planned_chain = [part.strip() for part in (args.planned_chain or "").split(",") if part.strip()]
    manifest_path = run_dir / "manifest.json"
    manifest = load_json(manifest_path) or {
        "schema_version": "paperskills-run/v1",
        "run_id": run_id,
        "task": args.task,
        "task_slug": task_slug,
        "root_dir": str(run_dir),
        "created_at": utc_now_iso(),
        "updated_at": utc_now_iso(),
        "entry_stage": args.entry_stage,
        "planned_chain": planned_chain,
        "language": args.language,
        "manuscript_type": args.manuscript_type,
        "target_artifact": args.target_artifact,
        "status": "in_progress",
        "stages": [],
    }

    manifest["updated_at"] = utc_now_iso()
    if args.entry_stage:
        manifest["entry_stage"] = args.entry_stage
    if planned_chain:
        manifest["planned_chain"] = planned_chain
    if args.language:
        manifest["language"] = args.language
    if args.manuscript_type:
        manifest["manuscript_type"] = args.manuscript_type
    if args.target_artifact:
        manifest["target_artifact"] = args.target_artifact

    dump_json(manifest_path, manifest)

    if args.entry_stage:
        stage_args = argparse.Namespace(
            run_dir=str(run_dir),
            stage=args.entry_stage,
            index=args.entry_index,
            status="in_progress",
            next_skill=planned_chain[0] if planned_chain else "",
        )
        cmd_ensure_stage(stage_args)

    print(run_dir)
    return 0


def cmd_ensure_stage(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir)
    stages_dir = run_dir / "stages"
    stages_dir.mkdir(parents=True, exist_ok=True)
    stage_path = stages_dir / stage_dir_name(args.index, args.stage)
    stage_path.mkdir(parents=True, exist_ok=True)

    write_json_if_missing(
        stage_path / "brief.json",
        {
            "stage": args.stage,
            "status": "draft",
            "created_at": utc_now_iso(),
        },
    )
    write_text_if_missing(stage_path / "notes.md", f"# {args.stage} Notes\n\n")
    write_text_if_missing(stage_path / "output.md", f"# {args.stage} Output\n\n")
    write_json_if_missing(
        stage_path / "status.json",
        {
            "stage": args.stage,
            "status": args.status,
            "evidence_status": "unknown",
            "created_at": utc_now_iso(),
            "updated_at": utc_now_iso(),
        },
    )

    if args.next_skill:
        write_json_if_missing(
            stage_path / "handoff.json",
            {
                "from_stage": args.stage,
                "to_stage": args.next_skill,
                "created_at": utc_now_iso(),
                "ready": False,
            },
        )

    manifest_path = run_dir / "manifest.json"
    if manifest_path.exists():
        manifest = load_json(manifest_path)
        ensure_stage_entry(manifest, args.stage, stage_path, args.index, args.status)
        manifest["updated_at"] = utc_now_iso()
        dump_json(manifest_path, manifest)

    print(stage_path)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Initialize and maintain PaperSkills local artifact runs.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Create a run directory and an optional entry-stage package.")
    init_parser.add_argument("--task", required=True, help="Short task title used to derive the run id.")
    init_parser.add_argument("--root", default="artifacts/paperskills", help="Root directory for run storage.")
    init_parser.add_argument("--run-id", help="Explicit run id. Defaults to timestamp plus slug.")
    init_parser.add_argument("--entry-stage", help="Entry stage name, such as using-paperskills.")
    init_parser.add_argument("--entry-index", type=int, default=1, help="Stage index for the entry stage.")
    init_parser.add_argument("--planned-chain", help="Comma-separated downstream stage chain.")
    init_parser.add_argument("--language", help="Normalized workflow language.")
    init_parser.add_argument("--manuscript-type", help="Normalized manuscript type.")
    init_parser.add_argument("--target-artifact", help="Target artifact for the run.")
    init_parser.set_defaults(func=cmd_init)

    stage_parser = subparsers.add_parser("ensure-stage", help="Create or reuse a stage package inside an existing run.")
    stage_parser.add_argument("--run-dir", required=True, help="Existing run directory path.")
    stage_parser.add_argument("--stage", required=True, help="Stage name.")
    stage_parser.add_argument("--index", type=int, required=True, help="Stage sequence index.")
    stage_parser.add_argument("--status", default="in_progress", help="Initial stage status.")
    stage_parser.add_argument("--next-skill", help="Optional downstream skill name for handoff.json.")
    stage_parser.set_defaults(func=cmd_ensure_stage)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
