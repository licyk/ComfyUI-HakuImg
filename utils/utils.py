import importlib
import os
import re
import shutil
import sys
import subprocess
import logging
import copy
from typing import Optional
from pathlib import Path



class ColoredFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[0;36m",  # CYAN
        "INFO": "\033[0;32m",  # GREEN
        "WARNING": "\033[0;33m",  # YELLOW
        "ERROR": "\033[0;31m",  # RED
        "CRITICAL": "\033[0;37;41m",  # WHITE ON RED
        "RESET": "\033[0m",  # RESET COLOR
    }

    def format(self, record):
        colored_record = copy.copy(record)
        levelname = colored_record.levelname
        seq = self.COLORS.get(levelname, self.COLORS["RESET"])
        colored_record.levelname = f"{seq}{levelname}{self.COLORS['RESET']}"
        return super().format(colored_record)



logger = logging.getLogger("ComfyUI-HakuImg")
logger.propagate = False


if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        ColoredFormatter(
            "[%(name)s]-|%(asctime)s|-%(levelname)s: %(message)s", "%H:%M:%S"
        )
    )
    logger.addHandler(handler)

logger.setLevel(logging.INFO)
logger.debug("Logger initialized.")



def run(command,
        desc: Optional[str] = None,
        errdesc: Optional[str] = None,
        custom_env: Optional[list] = None,
        live: Optional[bool] = True,
        shell: Optional[bool] = None):

    if shell is None:
        shell = False if sys.platform == "win32" else True

    if desc is not None:
        logger.info(desc)

    if live:
        result = subprocess.run(command, shell=shell, env=os.environ if custom_env is None else custom_env)
        if result.returncode != 0:
            raise RuntimeError(f"""{errdesc or 'Error running command'}.
Command: {command}
Error code: {result.returncode}""")

        return ""

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            shell=shell, env=os.environ if custom_env is None else custom_env)

    if result.returncode != 0:
        message = f"""{errdesc or 'Error running command'}.
Command: {command}
Error code: {result.returncode}
stdout: {result.stdout.decode(encoding="utf8", errors="ignore") if len(result.stdout) > 0 else '<empty>'}
stderr: {result.stderr.decode(encoding="utf8", errors="ignore") if len(result.stderr) > 0 else '<empty>'}
"""
        raise RuntimeError(message)

    return result.stdout.decode(encoding="utf8", errors="ignore")


def run_pip(command, desc=None, live=False):
    return run(f'"{sys.executable}" -m pip {command}', desc=f"Installing {desc}", errdesc=f"Couldn't install {desc}", live=live)


def get_package_version(pkg_name: str) -> str:
    try:
        ver = importlib.metadata.version(pkg_name)
    except:
        ver = None

    if ver is None:
        try:
            ver = importlib.metadata.version(pkg_name.lower())
        except:
            ver = None

    if ver is None:
        try:
            ver = importlib.metadata.version(pkg_name.replace("_", "-"))
        except:
            ver = None

    return ver


def compare_versions(version1: str, version2: str) -> int:
    try:
        nums1 = re.sub(r'[a-zA-Z]+', '', version1).replace('-', '.').replace('+', '.').split(".")
        nums2 = re.sub(r'[a-zA-Z]+', '', version2).replace('-', '.').replace('+', '.').split(".")
    except:
        return 0

    for i in range(max(len(nums1), len(nums2))):
        num1 = int(nums1[i]) if i < len(nums1) else 0
        num2 = int(nums2[i]) if i < len(nums2) else 0

        if num1 == num2:
            continue
        elif num1 > num2:
            return 1
        else:
            return -1

    return 0


def is_installed(package, friendly: str = None):
    #
    # This function was adapted from code written by vladimandic: https://github.com/vladmandic/automatic/commits/master
    #

    # Remove brackets and their contents from the line using regular expressions
    # e.g., diffusers[torch]==0.10.2 becomes diffusers==0.10.2
    package = re.sub(r'\[.*?\]', '', package)

    try:
        if friendly:
            pkgs = friendly.split()
        else:
            pkgs = [
                p
                for p in package.split()
                if not p.startswith('-') and not p.startswith('=')
            ]
            pkgs = [
                p.split('/')[-1] for p in pkgs
            ]   # get only package name if installing from URL

        for pkg in pkgs:
            pkg = pkg.split(".git")[0] if pkg.endswith(".git") else pkg
            if '>=' in pkg:
                pkg_name, pkg_version = [x.strip() for x in pkg.split('>=')]
            elif '==' in pkg:
                pkg_name, pkg_version = [x.strip() for x in pkg.split('==')]
            elif '<=' in pkg:
                pkg_name, pkg_version = [x.strip() for x in pkg.split('<=')]
            elif '>' in pkg:
                pkg_name, pkg_version = [x.strip() for x in pkg.split('>')]
            elif '<' in pkg:
                pkg_name, pkg_version = [x.strip() for x in pkg.split('<')]
            else:
                pkg_name, pkg_version = pkg.strip(), None

            version = get_package_version(pkg_name)

            if version is not None:
                if pkg_version is not None:
                    if '>=' in pkg:
                        if compare_versions(version, pkg_version) == 1 or compare_versions(version, pkg_version) == 0:
                            ok = True
                        else:
                            ok = False
                    elif '<=' in pkg:
                        if compare_versions(version, pkg_version) == -1 or compare_versions(version, pkg_version) == 0:
                            ok = True
                        else:
                            ok = False
                    elif '>' in pkg:
                        if compare_versions(version, pkg_version) == 1:
                            ok = True
                        else:
                            ok = False
                    elif '<' in pkg:
                        if compare_versions(version, pkg_version) == -1:
                            ok = True
                        else:
                            ok = False
                    else:
                        if compare_versions(version, pkg_version) == 0:
                            ok = True
                        else:
                            ok = False

                    if not ok:
                        return False
            else:
                return False

        return True
    except ModuleNotFoundError:
        return False


def validate_requirements(requirements_file: str):
    with open(requirements_file, 'r', encoding='utf8') as f:
        lines = [
            line.strip()
            for line in f.readlines()
            if line.strip() != ''
            and not line.startswith("#")
            and not (line.startswith("-") and not line.startswith("--index-url "))
            and line is not None
            and "# skip_verify" not in line
        ]

        for line in lines:
            if line.startswith("--index-url "):
                continue

            if not is_installed(line):
                print(f"{line} not install")
                return False

        return True


def setup_hakuimg():
    logger.info("Check HakuImg requirements")
    requirements_file = os.path.join(Path(__file__).resolve().parent.parent.as_posix(), "requirements.txt")
    if not validate_requirements(requirements_file):
        print(f":: {validate_requirements(requirements_file)}")
        try:
            run_pip(f"install -r \"{requirements_file}\"", "Installing HakuImg requirements", live=True)
        except:
            logger.error("Install HakuImg requirements failed, may cause HakuImg not to work")
            return

    logger.info("Check HakuImg requirements done")


def setup_pixeloe():
    logger.info("Check HakuImg submodule module: PixelOE")
    try:
        from ..hakuimg.PixelOE.pixeloe.pixelize import pixelize
    except:
        if not shutil.which("git"):
            logger.error("Git not found in, cannot init HakuImg submodule module and may cause HakuImg not to work")
            return

        logger.info("Initializing HakuImg submodule module: PixelOE")
        hakuimg_path = Path(__file__).resolve().parent.parent.as_posix()
        try:
            run(f"git -C \"{hakuimg_path}\" submodule update --init --recursive")
        except:
            logger.error("Init HakuImg submodule module failed, may cause HakuImg not to work")
            return

    logger.info("Check HakuImg submodule module done")