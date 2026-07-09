# PaperSkills Registry

This directory is the public source of truth for PaperSkills skill metadata.

- `skills.json` lists the core open-source skills and their install paths.
- `packs.json` defines reusable skill bundles that can be installed together.
- `scenarios.json` defines public research workflows and suggested skill sequences.
- `academicforge-skills.json` mirrors the latest AcademicForge catalog.
- `academicforge-overrides.json` stores PaperSkills-specific aliases and
  scenario metadata for curated AcademicForge skills.

## Skill Collection Layout

PaperSkills follows the same collection shape as AcademicForge:

```text
skills/
  paperskills-core/
    topic-framing/
      SKILL.md
    lit-search/
      SKILL.md
```

`skills/paperskills-core` is the PaperSkills-maintained collection, comparable
to AcademicForge's `skills/claude-science`. Each entry in `skills.json` should
point its `install.sparsePath` to a concrete sub-skill directory such as
`skills/paperskills-core/lit-search`.

The private website consumes these files through its `external/paperskills`
submodule. Website-only presentation settings, private experiments, and external
catalog snapshots should stay in `paperskills-web`.
