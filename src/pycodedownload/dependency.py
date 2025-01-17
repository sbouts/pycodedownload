# src/vscode_ext_manager/dependency.py
from typing import List, Set
from .models import Extension, ExtensionMetadata
from .api import MarketplaceAPI

class DependencyHandler:
    def __init__(self):
        self.api = MarketplaceAPI()
        self.processed = set()

    def resolve_dependencies(self, extension: Extension) -> List[Extension]:
        dependencies = []
        self._resolve_recursive(extension, dependencies)
        return dependencies

    def _resolve_recursive(self, extension: Extension, dependencies: List[Extension]):
        if extension.full_name in self.processed:
            return

        self.processed.add(extension.full_name)
        metadata = self.api.get_extension_metadata(extension)

        for dep in metadata.dependencies:
            if dep.startswith('extension/'):
                dep_parts = dep.split('/')[-1].split('.')
                dep_ext = Extension(
                    publisher=dep_parts[0],
                    name=dep_parts[1]
                )
                dependencies.append(dep_ext)
                self._resolve_recursive(dep_ext, dependencies)
