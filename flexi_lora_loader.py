import os
import comfy.utils
import comfy.sd
import folder_paths
import safetensors.torch
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
                lora = comfy.utils.load_torch_file(lorapath)
                return lora
            except Exception as e:
                print(f"Error loading LoRA from {lorapath}: {e}")
                return None
        else:
            print(f"LoRA file not found: {lorapath}")
            return None

    def apply_loras(self, mode, album_name, model, clip, lora1, lora1_text, lora2, lora2_text, lora3, lora3_text, weights_display, debug_display):
        debug_messages = []

        # 各LoRAの最初の値だけを取得
        lora1_weight = float((lora1_text or self.DEFAULT_LORA1_WEIGHTS).split(',')[0])
        lora2_weight = float((lora2_text or self.DEFAULT_LORA2_WEIGHTS).split(',')[0])
        lora3_weight = float((lora3_text or self.DEFAULT_LORA3_WEIGHTS).split(',')[0])

        applied_queues = []

        current_lora1 = self.get_lora_object(lora1)
        current_lora2 = self.get_lora_object(lora2)
        current_lora3 = self.get_lora_object(lora3)

        if current_lora1 is not None and lora1_weight > 0:
            debug_messages.append(f"Loading LoRA: {lora1} with weight: {lora1_weight}")
            model, clip = comfy.sd.load_lora_for_models(model, clip, current_lora1, lora1_weight, lora1_weight)
            applied_queues.append(f'lora1:{lora1_weight}')

        if current_lora2 is not None and lora2_weight > 0:
            debug_messages.append(f"Loading LoRA: {lora2} with weight: {lora2_weight}")
            model, clip = comfy.sd.load_lora_for_models(model, clip, current_lora2, lora2_weight, lora2_weight)
            applied_queues.append(f'lora2:{lora2_weight}')

        if current_lora3 is not None and lora3_weight > 0:
            debug_messages.append(f"Loading LoRA: {lora3} with weight: {lora3_weight}")
            model, clip = comfy.sd.load_lora_for_models(model, clip, current_lora3, lora3_weight, lora3_weight)
            applied_queues.append(f'lora3:{lora3_weight}')

        output_string = f"Album: {album_name}, Applied LoRAs: " + " | ".join(applied_queues)
        weights_display = output_string
        debug_display = "\n".join(debug_messages)

        return (model, clip, output_string, weights_display, debug_display)
