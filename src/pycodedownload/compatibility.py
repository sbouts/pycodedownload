# src/vscode_ext_manager/compatibility.py
import semver
from .models import Extension, ExtensionMetadata

class CompatibilityChecker:
    def __init__(self, vscode_version: str = "latest"):
        self.vscode_version = vscode_version

    def check_compatibility(self, extension: Extension, metadata: ExtensionMetadata) -> bool:
        if self.vscode_version == "latest":
            return True

        engine_version = metadata.engine.get('vscode', '')
        if not engine_version:
            return True

        try:
            required_version = engine_version.replace('^', '').replace('>=', '')
            return semver.compare(self.vscode_version, required_version) >= 0
        except ValueError:
            return True
