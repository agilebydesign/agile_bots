"""
DrawIO Synchronizer

Uses the DrawIOStoryMap domain model for rendering. Extraction and
merge operations delegate to story_map_drawio_synchronizer functions.
"""

from pathlib import Path
from typing import Dict, Any, Optional, Union
import json

from .story_map_drawio_synchronizer import (
    synchronize_story_graph_from_drawio_outline,
    synchronize_story_graph_from_drawio_increments,
    generate_merge_report,
    merge_story_graphs
)


class DrawIOSynchronizer:
    """Synchronizer for story diagrams using the DrawIOStoryMap domain model."""

    def render(self, input_path: Union[str, Path], output_path: Union[str, Path],
               renderer_command: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        from .drawio_story_map import DrawIOStoryMap
        from .layout_data import LayoutData
        from story_graph.nodes import StoryMap

        input_path = Path(input_path)
        output_path = Path(output_path)

        # Load story graph
        with open(input_path, 'r', encoding='utf-8') as f:
            graph_data = json.load(f)

        story_map = StoryMap(graph_data)

        # Load layout data if it exists alongside the output
        layout_path = output_path.parent / f"{output_path.stem}-layout.json"
        layout_data = LayoutData.load(layout_path) if layout_path.exists() else None

        # Render via domain model
        drawio_map = DrawIOStoryMap()

        if renderer_command == 'render-increments':
            increments = graph_data.get('increments', [])
            summary = drawio_map.render_increments_from_story_map(
                story_map, increments, layout_data)
        elif renderer_command == 'render-exploration':
            scope = kwargs.get('scope')
            summary = drawio_map.render_exploration_from_story_map(
                story_map, layout_data, scope=scope)
        else:
            summary = drawio_map.render_from_story_map(story_map, layout_data)

        # Save diagram
        output_path.parent.mkdir(parents=True, exist_ok=True)
        drawio_map.save(output_path)

        # Save layout data for future re-renders
        layout = drawio_map.extract_layout()
        layout.save(output_path.parent / f"{output_path.stem}-layout.json")

        return {
            "output_path": str(output_path),
            "summary": summary,
        }

    def synchronize_outline(self, drawio_path: Path,
                           original_path: Optional[Path] = None,
                           output_path: Optional[Path] = None) -> Dict[str, Any]:
        if output_path is None:
            output_path = drawio_path.parent / "story-graph-drawio-extracted.json"

        return synchronize_story_graph_from_drawio_outline(
            drawio_path=drawio_path,
            output_path=output_path,
            original_path=original_path
        )

    def synchronize_increments(self, drawio_path: Path,
                              original_path: Optional[Path] = None,
                              output_path: Optional[Path] = None) -> Dict[str, Any]:
        if output_path is None:
            output_path = drawio_path.parent / "story-graph-drawio-extracted.json"

        return synchronize_story_graph_from_drawio_increments(
            drawio_path=drawio_path,
            output_path=output_path,
            original_path=original_path
        )

    def generate_merge_report(self, extracted_path: Union[str, Path],
                              original_path: Union[str, Path],
                              report_path: Optional[Union[str, Path]] = None) -> Dict[str, Any]:
        extracted_path = Path(extracted_path)
        original_path = Path(original_path)
        if report_path:
            report_path = Path(report_path)

        return generate_merge_report(extracted_path, original_path, report_path)

    def merge_story_graphs(self, extracted_path: Union[str, Path],
                          original_path: Union[str, Path],
                          report_path: Union[str, Path],
                          output_path: Union[str, Path]) -> Dict[str, Any]:
        extracted_path = Path(extracted_path)
        original_path = Path(original_path)
        report_path = Path(report_path)
        output_path = Path(output_path)

        return merge_story_graphs(extracted_path, original_path, report_path, output_path)
