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
import random
import pydub
import tqdm
from utils import frames_to_ms


def validate_file(file: str) -> bool:
    with open(file) as f:
        data = json.load(f)

        end_xpos = data.get("end_xpos")
        fps = data.get("fps")
        inputs = data.get("inputs")

        if (
            end_xpos is None
            or fps is None
            or inputs is None
            or not isinstance(end_xpos, float)
            or not isinstance(fps, float)
            or not isinstance(inputs, list)
            or fps <= 0
            or len(inputs) == 0
        ):
            return False

        prev_frame = 0

        for inp in inputs:
            frame = inp.get("frame")
            holding = inp.get("holding")

            if (
                frame is None
                or holding is None
                or not isinstance(frame, int)
                or not isinstance(holding, bool)
                or frame < 0
                or frame < prev_frame
            ):
                return False

            prev_frame = frame

        return True


def process_macro(
    file: str,
    clicks: dict[str, list[pydub.AudioSegment]],
    volume_config: dict[str, float],
    verbose: bool = False,
) -> pydub.AudioSegment:
    with (open(file) as f):
        data = json.load(f)

        fps = data["fps"]
        inputs = data["inputs"]

        final_frame = max(map(lambda x: x["frame"], inputs))
        seconds = final_frame / fps

        audio = pydub.AudioSegment.silent(duration=seconds * 1000)

        prev_frame = 0
        prev_input = None
        prev_click_type = "clicks"
        prev_release_type = "releases"

        with tqdm.tqdm(
            total=len(inputs), desc="Processing macro", delay=0.01
        ) as prog_bar:
            for i, inp in enumerate(inputs):
                frame = inp["frame"]
                holding = inp["holding"]

                click_type = prev_click_type
                releases_type = prev_release_type
                if prev_input == "holding":
                    click_duration = frames_to_ms(frame - prev_frame, fps)
                    if 150 < click_duration < 1000 or prev_frame == 0:
                        click_type = "clicks"
                        releases_type = "releases"
                    elif click_duration <= 30:
                        click_type = "micro_clicks"
                        releases_type = "micro_releases"
                    elif click_duration <= 150:
                        click_type = "soft_clicks"
                        releases_type = "soft_releases"
                    else:
                        click_type = "hard_clicks"
                        releases_type = "hard_releases"

                prev_frame = frame
                prev_input = "holding" if holding else "release"
                prev_click_type = click_type
                prev_release_type = releases_type

                if holding:
                    if clicks.get(click_type) is not None:
                        click_sound = random.choice(clicks[click_type]) + (
                            volume_config["click_volume_change"]
                            + volume_config[f"{click_type}_volume_change"]
                        )
                    else:
                        click_sound = random.choice(clicks["clicks"]) + (
                            volume_config["click_volume_change"]
                            + volume_config[f"{click_type}_volume_change"]
                        )
                    audio = audio.overlay(click_sound, position=frame / fps * 1000)
                else:
                    if clicks.get(releases_type) is not None:
                        click_sound = random.choice(clicks[releases_type]) + (
                            volume_config["release_volume_change"]
                            + volume_config[f"{releases_type}_volume_change"]
                        )
                    else:
                        click_sound = random.choice(clicks["releases"]) + (
                            volume_config["release_volume_change"]
                            + volume_config[f"{releases_type}_volume_change"]
                        )
                    audio = audio.overlay(click_sound, position=frame / fps * 1000)

                if verbose:
                    print(
                        f"Input: {i}, Frame: {frame}, Holding: {holding}, Type: {click_type}"
                    )
                    prog_bar.update(1)
                else:
                    prog_bar.update(1)

            prog_bar.close()

        return audio
