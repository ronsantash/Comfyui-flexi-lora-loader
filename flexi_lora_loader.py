import os
import comfy.utils
import comfy.sd
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
            loras_to_apply = [
                (lora1, lora1_weights[i], "lora1"),
                (lora2, lora2_weights[i], "lora2"),
                (lora3, lora3_weights[i], "lora3")
            ]

            for lora_name, weight, lora_key in loras_to_apply:
                if lora_name != 'None' and weight > 0:
                    try:
                        debug_messages.append(f"Loading LoRA: {lora_name} with weight: {weight}")
                        lora_path = folder_paths.get_full_path("loras", lora_name)
                        lora = comfy.utils.load_torch_file(lora_path, safe_load=True)
                        model, clip = comfy.sd.load_lora_for_models(model, clip, lora, weight, weight)
                        queue.append(f'{lora_key}:{weight}')
                    except Exception as e:
                        debug_messages.append(f"Error applying LoRA {lora_name}: {str(e)}")

            if queue:
                applied_queues.append(' '.join(queue))

        output_string = f"Album: {album_name}, Applied LoRAs: " + " | ".join(applied_queues)
        weights_display = output_string
        debug_display = "\n".join(debug_messages)

        # クリッピングを適用（必要に応じて）
        # model = self.clip_weights(model)
        # clip = self.clip_weights(clip)

        return (model, clip, output_string, weights_display, debug_display)

    # 必要に応じて重みをクリッピングするメソッド
    def clip_weights(self, module, min_val=-5, max_val=5):
        with torch.no_grad():
            for param in module.parameters():
                param.clamp_(min_val, max_val)
        return module
