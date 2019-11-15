import os
from pathlib import Path
from dotenv import load_dotenv
from .paths import env_dir
from boucanpy.core.logger import logger

# bootleg history of loaded envs
# ALREAD_LOADED_ENVS = {}


# def load_env(target):
#     global ALREAD_LOADED_ENVS
#     if target not in ALREAD_LOADED_ENVS.keys():
#         target_file = target + ".env"
#         target_path = env_dir(target_file)
#         if Path(target_path).is_file():
#             logger.debug(f"loading {target} environment")
#             load_dotenv(dotenv_path=target_path)
#             ALREAD_LOADED_ENVS[target] = "loaded"
#         else:
#             logger.warning(f"failed to load {target} environment file")


def setenv(key, val):
    os.environ[key] = val


def getenv(key, default=None, optional=False):
    val = os.getenv(key, default)
    if not val and not optional:
        raise Exception(f"Value {key} cannot be null")
    return val


def getenv_bool(var_name, default=False, optional=False):
    result = default_value
    env_value = os.getenv(var_name)
    if env_value is not None:
        result = env_value.upper() in ("TRUE", "1")
    return result
