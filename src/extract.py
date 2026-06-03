import pandas as pd
from pathlib import Path
from src.utils import get_logger

logger = get_logger(__name__)


def load_data(file_path: str) -> pd.DataFrame:
    """Загружает файл CSV, проверяет его наличие"""
    path = Path(file_path)

    if not path.exists():
        logger.error(f"Файл не найден {file_path}")
        raise FileNotFoundError(f"Файл не найден {file_path}")

    logger.info(f"Загрузка данных из CSV {file_path}")
    df = pd.read_csv(file_path)

    if df.empty:
        logger.error("Файл пуст")
        raise ValueError("Файл пуст")

    logger.info(f"Загружено {len(df)} строк, {len(df.columns)} колонок")
    return df

def get_data_info(df: pd.DataFrame) -> dict:
    """Возвращает метаданные DataFrame: размер, типы, пропуски, память."""
    return {
        "shape": df.shape,
        "columns": list(df.columns),
        "dtypes": df.dtypes.to_dict(),
        "null_counts": df.isnull().sum().to_dict(),
        "memory_usage": df.memory_usage(deep=True).sum() / 1024 ** 2,
    }

def print_extract_report(df: pd.DataFrame) -> None:
    """Выводит отчёт: df.head(), df.info(), df.describe(), пропуски."""
    logger.info("=" * 60)
    logger.info('EXTRACT ОТЧЁТ')
    logger.info("=" * 60)

    logger.info(f"Формат данных {df.shape[0]} строк x {df.shape[1]} колонок")
    logger.info(f"Память {df.memory_usage(deep=True).sum() / 1024 ** 2} MB")

    logger.info("\nПервые 5 строк:")
    print(df.head())

    logger.info("\nИнформация о данных:")
    buffer = []
    df.info(buf=buffer)
    logger.info("\n".join(buffer))

    logger.info("\nСтатистика по числовым колонкам")
    print(df.describe())

    logger.info("\n Пропуски в колонках")
    print(df.isnull().sum())
