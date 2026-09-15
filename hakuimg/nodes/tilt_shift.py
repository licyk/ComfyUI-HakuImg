import torch
import numpy as np
from PIL import Image
from comfy_api.latest import IO
from ..effects.lens_distortion import run


class TiltShift(IO.ComfyNode):
    @classmethod
    def define_schema(cls) -> IO.Schema:
        return IO.Schema(
            node_id="TiltShift",
            category="image/HakuImg",
            inputs=[
                IO.Image.Input("image"),
                IO.Float.Input("tilt_shift_focus_ratio", default=0, min=-3, max=3, step=0.5),
                IO.Int.Input("tilt_shift_dof", default=60, min=10, max=100, step=1),
            ],
            outputs=[IO.Image.Output(display_name="image")],
        )

    @classmethod
    def execute(
        cls,
        image: torch.Tensor,
        tilt_shift_focus_ratio: float,
        tilt_shift_dof: int,
    ) -> IO.NodeOutput:
        image_tensor = image.squeeze().numpy()
        image_tensor = (image_tensor * 255).astype(np.uint8)
        image_pil = Image.fromarray(image_tensor, "RGB").convert("RGBA")

        image_pil = run(
            image_pil,
            tilt_shift_focus_ratio,
            tilt_shift_dof,
        )

        image_output = np.array(image_pil).astype(np.float32) / 255.0
        image_output = torch.from_numpy(image_output)[None,]

        return IO.NodeOutput(image_output)
