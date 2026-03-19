#!/usr/bin/env python3

import argparse
import json
from pathlib import Path


TEXT = {
    "en": {
        "title": "Revision Plan",
        "manuscript_status": "Manuscript Status",
        "target_venue": "Target Venue",
        "deadline": "Deadline",
        "language": "Language",
        "comments": "Comments",
        "constraints": "Constraints",
        "id": "ID",
        "severity": "Severity",
        "source": "Source",
        "comment": "Comment",
        "unspecified": "unspecified",
        "unknown": "unknown",
        "none": "None",
    },
    "zh": {
        "title": "修改计划",
        "manuscript_status": "稿件状态",
        "target_venue": "目标期刊/会议",
        "deadline": "截止时间",
        "language": "语言",
        "comments": "审稿意见",
        "constraints": "约束条件",
        "id": "编号",
        "severity": "严重程度",
        "source": "来源",
        "comment": "意见内容",
        "unspecified": "未指定",
        "unknown": "未知",
        "none": "无",
    },
}


def is_zh(language: str) -> bool:
    return language.lower().startswith("zh")


def localize(language: str) -> dict[str, str]:
    return TEXT["zh" if is_zh(language) else "en"]


def main():
    parser = argparse.ArgumentParser(description="Render a revision brief into markdown.")
    parser.add_argument("--brief", required=True, help="Path to revision brief JSON")
    parser.add_argument("--output", required=True, help="Output markdown path")
    args = parser.parse_args()

    brief = json.loads(Path(args.brief).read_text())
    language = brief.get("language", "en")
    t = localize(language)
    rows = []
    for comment in brief.get("comments", []):
        text = comment.get("text", "").replace("|", "/")
        rows.append(
            f"| {comment.get('id', 'TBD')} | {comment.get('severity', 'unknown')} | "
            f"{comment.get('source', 'unknown')} | {text} |"
        )
    table = "\n".join(rows) if rows else "| TBD | TBD | TBD | TBD |"
    constraints = "\n".join(f"- {item}" for item in brief.get("constraints", [])) or f"- {t['none']}"

    markdown = f"""# {t["title"]}

**{t["manuscript_status"]}**: {brief.get("manuscript_status", t["unknown"])}  
**{t["target_venue"]}**: {brief.get("target_venue", t["unspecified"])}  
**{t["deadline"]}**: {brief.get("deadline", t["unspecified"])}  
**{t["language"]}**: {language}

## {t["comments"]}

| {t["id"]} | {t["severity"]} | {t["source"]} | {t["comment"]} |
| --- | --- | --- | --- |
{table}

## {t["constraints"]}

{constraints}
"""

    Path(args.output).write_text(markdown)


if __name__ == "__main__":
    main()
