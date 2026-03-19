# Revision Brief Schema

Use this schema when converting review comments into a revision plan.

## Minimal shape

```json
{
  "language": "en",
  "comments": [
    {
      "id": "R1-C1",
      "text": "The novelty relative to existing grounded writing systems is unclear.",
      "severity": "major",
      "source": "reviewer-1"
    }
  ],
  "manuscript_status": "under review",
  "target_venue": "conference",
  "deadline": "2026-04-15",
  "constraints": [
    "No time for new large-scale user study",
    "Can add clarifying ablations and stronger positioning"
  ]
}
```

## Field rules

- `language`: output language for the revision plan, for example `zh-CN` or `en`.
- `comments`: normalized review items, one issue per item.
- `manuscript_status`: for example `draft`, `under review`, `revision requested`, or `camera ready`.
- `target_venue`: optional, but useful for tone and expectations.
- `deadline`: optional date or milestone label.
- `constraints`: practical limits on experiments, data, or rewrite scope.
