import os
import sys
import subprocess
from typing import Optional
from pathlib import Path
from .logging import get_logger
from .check import validate_requirements



logger = get_logger()


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


def setup_hakuimg():
    logger.info("Check HakuImg requirements")
    requirements_file = os.path.join(Path(__file__).resolve().parent.parent.as_posix(), "requirements.txt")
    if not validate_requirements(requirements_file):
        try:
            run_pip(f"install -r \"{requirements_file}\"", "HakuImg requirements", live=True)
        except:
            logger.error("Install HakuImg requirements failed, may cause HakuImg not to work")
            return

    logger.info("Check HakuImg requirements done")
