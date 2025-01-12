# ComfyUIFlexiLoRALoader

![version](https://img.shields.io/badge/version-0.1.0-blue)

## Changelog

### v0.2.0

- Modified album_name output to automatically append applied weight values
  - Example: If input is "FLL" and weights are 0.5, 0.6, 0.1, output will be "FLL050601"
- Added support for negative weight values

### v0.1.0

- Initial release
- Support for applying multiple LoRA models simultaneously
- Multiple weights can be set as a list for each LoRA
- Implementation of randomize mode

A ComfyUI custom node for experimenting with multiple LoRA models using various weight combinations.

## Purpose and Features

This custom node aims to maximize the potential of LoRA models.

While LoRA weights significantly influence expressions and poses, using fixed values can limit specific expressions. With this node:

- You can set multiple weight values as a list to try various combinations
- Observe generation results to find weights that achieve desired expressions
- Check applied LoRA weights through string output and save records by connecting to memo inputs like D2 Send Eagle node

## Features

- Apply up to 3 LoRA models simultaneously
- Set multiple weights for each LoRA model
- Applies nth weight for each queue
- LoRAs without nth element default to 0.0 weight
- Operation modes:
  - randomize: randomly select weights (currently implemented)
  - in order: apply weights sequentially (planned for future update)

## Usage

### Basic Setup

1. Add FlexiLoRALoader node to your workflow
2. Select desired LoRA models
3. Adjust weight values as needed
4. Currently only 'randomize' mode is available

### Recommended Workflow

1. Start with a wide range of weight values (0.0-1.0)
2. Use string output to record generation results and weight values
3. Identify weight values that produce favorable results
4. Adjust weight lists to achieve desired expressions

## Parameters

- `mode`: Currently only 'randomize' is active
- `album_name`: Group name for generated images
- `model`: Base model
- `clip`: CLIP model
- `lora1`, `lora2`, `lora3`: LoRA models to apply
- `lora1_weight`, `lora2_weight`, `lora3_weight`: Comma-separated weight value lists
- `seed`: Seed value for random selection

## Default Weight Settings

- LoRA1: 0.6,0.4,0.5,0.3,0.2,0.3,0.1,0.1,0.5,0.2
- LoRA2: 0.4,0.6,0.5,0.6,0.4,0.3,0.6,0.4,0.5,0.2
- LoRA3: 0.2,0.0,0.1,0.3,0.2,0.3,0.2,0.1,0.1,0.1

## Installation

1. Place in ComfyUI's custom nodes folder
2. Restart ComfyUI

## Development Status

Currently in test release. Please report bugs and feature requests through Issues.
'in order' mode planned for future updates.

## Notes

- Specify weight values between 0.0 and 1.0
- Shorter weight lists are padded with 0.0

## Acknowledgments

The amazing LoRA that inspired the development of this node:

- ["Analog Film Gravure for Flux" by AI Image Studio](https://civitai.com/user/AIImageStudio)
  - I use this wonderful LoRA with various weights in almost all of my works. This node would not exist without this amazing LoRA.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Author

Created by [@ronsantash](https://github.com/ronsantash)
