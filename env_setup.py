#!/usr/bin/env python3

"""
FurAffinity Tor Archive Downloader Environment Setup

Sets up and ensures a proper operating environment for
the Furaffinity Tor Archive Downloader script.
"""

import os
import pathlib
import sys


def main():
    dl_dir = os.path.join(
        pathlib.Path(__file__).parent.absolute(),
        "cwd",
        "downloads"
    )
    try:
        os.makedirs(dl_dir, exist_ok=True)
    except PermissionError:
        print(
            """Could not make directory: downloads\n
            No permission\n
            Try running from a writable directory (Check README)""",
            file=sys.stderr,
            flush=True
        )


if __name__ == "__main__":
    main()
