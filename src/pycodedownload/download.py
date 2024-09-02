import argparse
import logging
import os

import requests
import urllib3
from validators import CodeVersion

################################################################

DEFAULT_CONF_LOCATION = "extensions.yaml"
DEFAULT_DIR = os.path.expanduser("~/.cache/pycodedownload")

VSCODE_REPO_BASE_URL = "https://api.github.com/repos/microsoft/vscode"

################################################################


# def dl_code(dst_dir, channel="stable", revision="latest"):
#     """
#     download code for Linux from Microsoft debian-like repo
#     """

#     url = f"https://update.code.visualstudio.com/{revision}/linux-deb-x64/{channel}"
#     r = requests.get(url, allow_redirects=False)
#     if r.status_code != 302:
#         logging.error(f"cannot get {channel} channel")
#         return

#     url = r.headers["Location"]
#     path = urllib3.parse.urlsplit(url).path.split("/")
#     if len(path) != 4:
#         logging.error(f"cannot parse url {url}")
#         return

#     commit_id = path[2]
#     deb_filename = path[3]
#     package = "code"
#     filename = dst_dir / "code" / commit_id / deb_filename
#     tag = re.search(r"_(.+)_", deb_filename).group(1)
#     version = tag.split("-", 1)[0]

#     if filename.is_file():
#         print("{:50} {:20} {}".format(package, tag, CHECK_MARK))
#     else:
#         print(
#             "{:50} {:20} {} downloading...".format(
#                 package, tag, HEAVY_BALLOT_X
#             )
#         )
#         download(url, filename)

#         d = filename.parent.parent / revision
#         if d.is_symlink():
#             d.unlink()
#         d.symlink_to(commit_id, target_is_directory=True)

#         d = filename.parent.parent / version
#         if d.is_symlink():
#             d.unlink()
#         d.symlink_to(commit_id, target_is_directory=True)

#     data = {}
#     data["version"] = version
#     data["tag"] = tag
#     data["channel"] = channel
#     data["commit_id"] = commit_id
#     data["url"] = str(filename.relative_to(dst_dir))
#     data["deb"] = deb_filename
#     data["server"] = []

#     for arch in ["x64", "armhf", "alpine", "arm64"]:
#         package = f"server-linux-{arch}"
#         url = f"https://update.code.visualstudio.com/commit:{commit_id}/{package}/{channel}"
#         r = requests.get(url, allow_redirects=False)
#         if r.status_code == 302:
#             url = r.headers["Location"]
#             path = urllib.parse.urlsplit(url).path.split("/")
#             if len(path) != 4:
#                 continue
#             filename = dst_dir / "code" / commit_id / path[3]
#             data["server"].append(path[3])

#             if filename.is_file():
#                 print("{:50} {:20} {}".format(package, version, CHECK_MARK))
#             else:
#                 print(
#                     "{:50} {:20} {} downloading...".format(
#                         package, version, HEAVY_BALLOT_X
#                     )
#                 )
#                 download(url, filename)

#     return data


def download_code(code_version: str):
    """
    Download code for Linux from Microsoft debian-like repo.
    """

    if code_version != "latest":
        url = f"{VSCODE_REPO_BASE_URL}/"

    url = f"https://update.code.visualstudio.com/latest/linux-deb-x64/stable"
    r = requests.get(url, allow_redirects=False)
    if r.status_code != 302:
        logging.error(f"cannot get stable channel")
        return

    url = r.headers["Location"]
    path = urllib3.parse.urlsplit(url).path.split("/")
    if len(path) != 4:
        logging.error(f"cannot parse url {url}")
        return


def download_extensions():
    pass


def main():
    """
    Parse arguments and pass them to the logic to download VSCode extensions
    and optionally VSCode Server.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v", "--verbose", help="increase verbosity", action="store_true"
    )
    parser.add_argument(
        "-c",
        "--conf",
        help="configuration file",
        default=DEFAULT_CONF_LOCATION,
    )
    parser.add_argument("--no-code", help="do not download Code", action="store_true")
    parser.add_argument(
        "--code-version",
        type=CodeVersion(),
        help="set the required vscode version",
        default="1.92.331231223",
    )
    parser.add_argument(
        "-d",
        "--dir",
        help="set the directory to store vscode and/or extensions",
        default=DEFAULT_DIR,
    )
    parser.add_argument("--dry-run", help="dry run", action="store_true")

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(
            format="%(asctime)s:%(levelname)s:%(message)s",
            level=logging.DEBUG,
            datefmt="%H:%M:%S",
        )
        logging.debug("args {}".format(args))
    else:
        logging.basicConfig(
            format="%(asctime)s:%(levelname)s:%(message)s",
            level=logging.INFO,
            datefmt="%H:%M:%S",
        )

    args.conf = os.path.abspath(args.conf)
    if not os.path.isfile(args.conf):
        logging.error(f"no config file found {args.conf}")
        exit(2)

    if not os.path.isdir(args.dir):
        if args.dir == DEFAULT_DIR:
            os.makedirs(name=DEFAULT_DIR, exist_ok=True)
        else:
            logging.error(f"directory does not exist: {args.dir}")
            exit(2)

    if not args.no_code:
        download_code(code_version=args.code_version)

    download_extensions()

    # Download VSCode
    # Download Extensions
    # Cleanup
    # if args.keep is not None:
    #     purge("code", args.keep)
    #     purge("vsix", args.keep)
    # else:
    #     purge("code", 0)
    #     purge("vsix", 0)


if __name__ == "__main__":
    main()
