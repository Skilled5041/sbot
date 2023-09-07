# Copyright (C) 2023 Skilled5041
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import argparse
import json
import os
import echo_json
from termcolor import colored
from clicks import validate_clicks, load_clicks, validate_volume_file

parser = argparse.ArgumentParser(
    prog="sbot",
    description="Generates a wav file with clicks based on a Geometry Dash bot macro",
)

parser.add_argument(
    "-v",
    "--verbose",
    action="store_true",
    help="Prints additional info when processing a macro",
)

parser.add_argument(
    "-c",
    "--clicks",
    type=str,
    help="Path to the clicks folder",
    nargs="?",
)

parser.add_argument("-m", "--macro", type=str, help="Path to the macro file", nargs="?")

parser.add_argument(
    "-t", "--type", choices=["echo_json"], type=str, help="Type of the macro", nargs="?"
)

parser.add_argument(
    "-o", "--output", type=str, help="Path to the output file", nargs="?"
)

parser.add_argument(
    "-V",
    "--volume",
    type=str,
    help="JSON file with the volume. If it is not specified, it will try to find a file "
    "called volume.json, and if it is not found it will use the default settings.",
    nargs="?",
)


parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")


args = parser.parse_args()

if args.clicks is None:
    parser.error(colored("The clicks folder is required", "red"))
if args.macro is None:
    parser.error(colored("The macro file is required", "red"))
if args.type is None:
    parser.error(colored("The macro type is required", "red"))
if args.output is None:
    parser.error(colored("The output file is required", "red"))


valid_clicks = validate_clicks(args.clicks)
if not valid_clicks:
    parser.error(
        colored(
            "The clicks folder is invalid. The folder either does not exist, or the structure is invalid Check the "
            "click"
            "pack structure in the README for more info",
            "red",
        )
    )

if not os.path.isfile(args.macro):
    parser.error(colored("The macro file does not exist", "red"))

if not os.path.isdir(args.output.rsplit("/", 1)[0]):
    parser.error(colored("The output folder does not exist", "red"))

if args.volume is None:
    if os.path.isfile("volume.json"):
        with open("volume.json", "r") as f:
            volume = json.load(f)
    else:
        volume = {
            "overall_volume_change": 20.0,
            "click_volume_change": 0.0,
            "release_volume_change": 0.0,
            "clicks_volume_change": 0.0,
            "releases_volume_change": 0.0,
            "soft_clicks_volume_change": 0.0,
            "soft_releases_volume_change": 0.0,
            "hard_clicks_volume_change": 0.0,
            "hard_releases_volume_change": 0.0,
            "micro_clicks_volume_change": 0.0,
            "micro_releases_volume_change": 0.0,
        }

else:
    if not os.path.isfile(args.volume):
        parser.error(colored("The volume file does not exist", "red"))

    valid_volume = validate_volume_file(args.volume)

    with open(args.volume, "r") as f:
        volume = json.load(f)

print(colored("Loading clicks...", "cyan"))

try:
    clicks = load_clicks(args.clicks)
except Exception as e:
    parser.error(colored(f"Failed to load the clicks: {e}", "red"))

print(colored("Processing macro...", "cyan"))

if args.type == "echo_json":
    valid_macro = echo_json.validate_file(args.macro)
    if not valid_macro:
        parser.error(colored("The macro file is invalid or corrupted", "red"))

    audio = echo_json.process_macro(
        args.macro, clicks, verbose=args.verbose, volume_config=volume
    )

print(colored("Exporting audio...", "cyan"))

audio + volume["overall_volume_change"]
audio.export(args.output, format="wav")

print(colored(f"Successfully exported the audio to {args.output}", "light_green"))
