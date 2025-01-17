# src/vscode_ext_manager/models.py
from dataclasses import dataclass
from typing import Optional, List, Dict

@dataclass
class Extension:
    publisher: str
    name: str
    version: str = "latest"
    architecture: Optional[str] = None
    vscode_version: Optional[str] = None
    dependencies: List[str] = None

    @property
    def full_name(self) -> str:
        return f"{self.publisher}.{self.name}"

@dataclass
class ExtensionMetadata:
    id: str
    version: str
    dependencies: List[str]
    engine: Dict[str, str]
    asset_uri: str
