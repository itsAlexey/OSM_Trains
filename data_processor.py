import json
from typing import Dict, List


def generate_junctions(connections: List[Dict]) -> List[Dict]:
    """Находит узловые станции (развязки), где сходится 3 и более пути."""
    print("Анализ связей для поиска развязок...")

    # Сначала посчитаем, сколько путей подходит к каждой станции
    station_links = {}
    for conn in connections:
        # Учитываем оба конца пути
        station_links[conn['station_from']] = station_links.get(conn['station_from'], set())
        station_links[conn['station_from']].add(conn['station_to'])

        station_links[conn['station_to']] = station_links.get(conn['station_to'], set())
        station_links[conn['station_to']].add(conn['station_from'])

    junctions = []
    junction_id_counter = 1
    # Теперь найдем станции, у которых 3 и более соседей
    for station_id, neighbours in station_links.items():
        if len(neighbours) >= 3:
            junctions.append({
                'junction_id': f'JNC_{junction_id_counter:04d}',
                'station_id': station_id,
                'connected_stations': json.dumps(list(neighbours)),
                'connections_count': len(neighbours)
            })
            junction_id_counter += 1

    print(f"Найдено {len(junctions)} развязок.")
    return junctions


def generate_sample_trains(stations: List[Dict]) -> List[Dict]:
    """Создает тестовый набор данных о поездах."""
    print("Генерация примерных данных о поездах...")

    if len(stations) < 5:
        print("Недостаточно станций для создания примеров поездов.")
        return []

    train_templates = [
        {'number': '001А', 'name': 'Красная стрела', 'type': 'скорый'},
        {'number': '002М', 'name': 'Россия', 'type': 'пассажирский'},
        {'number': '751А', 'name': 'Сапсан', 'type': 'скоростной'},
    ]

    trains = []
    for i, template in enumerate(train_templates):
        # Для примера берем 3-5 станций из общего списка как маршрут
        route_station_ids = [s['station_id'] for s in stations[i : i + 5]]
        trains.append({
            'train_id': f'TRN_{i+1:04d}',
            'train_number': template['number'],
            'name': template['name'],
            'type': template['type'],
            'route': json.dumps(route_station_ids)
        })

    print(f"Создано {len(trains)} примерных поездов.")
    return trains
