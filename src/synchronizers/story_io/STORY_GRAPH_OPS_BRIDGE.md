# DrawIO story_io ↔ story-graph-ops

## Dependency direction

- **This package** (`synchronizers/story_io`): DrawIO load/render/extract, **`DrawIOStoryMap.generate_update_report`**, and `UpdateReport` serialization.
- **story-graph-ops** (agilebydesign-skills `skills/story-graph-ops/scripts/story_graph_ops/`): vendored **`StoryMap`**, **`UpdateReport`**, **`StoryMapUpdater.update_from_report`** — applies a report to `story-graph.json` **without** reading `.drawio` files.

story-graph-ops **must not** import synchronizers or DrawIO parsers. After a report exists, tooling may call **`StoryMap.apply_update_report`** (or `StoryMapUpdater`) from story-graph-ops, or use the **drawio-story-sync** CLI `apply-report`.

## agile_bots vs skills

| Step | Where |
| --- | --- |
| Render / extract / `generate_update_report` | agile_bots `DrawIOStoryMap` or **drawio-story-sync** vendored copy |
| Validated JSON load (optional) | **story-graph-ops** `story_graph_file.load_story_graph_dict` when `skills/story-graph-ops/scripts` is on `PYTHONPATH` (see `story_io_synchronizer.load_story_graph_json`) |
| Apply report to disk | **story-graph-ops** `StoryMap.from_json_file` + `apply_update_report` + `save`, or **drawio-story-sync** `drawio_story_sync_cli.py apply-report` |

## Scoping

Bot **Scope** / **StoryGraphFilter** (agile_bots `src/scope/scope.py`) filters dicts before building **`StoryGraph`**. The same filter logic is vendored for standalone tools as **`story_graph_ops.story_graph_scope`** (`StoryGraphScope`, `StoryGraphFilter`, `ScopeType`, `FileFilter`) so CLIs and scanners can narrow graphs without a full bot.
