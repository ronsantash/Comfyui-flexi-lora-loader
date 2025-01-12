__version__ = '0.2.1'

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

class ComfyUIFlexiLoRALoader:
    # 定数の定義
    MAX_WEIGHT = 1.0
    MIN_WEIGHT = 0.0
    DEFAULT_LORA1_WEIGHTS = '0.6,0.4,0.5,0.3,0.2,0.3,0.1,0.1,0.5,0.2'
    DEFAULT_LORA2_WEIGHTS = '0.4,0.6,0.5,0.6,0.4,0.3,0.6,0.4,0.5,0.2'
    DEFAULT_LORA3_WEIGHTS = '0.2,0.0,0.1,0.3,0.2,0.3,0.2,0.1,0.1,0.1'

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
                'lora1_weight': ('STRING', {'multiline': False, 'default': cls.DEFAULT_LORA1_WEIGHTS}),
                'lora2': (lora_list,),
                'lora2_weight': ('STRING', {'multiline': False, 'default': cls.DEFAULT_LORA2_WEIGHTS}),
                'lora3': (lora_list,),
                'lora3_weight': ('STRING', {'multiline': False, 'default': cls.DEFAULT_LORA3_WEIGHTS}),
                'seed': ('INT', {'default': 0, 'min': 0, 'max': 0xffffffffffffffff}),
            },
        }

    RETURN_TYPES = ("MODEL", "CLIP", "STRING", "STRING", "INT")
    RETURN_NAMES = ("model", "clip", "memo", "album_name", "seed")
    FUNCTION = "apply_loras"
    CATEGORY = "loaders/lora"

    def get_weights(self, input_text):
        try:
            if not input_text.strip():
                return [0.0]
            return [float(x) for x in input_text.split(',')]
        except ValueError:
            logger.error(f"Invalid weight format: {input_text}")
            return [0.0]

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

    def get_next_seed(self, current_seed, mode='randomize'):
        if mode == 'increment':
            return (current_seed + 1) & 0xffffffffffffffff
        elif mode == 'decrement':
            return (current_seed - 1) & 0xffffffffffffffff
        elif mode == 'randomize':
            return self.rng.randint(0, 0xffffffffffffffff)
        return current_seed

    def format_output_message(self, album_name, applied_queues, debug_messages, random_index, max_length):
        output_lines = [
            f"Album: {album_name}",
            f"Applied LoRAs: {' | '.join(applied_queues)}",
            f"Index: {random_index + 1}/{max_length}",
            "Debug Info:",
            *debug_messages
        ]
        return "\n".join(output_lines)

    def apply_loras(self, mode, album_name, model, clip, lora1, lora1_weight, lora2, lora2_weight,
                   lora3, lora3_weight, seed, control_after_generate='randomize'):
        debug_messages = []

        # 重み値の処理
        lora1_weights = self.get_weights(lora1_weight)
        lora2_weights = self.get_weights(lora2_weight)
        lora3_weights = self.get_weights(lora3_weight)

        # 最大長を取得
        max_length = max(len(lora1_weights), len(lora2_weights), len(lora3_weights))
        debug_messages.append(f"Max length: {max_length}")

        # 足りない要素を0で補完
        lora1_weights.extend([0.0] * (max_length - len(lora1_weights)))
        lora2_weights.extend([0.0] * (max_length - len(lora2_weights)))
        lora3_weights.extend([0.0] * (max_length - len(lora3_weights)))

        # 新しい乱数生成器を作成
        self.rng = random.Random(seed)
        debug_messages.append(f"Using seed: {seed}")

        # ランダムインデックスを生成
        random_index = self.rng.randint(0, max_length - 1) if mode == 'randomize' else 0
        debug_messages.append(f"Generated index: {random_index + 1}")

        applied_queues = []

        # LoRAの適用
        lora_configs = [
            (lora1, lora1_weights, "lora1"),
            (lora2, lora2_weights, "lora2"),
            (lora3, lora3_weights, "lora3")
        ]

        for lora_name, weights, lora_id in lora_configs:
            current_lora = self.get_lora_object(lora_name)
            if current_lora is not None:
                weight = weights[random_index]
                debug_messages.append(f"Applying LoRA: {lora_name} with weight: {weight}")
                model, clip = comfy.sd.load_lora_for_models(model, clip, current_lora, weight, weight)
                applied_queues.append(f'{lora_id}:{weight}')

        # 出力メッセージの作成
        output_message = self.format_output_message(
            album_name, applied_queues, debug_messages, random_index, max_length
        )

        # 次のシード値を準備
        next_seed = self.get_next_seed(seed, control_after_generate)

        return (model, clip, output_message, album_name, next_seed)
