from __future__ import annotations

from typing import Any, Callable, cast

from PIL import Image
import numpy as np
from scipy import interpolate

import matplotlib

matplotlib.use("agg")
from matplotlib import pyplot as plt

plt.style.use("dark_background")


def make_curve(x_in: list[int], y_in: list[int]) -> Callable[[Any], Any]:
    assert len(x_in) == len(y_in)
    his = set([0, 255])

    xs = []
    ys = []
    for x, y in sorted(zip(x_in, y_in)):
        if x not in his:
            xs.append(x)
            ys.append(y)
            his.add(x)

    if len(xs):
        spline = interpolate.make_interp_spline(
            [0, *xs, 255], [0, *ys, 255], 2 + (len(xs) > 1)
        )
        return lambda x: np.clip(spline(x), 0, 255)
    else:
        return lambda x: x


def make_plot(points: tuple[list[int], list[int]]) -> Image.Image:
    xs, ys = points
    curve = make_curve(xs, ys)
    fig, ax = plt.subplots(1, 1)

    x = np.arange(0, 255, 1)
    y = np.clip(curve(x), 0, 255)

    ax.set_xlim(0, 255)
    ax.set_ylim(0, 255)
    ax.plot([0, 255], [0, 255], "white")
    ax.plot(x, y)
    ax.plot([0, *sorted(xs), 255], [0, *sorted(ys), 255], "ro")

    fig.canvas.draw()
    canvas = cast(Any, fig.canvas)
    rgba = np.asarray(canvas.buffer_rgba())
    img = Image.fromarray(rgba[:, :, :3], "RGB")
    plt.close("all")
    del fig, ax
    return img


def run(points: int) -> Callable[..., np.ndarray]:
    def curve(img: np.ndarray[Any, Any], *args: list[int]) -> np.ndarray:
        nonlocal points
        # all, r, g, b
        point = points * 2
        all, r, g, b = (
            (k[::2], k[1::2])
            for i in range(4)
            for k in [args[i * point : i * point + point]]
        )

        img = np.array(img)
        img[:, :, 0] = make_curve(*r)(img[:, :, 0])
        img[:, :, 1] = make_curve(*g)(img[:, :, 1])
        img[:, :, 2] = make_curve(*b)(img[:, :, 2])
        img = make_curve(*all)(img)
        return img.astype(np.uint8)

    return curve


def curve_img(*all_points: int) -> Image.Image:
    return make_plot((all_points[::2], all_points[1::2]))


if __name__ == "__main__":
    from matplotlib import pyplot as plt
    from time import time_ns

    plt.style.use("dark_background")

    t0 = time_ns()
    fig, ax = plt.subplots(1, 1)

    xs = [50, 125, 200]
    ys = [40, 150, 180]

    t2 = time_ns()
    curve = make_curve(xs, ys)
    x = np.arange(0, 255, 0.00001)
    y = np.clip(curve(x), 0, 255)
    t3 = time_ns()

    ax.set_xlim(0, 255)
    ax.set_ylim(0, 255)
    ax.plot([0, 255], [0, 255], "white")
    ax.plot(x[::10000], y[::10000])
    ax.plot([0, *xs, 255], [0, *ys, 255], "ro")

    fig.canvas.draw()
    canvas = cast(Any, fig.canvas)
    img = Image.frombytes("RGB", canvas.get_width_height(), canvas.tostring_rgb())
    plt.close(fig)

    t1 = time_ns()
    print((t1 - t0) / 1e6)
    print((t3 - t2) / 1e6, x.size)

    img.show()
