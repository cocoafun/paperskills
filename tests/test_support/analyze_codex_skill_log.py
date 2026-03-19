#!/usr/bin/env python3

import argparse
import json
import re
import sys
from pathlib import Path


READ_PATTERNS = (
    "SKILL.md",
    "/references/",
    "/examples/",
    "/assets/",
    "/scripts/",
)


def parse_jsonl(path: Path):
    items = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            items.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return items


def extract_texts(items):
    messages = []
    for item in items:
        if item.get("type") == "response_item":
            payload = item.get("payload", {})
            if payload.get("type") != "message":
                continue
            for content in payload.get("content", []):
                text = content.get("text")
                if text:
                    messages.append(text)
        elif item.get("type") == "item.completed":
            data = item.get("item", {})
            if data.get("type") == "agent_message":
                text = data.get("text", "")
                if text:
                    messages.append(text)
    return "\n".join(messages)


def extract_function_arguments(items):
    values = []
    for item in items:
        if item.get("type") == "response_item":
            payload = item.get("payload", {})
            if payload.get("type") != "function_call":
                continue
            arguments = payload.get("arguments", "")
            if arguments:
                values.append(arguments)
        elif item.get("type") in {"item.started", "item.completed"}:
            data = item.get("item", {})
            if data.get("type") == "command_execution":
                command = data.get("command", "")
                output = data.get("aggregated_output", "")
                if command:
                    values.append(command)
                if output:
                    values.append(output)
    return values


def was_skill_used(skill, arguments_list, message_text):
    skill_path_fragments = [
        f"/skills/paperskills/{skill}/SKILL.md",
        f"/skills/{skill}/SKILL.md",
        f"/{skill}/references/",
        f"/{skill}/examples/",
        f"/{skill}/assets/",
        f"/{skill}/scripts/",
    ]
    for arguments in arguments_list:
        if any(fragment in arguments for fragment in skill_path_fragments):
            if any(pattern in arguments for pattern in READ_PATTERNS):
                return True
    patterns = [
        rf"\b{re.escape(skill)}\b",
        rf"`{re.escape(skill)}`",
        rf"Using .*{re.escape(skill)}",
        rf"使用.*{re.escape(skill)}",
    ]
    return any(re.search(pattern, message_text, re.I) for pattern in patterns)


def find_missing_skills(expected_skills, arguments_list, message_text):
    return [skill for skill in expected_skills if not was_skill_used(skill, arguments_list, message_text)]


def list_observed_skill_reads(arguments_list):
    observed = set()
    for arguments in arguments_list:
        match = re.findall(r"/skills/(?:paperskills/)?([^/]+)/", arguments)
        for skill in match:
            observed.add(skill)
    return sorted(observed)


def main():
    parser = argparse.ArgumentParser(description="Analyze Codex JSONL output for skill usage.")
    parser.add_argument("--log", required=True, help="Path to codex JSONL log")
    parser.add_argument("--expected-skills", required=True, help="Comma-separated expected skills")
    args = parser.parse_args()

    items = parse_jsonl(Path(args.log))
    arguments_list = extract_function_arguments(items)
    message_text = extract_texts(items)
    expected_skills = [skill.strip() for skill in args.expected_skills.split(",") if skill.strip()]

    missing = find_missing_skills(expected_skills, arguments_list, message_text)
    observed = list_observed_skill_reads(arguments_list)

    print("Observed skill-related file reads:")
    for skill in observed:
        print(f"  - {skill}")
    if not observed:
        print("  (none detected)")

    if missing:
        print("Missing expected skills:")
        for skill in missing:
            print(f"  - {skill}")
        sys.exit(1)

    print("PASS: expected skills were detected")


if __name__ == "__main__":
    main()
