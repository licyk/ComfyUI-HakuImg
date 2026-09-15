import torch
import numpy as np
from PIL import Image
from comfy_api.latest import IO
from ..effects.pixel import run


class Pixelize(IO.ComfyNode):
    @classmethod
    def define_schema(cls) -> IO.Schema:
        return IO.Schema(
            node_id="Pixelize",
            category="image/HakuImg",
            inputs=[
                IO.Image.Input("image"),
                IO.Int.Input("colors", default=128, min=2, max=256, step=1),
                IO.Int.Input("dot_size", default=6, min=1, max=32, step=1),
                IO.Int.Input("outline", default=1, min=0, max=10, step=1),
                IO.Int.Input("smooth", default=4, min=0, max=10, step=1),
                IO.Combo.Input("mode", options=["kmeans", "dithering", "kmeans with dithering"]),
                IO.Int.Input("precise", default=10, min=0, max=1024, step=1),
                IO.Boolean.Input("resize", default=True),
            ],
            outputs=[IO.Image.Output(display_name="image")],
        )

    @classmethod
    def execute(
        cls,
        image: torch.Tensor,
        colors: int,
        dot_size: int,
        outline: int,
        smooth: int,
        mode: str,
        precise: int,
        resize: bool,
    ) -> IO.NodeOutput:
        image_array = image.squeeze().numpy()
        image_array = (image_array * 255).astype(np.uint8)

        pil_image = Image.fromarray(
            image_array,
            "RGB",
        ).convert("RGBA")

        pil_image = run(
            pil_image,
            colors,
            dot_size,
            outline,
            smooth,
            mode,
            precise,
            resize,
        )

        output_array = np.asarray(pil_image).astype(np.float32) / 255.0
        output_image = torch.from_numpy(output_array)[None,]

        return IO.NodeOutput(output_image)
