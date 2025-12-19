import torch


class NthLastFrameSelector:
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
    RETURN_NAMES = ("selected_frame", "trimmed_batch")
    FUNCTION = "process_images"

    CATEGORY = "Utils"

    def process_images(self, images, n):
        # Ensure input is treated as a batch (Batch, H, W, C)
        if images.dim() == 3:
            images = images.unsqueeze(0)

        total_frames = images.shape[0]

        # Logic: n=1 is the last frame (-1), n=total_frames is the first frame (-total_frames)

        if n > total_frames:
            print(
                f"Warning: Requested {n}th to last frame, but video only has {total_frames} frames. Returning closest appropriate frame (Frame 0)."
            )
            # If we go back further than the start, the closest frame is the first one.
            target_index = 0
        else:
            target_index = total_frames - n

        final_image = images[target_index]

        # This effectively removes all frames coming *after* the selected frame
        trimmed_images = images[: target_index + 1]

        # Ensure the single frame output is returned as a batch of 1 (1, H, W, C)
        return (final_image.unsqueeze(0), trimmed_images)


NODE_CLASS_MAPPINGS = {"NthLastFrameSelector": NthLastFrameSelector}

NODE_DISPLAY_NAME_MAPPINGS = {"NthLastFrameSelector": "Nth Last Frame Selector"}

