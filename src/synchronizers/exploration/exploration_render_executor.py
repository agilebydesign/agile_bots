"""
Exploration render executor.

Processes exploration behavior render configs: template-based (render_story_exploration,
render_story_map) and synchronizer-based (render_exploration_acceptance_criteria_drawio,
render_story_exploration_drawio).

Priority: synchronizer > template (per exploration action instructions).
"""
import importlib
import json
from pathlib import Path
from typing import Any, Dict, List

from .story_exploration_md_renderer import render_all_increment_explorations
from .story_map_txt_renderer import render_story_map_txt


def _load_render_configs(render_dir: Path) -> List[Dict[str, Any]]:
    """Load all render_*.json configs from behavior content/render."""
    configs = []
    if not render_dir.exists():
        return configs

    for f in sorted(render_dir.glob("render_*.json")):
        try:
            content = f.read_text(encoding="utf-8")
            # Handle both .json and .md.json / _txt.json suffixes
            data = json.loads(content)
            configs.append(data)
        except (json.JSONDecodeError, OSError):
            continue
    return configs


def _is_synchronizer_config(config: Dict[str, Any]) -> bool:
    """Check if config uses a synchronizer."""
    return "synchronizer" in config


def _is_template_config(config: Dict[str, Any]) -> bool:
    """Check if config uses a template."""
    return "template" in config


def _run_synchronizer(
    config: Dict[str, Any],
    workspace_root: Path,
    story_graph_path: Path,
) -> Dict[str, Any]:
    """Execute synchronizer-based render."""
    module_path = config.get("synchronizer", "")
    renderer_command = config.get("renderer_command", "render-exploration")
    output_pattern = config.get("output", "story-map-explored.drawio")
    path_rel = config.get("path", "docs/story/exploration")
    params = config.get("parameters", {})

    # Resolve paths - story graph as input
    input_path = story_graph_path
    output_dir = workspace_root / path_rel
    output_dir.mkdir(parents=True, exist_ok=True)

    # Resolve output filename (may have {scope} placeholder)
    scope = params.get("scope", "outline")
    if scope == "{scope}":
        scope = "outline"
    output_name = output_pattern.replace("{scope}", scope)
    output_path = output_dir / output_name

    # Dynamic import synchronizer
    module_name, class_name = module_path.rsplit(".", 1)
    mod = importlib.import_module(module_name)
    sync_class = getattr(mod, class_name)
    synchronizer = sync_class()

    result = synchronizer.render(
        input_path=input_path,
        output_path=output_path,
        renderer_command=renderer_command,
        scope=params.get("scope"),
    )
    return {"config": config.get("name"), "result": result, "output_path": str(output_path)}


def _run_template_render_story_map(
    config: Dict[str, Any],
    workspace_root: Path,
    story_graph_path: Path,
    behavior_render_dir: Path,
) -> Path:
    """Execute render_story_map template."""
    path_rel = config.get("path", "docs/story/exploration")
    template_name = config.get("template", "story-map.txt")
    output_name = config.get("output", "story-map.txt")

    template_path = behavior_render_dir / "templates" / template_name
    output_path = workspace_root / path_rel / output_name

    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")

    render_story_map_txt(story_graph_path, output_path)
    return output_path


def _run_template_render_story_exploration(
    config: Dict[str, Any],
    workspace_root: Path,
    story_graph_path: Path,
    behavior_render_dir: Path,
) -> List[Path]:
    """Execute render_story_exploration template (per increment)."""
    path_rel = config.get("path", "docs/story/exploration")
    template_name = config.get("template", "story-exploration.md")
    output_pattern = config.get("output", "{increment_name_slug}-exploration.md")

    template_path = behavior_render_dir / "templates" / template_name
    output_dir = workspace_root / path_rel

    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")

    return render_all_increment_explorations(
        story_graph_path=story_graph_path,
        template_path=template_path,
        output_dir=output_dir,
    )


class ExplorationRenderExecutor:
    """
    Executes exploration render configs.

    Processes template configs (render_story_exploration, render_story_map) and
    synchronizer configs (render_exploration_acceptance_criteria_drawio,
    render_story_exploration_drawio).
    """

    def __init__(
        self,
        workspace_root: Path,
        story_graph_path: Path,
        behavior_render_dir: Path,
    ):
        """
        Args:
            workspace_root: Workspace root (e.g. agile_bots)
            story_graph_path: Path to story-graph.json
            behavior_render_dir: Path to exploration content/render (contains configs + templates)
        """
        self.workspace_root = Path(workspace_root)
        self.story_graph_path = Path(story_graph_path)
        self.behavior_render_dir = Path(behavior_render_dir)

    def render_all(self) -> Dict[str, Any]:
        """
        Process all render configs. Priority: synchronizer > template.

        Returns:
            Summary dict with outputs, errors, created paths
        """
        configs = _load_render_configs(self.behavior_render_dir)
        synchronizer_configs = [c for c in configs if _is_synchronizer_config(c)]
        template_configs = [c for c in configs if _is_template_config(c)]

        created: List[str] = []
        errors: List[Dict[str, str]] = []

        # 1. Run synchronizers first (priority)
        for config in synchronizer_configs:
            name = config.get("name", "unknown")
            try:
                result = _run_synchronizer(
                    config=config,
                    workspace_root=self.workspace_root,
                    story_graph_path=self.story_graph_path,
                )
                out_path = result.get("output_path", "")
                if out_path:
                    created.append(out_path)
            except Exception as e:
                errors.append({"config": name, "error": str(e)})

        # 2. Run template configs
        for config in template_configs:
            name = config.get("name", "unknown")
            try:
                if name == "render_story_map":
                    out_path = _run_template_render_story_map(
                        config=config,
                        workspace_root=self.workspace_root,
                        story_graph_path=self.story_graph_path,
                        behavior_render_dir=self.behavior_render_dir,
                    )
                    created.append(str(out_path))
                elif name == "render_story_exploration":
                    out_paths = _run_template_render_story_exploration(
                        config=config,
                        workspace_root=self.workspace_root,
                        story_graph_path=self.story_graph_path,
                        behavior_render_dir=self.behavior_render_dir,
                    )
                    created.extend(str(p) for p in out_paths)
                else:
                    errors.append({"config": name, "error": f"Unknown template config: {name}"})
            except Exception as e:
                errors.append({"config": name, "error": str(e)})

        return {
            "created": created,
            "errors": errors,
            "summary": f"Created {len(created)} output(s), {len(errors)} error(s)",
        }
