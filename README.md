# sbot

A non-live click-bot for Geometry Dash

# Demo

TODO: Add demo

# Features

- Random click and release sounds
- Different click types based on duration of the click
- Customisable volume

# Installation

1. Make sure python is installed. If not, it can be installed it from [here](https://www.python.org/downloads/). This
   was made using python 3.11.5, but should most likely work on previous versions as well, although it has not been
   tested.
2. Git clone the repository (requires git to be installed) or download the source code from above and extract
   it.
3. Go into the downloaded directory and install the requirements using `python -m pip install -r requirements.txt`

# Usage

1. A help message can be displayed by running `python src/sbot.py -h`, which will display all options and information
   needed
   to use the bot. (A wiki will be added soon with more detailed information)
2. The bot can be run by running `python src/sbot.py` with the required arguments. The bot will generate the clicks and
   output it to the specified file.

#### Note:

All volume values are in decibels (dB) and can be negative or positive. The default volume is 0dB, which is the same
as a volume multiplier of 1.0.

### Example:

`python src/sbot.py -c ./my_clicks -m acheron.echo.jsoon -t echo_json -o ./out.wav -V 15`

# Supported macro types

[Echo](https://github.com/lcm7341/Echo) (Only json format)

# Supported audio formats

All audio formats supported by [ffmpeg](http://www.ffmpeg.org/general.html#File-Formats) are supported

# Click packs

Each click pack consists of a directory with subdirectories that contain the different clicks types

#### Structure:

Note that clicks do not have to be named 0.wav, 1.wav, 2.wav, etc. but can be named anything. Not all the clicks
types are required, but `clicks` and `releases` are. If a type is missing, it will fall back to `clicks` or `releases`

```
└── directory_name
    ├── clicks
    │   ├── 0.wav
    │   ├── 1.wav
    │   ├── 2.wav
    │   └── ...
    ├── releases
    │   ├── 0.wav
    │   ├── 1.wav
    │   ├── 2.wav
    │   └── ...
    ├── soft_clicks
    │   ├── 0.wav
    │   └── ...
    ├─ soft_releases
    │   ├── 0.wav
    │   └── ...
    ├── hard_clicks
    │   ├── 0.wav
    │   └── ...
    ├─ hard_releases
    │   ├── 0.wav
    │   └── ...
    ├── micro_clicks
    │   ├── 0.wav
    │   └── ...
    ├─ micro_releases
    │   ├── 0.wav
    │   └── ...
```

# Configuring volume

The settings for the volume is stored in a JSON file. An example of the file can be found in `config/volume.json`. This
file will automatically be used, but you can supply a custom file using the "-V" option. ``overall_volume_change``
changes the volume of the entire audio file once it has been generated. ``click_volume_change``
and `release_volume_change` changes the volume of all clicks and releases respectively. The other options change the
volume of the different click types. The volume change of each click type is added to the volume change of the click and
the same for releases. `overall_volume_change` is added on top of all this.

# Todo

- [ ] Add support for more macro types
- [ ] Make it sound more realistic
- [ ] Make volume and pitch be random
- [ ] Add feature to change the volume depending on the position of the level

# Bugs and suggestions

TODO: Write this

# Contributing

TODO: Add contributing guidelines

# Credits

The design of the click-bot and many of the features are inspired
by [Zeo's ClickBot](https://github.com/zeopticz/zcb-2.0) and [Echo](https://github.com/lcm7341/Echo)