import sys
import importlib
import gc
from pathlib import Path
from types import TracebackType


class TemporaryModulePath:
    """临时将指定目录添加到 ``sys.path``, 并在退出上下文时卸载在此期间导入的所有模块

    Example
    -------
    >>> with TemporaryModulePath("ComfyUI"):
    ...     import comfy
    ...
    >>> import comfy
    Traceback (most recent call last):
        ...
    ModuleNotFoundError
    """

    def __init__(self, path: str | Path) -> None:
        self.path = str(Path(path).resolve())

        self._old_path: list[str] | None = None
        self._new_modules: set[str] | None = None

    def __enter__(self) -> "TemporaryModulePath":
        # 保存 sys.path
        self._old_path = list(sys.path)

        # 加入模块搜索路径
        if self.path not in sys.path:
            sys.path.insert(0, self.path)

        importlib.invalidate_caches()

        # 记录进入时已经存在的模块
        self._new_modules = set(sys.modules)

        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        old_path = self._old_path
        old_modules = self._new_modules

        if old_path is None or old_modules is None:
            return False

        # 找出本次新增模块
        new_modules = set(sys.modules) - old_modules

        # 深层模块优先删除
        for name in sorted(
            new_modules,
            key=lambda name: name.count("."),
            reverse=True,
        ):
            sys.modules.pop(name, None)

        # 恢复 sys.path
        sys.path[:] = old_path

        # 清理 importlib 缓存
        importlib.invalidate_caches()

        # 尝试回收模块对象
        gc.collect()

        return False


with TemporaryModulePath(Path(__file__).parent):
    from hakuimg.runtime.requirements import setup_hakuimg

    setup_hakuimg()
