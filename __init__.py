from comfy_api.latest import ComfyExtension, IO

from .hakuimg.nodes.blend import BlendImage
from .hakuimg.nodes.blur import Blur
from .hakuimg.nodes.chromatic import Chromatic
from .hakuimg.nodes.color import Color
from .hakuimg.nodes.curve import Curve
from .hakuimg.nodes.custom_exif import CustomExif
from .hakuimg.nodes.flip import Flip
from .hakuimg.nodes.inoutpaint import InOutPaint
from .hakuimg.nodes.lens_distortion import LenDistortion
from .hakuimg.nodes.licyk_style import LicykStyle
from .hakuimg.nodes.neon import Neon
from .hakuimg.nodes.outline_expansion import OutlineExpansion
from .hakuimg.nodes.pixelize import Pixelize
from .hakuimg.nodes.pixeloe_ import PixelOE
from .hakuimg.nodes.pre_resize import PreResize
from .hakuimg.nodes.save_image import SaveImageWithCustomExif
from .hakuimg.nodes.sketch import Sketch
from .hakuimg.nodes.tilt_shift import TiltShift


class HakuImgExtension(ComfyExtension):
    async def get_node_list(self) -> list[type[IO.ComfyNode]]:
        return [
            BlendImage,
            Color,
            Curve,
            Blur,
            Sketch,
            PixelOE,
            Pixelize,
            Neon,
            Flip,
            Chromatic,
            LicykStyle,
            LenDistortion,
            TiltShift,
            InOutPaint,
            CustomExif,
            SaveImageWithCustomExif,
            OutlineExpansion,
            PreResize,
        ]


async def comfy_entrypoint() -> HakuImgExtension:
    return HakuImgExtension()


WEB_DIRECTORY = "./js"

__all__ = ["WEB_DIRECTORY", "comfy_entrypoint"]
