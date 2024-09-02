import re
from argparse import ArgumentTypeError


class CodeVersion:
    _version_regex = r"^(\d){1}\.(\d){2}\.(\d){1}$"

    def __call__(self, version):
        if version == "latest":
            return version
        if re.match(self._version_regex, version):
            return version
        else:
            raise ArgumentTypeError(
                f"should be in the format x.xx.x or 'latest'. Your input: {version}"
            )
