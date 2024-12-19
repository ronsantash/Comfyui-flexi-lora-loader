import os
import comfy.utils
import comfy.sd
import folder_paths
import safetensors.torch
import logging
import json
import random
import time

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FlexiLoRALoader:
    # 初期値を変数として定義
    DEFAULT_LORA1_WEIGHTS = '0.7,0.6,0.4,0.4,0.6,0.6,0.1,0.2,0.3,0.4,0.5,0.2,0.8,0.2,0.1,0.4,0.2,0.4,0.6,0.7,0.0,0.0,0.0'
    DEFAULT_LORA2_WEIGHTS = '0.3,0.4,0.6,0.6,0.4,0.4,0.1,0.2,0.3,0.4,0.5,0.8,0.2,0.6,0.4,0.2,0.1,0.0,0.0,0.0,0.4,0.6,0.7'
    DEFAULT_LORA3_WEIGHTS = '0.3,0.2,0.0,0.1,0.1,0.2,0.1,0.1,0.1,0.2,0.1,0.1,0.2,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.2,0.2'

    def __init__(self):
        self.rng = random.Random()

    @classmethod
    def INPUT_TYPES(cls):
        lora_list = ['None'] + folder_paths.get_filename_list('loras')
        return {
            'required': {
                'mode': (['in order', 'randomize'], {'default': 'randomize'}),
                'album_name': ('STRING', {'multiline': False}),
                'model': ('MODEL',),
                'clip': ('CLIP',),
                'lora1': (lora_list,),
                'lora1_text': ('STRING', {'multiline': False, 'default': cls.DEFAULT_LORA1_WEIGHTS}),
                'lora2': (lora_list,),
                'lora2_text': ('STRING', {'multiline': False, 'default': cls.DEFAULT_LORA2_WEIGHTS}),
                'lora3': (lora_list,),
                'lora3_text': ('STRING', {'multiline': False, 'default': cls.DEFAULT_LORA3_WEIGHTS}),
                'seed': ('INT', {'default': 0, 'min': 0, 'max': 0xffffffffffffffff}),
                'control_after_generate': (['fixed', 'increment', 'decrement', 'randomize'], {'default': 'randomize'}),
            },
        }

    RETURN_TYPES = ("MODEL", "CLIP", "STRING", "INT")
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
                logger.error(f"Error loading LoRA from {lorapath}: {e}")
                return None
        else:
            logger.warning(f"LoRA file not found: {lorapath}")
            return None

    def apply_loras(self, mode, album_name, model, clip, lora1, lora1_text, lora2, lora2_text, lora3, lora3_text, seed, control_after_generate):
        debug_messages = []

        # 重み値の処理を修正
        def get_weights(input_text):
            if not input_text.strip():
                return [0.0]
            return [float(x) for x in input_text.split(',')]

        lora1_weights = get_weights(lora1_text)
        lora2_weights = get_weights(lora2_text)
        lora3_weights = get_weights(lora3_text)

        # 最大長を取得
        max_length = max(len(lora1_weights), len(lora2_weights), len(lora3_weights))
        debug_messages.append(f"Max length: {max_length}")

        # 足りない要素を0で補完
        lora1_weights.extend([0.0] * (max_length - len(lora1_weights)))
        lora2_weights.extend([0.0] * (max_length - len(lora2_weights)))
        lora3_weights.extend([0.0] * (max_length - len(lora3_weights)))

        # 新しい乱数生成器を作成
        rng = random.Random(seed)
        debug_messages.append(f"Using seed: {seed}")

        # ランダムインデックスを生成（0ベース）
        random_index = rng.randint(0, max_length - 1) if mode == 'randomize' else 0
        # 表示用に1ベースのインデックスを使用
        display_index = random_index + 1
        debug_messages.append(f"Generated index: {display_index}")

        applied_queues = []

        current_lora1 = self.get_lora_object(lora1)
        current_lora2 = self.get_lora_object(lora2)
        current_lora3 = self.get_lora_object(lora3)

        if current_lora1 is not None:
            weight = lora1_weights[random_index]
            debug_messages.append(f"Applying LoRA: {lora1} with weight: {weight} (index: {random_index + 1}/{max_length})")
            model, clip = comfy.sd.load_lora_for_models(model, clip, current_lora1, weight, weight)
            applied_queues.append(f'lora1:{weight}')

        if current_lora2 is not None:
            weight = lora2_weights[random_index]
            debug_messages.append(f"Applying LoRA: {lora2} with weight: {weight} (index: {random_index + 1}/{max_length})")
            model, clip = comfy.sd.load_lora_for_models(model, clip, current_lora2, weight, weight)
            applied_queues.append(f'lora2:{weight}')

        if current_lora3 is not None:
            weight = lora3_weights[random_index]
            debug_messages.append(f"Applying LoRA: {lora3} with weight: {weight} (index: {random_index + 1}/{max_length})")
            model, clip = comfy.sd.load_lora_for_models(model, clip, current_lora3, weight, weight)
            applied_queues.append(f'lora3:{weight}')

        output_string = f"Album: {album_name}, Applied LoRAs: " + " | ".join(applied_queues)
        debug_string = "\n".join(debug_messages)

        logger.debug(f"Output: {output_string}")
        logger.debug(f"Debug: {debug_string}")

        # 次のシード値を準備
        if control_after_generate == 'increment':
            next_seed = (seed + 1) & 0xffffffffffffffff
        elif control_after_generate == 'decrement':
            next_seed = (seed - 1) & 0xffffffffffffffff
        elif control_after_generate == 'randomize':
            next_seed = rng.randint(0, 0xffffffffffffffff)
        else:  # 'fixed'
            next_seed = seed

        return (model, clip, f"{output_string}\nDebug: {debug_string}", next_seed)
