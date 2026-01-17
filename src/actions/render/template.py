from pathlib import Path
from typing import Optional

class Template:

    def __init__(self, template_path: Path):
        self._template_path = template_path
        self._content: Optional[str] = None
        self._load_template()

    def _load_template(self):
        if not self._template_path.exists():
            raise FileNotFoundError(f'Template file not found: {self._template_path}')
        self._content = self._template_path.read_text(encoding='utf-8')

    @property
    def content(self) -> str:
        return self._content

    @property
    def template_path(self) -> Path:
        return self._template_path