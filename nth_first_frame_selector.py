import torch


class NthFirstFrameSelector:
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



        if n > total_frames:
            print(
                f"Warning: Requested {n}th frame, but video only has {total_frames} frames. Returning closest appropriate frame (Last Frame)."
            )

            target_index = total_frames - 1
        else:

            target_index = n - 1

        final_image = images[target_index]


        # (Symmetric to NthLastFrameSelector which returns UP TO the selected frame)
        trimmed_images = images[target_index:]

        # Ensure the single frame output is returned as a batch of 1 (1, H, W, C)
        return (final_image.unsqueeze(0), trimmed_images)


NODE_CLASS_MAPPINGS = {"NthFirstFrameSelector": NthFirstFrameSelector}

NODE_DISPLAY_NAME_MAPPINGS = {"NthFirstFrameSelector": "Nth First Frame Selector"}