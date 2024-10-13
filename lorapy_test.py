try:
    from comfy.lora import load_lora
    print("Import successful")
except ImportError as e:
    print(f"Import failed: {e}")