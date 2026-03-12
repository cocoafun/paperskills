#!/usr/bin/env python3
"""Shared helpers for the paper-tracker scripts."""

from __future__ import annotations

import json
import re
import time
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any


USER_AGENT = "paper-tracker/0.1 (https://github.com/openai/codex)"


def load_json(path: str) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def dump_json(data: Any) -> None:
    json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def normalize_window(window: dict[str, Any]) -> dict[str, str]:
    if "from" in window and "to" in window:
        start = parse_date(window["from"])
        end = parse_date(window["to"])
    else:
        days = int(window.get("days", 7))
        end = date.today()
        start = end - timedelta(days=days)
    if start > end:
        raise ValueError("window.from must be <= window.to")
    return {"from": start.isoformat(), "to": end.isoformat()}


def http_get_json(url: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    if params:
        query = urllib.parse.urlencode(params, doseq=True)
        url = f"{url}?{query}"
    last_error: Exception | None = None
    for attempt in range(3):
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            message = exc.read().decode("utf-8", errors="ignore")
            if exc.code == 429 and attempt < 2:
                time.sleep(2 * (attempt + 1))
                last_error = exc
                continue
            raise RuntimeError(f"HTTP {exc.code} for {url}: {message[:200]}") from exc
        except urllib.error.URLError as exc:
            last_error = exc
            if attempt < 2:
                time.sleep(2 * (attempt + 1))
                continue
            raise RuntimeError(f"Network error for {url}: {exc}") from exc
    raise RuntimeError(f"Request failed for {url}: {last_error}")


def read_registry(registry_path: str | None) -> list[dict[str, Any]]:
    if not registry_path:
        return []
    path = Path(registry_path)
    if not path.exists():
        raise FileNotFoundError(f"Registry file not found: {registry_path}")
    rows: list[dict[str, Any]] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line.startswith("|") or line.startswith("| ---"):
            continue
        parts = [part.strip() for part in line.strip("|").split("|")]
        if len(parts) < 3 or parts[0] == "Journal":
            continue
        issns = [token.strip() for token in parts[1].split("/") if token.strip()]
        rows.append(
            {
                "journal": parts[0],
                "issns": issns,
                "publisher_hint": parts[2],
            }
        )
    return rows


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def title_key(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", title.lower())


def extract_date_parts(item: dict[str, Any], field: str) -> str | None:
    block = item.get(field) or {}
    parts = block.get("date-parts") or []
    if not parts or not parts[0]:
        return None
    tokens = [str(piece) for piece in parts[0]]
    while len(tokens) < 3:
        tokens.append("1")
    return f"{int(tokens[0]):04d}-{int(tokens[1]):02d}-{int(tokens[2]):02d}"


def best_publication_date(item: dict[str, Any]) -> tuple[str | None, str | None]:
    for field, label in [
        ("published-online", "published-online"),
        ("published-print", "published-print"),
        ("issued", "issued"),
        ("created", "created"),
    ]:
        value = extract_date_parts(item, field)
        if value:
            return value, label
    return None, None


def authors_from_crossref(item: dict[str, Any]) -> list[str]:
    authors = []
    for author in item.get("author", []):
        given = author.get("given", "").strip()
        family = author.get("family", "").strip()
        name = " ".join(part for part in [given, family] if part).strip()
        if name:
            authors.append(name)
    return authors


def within_window(date_value: str | None, window: dict[str, str]) -> bool:
    if not date_value:
        return False
    return window["from"] <= date_value <= window["to"]
