import yaml
from pathlib import Path
from typing import List
from .models import Extension

def load_config(config_path: Path) -> List[Extension]:
    with open(config_path) as f:
        data = yaml.safe_load(f)
        
    extensions = []
    for ext in data.get('extensions', []):
        extensions.append(Extension(
            publisher=ext['publisher'],
            name=ext['name'],
            version=ext.get('version', 'latest'),
            architecture=ext.get('architecture')
        ))
    
    return extensions
