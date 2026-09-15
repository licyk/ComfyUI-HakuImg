"""配置管理"""

import os
import logging
from pathlib import Path

LOGGER_NAME = None if os.getenv("HAKUIMG_LOGGER_NAME") in ["none", "None", "NONE"] else os.getenv("HAKUIMG_LOGGER_NAME", "HakuImg")
"""日志器名字"""

LOGGER_LEVEL = int(os.getenv("HAKUIMG_LOGGER_LEVEL", str(logging.INFO)))
"""日志等级"""

LOGGER_COLOR = os.getenv("HAKUIMG_LOGGER_COLOR") not in ["0", "False", "false", "None", "none", "null"]
"""日志颜色"""

ROOT_PATH = Path(__file__).parent.parent
"""SD WebUI All In One 根目录"""

REQUIREMENTS_PATH = ROOT_PATH.parent.parent / "requirements.txt"
"""依赖文件路径"""
