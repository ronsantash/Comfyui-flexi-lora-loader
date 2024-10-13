import os
import json
from comfy.sd import load_lora_for_models
from comfy.lora import load_lora  # 新しくインポート
import sys
import folder_paths
import safetensors.torch

class FlexiLoRALoader:
    # 初期値を変数として定義
    DEFAULT_LORA1_WEIGHTS = '0.7,0.6,0.4,0.3,0.4,0.2,0.5,0.4'
    DEFAULT_LORA2_WEIGHTS = '0.3,0.4,0.6,0.3,0.4,0.8,0.5,0.7'
    DEFAULT_LORA3_WEIGHTS = '0.1'

    @classmethod
    def INPUT_TYPES(cls):
        lora_list = ['None'] + folder_paths.get_filename_list('loras')
        return {
            'required': {
                'mode': (['in order', 'randomize'], {'default': 'in order'}),
                'album_name': ('STRING', {'multiline': False}),
                'model': ('MODEL',),
                'clip': ('CLIP',),
                'lora1': (lora_list,),
                'lora1_text': ('STRING', {'multiline': False, 'default': cls.DEFAULT_LORA1_WEIGHTS}),
                'lora2': (lora_list,),
                'lora2_text': ('STRING', {'multiline': False, 'default': cls.DEFAULT_LORA2_WEIGHTS}),
                'lora3': (lora_list,),
                'lora3_text': ('STRING', {'multiline': False, 'default': cls.DEFAULT_LORA3_WEIGHTS}),
                'weights_display': ('STRING', {'multiline': True, 'lines': 10, 'default': ''}),
                'debug_display': ('STRING', {'multiline': True, 'lines': 10, 'default': ''}),
            },
        }

    RETURN_TYPES = ("MODEL", "CLIP", "STRING", "STRING", "STRING")
    FUNCTION = "apply_loras"
    CATEGORY = "loaders"

    def get_lora_object(self, loraname):
        if loraname == 'None':
            return None
        lorapath = folder_paths.get_full_path("loras", loraname)
        if os.path.exists(lorapath):
            try:
                lora_object = safetensors.torch.load_file(lorapath)
                return lora_object
            except Exception as e:
                print(f"Error loading LoRA from {lorapath}: {e}")
                return None
        else:
            print(f"LoRA file not found: {lorapath}")
            return None

    def apply_loras(self, mode, album_name, model, clip, lora1, lora1_text, lora2, lora2_text, lora3, lora3_text, weights_display, debug_display):
        debug_messages = []

        lora1_weights = [float(x) for x in (lora1_text or self.DEFAULT_LORA1_WEIGHTS).split(',')]
        lora2_weights = [float(x) for x in (lora2_text or self.DEFAULT_LORA2_WEIGHTS).split(',')]
        lora3_weights = [float(x) for x in (lora3_text or self.DEFAULT_LORA3_WEIGHTS).split(',')]

        max_length = max(len(lora1_weights), len(lora2_weights), len(lora3_weights))

        lora1_weights += [0] * (max_length - len(lora1_weights))
        lora2_weights += [0] * (max_length - len(lora2_weights))
        lora3_weights += [0] * (max_length - len(lora3_weights))

        applied_queues = []

        for i in range(max_length):
            queue = []
            current_lora1 = self.get_lora_object(lora1)
            current_lora2 = self.get_lora_object(lora2)
            current_lora3 = self.get_lora_object(lora3)

            if current_lora1 and lora1_weights[i] > 0:
                debug_messages.append(f"Loading LoRA: {lora1} with weight: {lora1_weights[i]}")
                model, clip = load_lora_for_models(model, clip, current_lora1, lora1_weights[i], lora1_weights[i])  # strength_clip を lora1_weights[i] として使用
                queue.append(f'lora1:{lora1_weights[i]}')

            if current_lora2 and lora2_weights[i] > 0:
                debug_messages.append(f"Loading LoRA: {lora2} with weight: {lora2_weights[i]}")
                model, clip = load_lora_for_models(model, clip, current_lora2, lora2_weights[i], lora2_weights[i])  # strength_clip を lora2_weights[i] として使用
                queue.append(f'lora2:{lora2_weights[i]}')

            if current_lora3 and lora3_weights[i] > 0:
                debug_messages.append(f"Loading LoRA: {lora3} with weight: {lora3_weights[i]}")
                model, clip = load_lora_for_models(model, clip, current_lora3, lora3_weights[i], lora3_weights[i])  # strength_clip を lora3_weights[i] として使用
                queue.append(f'lora3:{lora3_weights[i]}')

            if queue:
                applied_queues.append(' '.join(queue))

        output_string = f"Album: {album_name}, Applied LoRAs: " + " | ".join(applied_queues)
        weights_display = output_string
        debug_display = "\n".join(debug_messages)

        return (model, clip, output_string, weights_display, debug_display)
