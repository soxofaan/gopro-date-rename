Rename GoPro MP4 files based on creation date
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
