import torch
from comfy_api.latest import IO
from ..effects.pixeloe import run


def image_preprocess(img: torch.Tensor, device: str) -> tuple[torch.Tensor, bool, torch.device]:
    if img.ndim == 3:
        img = img.unsqueeze(0)
    if img.size(3) <= 4:
        img = img.permute(0, 3, 1, 2)
        use_channel_last = True
    if img.size(1) == 4:
        img = img[:, :3]
    org_device = img.device
    if device != "default":
        img = img.to(device)
    return img, use_channel_last, org_device


class PixelOE(IO.ComfyNode):
    @classmethod
    def define_schema(cls) -> IO.Schema:
        return IO.Schema(
            node_id="PixelOE",
            category="image/HakuImg",
            inputs=[
                IO.Int.Input("pixel_size", default=4, min=1, max=32),
                IO.Int.Input("thickness", default=2, min=0, max=6),
                IO.Image.Input("img"),
                IO.Combo.Input("mode", options=["contrast", "k_centroid", "lanczos", "nearest", "bilinear"]),
                IO.Boolean.Input("color_quant", default=False),
                IO.Boolean.Input("no_post_upscale", default=False),
                IO.Int.Input("num_colors", default=256, min=2, max=256),
                IO.Combo.Input("quant_mode", options=["kmeans", "weighted-kmeans", "repeat-kmeans"]),
                IO.Combo.Input("dither_mode", options=["ordered", "error_diffusion", "none"]),
                IO.Combo.Input("device", options=["default", "cpu", "cuda", "mps"]),
            ],
            outputs=[
                IO.Image.Output(display_name="pixel_image"),
                IO.Image.Output(display_name="oe_image"),
                IO.Image.Output(display_name="oe_weight"),
            ],
        )

    @classmethod
    def execute(
        cls,
        pixel_size: int,
        thickness: int,
        img: torch.Tensor,
        mode: str,
        color_quant: bool,
        no_post_upscale: bool,
        num_colors: int,
        quant_mode: str,
        dither_mode: str,
        device: str,
    ) -> IO.NodeOutput:
        result, oe_image, oe_weight = run(
            pixel_size=pixel_size,
            thickness=thickness,
            img=img,
            mode=mode,
            color_quant=color_quant,
            no_post_upscale=no_post_upscale,
            num_colors=num_colors,
            quant_mode=quant_mode,
            dither_mode=dither_mode,
            device=device,
        )

        return IO.NodeOutput(result, oe_image, oe_weight)
