#!/usr/bin/env python3

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SKILLS = {
    "using-paperskills": {"needs_assets": False, "needs_examples": True, "needs_references": True},
    "research-scoping": {"needs_assets": True, "needs_examples": True, "needs_references": True},
    "research-design": {"needs_assets": True, "needs_examples": True, "needs_references": True},
    "paper-drafting": {"needs_assets": True, "needs_examples": True, "needs_references": True},
    "revision-planning": {"needs_assets": True, "needs_examples": True, "needs_references": True},
}


def fail(message):
    print(f"FAIL: {message}")
    sys.exit(1)


def ensure(condition, message):
    if not condition:
        fail(message)


def read_text(path):
    ensure(path.exists(), f"Missing file: {path}")
    return path.read_text()


def validate_frontmatter(skill, text):
    ensure(text.startswith("---\n"), f"{skill}: missing frontmatter start")
    match = re.match(r"---\n(.*?)\n---\n", text, re.S)
    ensure(match is not None, f"{skill}: invalid frontmatter block")
    frontmatter = match.group(1)
    ensure(f"name: {skill}" in frontmatter, f"{skill}: frontmatter name mismatch")
    ensure("description:" in frontmatter, f"{skill}: missing description")


def validate_link_targets(skill_dir, text):
    targets = re.findall(r"\[.*?\]\((.*?)\)", text)
    for target in targets:
        if target.startswith("http"):
            continue
        target_path = (skill_dir / target).resolve()
        ensure(target_path.exists(), f"{skill_dir.name}: missing linked file {target}")


def validate_json_files(paths):
    for path in paths:
        json.loads(path.read_text())


def validate_trigger_suite():
    prompts_dir = ROOT / "tests" / "skill-triggering" / "prompts"
    for skill, requirements in SKILLS.items():
        skill_dir = ROOT / "skills" / skill
        ensure(skill_dir.exists(), f"Missing skill dir: {skill_dir}")
        skill_md = skill_dir / "SKILL.md"
        text = read_text(skill_md)
        validate_frontmatter(skill, text)
        validate_link_targets(skill_dir, text)

        refs = list((skill_dir / "references").glob("*")) if (skill_dir / "references").exists() else []
        exs = list((skill_dir / "examples").glob("*")) if (skill_dir / "examples").exists() else []
        assets = list((skill_dir / "assets").glob("*")) if (skill_dir / "assets").exists() else []

        if requirements["needs_references"]:
            ensure(refs, f"{skill}: missing references")
        if requirements["needs_examples"]:
            ensure(exs, f"{skill}: missing examples")
        if requirements["needs_assets"]:
            ensure(assets, f"{skill}: missing assets")

        validate_json_files([path for path in exs if path.suffix == ".json"])

        prompt_file = prompts_dir / f"{skill}.txt"
        ensure(prompt_file.exists(), f"{skill}: missing prompt fixture {prompt_file.name}")
        ensure(prompt_file.read_text().strip(), f"{skill}: empty prompt fixture")

    schema_paths = list((ROOT / "schemas").glob("*.json"))
    ensure(schema_paths, "Missing shared schemas")
    validate_json_files(schema_paths)


def validate_workflow_suite():
    workflow_dir = ROOT / "examples" / "workflows"
    ensure(workflow_dir.exists(), "Missing examples/workflows directory")
    workflow_files = sorted(workflow_dir.glob("*.md"))
    ensure(workflow_files, "Missing workflow example markdown files")

    expected_mentions = {
        "idea-to-draft.md": [
            "using-paperskills",
            "research-scoping",
            "literature-review",
            "research-design",
            "paper-drafting",
        ],
        "review-to-revision.md": [
            "using-paperskills",
            "peer-review",
            "revision-planning",
        ],
    }

    for name, expected in expected_mentions.items():
        path = workflow_dir / name
        text = read_text(path)
        for item in expected:
            ensure(item in text, f"{name}: missing workflow stage {item}")

    required_examples = [
        ROOT / "skills" / "research-scoping" / "examples" / "topic-brief.json",
        ROOT / "skills" / "research-design" / "examples" / "proposal-brief.json",
        ROOT / "skills" / "paper-drafting" / "examples" / "section-brief.json",
        ROOT / "skills" / "revision-planning" / "examples" / "reviewer-comments-brief.json",
    ]
    for path in required_examples:
        ensure(path.exists(), f"Missing workflow example artifact: {path}")
        json.loads(path.read_text())


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in {"trigger", "workflow"}:
        fail("Usage: validate_paperskills.py [trigger|workflow]")

    if sys.argv[1] == "trigger":
        validate_trigger_suite()
        print("PASS: skill-triggering checks passed")
    else:
        validate_workflow_suite()
        print("PASS: workflow-smoke checks passed")


if __name__ == "__main__":
    main()
