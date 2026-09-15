import torch
import numpy as np
from PIL import Image
from comfy_api.latest import IO
from ..effects.inoutpaint.main import run


class InOutPaint(IO.ComfyNode):
    @classmethod
    def define_schema(cls) -> IO.Schema:
        return IO.Schema(
            node_id="InOutPaint",
            category="image/HakuImg",
            inputs=[
                IO.Image.Input("image"),
                IO.Int.Input("width", default=512, step=1),
                IO.Int.Input("height", default=512, step=1),
                IO.Int.Input("align_top", default=0, step=1),
                IO.Int.Input("align_left", default=0, step=1),
                IO.Int.Input("align_bottom", default=512, step=1),
                IO.Int.Input("align_right", default=512, step=1),
            ],
            outputs=[IO.Image.Output(display_name="image")],
        )

    @classmethod
    def execute(
        cls,
        image: torch.Tensor,
        width: int,
        height: int,
        align_top: int,
        align_left: int,
        align_bottom: int,
        align_right: int,
    ) -> IO.NodeOutput:
        image_array = image.squeeze().numpy()
        image_array = (image_array * 255).astype(np.uint8)

        pil_image = Image.fromarray(
            image_array,
            "RGB",
        ).convert("RGBA")

        pil_image, _, _ = run(
            pil_image,
            width,
            height,
            align_top,
            align_bottom,
            align_left,
            align_right,
        )

        output_array = np.array(pil_image).astype(np.float32) / 255.0
        output_image = torch.from_numpy(output_array)[None,]

        return IO.NodeOutput(output_image)
