import csv
import hashlib
import math
from pathlib import Path
from typing import Dict, List


def setup_data_directory():
    """Создает папку 'data', если она еще не существует."""
    Path("data").mkdir(exist_ok=True)


def generate_id(text: str) -> str:
    """
    Создает короткий уникальный ID из строки (например, из ID объекта OSM).
    Это нужно, чтобы иметь идентификаторы в нашей системе.
    """
    return hashlib.md5(text.encode()).hexdigest()[:12]


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Вычисляет расстояние между двумя GPS-координатами в километрах.
    Используется формула гаверсинуса.
    """
    R = 6371.0  # Радиус Земли в км
    lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
    lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return round(R * c, 2)


def write_csv(filename: str, data: List[Dict]):
    """
    Записывает список словарей в CSV-файл.
    Заголовки берутся из ключей первого словаря в списке.
    """
    if not data:
        print(f"Предупреждение: Нет данных для записи в файл {filename}.")
        return

    # Открываем файл для записи. `newline=''` убирает пустые строки в Windows.
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        # Используем ключи первого элемента как заголовки колонок
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()  # Записываем строку с заголовками
        writer.writerows(data) # Записываем все остальные строки

    print(f"✓ Данные сохранены в {filename}")