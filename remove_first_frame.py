import torch


class RemoveFirstFrame:
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


        if total_frames > 1:
            # Return everything from index 1 onwards
            return (images[1:],)
        else:
            print(
                f"Warning: RemoveFirstFrame received only {total_frames} frame. Cannot remove first frame without emptying batch. Returning original."
            )
            return (images,)


NODE_CLASS_MAPPINGS = {"RemoveFirstFrame": RemoveFirstFrame}

NODE_DISPLAY_NAME_MAPPINGS = {"RemoveFirstFrame": "Remove First Frame"}