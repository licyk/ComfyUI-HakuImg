from .hakuimg.nodes.pixelize import PIXELIZE
from .hakuimg.nodes.blur import BLUR
from .hakuimg.nodes.neon import NEON
from .hakuimg.nodes.flip import FLIP
from .hakuimg.nodes.sketch import SKETCH
from .hakuimg.nodes.color import COLOR
from .hakuimg.nodes.curve import CURVE
from .hakuimg.nodes.chromatic import CHROMATIC
from .hakuimg.nodes.lens_distortion import LENDISTORTION
from .hakuimg.nodes.tilt_shift import TILTSHIFT
from .hakuimg.nodes.inoutpaint import INOUTPAINT
from .hakuimg.nodes.custom_exif import CUSTOMEXIF
from .hakuimg.nodes.blend import BLENDIMAGE
from .hakuimg.nodes.save_image import SaveImageWithCustomExif
from .hakuimg.nodes.pixeloe_ import PixelOE
from .hakuimg.nodes.outline_expansion import OutlineExpansion
from .hakuimg.nodes.pre_resize import PreResize

NODE_CLASS_MAPPINGS = {
    "BlendImage": BLENDIMAGE,
    "Color": COLOR,
    "Curve": CURVE,
    "Blur" : BLUR,
    "Sketch" : SKETCH,
    "Glow" : NEON,
    "Flip" : FLIP,
    "Chromatic": CHROMATIC,
    "LenDistortion": LENDISTORTION,
    "TiltShift": TILTSHIFT,
    "InOutPaint": INOUTPAINT,
    "CustomExif": CUSTOMEXIF,
    "SaveImageWithCustomExif": SaveImageWithCustomExif,
    "Pixelize": PIXELIZE,
    "PixelOE": PixelOE,
    "OutlineExpansion": OutlineExpansion,
    "PreResize": PreResize,
}


WEB_DIRECTORY = "./js"

__all__ = ["NODE_CLASS_MAPPINGS", "WEB_DIRECTORY"]
