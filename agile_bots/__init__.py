# Agile Bots Package
__version__ = '0.1.0'

import os
import sys
from pathlib import Path

# Get the root directory (parent of this agile_bots package)
_root = Path(__file__).parent.parent

# Add src, test, and bots to the package path
__path__ = [
    str(_root / 'src'),
    str(_root / 'test'),  
    str(_root / 'bots'),
]

# Make src, test, and bots available as subpackages
sys.modules['agile_bots.src'] = __import__('src')
sys.modules['agile_bots.test'] = __import__('test')
sys.modules['agile_bots.bots'] = __import__('bots')