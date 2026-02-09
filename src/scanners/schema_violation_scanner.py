"""
Schema Violation Scanner

Detects fields in story-graph.json that are not defined in the behavior's template.
This ensures that when building during a specific phase (e.g., shaping), 
only fields defined in that phase's template are added.

Edge case handling:
- Existing fields from previous phases are not flagged as violations
- Only NEW or EDITED fields that don't conform to template are flagged
"""

from pathlib import Path
from typing import Dict, Any, List, Optional, Set
import logging

logger = logging.getLogger(__name__)


class SchemaViolation:
    """Represents a single schema violation."""
    
    def __init__(
        self,
        path: str,
        field_name: str,
        message: str,
        severity: str = 'error'
    ):
        self.path = path
        self.field_name = field_name
        self.message = message
        self.severity = severity
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'path': self.path,
            'field_name': self.field_name,
            'message': self.message,
            'severity': self.severity
        }


class SchemaViolationScanner:
    """
    Scans story graph for fields that violate the behavior's template schema.
    
    This scanner compares the actual story-graph.json against the template
    defined for the current behavior and reports any extra fields.
    """
    
    # Fields that are always allowed (meta/explanation fields)
    ALWAYS_ALLOWED_FIELDS = {'_explanation', '_meta', '_comment'}
    
    def __init__(self, behavior, bot_paths):
        self.behavior = behavior
        self.bot_paths = bot_paths
        self._template_schema: Optional[Dict[str, Any]] = None
        self._template_path: Optional[Path] = None
    
    def get_template_for_behavior(self) -> Optional[Dict[str, Any]]:
        """Load the template schema for the current behavior."""
        if self._template_schema is not None:
            return self._template_schema
        
        behavior_name = self.behavior.name if hasattr(self.behavior, 'name') else str(self.behavior)
        
        # Find the content/story_graph directory for the behavior
        sg_dir = (
            self.bot_paths.bot_directory / 
            'behaviors' / 
            behavior_name / 
            'content' / 
            'story_graph'
        )
        
        if not sg_dir.exists():
            logger.info(f"No story_graph content directory found for behavior '{behavior_name}'")
            return None
        
        # Find the build config to get the template filename
        build_config_files = list(sg_dir.glob('build*.json'))
        if not build_config_files:
            logger.info(f"No build config found in {sg_dir}")
            return None
        
        from utils import read_json_file
        build_config = read_json_file(build_config_files[0])
        template_filename = build_config.get('template')
        
        if not template_filename:
            logger.info(f"No template specified in build config for behavior '{behavior_name}'")
            return None
        
        # Load the template
        template_path = sg_dir / template_filename
        if not template_path.exists():
            logger.warning(f"Template file not found: {template_path}")
            return None
        
        self._template_path = template_path
        self._template_schema = read_json_file(template_path)
        logger.info(f"Loaded template schema from: {template_path}")
        
        return self._template_schema
    
    def extract_allowed_fields(self, template: Dict[str, Any], path: str = '') -> Dict[str, Set[str]]:
        """
        Extract allowed field names at each level of the template.
        
        Returns a dict mapping path patterns to sets of allowed field names.
        """
        allowed_fields: Dict[str, Set[str]] = {}
        
        if not isinstance(template, dict):
            return allowed_fields
        
        # Get fields at current level
        current_fields = set(template.keys()) | self.ALWAYS_ALLOWED_FIELDS
        allowed_fields[path or 'root'] = current_fields
        
        # Recursively process nested structures
        for key, value in template.items():
            if key.startswith('_'):
                continue  # Skip meta fields
            
            new_path = f"{path}.{key}" if path else key
            
            if isinstance(value, dict):
                nested = self.extract_allowed_fields(value, new_path)
                allowed_fields.update(nested)
            elif isinstance(value, list) and value:
                # For arrays, check the first element as the template
                first_elem = value[0]
                if isinstance(first_elem, dict):
                    array_path = f"{new_path}[]"
                    nested = self.extract_allowed_fields(first_elem, array_path)
                    allowed_fields.update(nested)
        
        return allowed_fields
    
    def _get_path_pattern(self, path: str) -> str:
        """Convert a specific path to a pattern for matching against template."""
        import re
        # Replace numeric indices with []
        pattern = re.sub(r'\[\d+\]', '[]', path)
        return pattern
    
    def scan_for_violations(
        self,
        story_graph: Dict[str, Any],
        template: Dict[str, Any],
        baseline: Optional[Dict[str, Any]] = None
    ) -> List[SchemaViolation]:
        """
        Scan story graph for schema violations.
        
        Args:
            story_graph: The current story-graph.json content
            template: The template schema for the behavior
            baseline: Optional previous version of story-graph for incremental checking
        
        Returns:
            List of SchemaViolation objects
        """
        violations = []
        
        # Extract allowed fields from template
        allowed_fields_by_path = self.extract_allowed_fields(template)
        
        # Also extract baseline fields if provided (for edge case handling)
        baseline_fields_by_path: Dict[str, Set[str]] = {}
        if baseline:
            baseline_fields_by_path = self._extract_existing_fields(baseline)
        
        # Scan the story graph recursively
        self._scan_node(
            node=story_graph,
            template_node=template,
            path='',
            allowed_fields_by_path=allowed_fields_by_path,
            baseline_fields_by_path=baseline_fields_by_path,
            violations=violations
        )
        
        return violations
    
    def _extract_existing_fields(self, data: Dict[str, Any], path: str = '') -> Dict[str, Set[str]]:
        """Extract all fields that exist in the baseline data."""
        existing: Dict[str, Set[str]] = {}
        
        if not isinstance(data, dict):
            return existing
        
        pattern = self._get_path_pattern(path) or 'root'
        if pattern not in existing:
            existing[pattern] = set()
        existing[pattern].update(data.keys())
        
        for key, value in data.items():
            new_path = f"{path}.{key}" if path else key
            
            if isinstance(value, dict):
                nested = self._extract_existing_fields(value, new_path)
                for p, fields in nested.items():
                    if p not in existing:
                        existing[p] = set()
                    existing[p].update(fields)
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    if isinstance(item, dict):
                        item_path = f"{new_path}[{i}]"
                        nested = self._extract_existing_fields(item, item_path)
                        for p, fields in nested.items():
                            if p not in existing:
                                existing[p] = set()
                            existing[p].update(fields)
        
        return existing
    
    def _scan_node(
        self,
        node: Any,
        template_node: Any,
        path: str,
        allowed_fields_by_path: Dict[str, Set[str]],
        baseline_fields_by_path: Dict[str, Set[str]],
        violations: List[SchemaViolation]
    ):
        """Recursively scan a node for schema violations."""
        if not isinstance(node, dict):
            return
        
        path_pattern = self._get_path_pattern(path) or 'root'
        
        # Get allowed fields for this path
        allowed_fields = allowed_fields_by_path.get(path_pattern, set())
        
        # Get baseline fields for this path (fields that existed before)
        baseline_fields = baseline_fields_by_path.get(path_pattern, set())
        
        # Get template fields (to determine what's expected at this level)
        template_fields = set()
        if isinstance(template_node, dict):
            template_fields = set(template_node.keys())
        
        # Check each field in the current node
        for field_name, field_value in node.items():
            # Skip always-allowed fields
            if field_name in self.ALWAYS_ALLOWED_FIELDS:
                continue
            
            field_path = f"{path}.{field_name}" if path else field_name
            
            # Check if field is allowed by template
            is_in_template = field_name in allowed_fields or field_name in template_fields
            
            # Check if field existed in baseline (edge case: re-shaping existing content)
            is_in_baseline = field_name in baseline_fields
            
            if not is_in_template and not is_in_baseline:
                # This is a violation - field not in template and not pre-existing
                violations.append(SchemaViolation(
                    path=field_path,
                    field_name=field_name,
                    message=f"Field '{field_name}' at '{field_path}' is not defined in the template schema. "
                           f"Only fields from the template are allowed during this phase.",
                    severity='error'
                ))
            
            # Recursively scan nested structures
            if isinstance(field_value, dict):
                nested_template = template_node.get(field_name) if isinstance(template_node, dict) else None
                self._scan_node(
                    node=field_value,
                    template_node=nested_template or {},
                    path=field_path,
                    allowed_fields_by_path=allowed_fields_by_path,
                    baseline_fields_by_path=baseline_fields_by_path,
                    violations=violations
                )
            elif isinstance(field_value, list):
                # Get template for array items
                array_template = None
                if isinstance(template_node, dict) and field_name in template_node:
                    template_array = template_node[field_name]
                    if isinstance(template_array, list) and template_array:
                        array_template = template_array[0]
                
                for i, item in enumerate(field_value):
                    if isinstance(item, dict):
                        self._scan_node(
                            node=item,
                            template_node=array_template or {},
                            path=f"{field_path}[{i}]",
                            allowed_fields_by_path=allowed_fields_by_path,
                            baseline_fields_by_path=baseline_fields_by_path,
                            violations=violations
                        )
    
    def scan(self, story_graph_content: Dict[str, Any], baseline: Optional[Dict[str, Any]] = None) -> List[SchemaViolation]:
        """
        Main entry point: scan story graph for schema violations.
        
        Args:
            story_graph_content: The story-graph.json content to validate
            baseline: Optional previous version for incremental checking
        
        Returns:
            List of SchemaViolation objects
        """
        template = self.get_template_for_behavior()
        
        if not template:
            logger.info(f"No template found for behavior '{self.behavior.name}', skipping schema validation")
            return []
        
        return self.scan_for_violations(story_graph_content, template, baseline)
    
    def format_violations(self, violations: List[SchemaViolation]) -> List[str]:
        """Format violations for display in the validation report."""
        if not violations:
            return []
        
        lines = [
            "## Schema Violations",
            "",
            f"Found {len(violations)} field(s) that violate the template schema:",
            ""
        ]
        
        for i, v in enumerate(violations, 1):
            lines.append(f"**{i}. {v.field_name}**")
            lines.append(f"   - Path: `{v.path}`")
            lines.append(f"   - Severity: {v.severity}")
            lines.append(f"   - {v.message}")
            lines.append("")
        
        template_info = f"Template: `{self._template_path}`" if self._template_path else ""
        if template_info:
            lines.append(template_info)
            lines.append("")
        
        return lines
