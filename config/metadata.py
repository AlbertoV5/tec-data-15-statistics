"""
Metadata Scraper
"""
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from argparse import ArgumentParser, Namespace
from selenium.webdriver import Chrome
from bs4 import BeautifulSoup
from typing import Generator
from pprint import pprint
from pathlib import Path
import asyncio
import json
import re


async def main(argv: Namespace):
    """Async scraping of all files in input directory and store the
    resulting metadata of id, text in output directory.

    Args:
        argv (Namespace): -h

    Raises:
        ValueError: If input directory doesn't exist.
    """
    target = Path(argv.input)
    output = Path(argv.output)
    if not target.is_dir():
        raise ValueError(f"Directory {target} doesn't exist.")
    if not output.is_dir():
        Path.mkdir(output)
    # Execute async scraping
    async for name, html in get_html(get_browser(), target):
        with open(f"{output / name}.json", "w") as file:
            json.dump(
                pre_json(name, get_headers(html), get_codes(html)), file, indent=4
            )


async def get_html(browser: Chrome, path: Path) -> Generator[tuple, None, None]:
    """Visit all html files in given path and get their name and html content.

    Args:
        browser (Chrome): Driver to use.
        path (Path): Path where all html files are located.

    Yields:
        Generator[tuple, None, None]: Tuple of file.stem and parsed html.
    """
    for file in path.glob("*.[html]*"):
        browser.get(f"file://{Path.cwd() / file}")
        if browser.page_source is not None:
            yield (file.stem, BeautifulSoup(browser.page_source, "html.parser"))
    browser.quit()


def pre_json(name: str, *args: Generator) -> dict:
    """Unpack all generators and store them in a dictionary with a given name.

    Args:
        name (str): Value for the "name" key.

    Returns:
        dict: {"name":name, "data":[unpacked data]}
    """
    return {"name": name, "data": [data for gen in args for data in gen]}


def get_codes(html: BeautifulSoup) -> Generator[dict, None, None]:
    """Find all divs of a given class and get is id and text.

    Args:
        html (BeautifulSoup): parsed html.

    Yields:
        Generator[dict, None, None]: dictionary of id, text.
    """
    for h in html.find_all("div", class_="org-src-container"):
        yield {"id": h.get("id"), "text": h.text}


def get_headers(html: BeautifulSoup) -> Generator[dict, None, None]:
    """Find all header elements with an id and get their non-numeric text too.

    Args:
        html (BeautifulSoup): parsed html.

    Yields:
        Generator[dict, None, None]: dictionary of id, text.
    """
    for h in html.find_all(re.compile("^h[1-6]$")):
        if h.get("id") is not None:
            yield {"id": h.get("id"), "text": re.sub(r"[0-9]\.\s*", "", h.text)}


def get_browser():
    """Start a headless Chrome browser."""
    options = Options()
    options.headless = True
    service = Service(ChromeDriverManager().install())
    return Chrome(service=service, options=options)


if __name__ == "__main__":
    default_input = "public/build"
    default_output = "public/resources/metadata"
    args = ArgumentParser(
        prog="Metadata scraper",
        usage=f"python config/metadata.py -i {default_input} -o {default_output}",
        description="Scrape id, text metadata from HTML files.",
    )
    args.add_argument(
        "-i",
        "--input",
        metavar="path",
        default=f"{default_input}",
        help="Directory with the files to scrape. Defaults to public/build.",
    )
    args.add_argument(
        "-o",
        "--output",
        metavar="path",
        default=f"{default_output}",
        help=f"Directory for json files output. Defaults to {default_output}",
    )
    asyncio.run(main(args.parse_args()))
