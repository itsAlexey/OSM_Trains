import overpy

import data_loader
import data_processor
import network_analyzer
import utils


def run_pipeline():
    """Основная функция, которая запускает весь процесс."""
    print("=" * 60)
    print("ЗАГРУЗЧИК ЖЕЛЕЗНОДОРОЖНОЙ СЕТИ")
    print("=" * 60)

    # Настройка
    api = overpy.Overpass()
    # Область для загрузки (пример - район Москвы)
    # Формат: (min_lat, min_lon, max_lat, max_lon)
    bbox = (55.5, 37.3, 55.9, 37.9)
    print(f"\nОбласть загрузки: {bbox}")

    try:
        # 1. Подготовка
        utils.setup_data_directory()

        # 2. Загрузка данных из OSM
        stations = data_loader.load_stations(api, bbox)
        if not stations:
            print("\n⚠ Станции не найдены. Программа завершает работу.")
            print("  Попробуйте изменить координаты bbox или проверить интернет.")
            return

        connections = data_loader.load_connections(api, bbox, stations)

        # 3. Обработка и генерация данных
        junctions = data_processor.generate_junctions(connections)
        trains = data_processor.generate_sample_trains(stations)

        # 4. Сохранение результатов в CSV
        print("\nСохранение данных в CSV-файлы...")
        utils.write_csv('data/stations.csv', stations)
        utils.write_csv('data/connections.csv', connections)
        utils.write_csv('data/junctions.csv', junctions)
        utils.write_csv('data/trains.csv', trains)

        # 5. Построение и анализ графа
        graph = network_analyzer.build_graph(stations, connections)
        stats = network_analyzer.analyze_network(graph)

        # 6. Вывод итоговой статистики
        print("\n" + "=" * 60)
        print("СТАТИСТИКА СЕТИ:")
        if stats:
            print(f"  Узлов (станций): {stats.get('nodes', 0)}")
            print(f"  Связей (путей): {stats.get('edges', 0)}")
            print(f"  Компонент связности: {stats.get('components', 0)}")
            print(f"  Среднее число связей на узел: {stats.get('avg_degree', 0):.2f}")
            if 'top_hubs' in stats and stats['top_hubs']:
                print("\n  Важнейшие узлы (хабы):")
                for hub in stats['top_hubs']:
                    print(f"    - {hub['name']} (оценка: {hub['score']:.3f})")
        print("=" * 60)
        print("\n✓ Программа успешно завершила работу!")

    except Exception as e:
        print(f"\n✗ Произошла непредвиденная ошибка: {e}")


if __name__ == "__main__":
    run_pipeline()
