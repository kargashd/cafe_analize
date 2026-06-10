import pandas as pd
from src.utils import get_logger


logger = get_logger(__name__)

def top_items_by_revenue(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """Функция для определения топ n товаров по выручке"""
    logger.info(f"Топ {n} товаров по выручке")
    result = df.groupby('Item')['Total_Spent'].sum().sort_values(ascending=False).head(n).reset_index()
    result.columns = ['Item', 'Total_Revenue']
    return result


def top_items_by_quantity(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """Функция для определения топ n товаров по количеству продаж"""
    logger.info(f"Топ {n} товаров по количеству продаж")
    result = df.groupby('Item')['Quantity'].sum().sort_values(ascending=False).head(n).reset_index()
    result.columns = ['Item', 'Total_Quantity']
    return result


def popular_method_by_count(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """Функция для определения самого популярного способа оплаты по количеству транзакций"""
    logger.info("Самый популярный способ оплаты по количеству транзакций")
    result = df['Payment_Method'].value_counts()
    return result


def popular_method_by_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """Функция для определения самого популярного способа оплаты по выручке"""
    logger.info(f"Самый популярный способ по выручке")
    result = df.groupby('Payment_Method')['Total_Spent'].sum().sort_values(ascending=False)
    return result


def revenue_by_location(df: pd.DataFrame) -> pd.Series:
    """Функция для сравнение выручки Takeaway vs Dine-in"""
    logger.info(f"Сравниваем выручку Takeaway и Dine-in")
    result = df.groupby('Location')['Total_Spent'].sum().sort_values(ascending=False)
    return result


def revenue_by_month(df: pd.DataFrame) -> pd.DataFrame:
    """Функция для определения выручки по месяцам(сортировка по убыванию)"""
    logger.info(f"Определим выручку по месяцам")
    result = df.groupby('Month')['Total_Spent'].sum().sort_values(ascending=False).reset_index()
    result.columns = ['Month', 'Total_revenue']
    return result


def avg_check_by_month(df: pd.DataFrame) -> pd.DataFrame:
    """Функция для определения среднего чека по месяцам"""
    logger.info(f"Определим средний чек по месяцам")
    result = df.groupby('Month')['Total_Spent'].mean().sort_values(ascending=False).reset_index()
    result.columns = ['Month', 'Avg_Check']
    return result


def best_day_by_revenue(df: pd.DataFrame) -> pd.Series:
    """Функция для определения дня недели с максимальной выручкой"""
    logger.info(f"Определим день недели с максимальной выручкой")
    return df.groupby('Day_Name')['Total_Spent'].sum().sort_values(ascending=False)


def item_preference_by_location(df: pd.DataFrame) -> pd.DataFrame:
    """Функция определяет какой товар покупают чаще с собой(Takeaway), а какой в зале (Dine-in)."""
    logger.info("Предпочтения по товарам в зависимости от типа заказа")

    cross = pd.crosstab(df['Item'], df['Location'], values=df['Quantity'], aggfunc='sum')
    cross = cross.fillna(0)

    cross['Preference'] = cross.apply(
        lambda row: 'Takeaway' if row['Takeaway'] > row['In_Store'] else ('In_Store' if row['In_Store'] > row['Takeaway'] else 'Equal'),
        axis=1
    )

    top_takeaway = cross.nlargest(5, 'Takeaway')[['Takeaway', 'Preference']]
    top_in_store = cross.nlargest(5, 'In_Store')[['In_Store', 'Preference']]

    return {'cross_table': cross, 'top_takeaway': top_takeaway, 'top_in_store': top_in_store}


def run_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Запускает все аналитические функции и возвращает результаты"""
    logger.info("=" * 60)
    logger.info("ЗАПУСК АНАЛИТИКИ ДАННЫХ")
    logger.info("=" * 60)

    results = {
        "top_items_by_revenue": top_items_by_revenue(df),
        "top_items_by_quantity": top_items_by_quantity(df),
        "popular_method_by_count": popular_method_by_count(df),
        "popular_method_by_revenue": popular_method_by_revenue(df),
        "revenue_by_location": revenue_by_location(df),
        "revenue_by_month": revenue_by_month(df),
        "avg_check_by_month": avg_check_by_month(df),
        "best_day_by_revenue": best_day_by_revenue(df),
        "item_preference_by_location": item_preference_by_location(df),
    }

    logger.info("Аналитика завершена")
    return results


def print_analysis_results(results: dict) -> None:
    """Выводит результаты анализа в читаемом формате"""
    print("\n" + "=" * 60)
    print("РЕЗУЛЬТАТЫ АНАЛИЗА")
    print("=" * 60)

    print("\n1. Топ-5 товаров по выручке:")
    print(results["top_items_by_revenue"].to_string(index=False))

    print("\n2. Топ-5 товаров по количеству продаж:")
    print(results["top_items_by_quantity"].to_string(index=False))

    print("\n3. Способы оплаты (по количеству транзакций):")
    print(results["popular_method_by_count"])

    print("\n4. Способы оплаты (по сумме выручки):")
    print(results["popular_method_by_revenue"])

    print("\n5. Сравнение выручки Takeaway vs Dine-in:")
    print(results["revenue_by_location"])

    print("\n6. Выручка по месяцам (от большего к меньшему):")
    print(results["revenue_by_month"].to_string(index=False))

    print("\n7. Средний чек по месяцам:")
    print(results["avg_check_by_month"].to_string(index=False))

    print("\n8. День недели с максимальной выручкой:")
    print(results["best_day_by_revenue"])

    print("\n9. Предпочтения по товарам:")
    print("Топ-5 товаров, которые чаще берут с собой (Takeaway):")
    print(results["item_preference_by_location"]["top_takeaway"].to_string())
    print("\nТоп-5 товаров, которые чаще берут в зале (In_Store):")
    print(results["item_preference_by_location"]["top_in_store"].to_string())

    print("\n" + "=" * 60)
