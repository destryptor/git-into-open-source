"""
Reads the list of resources from the ./resources.yml
For each file, metadata will be inserted as a header
Then copies it over to the website's pages directory
"""

import os
import yaml
import logging
from pathlib import Path
from datetime import datetime


# Configure Logging
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)


def read_file(file_path: str, mode: str = "r") -> str:
    try:
        with open(file_path, mode) as file:
            logger.info(f"Reading file: {file_path}")
            return yaml.safe_load(file)
    except FileNotFoundError:
        logger.error(f"Error: File {file_path} not found.")
        exit(1)


def write_file(file_path: str, content: str, mode: str = "w") -> None:
    with open(file_path, mode) as f:
        logging.info(f"Writing to file: {file_path}")
        f.write(content)


def main():
    # Get the project root, from location of this script
    project_root = Path(__file__).parent.parent
    # The location of the YAML file to read resource list from
    resources_file_path = project_root / "resources.yml"
    # The location of the source guide files
    guides_directory = project_root / "guides"
    # The location of the destination for the guide files
    destination_directory = project_root / "web/src/pages/guides"

    data = read_file(resources_file_path)

    for guide in data["guides"]:
        source_file_path = guides_directory / f"{guide['file']}.md"

        if source_file_path.exists():
            destination_file_path = destination_directory / f"{guide['file']}.md"

            header = (
              f"---\n"
              f"layout: ../../layouts/MarkdownLayout.astro\n"
              f"title: {guide.get('title')}\n"
              f"description: {guide.get('description')}\n"
              f"author: {guide.get('author')}\n"
              f"icon: '{guide.get('icon')}'\n"
              f"tags: '{guide.get('tags')}'\n"
              f"index: '{guide.get('index')}'\n"
              f"created: {guide.get('created')}\n"
              f"updated: {datetime.now().strftime('%Y-%m-%d')}\n"
              f"---\n\n"
              
              f"<!--\n  IMPORTANT: Do not edit this file directly!\n  "
              f"It is generated from the /guides directory\n-->\n\n"
            )

            footer = (
                f"\n\n<!--\n"
                f"\tArticle sourced from https://github.com/lissy93/git-into-opensource\n"
                f"\tLicensed under MIT License, (C) Alicia Sykes <alicia@as93.net> 2023\n"
                f"\t---\n"
                f"\tThis file was auto-generated at {datetime.now()}\n"
                f"\tfrom {source_file_path}\n"
                f"\tusing {__file__}\n"
                f"-->\n"
            )

            content = header + source_file_path.read_text() + footer
            write_file(destination_file_path, content)
            logging.info(f"Copied {source_file_path} to {destination_file_path}")
        else:
            logging.warning(f"Skipping {guide['file']} as doc could not be found in {source_file_path}")

        # Copy the contributing guidleines from ./CONTRIBUTING.md to /web/src/pages/contributing.md
        contributing_source_path = project_root / ".github/CONTRIBUTING.md"
        contributing_destination_path = project_root / "web/src/pages/contributing.md"
        content = contributing_source_path.read_text()
        contributing_headers = (
            f"---\n"
            f"layout: ../layouts/MarkdownLayout.astro\n"
            f"title: Contributing Guidelines\n"
            f"---\n\n"
            f"<!-- This file was auto-generated from ./.github/CONTRIBUTING.md -->\n\n"
        )
        write_file(contributing_destination_path, contributing_headers + content)
        logging.info(f"Copied {contributing_source_path} to {contributing_destination_path}")


if __name__ == "__main__":
    main()
