import torch


class RemoveFirstAndLastFrame:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "process_images"

    CATEGORY = "Utils"

    def process_images(self, images):
        # Ensure input is treated as a batch (Batch, H, W, C)
        if images.dim() == 3:
            images = images.unsqueeze(0)

        total_frames = images.shape[0]


        if total_frames > 2:
            # Return everything from index 1 to -1 (excluding the last one)
            return (images[1:-1],)
        else:
            print(
                f"Warning: RemoveFirstAndLastFrame received only {total_frames} frames. Cannot remove first and last frame without emptying batch. Returning original."
            )
            return (images,)


NODE_CLASS_MAPPINGS = {"RemoveFirstAndLastFrame": RemoveFirstAndLastFrame}

NODE_DISPLAY_NAME_MAPPINGS = {"RemoveFirstAndLastFrame": "Remove First and Last Frame"}