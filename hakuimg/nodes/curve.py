import numpy as np
import torch
from PIL import Image
from comfy_api.latest import IO

from ..effects.curve import run


class Curve(IO.ComfyNode):
    @classmethod
    def define_schema(cls) -> IO.Schema:
        inputs = [IO.Image.Input("image")]
        for channel in ("all", "r", "g", "b"):
            for index, default in enumerate((63, 127, 191), start=1):
                inputs.extend(
                    [
                        IO.Int.Input(f"{channel}_x_point_{index}", default=default, min=0, max=255, step=1),
                        IO.Int.Input(f"{channel}_y_point_{index}", default=default, min=0, max=255, step=1),
                    ]
                )
        return IO.Schema(
            node_id="Curve",
            category="image/HakuImg",
            inputs=inputs,
            outputs=[IO.Image.Output(display_name="image")],
        )

    @classmethod
    def execute(
        cls,
        image: torch.Tensor,
        all_x_point_1: int,
        all_y_point_1: int,
        all_x_point_2: int,
        all_y_point_2: int,
        all_x_point_3: int,
        all_y_point_3: int,
        r_x_point_1: int,
        r_y_point_1: int,
        r_x_point_2: int,
        r_y_point_2: int,
        r_x_point_3: int,
        r_y_point_3: int,
        g_x_point_1: int,
        g_y_point_1: int,
        g_x_point_2: int,
        g_y_point_2: int,
        g_x_point_3: int,
        g_y_point_3: int,
        b_x_point_1: int,
        b_y_point_1: int,
        b_x_point_2: int,
        b_y_point_2: int,
        b_x_point_3: int,
        b_y_point_3: int,
    ) -> IO.NodeOutput:
        image_array = image.squeeze().numpy()
        image_array = (image_array * 255).astype(np.uint8)

        pil_image = Image.fromarray(image_array, "RGB").convert("RGBA")

        curve_func = run(3)
        pil_image = curve_func(
            pil_image,
            all_x_point_1,
            all_y_point_1,
            all_x_point_2,
            all_y_point_2,
            all_x_point_3,
            all_y_point_3,
            r_x_point_1,
            r_y_point_1,
            r_x_point_2,
            r_y_point_2,
            r_x_point_3,
            r_y_point_3,
            g_x_point_1,
            g_y_point_1,
            g_x_point_2,
            g_y_point_2,
            g_x_point_3,
            g_y_point_3,
            b_x_point_1,
            b_y_point_1,
            b_x_point_2,
            b_y_point_2,
            b_x_point_3,
            b_y_point_3,
        )

        output_array = np.asarray(pil_image).astype(np.float32) / 255.0
        output_image = torch.from_numpy(output_array)[None,]

        return IO.NodeOutput(output_image)
