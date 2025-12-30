import torch


class FirstNFramesSelector:
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
    RETURN_NAMES = ("first_n_frames", "remaining_frames")
    FUNCTION = "process_images"

    CATEGORY = "Utils"

    def process_images(self, images, n):
        # Ensure input is treated as a batch (Batch, H, W, C)
        if images.dim() == 3:
            images = images.unsqueeze(0)

        total_frames = images.shape[0]

        if n >= total_frames:
            print(
                f"Warning: Requested {n} frames, but only {total_frames} available. Returning all frames as first_n."
            )
            return (images, None)

        first_n = images[:n]
        remaining = images[n:]

        return (first_n, remaining)


NODE_CLASS_MAPPINGS = {"FirstNFramesSelector": FirstNFramesSelector}

NODE_DISPLAY_NAME_MAPPINGS = {"FirstNFramesSelector": "First N Frames Selector"}
