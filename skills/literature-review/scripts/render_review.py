#!/usr/bin/env python3
"""Render a starter literature-review markdown file from a structured brief."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


TEXT = {
    "en": {
        "title_fallback": "Literature Review Draft",
        "meta_topic": "Topic",
        "meta_objective": "Objective",
        "meta_type": "Review Type",
        "meta_window": "Time Window",
        "meta_language": "Language",
        "meta_citation": "Citation Style",
        "meta_depth": "Depth",
        "brief": "1. Request Normalization",
        "questions": "Key Questions",
        "strategy": "2. Search Strategy and Coverage",
        "sources": "Preferred Sources",
        "keywords": "Keywords",
        "queries": "Suggested Search Strings",
        "criteria_in": "Inclusion Criteria",
        "criteria_ex": "Exclusion Criteria",
        "abstract": "3. Draft Abstract",
        "intro": "4. Introduction",
        "themes": "5. Thematic Synthesis",
        "gaps": "6. Research Gaps",
        "limits": "7. Limitations",
        "future": "8. Future Directions",
        "refs": "References",
        "theme_prefix": "Theme",
        "placeholder_theme": "Synthesize representative papers, methods, and disagreements here.",
        "placeholder_gap": "Gap: specify what remains unresolved and why it matters.",
        "placeholder_limit": "State any source-coverage or evidence-quality limitations here.",
        "placeholder_future": "Direction: propose a concrete next step for research or practice.",
    },
    "zh": {
        "title_fallback": "文献综述初稿",
        "meta_topic": "主题",
        "meta_objective": "目标",
        "meta_type": "综述类型",
        "meta_window": "时间范围",
        "meta_language": "语言",
        "meta_citation": "引文格式",
        "meta_depth": "深度",
        "brief": "1. 需求归一化",
        "questions": "核心问题",
        "strategy": "2. 检索策略与覆盖范围",
        "sources": "优先来源",
        "keywords": "关键词",
        "queries": "建议检索式",
        "criteria_in": "纳入标准",
        "criteria_ex": "排除标准",
        "abstract": "3. 摘要草稿",
        "intro": "4. 引言",
        "themes": "5. 主题综合",
        "gaps": "6. 研究空白",
        "limits": "7. 局限性",
        "future": "8. 未来方向",
        "refs": "参考文献",
        "theme_prefix": "主题",
        "placeholder_theme": "在这里综合代表性论文、方法路线以及分歧点。",
        "placeholder_gap": "空白点：说明尚未解决的问题及其重要性。",
        "placeholder_limit": "说明检索覆盖、证据质量或全文可得性的限制。",
        "placeholder_future": "未来方向：提出具体、可操作的研究或应用方向。",
    },
}


def is_zh(language: str) -> bool:
    return language.lower().startswith("zh")


def localize(language: str) -> dict[str, str]:
    return TEXT["zh" if is_zh(language) else "en"]


def format_window(window: dict) -> str:
    if not window:
        return "TBD"
    if "from_year" in window or "to_year" in window:
        start = window.get("from_year", "?")
        end = window.get("to_year", "?")
        return f"{start}-{end}"
    if "from" in window or "to" in window:
        start = window.get("from", "?")
        end = window.get("to", "?")
        return f"{start} to {end}"
    return "TBD"


def list_or_placeholder(items: list[str] | None, placeholder: str = "TBD") -> list[str]:
    return items if items else [placeholder]


def strip_terminal_punctuation(text: str) -> str:
    return text.rstrip("。．.!?！？;； ")


def join_question_summary(questions: list[str], language: str) -> str:
    cleaned = [strip_terminal_punctuation(question) for question in questions if question]
    if not cleaned:
        return ""
    separator = "；" if is_zh(language) else "; "
    return separator.join(cleaned[:3])


def build_queries(brief: dict) -> list[str]:
    groups = brief.get("concept_groups") or []
    if groups:
        rendered = []
        for group in groups:
            terms = group.get("terms") or []
            if not terms:
                continue
            rendered.append("(" + " OR ".join(f'"{term}"' for term in terms) + ")")
        if rendered:
            return [" AND ".join(rendered)]

    keywords = brief.get("keywords") or []
    if not keywords:
        return []

    query = " OR ".join(f'"{term}"' for term in keywords[:6])
    return [query]


def build_abstract(brief: dict, t: dict[str, str]) -> str:
    topic = brief.get("topic", "the topic")
    review_type = brief.get("review_type", "narrative")
    objective = strip_terminal_punctuation(brief.get("objective", "summarize the field"))
    questions = brief.get("questions") or []
    language = brief.get("language", "en")
    window = format_window(brief.get("window", {}))
    sources = ", ".join((brief.get("source_preferences") or [])[:4]) or "multiple academic sources"
    question_part = join_question_summary(questions, language)

    if t["title_fallback"] == "文献综述初稿":
        question_part = question_part or "研究现状、评测方式与关键局限"
        return (
            f"本文围绕“{topic}”开展一篇{review_type}文献综述，目标是{objective}"
            f"。综述拟覆盖 {window} 年间的相关研究，优先参考 {sources} 等来源，重点回答以下问题：{question_part}。"
            "正式定稿时需要用实际检索到的代表性论文补全证据、比较不同方法路线，并明确研究空白。"
        )

    question_part = question_part or "current approaches, evaluation practices, and open limitations"
    return (
        f"This {review_type} review examines {topic} with the objective of {objective}. "
        f"It is scoped to literature from {window} and prioritizes evidence from {sources}. "
        f"The draft is organized around {question_part}. Replace this starter paragraph with evidence-backed claims after retrieval."
    )


def build_intro(brief: dict, t: dict[str, str]) -> str:
    topic = brief.get("topic", "the topic")
    objective = strip_terminal_punctuation(brief.get("objective", "summarize the field"))
    questions = brief.get("questions") or []
    language = brief.get("language", "en")
    question_part = join_question_summary(questions, language)

    if t["title_fallback"] == "文献综述初稿":
        tail = question_part or "研究背景、主流路径与未解决问题"
        return (
            f"{topic} 已成为一个值得系统梳理的研究方向。本综述的目标是{objective}"
            f"，并围绕以下问题展开：{tail}。正文应在引出研究背景后，按主题而不是按单篇论文组织证据。"
        )

    tail = question_part or "background, dominant approaches, and unresolved problems"
    return (
        f"{topic} is now mature enough to justify structured synthesis. "
        f"This review is intended to {objective} and is organized around {tail}. "
        "The final draft should group the literature by themes rather than paper-by-paper summaries."
    )


def render_markdown(brief: dict) -> str:
    language = brief.get("language", "en")
    t = localize(language)

    title = brief.get("title") or brief.get("topic") or t["title_fallback"]
    objective = brief.get("objective", "TBD")
    review_type = brief.get("review_type", "narrative")
    window = format_window(brief.get("window", {}))
    citation_style = brief.get("citation_style", "APA")
    depth = brief.get("depth", "standard")
    questions = list_or_placeholder(brief.get("questions"))
    keywords = list_or_placeholder(brief.get("keywords"))
    sources = list_or_placeholder(brief.get("source_preferences"))
    inclusion = list_or_placeholder(brief.get("inclusion_criteria"))
    exclusion = list_or_placeholder(brief.get("exclusion_criteria"))
    queries = list_or_placeholder(build_queries(brief), placeholder="Build a boolean query from concept groups.")

    lines: list[str] = [
        f"# {title}",
        "",
        f"**{t['meta_topic']}**: {brief.get('topic', 'TBD')}  ",
        f"**{t['meta_objective']}**: {objective}  ",
        f"**{t['meta_type']}**: {review_type}  ",
        f"**{t['meta_window']}**: {window}  ",
        f"**{t['meta_language']}**: {language}  ",
        f"**{t['meta_citation']}**: {citation_style}  ",
        f"**{t['meta_depth']}**: {depth}",
        "",
        f"## {t['brief']}",
        "",
        f"- {t['meta_topic']}: {brief.get('topic', 'TBD')}",
        f"- {t['meta_objective']}: {objective}",
        f"- {t['meta_type']}: {review_type}",
        f"- {t['meta_window']}: {window}",
        f"- {t['questions']}:",
    ]

    for question in questions:
        lines.append(f"  - {question}")

    lines.extend(
        [
            "",
            f"## {t['strategy']}",
            "",
            f"### {t['sources']}",
            "",
        ]
    )

    for source in sources:
        lines.append(f"- {source}")

    lines.extend(
        [
            "",
            f"### {t['keywords']}",
            "",
        ]
    )

    for keyword in keywords:
        lines.append(f"- {keyword}")

    lines.extend(
        [
            "",
            f"### {t['queries']}",
            "",
            "```text",
        ]
    )
    lines.extend(queries)
    lines.extend(
        [
            "```",
            "",
            f"### {t['criteria_in']}",
            "",
        ]
    )

    for criterion in inclusion:
        lines.append(f"- {criterion}")

    lines.extend(
        [
            "",
            f"### {t['criteria_ex']}",
            "",
        ]
    )

    for criterion in exclusion:
        lines.append(f"- {criterion}")

    lines.extend(
        [
            "",
            f"## {t['abstract']}",
            "",
            build_abstract(brief, t),
            "",
            f"## {t['intro']}",
            "",
            build_intro(brief, t),
            "",
            f"## {t['themes']}",
            "",
        ]
    )

    for index, question in enumerate(questions[:4], start=1):
        lines.extend(
            [
                f"### {t['theme_prefix']} {index}: {question}",
                "",
                t["placeholder_theme"],
                "",
            ]
        )

    lines.extend(
        [
            f"## {t['gaps']}",
            "",
            f"- {t['placeholder_gap']}",
            f"- {t['placeholder_gap']}",
            "",
            f"## {t['limits']}",
            "",
            f"- {t['placeholder_limit']}",
            "",
            f"## {t['future']}",
            "",
            f"- {t['placeholder_future']}",
            f"- {t['placeholder_future']}",
            "",
            f"## {t['refs']}",
            "",
            "- [Add verified citations here]",
            "",
        ]
    )

    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--brief", required=True, help="Path to the review brief JSON file.")
    parser.add_argument("--output", help="Optional output markdown path. Prints to stdout if omitted.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    brief_path = Path(args.brief)
    with brief_path.open("r", encoding="utf-8") as handle:
        brief = json.load(handle)

    markdown = render_markdown(brief)

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(markdown, encoding="utf-8")
    else:
        sys.stdout.write(markdown)


if __name__ == "__main__":
    main()
