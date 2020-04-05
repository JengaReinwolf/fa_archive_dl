#!/usr/bin/env python3

"""
FurAffinity Tor Archive Downloader

Downloads content from a single artist leveraging the
unofficial FurAffinity Tor Archive.
"""

import argparse
import logging
import os
import pathlib
import re
from time import sleep

import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(message)s")
log = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(__doc__.split("\n")[0])
    parser.add_argument(
        "artist",
        help="The name of the artist (not a link) from whom the content should be downloaded"
    )
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    if args.debug:
        log.setLevel(logging.DEBUG)

    proxies = {
        f"http": "socks5h://127.0.0.1:9050",
        f"https": "socks5h://127.0.0.1:9050"
    }

    log.info("Verifying Tor connection (this may take a moment)")
    if not init_tor_connection(proxies):
        exit(-1)
    log.info("Successfully connected")

    target = f"http://vj5pbopejlhcbz4n.onion/fa/{args.artist}"
    resp = requests.get(
        target,
        proxies=proxies
    )
    soup = BeautifulSoup(resp.content, "html.parser")
    log.debug(soup.prettify())

    dl_dir = os.path.join(
        pathlib.Path(__file__).parent.absolute(),
        "cwd",
        "downloads",
        args.artist
    )
    log.debug(f"dl_dir: {dl_dir}")
    os.makedirs(dl_dir, exist_ok=True)

    for link in get_links(soup):
        if download_media(
            location=f"{target}/{link}",
            save_to=os.path.join(dl_dir, link),
            artist=args.artist,
            proxies=proxies
        ):
            log.info(f"Downloaded: {link}")


def init_tor_connection(proxies):
    attempts = 0
    while attempts < 10:  # 3sec/10: 30 seconds
        log.debug(f"Connection attempt {attempts}")
        try:
            resp = requests.get(
                "https://check.torproject.org/",
                proxies=proxies
            )

            if re.search(b'Congratulations', resp.content) is not None:
                return True

        except Exception as ex:
            log.error(ex)
            attempts += 1
            sleep(3)
            continue
    return False


def get_links(soup):
    acceptable_types = [
        ".jpg", ".png", ".gif", ".jpeg",  # Image
        ".swf",  # Flash
        "txt", "doc", "docx", "odt", "rtf", "pdf",  # Text
        "mp3", "wav", "mid"  # Audio
    ]
    for a in soup.find_all("a"):
        href = a.get("href")
        if href[-4:].lower() in acceptable_types:
            yield href


def download_media(location, save_to, artist, proxies):
    if not os.path.exists(save_to):
        open(save_to, "wb").write(
            requests.get(location, proxies=proxies, allow_redirects=True).content
        )
        return True
    else:
        log.info(f"Skipping file: {os.path.basename(save_to)}: Already exists")
    return False


if __name__ == "__main__":
    main()
