from pathlib import Path
from typing import Dict, Any, Optional
from utils import read_json_file

class StoryGraphTemplate:

    def __init__(self, sg_dir: Path, template_filename: Optional[str]):
        self._sg_dir = sg_dir
        self._template_filename = template_filename
        self._template_content: Dict[str, Any] = {}
        self._template_path: Optional[Path] = None
        self._load_template()

    def _load_template(self):
        if not self._template_filename:
            return
        template_path = self._sg_dir / self._template_filename
        if not template_path.exists():
            return
        self._template_content = read_json_file(template_path)
        self._template_path = template_path

    @property
    def template_content(self) -> Dict[str, Any]:
        return self._template_content

    @property
    def schema(self) -> Dict[str, Any]:
        return self.template_content

    @property
    def template_path(self) -> Optional[Path]:
        return self._template_path

    @property
    def exists(self) -> bool:
        return self._template_path is not None and self._template_path.exists()