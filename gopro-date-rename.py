"""
Rename GoPro MP4 files based on creation date,
(which is well hidden in the file's metadata).

Assumes availability of the `ffprobe` command line tool
(https://ffmpeg.org/ffprobe.html).

Usage example:

    $ python gopro-date-rename.py GH0*
    Renaming GH018113.MP4 to 20230222-163014-GH018113.MP4
    Renaming GH018114.MP4 to 20230222-163104-GH018114.MP4
    Renaming GH018115.MP4 to 20230222-163828-GH018115.MP4
    Renaming GH018116.MP4 to 20230223-110120-GH018116.MP4
    Renaming GH018117.MP4 to 20230223-113956-GH018117.MP4

"""

import argparse
import datetime
import json
import logging
import re
import subprocess
import pathlib
from typing import Union

_log = logging.getLogger("gopro-date-rename")


def main():
    cli = argparse.ArgumentParser()
    cli.add_argument("filename", nargs="+", help="GoPro MP4 file name(s).")
    cli.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="Dry run instead of actual renaming files.",
    )
    cli.add_argument("-v", "--verbose", action="store_true", help="Verbose logging.")
    arguments = cli.parse_args()

    do_dry_run = arguments.dry_run
    log_level = logging.INFO if arguments.verbose else logging.WARNING

    logging.basicConfig(level=log_level)

    for path in (pathlib.Path(f) for f in arguments.filename):
        date = extract_creation_time(path)
        _log.info(f"Extracted creation_time {date!r} from {str(path)!r}")
        target = date.strftime("%Y%m%d-%H%M%S") + "-" + str(path.name)
        _log.info(f"Target filename for {path}: {target}")

        if do_dry_run:
            print(f"mv {path} {target}")
        else:
            print(f"Renaming {path} to {target}")
            path.rename(target)


def extract_creation_time(path: Union[str, pathlib.Path]) -> datetime.datetime:
    """
    Extract creation_time from GoPro MP4 file, using ffprobe
    """
    cmd = [
        "ffprobe",
        "-loglevel",
        "error",
        "-print_format",
        "json",
        "-show_format",
        "-show_streams",
        str(path),
    ]
    _log.info(f"Executing {cmd}")
    dump = subprocess.check_output(cmd)
    metadata = json.loads(dump)
    date = metadata["format"]["tags"]["creation_time"]
    # `fromisoformat` does not support GoPro date format directly, so a bit of massaging.
    date = re.match(r"\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d", date).group(0)
    date = datetime.datetime.fromisoformat(date)
    return date


if __name__ == "__main__":
    main()
