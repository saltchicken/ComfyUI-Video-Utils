import torch


class LastNFramesSelector:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "n": ("INT", {"default": 1, "min": 1, "max": 1000000, "step": 1}),
            },
        }

    RETURN_TYPES = ("IMAGE", "IMAGE")
    RETURN_NAMES = ("last_n_frames", "preceding_frames")
    FUNCTION = "process_images"

    CATEGORY = "Utils"

    def process_images(self, images, n):
        # Ensure input is treated as a batch (Batch, H, W, C)
        if images.dim() == 3:
            images = images.unsqueeze(0)

        total_frames = images.shape[0]

        if n >= total_frames:
            print(
                f"Warning: Requested last {n} frames, but only {total_frames} available. Returning all frames as last_n."
            )
            return (images, None)

        # Slice for last n frames
        last_n = images[-n:]
        # Slice for frames before the last n
        preceding = images[:-n]

        return (last_n, preceding)


NODE_CLASS_MAPPINGS = {"LastNFramesSelector": LastNFramesSelector}

NODE_DISPLAY_NAME_MAPPINGS = {"LastNFramesSelector": "Last N Frames Selector"}
