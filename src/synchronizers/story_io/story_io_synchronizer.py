from pathlib import Path
from typing import Dict, Any, Optional, Union
import json


class DrawIOSynchronizer:

    def render(self, input_path: Union[str, Path], output_path: Union[str, Path],
               renderer_command: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        from .drawio_story_map import DrawIOStoryMap
        from .layout_data import LayoutData
        from story_graph.nodes import StoryMap

        input_path = Path(input_path)
        output_path = Path(output_path)

        with open(input_path, 'r', encoding='utf-8') as f:
            graph_data = json.load(f)

        story_map = StoryMap(graph_data)

        scope = kwargs.get('scope')
        if scope:
            filtered = story_map.filter_by_name(scope)
            if filtered is not None:
                story_map = filtered

        layout_path = output_path.parent / f"{output_path.stem}-layout.json"
        layout_data = LayoutData.load(layout_path) if layout_path.exists() else None

        drawio_map = DrawIOStoryMap()

        if renderer_command == 'render-increments':
            increments = graph_data.get('increments', [])
            summary = drawio_map.render_increments_from_story_map(
                story_map, increments, layout_data)
        elif renderer_command == 'render-exploration':
            summary = drawio_map.render_exploration_from_story_map(
                story_map, layout_data)
        else:
            summary = drawio_map.render_from_story_map(story_map, layout_data)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        drawio_map.save(output_path)

        return {
            "output_path": str(output_path),
            "summary": summary,
        }

    def save_layout(self, drawio_path: Union[str, Path]) -> Dict[str, Any]:
        from .drawio_story_map import DrawIOStoryMap

        drawio_path = Path(drawio_path)
        if not drawio_path.exists():
            return {"status": "error", "message": f"File not found: {drawio_path}"}

        drawio_map = DrawIOStoryMap.load(drawio_path)
        layout = drawio_map.extract_layout()
        layout_path = drawio_path.parent / f"{drawio_path.stem}-layout.json"
        layout.save(layout_path)

        return {"status": "success", "layout_path": str(layout_path)}
