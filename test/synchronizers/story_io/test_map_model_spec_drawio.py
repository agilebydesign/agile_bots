"""Smoke tests for map-model-spec → Draw.io XML."""
import json
from pathlib import Path

from synchronizers.story_io.map_model_spec_drawio import (
    map_model_spec_to_drawio_xml,
    write_map_model_class_diagram,
)


def test_minimal_spec_emits_mxfile_and_edges():
    spec = {
        "modules_and_epics": [
            {
                "module": {
                    "name": "ModA",
                    "concepts": [
                        {
                            "name": "Foo",
                            "properties": [],
                            "operations": [
                                {
                                    "name": "run",
                                    "depends_on": [{"concept": "Bar"}],
                                }
                            ],
                        },
                        {"name": "Bar", "properties": [], "operations": []},
                    ],
                }
            }
        ]
    }
    xml = map_model_spec_to_drawio_xml(spec)
    assert 'host="app.diagrams.net"' in xml
    assert "mm-edge-0" in xml
    assert "mm/ModA/Foo" in xml and "mm/ModA/Bar" in xml


def test_write_roundtrip_tmp_path(tmp_path: Path):
    spec = {
        "modules_and_epics": [
            {"module": {"name": "M", "concepts": [{"name": "X", "properties": [], "operations": []}]}}
        ]
    }
    inp = tmp_path / "map-model-spec.json"
    inp.write_text(json.dumps(spec), encoding="utf-8")
    out = tmp_path / "out.drawio"
    write_map_model_class_diagram(inp, out)
    assert out.is_file()
    body = out.read_text(encoding="utf-8")
    assert "<mxfile" in body
