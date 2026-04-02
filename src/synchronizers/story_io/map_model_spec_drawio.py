"""
map-model-spec.json → native Draw.io XML (diagrams.net).

Uses the same mxfile / mxCell pipeline as DrawIOStoryNodeSerializer.to_drawio_xml,
with orthogonal edges for depends_on relationships.
"""
from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from .drawio_element import DrawIOElement
from .drawio_story_node_serializer import DrawIOStoryNodeSerializer


def _slug(s: str) -> str:
    s = re.sub(r"[^0-9a-zA-Z_]+", "-", (s or "").strip())
    s = re.sub(r"-+", "-", s).strip("-")
    return s or "x"


def _depends_targets(obj: dict[str, Any]) -> list[str]:
    out: list[str] = []
    for d in obj.get("depends_on") or []:
        if isinstance(d, dict):
            c = d.get("concept")
            if c:
                out.append(str(c))
    return out


def _collect_concept_edges(spec: dict[str, Any]) -> tuple[set[str], set[tuple[str, str]]]:
    concept_names: set[str] = set()
    edges: set[tuple[str, str]] = set()

    for row in spec.get("modules_and_epics") or []:
        mod = row.get("module") or {}
        for c in mod.get("concepts") or []:
            if not isinstance(c, dict):
                continue
            cn = c.get("name")
            if not cn:
                continue
            cn = str(cn)
            concept_names.add(cn)
            for tgt in _depends_targets(c):
                edges.add((cn, tgt))
            for p in c.get("properties") or []:
                if isinstance(p, dict):
                    for tgt in _depends_targets(p):
                        edges.add((cn, tgt))
            for o in c.get("operations") or []:
                if isinstance(o, dict):
                    for tgt in _depends_targets(o):
                        edges.add((cn, tgt))
    return concept_names, edges


def _format_concept_value(c: dict[str, Any]) -> tuple[str, float]:
    """Cell label and suggested min height."""
    name = str(c.get("name") or "?")
    lines: list[str] = [name]
    for p in (c.get("properties") or [])[:10]:
        if isinstance(p, dict) and p.get("name"):
            lines.append(f"+ {p['name']}: {p.get('type') or '?'}")
    for o in (c.get("operations") or [])[:10]:
        if isinstance(o, dict) and o.get("name"):
            lines.append(f"+ {o['name']}()")
    text = "\n".join(lines)
    h = max(52.0, 16.0 * len(lines) + 24.0)
    return text, h


def _concept_cell_id(module_name: str, concept_name: str) -> str:
    return f"mm/{_slug(module_name)}/{_slug(concept_name)}"


def _mx_edge(edge_id: str, source: str, target: str) -> ET.Element:
    cell = ET.Element("mxCell")
    cell.set("id", edge_id)
    cell.set(
        "style",
        "edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=classic;strokeColor=#666666;",
    )
    cell.set("edge", "1")
    cell.set("parent", "1")
    cell.set("source", source)
    cell.set("target", target)
    geom = ET.SubElement(cell, "mxGeometry")
    geom.set("relative", "1")
    geom.set("as", "geometry")
    return cell


def map_model_spec_to_elements_and_edges(
    spec: dict[str, Any],
) -> tuple[list[DrawIOElement], list[tuple[str, str, str]]]:
    """
    Build DrawIO vertex elements and edge triples (edge_id, source_cell_id, target_cell_id).

    Layout: per module, a module title (epic style) then a grid of concept boxes (sub_epic style).
    """
    vertices: list[DrawIOElement] = []
    edge_specs: list[tuple[str, str, str]] = []

    concept_names, raw_edges = _collect_concept_edges(spec)
    name_to_cell: dict[str, str] = {}

    COLS = 3
    BOX_W = 260.0
    GAP = 20.0
    x0 = 40.0
    y = 40.0

    for row in spec.get("modules_and_epics") or []:
        mod = row.get("module") or {}
        mname = str(mod.get("name") or "Module")
        concepts = [c for c in (mod.get("concepts") or []) if isinstance(c, dict) and c.get("name")]

        row_cols = min(COLS, max(1, len(concepts)))
        block_width = row_cols * (BOX_W + GAP) - GAP

        mod_cell = DrawIOElement(cell_id=f"mm-mod/{_slug(mname)}", value=mname)
        mod_cell.apply_style_for_type("epic")
        mod_cell.set_position(x0, y)
        mod_cell.set_size(block_width, 48.0)
        vertices.append(mod_cell)
        y += 48.0 + GAP

        col = 0
        row_max_h = 0.0
        row_y = y
        for c in concepts:
            cn = str(c["name"])
            cid = _concept_cell_id(mname, cn)
            name_to_cell[cn] = cid
            val, ch = _format_concept_value(c)
            cw = min(320.0, max(160.0, 7.5 * max(len(line) for line in val.split("\n")) + 24.0))
            el = DrawIOElement(cell_id=cid, value=val)
            el.apply_style_for_type("sub_epic")
            x = x0 + col * (BOX_W + GAP)
            el.set_position(x, row_y)
            el.set_size(cw, ch)
            vertices.append(el)
            row_max_h = max(row_max_h, ch)
            col += 1
            if col >= COLS:
                col = 0
                row_y += row_max_h + GAP
                row_max_h = 0.0

        if col > 0:
            row_y += row_max_h + GAP
        y = row_y + 24.0

    ei = 0
    for a, b in sorted(raw_edges):
        if a not in concept_names or b not in concept_names:
            continue
        sa = name_to_cell.get(a)
        ta = name_to_cell.get(b)
        if not sa or not ta:
            continue
        edge_specs.append((f"mm-edge-{ei}", sa, ta))
        ei += 1

    return vertices, edge_specs


def map_model_spec_to_drawio_xml(spec: dict[str, Any]) -> str:
    vertices, edges = map_model_spec_to_elements_and_edges(spec)

    mxfile = ET.Element("mxfile")
    mxfile.set("host", "app.diagrams.net")
    diagram = ET.SubElement(mxfile, "diagram")
    diagram.set("name", "Map Model Class")
    diagram.set("id", "map-model-class")
    model = ET.SubElement(diagram, "mxGraphModel")
    root = ET.SubElement(model, "root")
    ET.SubElement(root, "mxCell").set("id", "0")
    parent_cell = ET.SubElement(root, "mxCell")
    parent_cell.set("id", "1")
    parent_cell.set("parent", "0")

    for node in vertices:
        root.append(DrawIOStoryNodeSerializer.to_mx_cell(node))
    for eid, src, tgt in edges:
        root.append(_mx_edge(eid, src, tgt))

    return ET.tostring(mxfile, encoding="unicode", xml_declaration=True)


def write_map_model_class_diagram(spec_path: Path, out_path: Path) -> None:
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    xml = map_model_spec_to_drawio_xml(spec)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(xml, encoding="utf-8")
