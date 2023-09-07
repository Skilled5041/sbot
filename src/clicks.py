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
import json
import os
import pydub


def validate_clicks(directory: str) -> bool:
    directory = directory.rstrip("/\\")

    if not os.path.isdir(directory) or len(os.listdir(directory)) == 0:
        return False

    # Check if there is a clicks and releases folder inside the directory
    if not os.path.isdir(f"{directory}/releases") or not os.path.isdir(
        f"{directory}/clicks"
    ):
        return False

    if (
        len(os.listdir(f"{directory}/releases")) == 0
        or len(os.listdir(f"{directory}/clicks")) == 0
    ):
        return False

    return True


def load_clicks(directory: str) -> dict[str, list[pydub.AudioSegment]]:
    directory = directory.rstrip("/\\")

    clicks = {"clicks": [], "releases": []}

    for file in os.listdir(f"{directory}/clicks"):
        clicks["clicks"].append(
            pydub.AudioSegment.from_file(f"{directory}/clicks/{file}")
        )

    for file in os.listdir(f"{directory}/releases"):
        clicks["releases"].append(
            pydub.AudioSegment.from_file(f"{directory}/releases/{file}")
        )

    if os.path.isdir(f"{directory}/soft_clicks"):
        clicks["soft_clicks"] = []
        for file in os.listdir(f"{directory}/soft_clicks"):
            clicks["soft_clicks"].append(
                pydub.AudioSegment.from_file(f"{directory}/soft_clicks/{file}")
            )

    if os.path.isdir(f"{directory}/soft_releases"):
        clicks["soft_releases"] = []
        for file in os.listdir(f"{directory}/soft_releases"):
            clicks["soft_releases"].append(
                pydub.AudioSegment.from_file(f"{directory}/soft_releases/{file}")
            )

    if os.path.isdir(f"{directory}/hard_clicks"):
        clicks["hard_clicks"] = []
        for file in os.listdir(f"{directory}/hard_clicks"):
            clicks["hard_clicks"].append(
                pydub.AudioSegment.from_file(f"{directory}/hard_clicks/{file}")
            )

    if os.path.isdir(f"{directory}/hard_releases"):
        clicks["hard_releases"] = []
        for file in os.listdir(f"{directory}/hard_releases"):
            clicks["hard_releases"].append(
                pydub.AudioSegment.from_file(f"{directory}/hard_releases/{file}")
            )

    if os.path.isdir(f"{directory}/micro_clicks"):
        clicks["micro_clicks"] = []
        for file in os.listdir(f"{directory}/micro_clicks"):
            clicks["micro_clicks"].append(
                pydub.AudioSegment.from_file(f"{directory}/micro_clicks/{file}")
            )

    if os.path.isdir(f"{directory}/micro_releases"):
        clicks["micro_releases"] = []
        for file in os.listdir(f"{directory}/micro_releases"):
            clicks["micro_releases"].append(
                pydub.AudioSegment.from_file(f"{directory}/micro_releases/{file}")
            )

    return clicks


def validate_volume_file(file: str) -> bool:
    if not os.path.isfile(file):
        return False

    with open(file, "r") as f:
        data = json.load(f)

        required_fields = [
            "overall_volume_change",
            "click_volume_change",
            "release_volume_change",
            "clicks_volume_change",
            "releases_volume_change",
            "soft_clicks_volume_change",
            "soft_releases_volume_change",
            "hard_clicks_volume_change",
            "hard_releases_volume_change",
            "micro_clicks_volume_change",
            "micro_releases_volume_change",
        ]

        for field in required_fields:
            f = data.get(field)
            if f is None or not isinstance(f, float):
                return False
