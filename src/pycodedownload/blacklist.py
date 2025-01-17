# src/vscode_ext_manager/blacklist.py
class BlacklistChecker:
    def __init__(self):
        self.blacklist = self._load_blacklist()

    def _load_blacklist(self) -> set:
        # This could be loaded from a remote source or file
        return {
            "known.malicious.extension",
            "problematic.extension"
        }

    def is_blacklisted(self, extension_id: str) -> bool:
        return extension_id in self.blacklist
