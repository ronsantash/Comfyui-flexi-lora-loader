import os
import comfy.utils
import comfy.sd
import folder_paths
import safetensors.torch
import logging
import json

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

current_index = 0  # グローバル変数

class FlexiLoRALoader:

    # 初期値を変数として定義
    DEFAULT_LORA1_WEIGHTS = '0.7,0.6,0.4,0.1,0.2,0.3,0.4,0.5,0.2,0.8,0.2'
    DEFAULT_LORA2_WEIGHTS = '0.3,0.4,0.6,0.1,0.2,0.3,0.4,0.5,0.8,0.2,0.6'
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
            },
        }

    RETURN_TYPES = ("MODEL", "CLIP", "STRING")
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

    def apply_loras(self, mode, album_name, model, clip, lora1, lora1_text, lora2, lora2_text, lora3, lora3_text):
        global current_index

        # インデックスファイルのパスを設定
        index_file = os.path.join(os.path.dirname(__file__), 'lora_index.json')
        # インデックスをファイルから読み込む
        if os.path.exists(index_file):
            with open(index_file, 'r') as f:
                data = json.load(f)
                current_index = data['index']
        else:
            current_index = 0

        lora1_weights = [float(x) for x in (lora1_text or self.DEFAULT_LORA1_WEIGHTS).split(',')]
        lora2_weights = [float(x) for x in (lora2_text or self.DEFAULT_LORA2_WEIGHTS).split(',')]
        lora3_weights = [float(x) for x in (lora3_text or self.DEFAULT_LORA3_WEIGHTS).split(',')]

        max_length = max(len(lora1_weights), len(lora2_weights), len(lora3_weights))

        # 現在のインデックスが最大長を超えた場合、0にリセット
        if current_index >= max_length:
            current_index = 0

        current_lora1 = self.get_lora_object(lora1)
        current_lora2 = self.get_lora_object(lora2)
        current_lora3 = self.get_lora_object(lora3)

        applied_loras = []

        if current_lora1 is not None and current_index < len(lora1_weights):
            weight = lora1_weights[current_index]
            model, clip = comfy.sd.load_lora_for_models(model, clip, current_lora1, weight, weight)
            applied_loras.append(f"{lora1}:{weight}")

        if current_lora2 is not None and current_index < len(lora2_weights):
            weight = lora2_weights[current_index]
            model, clip = comfy.sd.load_lora_for_models(model, clip, current_lora2, weight, weight)
            applied_loras.append(f"{lora2}:{weight}")

        if current_lora3 is not None and current_index < len(lora3_weights):
            weight = lora3_weights[current_index]
            model, clip = comfy.sd.load_lora_for_models(model, clip, current_lora3, weight, weight)
            applied_loras.append(f"{lora3}:{weight}")

        # 次のインデックスを計算
        current_index = (current_index + 1) % max_length

        # 新しいインデックスを保存
        with open(index_file, 'w') as f:
            json.dump({'index': current_index}, f)

        output_string = ",".join(applied_loras)

        return (model, clip, output_string)
