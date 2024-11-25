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


class CodeArch:
    _architectures = ["x64", "arm64", "armhf", "alpine"]

    def __call__(self, arch):
        if arch not in self._architectures:
            raise ArgumentTypeError(
                f"architecture not supported. Supported architectures: 'x64', 'arm64', 'armhf', 'alpine'. Your input: {arch}"
            )
        return arch
