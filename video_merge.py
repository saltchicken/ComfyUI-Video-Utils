import torch


class VideoMerge:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):

        return {
            "required": {
                "video1": ("IMAGE",),
            },
            "optional": {
                "video2": ("IMAGE",),
                "video3": ("IMAGE",),
                "video4": ("IMAGE",),
                "video5": ("IMAGE",),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "merge_videos"

    CATEGORY = "Utils"

    def merge_videos(self, video1, video2=None, video3=None, video4=None, video5=None):

        videos = [video1, video2, video3, video4, video5]
        valid_videos = []

        for video in videos:
            if video is not None:
                # Ensure input is 4D tensor (Batch, H, W, C)
                if video.dim() == 3:
                    video = video.unsqueeze(0)
                valid_videos.append(video)


        if valid_videos:
            merged_video = torch.cat(valid_videos, dim=0)
            return (merged_video,)

        return (None,)



NODE_CLASS_MAPPINGS = {"VideoMerge": VideoMerge}

NODE_DISPLAY_NAME_MAPPINGS = {"VideoMerge": "Video Merge (5 Inputs)"}