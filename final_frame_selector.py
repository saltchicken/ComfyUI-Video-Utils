import torch


class FinalFrameSelector:
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

        if images.dim() == 4:

            final_image = images[-1]

            # Ensure the image is in the correct format (Batch, H, W, C)
            if final_image.dim() == 3:
                final_image = final_image.unsqueeze(0)

            return (final_image,)

        # Handle single image
        elif images.dim() == 3:
            return (images.unsqueeze(0),)

        else:
            return (None,)



NODE_CLASS_MAPPINGS = {"FinalFrameSelector": FinalFrameSelector}

NODE_DISPLAY_NAME_MAPPINGS = {"FinalFrameSelector": "Final Frame Selector"}