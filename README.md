# ComfyUIFlexiLoRALoader

![version](https://img.shields.io/badge/version-0.1.0-blue)

A custom node for ComfyUI that allows you to experiment with multiple LoRA models using various weight combinations.

## Purpose and Features

This custom node is designed to maximize the potential of LoRA models.

While LoRA weights significantly influence expressions and poses, using fixed values can limit specific expressions. This node offers:

- Ability to set multiple weight values as lists for various combinations
- Find desired expressions by observing generation results
- Track applied LoRA weights through string output, which can be connected to memo inputs of nodes like D2 Send Eagle

## Features

- Apply up to 3 LoRA models simultaneously
- Set multiple weights for each LoRA model
- Applies nth weight per queue
- LoRAs without nth element set will apply 0.0
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
2. Record generation results and weight values using string output
3. Identify weight values that produce favorable results
4. Adjust weight value lists to achieve desired expressions

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

Currently in beta testing. Please submit bug reports and feature requests through Issues.
'in order' mode will be implemented in a future update.

## Notes

- Weight values should be between 0.0 and 1.0
- Shorter weight lists will be padded with 0.0

## Acknowledgments

Special thanks to:
- [AI Image Studio](https://civitai.com/user/AIImageStudio) for their exceptional LoRA "Analog Film Gravure for Flux", which was the primary inspiration for this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

*Read this in other languages: [日本語](README.ja.md)*

## Author

Created by [@ronsantash](https://github.com/ronsantash)