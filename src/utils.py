import logging
import logging.config
import yaml
from pathlib import Path
from typing import Dict, Any

def setup_logging(config_path: str = "config/logging.conf") -> None:
    """Настройка логирования из конфигурационного файла"""
    if Path(config_path).exists():
        logging.config.fileConfig(config_path)
    else:
        logging.basicConfig(level=logging.INFO)

def load_config(config_path: str = "config/config.yaml") -> Dict[str, Any]:
    """Загрузка конфигурации из YAML-файла"""
    with open(config_path, 'r', encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config

def get_logger(name: str) -> logging.Logger:
    """Получить логгер по имени модуля"""
    return logging.getLogger(name)





