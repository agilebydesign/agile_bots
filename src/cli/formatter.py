
class CliTerminalFormatter:

    def _format_header_style(self, text: str) -> str:
        return f'## {text}'

    def _format_bold_style(self, text: str) -> str:
        return f'**{text}**'

    def _format_identity(self, text: str) -> str:
        return text

    def format_directive(self, text: str) -> str:
        return self.format_header(text)

    def format_header(self, text: str) -> str:
        return self._format_header_style(text)

    def format_workflow_status_header(self, text: str) -> str:
        return self.format_header(text)

    def format_command(self, text: str) -> str:
        return self._format_bold_style(text)

    def format_label(self, text: str) -> str:
        return self.format_command(text)

    def format_workflow_directory(self, text: str) -> str:
        return self.format_command(text)

    def format_workflow_current_state(self, text: str) -> str:
        return self.format_command(text)

    def format_workflow_next_step(self, text: str) -> str:
        return self.format_command(text)

    def format_workflow_current_marker(self, text: str) -> str:
        return self.format_command(text)

    def format_workflow_active_marker(self, text: str) -> str:
        return self.format_command(text)

    def format_workflow_completed(self, text: str) -> str:
        return self._format_identity(text)

    def format_workflow_pending(self, text: str) -> str:
        return self.format_workflow_completed(text)

    def format_parameter(self, text: str) -> str:
        return f'`{text}`'

    def format_error(self, text: str) -> str:
        return f'[ERROR] **{text}**'

    def format_warning(self, text: str) -> str:
        return f'[WARNING] **{text}**'

    def format_success(self, text: str) -> str:
        return f'[OK] **{text}**'

    def format_info(self, text: str) -> str:
        return f'[INFO] **{text}**'

    def format_separator(self, char: str='=', length: int=70) -> str:
        return '---'
