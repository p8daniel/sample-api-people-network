import json
from pathlib import Path
from typing import Dict

from pydantic import FilePath
from pydantic_settings import BaseSettings


class LogEnvSettings(BaseSettings):
    """Settings model from log configuration"""

    LOG_CONFIG: FilePath = Path(__file__).parent / "log_config/base_log_config.json"


def load_log_configuration() -> Dict:
    """Load log configuration from file"""
    with LogEnvSettings().LOG_CONFIG.open(encoding="UTF-8") as conf_file:
        logconfig_dict: Dict = json.load(conf_file)

    return logconfig_dict
