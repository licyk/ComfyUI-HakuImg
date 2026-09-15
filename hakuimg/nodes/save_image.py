import json
import os

import numpy as np
import torch
from PIL import Image
from PIL.PngImagePlugin import PngInfo

import folder_paths
from comfy.cli_args import args
from comfy_api.latest import IO


class SaveImageWithCustomExif(IO.ComfyNode):
    @classmethod
    def define_schema(cls) -> IO.Schema:
        return IO.Schema(
            node_id="SaveImageWithCustomExif",
            category="image/HakuImg",
            description="Saves the input images to your ComfyUI output directory.",
            inputs=[
                IO.Image.Input("images", tooltip="The images to save."),
                IO.String.Input(
                    "filename_prefix",
                    default="ComfyUI",
                    tooltip=("The prefix for the file to save. This may include formatting information such as %date:yyyy-MM-dd% or %Empty Latent Image.width% to include values from nodes."),
                ),
            ],
            outputs=[],
            is_output_node=True,
        )

    @classmethod
    def execute(
        cls,
        images: torch.Tensor,
        filename_prefix: str = "ComfyUI",
    ) -> IO.NodeOutput:
        output_dir = folder_paths.get_output_directory()
        full_output_folder, filename, counter, subfolder, _ = folder_paths.get_save_image_path(
            filename_prefix,
            output_dir,
            images[0].shape[1],
            images[0].shape[0],
        )
        extra_pnginfo = cls.hidden.extra_pnginfo
        prompt = cls.hidden.prompt
        results = []

        for batch_number, image in enumerate(images):
            image_array = 255.0 * image.cpu().numpy()
            output_image = Image.fromarray(np.clip(image_array, 0, 255).astype(np.uint8))
            metadata = None
            if not args.disable_metadata:
                metadata = PngInfo()
                if prompt is not None:
                    metadata.add_text("prompt", json.dumps(prompt))
                if extra_pnginfo is not None:
                    for key, value in extra_pnginfo.items():
                        metadata.add_text(key, json.dumps(value))

                    workflow = extra_pnginfo.get("workflow", {})
                    for node in workflow.get("nodes", []):
                        if node.get("type") == "CustomExif":
                            widgets_values = node.get("widgets_values", [])
                            if widgets_values:
                                metadata.add_text("parameters", widgets_values[0])

            filename_with_batch_num = filename.replace("%batch_num%", str(batch_number))
            file = f"{filename_with_batch_num}_{counter:05}_.png"
            output_image.save(
                os.path.join(full_output_folder, file),
                pnginfo=metadata,
                compress_level=4,
            )
            results.append({"filename": file, "subfolder": subfolder, "type": "output"})
            counter += 1

        return IO.NodeOutput(ui={"images": results})
