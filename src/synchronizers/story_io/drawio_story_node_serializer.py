"""
DrawIOStoryNodeSerializer - Creates, loads, and writes DrawIO story nodes to XML.
"""
import xml.etree.ElementTree as ET
from typing import Optional, List
from .drawio_element import DrawIOElement
from .drawio_story_node import DrawIOStoryNode, DrawIOEpic, DrawIOSubEpic, DrawIOStory
from .story_io_position import Position, Boundary


class DrawIOStoryNodeSerializer:

    @staticmethod
    def create_epic(name: str, sequential_order: float = 0.0) -> DrawIOEpic:
        return DrawIOEpic(name=name, sequential_order=sequential_order, domain_concepts=[])

    @staticmethod
    def create_sub_epic(name: str, sequential_order: float = 0.0) -> DrawIOSubEpic:
        return DrawIOSubEpic(name=name, sequential_order=sequential_order, domain_concepts=[])

    @staticmethod
    def create_story(name: str, sequential_order: float = 0.0,
                     story_type: str = None) -> DrawIOStory:
        return DrawIOStory(name=name, sequential_order=sequential_order,
                           story_type=story_type or 'user')

    @staticmethod
    def create_actor(name: str) -> DrawIOElement:
        element = DrawIOElement(cell_id=f'actor-{name.lower().replace(" ", "-")}', value=name)
        element.apply_style_for_type('actor')
        return element

    @staticmethod
    def to_mx_cell(node) -> ET.Element:
        cell = ET.Element('mxCell')
        if isinstance(node, DrawIOStoryNode):
            cell.set('id', node.cell_id)
            cell.set('value', node.name)
            cell.set('style', node.element.to_style_string())
            boundary = node.boundary
        else:
            cell.set('id', node.cell_id)
            cell.set('value', node.value)
            cell.set('style', node.to_style_string())
            boundary = node.boundary
        cell.set('vertex', '1')
        cell.set('parent', '1')
        geometry = ET.SubElement(cell, 'mxGeometry')
        geometry.set('x', str(node.position.x))
        geometry.set('y', str(node.position.y))
        geometry.set('width', str(boundary.width))
        geometry.set('height', str(boundary.height))
        geometry.set('as', 'geometry')
        return cell

    @staticmethod
    def from_mx_cell(cell: ET.Element) -> Optional[DrawIOStoryNode]:
        cell_id = cell.get('id', '')
        value = cell.get('value', '')
        style = cell.get('style', '')
        geometry = cell.find('mxGeometry')
        if geometry is None:
            return None
        x = float(geometry.get('x', '0'))
        y = float(geometry.get('y', '0'))
        width = float(geometry.get('width', '0'))
        height = float(geometry.get('height', '0'))
        style_dict = DrawIOElement.from_style_string(style)
        fill_color = style_dict.get('fillColor', '')
        node = DrawIOStoryNodeSerializer._classify_node(value, fill_color)
        if node:
            node._element._cell_id = cell_id
            node.set_position(x, y)
            node.set_size(width, height)
        return node

    @staticmethod
    def _classify_node(value: str, fill_color: str) -> Optional[DrawIOStoryNode]:
        if fill_color == '#e1d5e7':
            return DrawIOStoryNodeSerializer.create_epic(value, 0)
        elif fill_color == '#d5e8d4':
            return DrawIOStoryNodeSerializer.create_sub_epic(value, 0)
        elif fill_color in ('#fff2cc', '#1a237e', '#000000'):
            story_type = 'user'
            if fill_color == '#1a237e':
                story_type = 'system'
            elif fill_color == '#000000':
                story_type = 'technical'
            return DrawIOStoryNodeSerializer.create_story(value, 0, story_type)
        return None

    @staticmethod
    def to_drawio_xml(nodes: list) -> str:
        mxfile = ET.Element('mxfile')
        mxfile.set('host', 'app.diagrams.net')
        diagram = ET.SubElement(mxfile, 'diagram')
        diagram.set('name', 'Story Map')
        diagram.set('id', 'story-map')
        model = ET.SubElement(diagram, 'mxGraphModel')
        root = ET.SubElement(model, 'root')
        ET.SubElement(root, 'mxCell').set('id', '0')
        parent_cell = ET.SubElement(root, 'mxCell')
        parent_cell.set('id', '1')
        parent_cell.set('parent', '0')
        for node in nodes:
            root.append(DrawIOStoryNodeSerializer.to_mx_cell(node))
        return ET.tostring(mxfile, encoding='unicode', xml_declaration=True)

    @staticmethod
    def parse_nodes_from_xml(xml_content: str) -> List[DrawIOStoryNode]:
        tree = ET.fromstring(xml_content)
        nodes = []
        for cell in tree.iter('mxCell'):
            if cell.get('vertex') == '1':
                node = DrawIOStoryNodeSerializer.from_mx_cell(cell)
                if node:
                    nodes.append(node)
        return nodes
