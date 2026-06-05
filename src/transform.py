import pandas as pd
from src.utils import get_logger

logger = get_logger(__name__)


def clean_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Функция для преобразования строк Transaction_Date в datetime"""
    logger.info("Преобразуем в datetime")

    df["Transaction_Date"] = pd.to_datetime(df["Transaction_Date"], format="%d-%m-%Y", errors='coerce')

    invalid_dates = df["Transaction_Date"].isna().sum()

    if invalid_dates > 0:
        logger.warning(f"Мы нашли {invalid_dates} строк с некорректными датами. Они будут удалены.")

        df = df.dropna(subset=["Transaction_Date"])

    df["Month"] = df["Transaction_Date"].dt.month
    df["Month_name"] = df["Transaction_Date"].dt.strftime('%B')
    df["Day_Of_Week"] = df["Transaction_Date"].dt.dayofweek
    df["Day_Name"] = df["Transaction_Date"].dt.strftime('%a')

    logger.info(f'Диапазон дат с {df["Transaction_Date"].min()} по {df["Transaction_Date"].max()}')
    return df


def fix_total_spent(df: pd.DataFrame) -> pd.DataFrame:
    """Функция проверяет и исправляет Total Spent = Quantity * Price_Per_Unit"""
    logger.info("Проверка целостности Total-Spent...")

    calculated = df["Quantity"] * df["Price_Per_Unit"]
    mismatches = (df['Total_Spent'] != calculated).sum()

    if mismatches > 0:
        logger.warning(f"Найдено {mismatches} несоответствий в Total_Spent. Исправляем...")
        df["Total_Spent"] = calculated

    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Функция удаляет дубликаты в DataFrame"""
    before = len(df)
    df = df.drop_duplicates(subset=["Transaction_Id"], keep="first")
    after= len(df)

    if before - after > 0:
        logger.info(f"Удалено {before - after} дубликатов по Transaction_Id")

    return df


def handle_negative_values(df: pd.DataFrame) -> pd.DataFrame:
    """Функция проверяет строки с отрицательными значениями в Quantity, Price_Per_Unit, Total_Spent."""
    logger.info("""Проверка отрицательных значений""")

    before = len(df)
    mask = (df["Quantity"] < 0) | (df["Price_Per_Unit"] < 0) | (df["Total_Spent"] < 0)
    negative_count = mask.sum()

    if negative_count > 0:
        logger.warning(f"Найдено {negative_count} строк с отрицательными значениями. Удаляем...")
        df = df[~mask]

    logger.info(f"Удалено {before - len(df)} строк с отрицательными значениями")
    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Удаляет строки с пропусками в критических колонках."""
    critical_cols = ["Transaction_Id", "Item", "Quantity", "Price_Per_Unit", "Total_Spent"]

    before = len(df)
    df = df.dropna(subset=critical_cols)
    after = len(df)

    if before - after > 0:
        logger.info(f"Удалено {before - after} строк с пропусками в критических колонках")

    return df


def add_price_category(df: pd.DataFrame) -> pd.DataFrame:
    """Функция добавляет колонку Price_Category (Low/Medium/High)."""
    logger.info("Добавляем категории цен...")

    def categorize(price):
        if price < 5:
            return "Low"
        elif price < 8:
            return "Medium"
        else:
            return "High"

    df["Price_Category"] = df["Price_Per_Unit"].apply(categorize)

    logger.info(f"Категории: Low={len(df[df['Price_Category'] == 'Low'])}, "
            f"Medium={len(df[df['Price_Category'] == 'Medium'])}, "
            f"High={len(df[df['Price_Category'] == 'High'])}"
                )

    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Основная функция: запускает все шаги очистки по порядку."""
    logger.info("=" * 60)
    logger.info("ЗАПУСК ТРАНСФОРМАЦИИ ДАННЫХ")
    logger.info("=" * 60)

    df = clean_dates(df)
    df = fix_total_spent(df)
    df = remove_duplicates(df)
    df = handle_negative_values(df)
    df = handle_missing_values(df)
    df = add_price_category(df)

    logger.info(f"Итоговое количество строк после очистки: {len(df)}")
    logger.info("=" * 60)

    return df

