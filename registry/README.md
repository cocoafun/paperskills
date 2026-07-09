# PaperSkills Registry

This directory is the public source of truth for PaperSkills skill metadata.

- `skills.json` lists the core open-source skills and their install paths.
- `packs.json` defines reusable skill bundles that can be installed together.
- `scenarios.json` defines public research workflows and suggested skill sequences.

The private website consumes these files through its `external/paperskills`
submodule. Website-only presentation settings, private experiments, and external
catalog snapshots should stay in `paperskills-web`.

