#!/usr/bin/env python3

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


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
    now = utc_now_iso()
    for stage in stages:
        if stage.get("name") == stage_name and stage.get("path") == str(stage_path):
            stage["index"] = index
            stage["status"] = status
            stage.setdefault("started_at", now)
            if status == "completed":
                stage["completed_at"] = now
            else:
                stage.pop("completed_at", None)
            stage["updated_at"] = now
            return

    stages.append(
        {
            "index": index,
            "name": stage_name,
            "path": str(stage_path),
            "status": status,
            "created_at": now,
            "updated_at": now,
            "started_at": now,
        }
    )
    if status == "completed":
        stages[-1]["completed_at"] = now


def str_to_bool(value: Optional[str]) -> Optional[bool]:
    if value is None:
        return None
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "y"}:
        return True
    if normalized in {"0", "false", "no", "n"}:
        return False
    raise ValueError(f"Unsupported boolean value: {value}")


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
        "user_query": args.user_query or args.task,
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
    if args.user_query:
        manifest["user_query"] = args.user_query
    if planned_chain:
        manifest["planned_chain"] = planned_chain
    if args.language:
        manifest["language"] = args.language
    if args.manuscript_type:
        manifest["manuscript_type"] = args.manuscript_type
    if args.target_artifact:
        manifest["target_artifact"] = args.target_artifact

    dump_json(manifest_path, manifest)
    write_text_if_missing(
        run_dir / "user-query.md",
        "# User Query\n\n"
        f"{args.user_query or args.task}\n",
    )

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
    now = utc_now_iso()

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
    status_path = stage_path / "status.json"
    status_payload = load_json(status_path) if status_path.exists() else {}
    status_payload.setdefault("created_at", now)
    status_payload.setdefault("started_at", now)
    status_payload["stage"] = args.stage
    status_payload["status"] = args.status
    status_payload.setdefault("evidence_status", "unknown")
    if args.status == "completed":
        status_payload["completed_at"] = now
    else:
        status_payload.pop("completed_at", None)
    status_payload["updated_at"] = now
    dump_json(status_path, status_payload)

    if args.next_skill:
        handoff_path = stage_path / "handoff.json"
        handoff_payload = load_json(handoff_path) if handoff_path.exists() else {}
        handoff_payload.setdefault("created_at", now)
        handoff_payload.setdefault("ready", False)
        handoff_payload["from_stage"] = args.stage
        handoff_payload["to_stage"] = args.next_skill
        handoff_payload["updated_at"] = now
        dump_json(handoff_path, handoff_payload)

    manifest_path = run_dir / "manifest.json"
    if manifest_path.exists():
        manifest = load_json(manifest_path)
        ensure_stage_entry(manifest, args.stage, stage_path, args.index, args.status)
        manifest["updated_at"] = utc_now_iso()
        dump_json(manifest_path, manifest)

    print(stage_path)
    return 0


def cmd_update_stage(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir)
    stage_path = run_dir / "stages" / stage_dir_name(args.index, args.stage)
    if not stage_path.exists():
        raise FileNotFoundError(f"Stage path does not exist: {stage_path}")

    now = utc_now_iso()
    status_path = stage_path / "status.json"
    status_payload = load_json(status_path) if status_path.exists() else {"stage": args.stage, "created_at": now}
    status_payload["stage"] = args.stage
    status_payload.setdefault("started_at", now)
    status_payload["status"] = args.status
    if args.evidence_status:
        status_payload["evidence_status"] = args.evidence_status
    if args.status == "completed":
        status_payload["completed_at"] = now
    else:
        status_payload.pop("completed_at", None)
    status_payload["updated_at"] = now
    dump_json(status_path, status_payload)

    if args.next_skill or args.handoff_ready is not None:
        handoff_path = stage_path / "handoff.json"
        handoff_payload = load_json(handoff_path) if handoff_path.exists() else {
            "from_stage": args.stage,
            "to_stage": args.next_skill or "",
            "created_at": now,
            "ready": False,
        }
        if args.next_skill:
            handoff_payload["to_stage"] = args.next_skill
        handoff_ready = str_to_bool(args.handoff_ready)
        if handoff_ready is not None:
            handoff_payload["ready"] = handoff_ready
        handoff_payload["updated_at"] = now
        dump_json(handoff_path, handoff_payload)

    manifest_path = run_dir / "manifest.json"
    if manifest_path.exists():
        manifest = load_json(manifest_path)
        ensure_stage_entry(manifest, args.stage, stage_path, args.index, args.status)
        if args.run_status:
            manifest["status"] = args.run_status
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
    init_parser.add_argument(
        "--user-query",
        help="Original user request text for traceability. Defaults to --task when omitted.",
    )
    init_parser.set_defaults(func=cmd_init)

    stage_parser = subparsers.add_parser("ensure-stage", help="Create or reuse a stage package inside an existing run.")
    stage_parser.add_argument("--run-dir", required=True, help="Existing run directory path.")
    stage_parser.add_argument("--stage", required=True, help="Stage name.")
    stage_parser.add_argument("--index", type=int, required=True, help="Stage sequence index.")
    stage_parser.add_argument("--status", default="in_progress", help="Initial stage status.")
    stage_parser.add_argument("--next-skill", help="Optional downstream skill name for handoff.json.")
    stage_parser.set_defaults(func=cmd_ensure_stage)

    update_parser = subparsers.add_parser("update-stage", help="Update a stage package after content has been written.")
    update_parser.add_argument("--run-dir", required=True, help="Existing run directory path.")
    update_parser.add_argument("--stage", required=True, help="Stage name.")
    update_parser.add_argument("--index", type=int, required=True, help="Stage sequence index.")
    update_parser.add_argument("--status", required=True, help="Updated stage status.")
    update_parser.add_argument("--evidence-status", help="Updated evidence status.")
    update_parser.add_argument("--next-skill", help="Optional downstream skill name for handoff.json.")
    update_parser.add_argument("--handoff-ready", help="Optional boolean value for handoff readiness.")
    update_parser.add_argument("--run-status", help="Optional run-level status override.")
    update_parser.set_defaults(func=cmd_update_stage)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
