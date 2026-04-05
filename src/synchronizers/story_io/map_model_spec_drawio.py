"""
map-model-spec.json → Draw.io UML class diagram (native mxfile).

Delegates to vendored ``uml_drawio.model_to_drawio`` (``CLASS_STYLE`` / ``build_class_html``),
not story-map epic/sub-epic styling.
"""
from __future__ import annotations

from .uml_drawio.model_to_drawio import map_model_spec_to_drawio_xml, write_map_model_class_diagram

__all__ = ["map_model_spec_to_drawio_xml", "write_map_model_class_diagram"]
