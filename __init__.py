from .utils.utils import setup_hakuimg, setup_pixeloe

setup_hakuimg()
setup_pixeloe()

from .nodes.pixeloe import PIXELOE
from .nodes.pixelize import PIXELIZE
from .nodes.blur import BLUR
from .nodes.neon import NEON
from .nodes.flip import FLIP
from .nodes.sketch import SKETCH
from .nodes.color import COLOR
from .nodes.curve import CURVE
from .nodes.chromatic import CHROMATIC
from .nodes.lens_distortion import LENDISTORTION
from .nodes.tilt_shift import TILTSHIFT
from .nodes.inoutpaint import INOUTPAINT
from .nodes.custom_exif import CUSTOMEXIF
from .nodes.blend import BLENDIMAGE

NODE_CLASS_MAPPINGS = {
    "BlendImage": BLENDIMAGE,
    "Color": COLOR,
    "Curve": CURVE,
    "Blur" : BLUR,
    "Sketch" : SKETCH,
    "PixelOE" : PIXELOE,
    "Pixelize": PIXELIZE,
    "Glow" : NEON,
    "Flip" : FLIP,
    "Chromatic": CHROMATIC,
    "LenDistortion": LENDISTORTION,
    "TiltShift": TILTSHIFT,
    "InOutPaint": INOUTPAINT,
    "CustomExif": CUSTOMEXIF,
}

__all__ = ['NODE_CLASS_MAPPINGS']