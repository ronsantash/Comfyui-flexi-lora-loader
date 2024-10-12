import os
import json
from comfy.sd import load_lora_for_models
import folder_paths

class FlexiLoRALoader:
    @classmethod
    def INPUT_TYPES(cls):
        lora_list = ["None"] + folder_paths.get_filename_list("loras")
        return {
            "required": {
                "model": ("MODEL",),
                "clip": ("CLIP",),
                "lora1": (lora_list,),
                "lora2": (lora_list,),
                "lora3": (lora_list,),
            },
        }

    RETURN_TYPES = ("MODEL", "CLIP", "STRING")
    FUNCTION = "apply_loras"
    CATEGORY = "loaders"

    def apply_loras(self, model, clip, lora1, lora2, lora3):
        loras = [lora1, lora2, lora3]
        weights = self.load_weights()
        applied_loras = []

        for lora, weight in zip(loras, weights):
            if lora != "None" and weight != 0:
                model, clip = load_lora_for_models(lora, model, clip, weight)
                applied_loras.append(f"{lora}:{weight}")

        return (model, clip, ",".join(applied_loras))

    def load_weights(self):
        weights_file = "path/to/weights.json"
        try:
            with open(weights_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Weights file not found at {weights_file}")
            return [1.0, 1.0, 1.0]  # デフォルト値
