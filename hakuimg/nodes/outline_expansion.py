import torch
from comfy_api.latest import IO
from ..effects.outline_expansion import run


class OutlineExpansion(IO.ComfyNode):
    @classmethod
    def define_schema(cls) -> IO.Schema:
        return IO.Schema(
            node_id="OutlineExpansion",
            category="image/HakuImg",
            inputs=[
                IO.Image.Input("img"),
                IO.Int.Input("pixel_size", default=4, min=1, max=32),
                IO.Int.Input("thickness", default=3, min=1, max=6),
                IO.Combo.Input("device", options=["default", "cpu", "cuda", "mps"]),
            ],
            outputs=[
                IO.Image.Output(display_name="oe_image"),
                IO.Image.Output(display_name="oe_weight"),
            ],
        )

    @classmethod
    def execute(
        cls,
        img: torch.Tensor,
        pixel_size: int,
        thickness: int,
        device: str,
    ) -> IO.NodeOutput:
        oe_image, oe_weight = run(
            img=img,
            pixel_size=pixel_size,
            thickness=thickness,
            device=device,
        )

        return IO.NodeOutput(oe_image, oe_weight)
