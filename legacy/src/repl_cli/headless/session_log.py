from pathlib import Path
from datetime import datetime
from typing import Optional, Any


class SessionLog:
    
    def __init__(self, log_path: Path):
        self.log_path = log_path
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.log_path.exists():
            self.log_path.write_text('')
    
    @classmethod
    def creates_with_timestamped_path(cls, base_dir: Path) -> 'SessionLog':
        timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        log_path = base_dir / f'headless-{timestamp}.log'
        return cls(log_path)
    
    def appends_response(self, response: Any) -> bool:
        try:
            content = self.log_path.read_text()
            if isinstance(response, dict):
                response_text = str(response)
            else:
                response_text = str(response)
            
            # Add timestamp
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            timestamped_text = f'[{timestamp}] {response_text}'
            
            # Print to terminal
            print(timestamped_text)
            
            content += f'\n{timestamped_text}'
            self.log_path.write_text(content)
            return True
        except Exception:
            return False
    
    def appends_total_loops(self, total_loops: int):
        content = self.log_path.read_text()
        summary = f'\nTotal loops: {total_loops}\n'
        
        # Print to terminal
        print(summary)
        
        content += summary
        self.log_path.write_text(content)
    
    def get_transcript(self) -> str:
        if self.log_path.exists():
            return self.log_path.read_text()
        return ''

