import torch
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import folder_paths
import os
import random


class PreviewImageWithCounter:
    def __init__(self):
        self.output_dir = folder_paths.get_temp_directory()
        self.type = "temp"
        self.prefix_append = "_temp_" + "".join(
            random.choice("abcdefghijklmnopqrstupvxyz") for x in range(5)
        )

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

    RETURN_TYPES = ()
    OUTPUT_NODE = True
    FUNCTION = "save_images"
    CATEGORY = "Utils"

    def save_images(self, images, prompt=None, extra_pnginfo=None):
        results = list()

        if images.dim() == 3:
            images = images.unsqueeze(0)


        total_frames = images.shape[0]


        valid_font_path = None
        font_candidates = [
            "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/noto/NotoSans-Bold.ttf",
            "arial.ttf",
            "Arial.ttf",
        ]

        for path in font_candidates:
            try:
                # Test load with dummy size
                ImageFont.truetype(path, 10)
                valid_font_path = path
                break
            except (OSError, IOError):
                continue

        for batch_number, image in enumerate(images):
            i = 255.0 * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))

            draw = ImageDraw.Draw(img)

            font_size = max(16, int(img.height * 0.05))


            if valid_font_path:
                font = ImageFont.truetype(valid_font_path, font_size)
            else:
                font = ImageFont.load_default()


            n_value = total_frames - batch_number
            text = str(n_value)

            text_pos = (10, 10)

            # Calculate text background
            try:
                bbox = draw.textbbox(text_pos, text, font=font)
            except AttributeError:
                text_w, text_h = draw.textsize(text, font=font)
                bbox = (
                    text_pos[0],
                    text_pos[1],
                    text_pos[0] + text_w,
                    text_pos[1] + text_h,
                )

            draw.rectangle(bbox, fill="black", outline="black")
            draw.text(text_pos, text, fill="white", font=font)

            filename = f"{self.prefix_append}_{batch_number:05}_.png"
            file = os.path.join(self.output_dir, filename)


            img.save(file, compress_level=1)

            results.append({"filename": filename, "subfolder": "", "type": self.type})

        return {"ui": {"images": results}}


NODE_CLASS_MAPPINGS = {"PreviewImageWithCounter": PreviewImageWithCounter}

NODE_DISPLAY_NAME_MAPPINGS = {"PreviewImageWithCounter": "Preview Image (Frame Count)"}