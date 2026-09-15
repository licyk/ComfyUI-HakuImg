import torch
from comfy_api.latest import IO
from ..effects.pre_resize import run


class PreResize(IO.ComfyNode):
    @classmethod
    def define_schema(cls) -> IO.Schema:
        return IO.Schema(
            node_id="PreResize",
            category="image/HakuImg",
            inputs=[
                IO.Image.Input("img"),
                IO.Int.Input("target_pixels", default=256, min=1, max=1024),
                IO.Int.Input("pixel_size", default=4, min=1, max=32),
                IO.Combo.Input("device", options=["default", "cpu", "cuda", "mps"]),
            ],
            outputs=[IO.Image.Output(display_name="img")],
        )

    @classmethod
    def execute(
        cls,
        img: torch.Tensor,
        target_pixels: int,
        pixel_size: int,
        device: str,
    ) -> IO.NodeOutput:
        result = run(
            img=img,
            target_pixels=target_pixels,
            pixel_size=pixel_size,
            device=device,
        )

        return IO.NodeOutput(*result)
