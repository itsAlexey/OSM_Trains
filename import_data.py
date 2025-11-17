import os
from pathlib import Path
import overpy

import data_loader
import data_processor

from database import Base, engine, SessionLocal
from models import Station, Connection, Junction, Train


def run_import(bbox: tuple):
    """
    Выполняет полный цикл: загрузка данных из OSM, обработка
    и сохранение в базу данных.
    """
    print("=" * 60)
    print("НАЧАЛО ПРОЦЕССА ИМПОРТА ДАННЫХ")
    print("=" * 60)

    # --- Шаг 1: Подготовка базы данных ---
    db_path = Path("instance/railway.db")
    if db_path.exists():
        os.remove(db_path)
        print("Старая база данных удалена.")
    db_path.parent.mkdir(exist_ok=True)

    Base.metadata.create_all(bind=engine)
    print("Таблицы в базе данных созданы.")

    db = SessionLocal()
    api = overpy.Overpass()

    try:
        # --- Шаг 2: Загрузка и обработка данных ---
        stations_data = data_loader.load_stations(api, bbox)
        if not stations_data:
            print("Станции не найдены. Импорт прерван.")
            return

        connections_data = data_loader.load_connections(api, bbox, stations_data)
        junctions_data = data_processor.generate_junctions(connections_data)
        trains_data = data_processor.generate_sample_trains(stations_data)
        print("\nДанные из OpenStreetMap успешно загружены и обработаны.")

        # --- Шаг 3: Сохранение данных в базу ---
        print("\nСохранение данных в базу...")

        # `**s` распаковывает словарь, чтобы передать его поля как аргументы
        # в конструктор класса модели. Например: Station(station_id='...', name='...' ...)
        db.add_all([Station(**s) for s in stations_data])
        db.add_all([Connection(**c) for c in connections_data])
        db.add_all([Junction(**j) for j in junctions_data])
        db.add_all([Train(**t) for t in trains_data])

        # Фиксируем все изменения в базе
        db.commit()
        print("\nВсе данные успешно сохранены в базу данных!")

    except Exception as e:
        print(f"\n✗ Произошла ошибка во время импорта: {e}")
        db.rollback()
    finally:
        db.close()
