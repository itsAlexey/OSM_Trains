import time
from typing import Dict, List, Tuple

import overpy
from utils import generate_id, calculate_distance


def load_stations(api: overpy.Overpass, bbox: Tuple) -> List[Dict]:
    """Загружает станции и остановочные пункты из OSM."""
    print(f"Загрузка станций для области {bbox}...")

    query = f"""
    [out:json][timeout:60];
    (
        node["railway"="station"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
        node["railway"="halt"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
    );
    out body;
    """

    try:
        result = api.query(query)
        stations = []
        for node in result.nodes:
            stations.append({
                'station_id': generate_id(str(node.id)),
                'name': node.tags.get('name', f'Станция_{node.id}'),
                'latitude': float(node.lat),
                'longitude': float(node.lon),
                'type': node.tags.get('railway', 'station'),
                'city': node.tags.get('addr:city', ''),
                'osm_id': node.id
            })
        print(f"Загружено {len(stations)} станций.")
        return stations
    except Exception as e:
        print(f"Ошибка при загрузке станций: {e}")
        time.sleep(2)
        return []


def load_connections(api: overpy.Overpass, bbox: Tuple, stations: List[Dict]) -> List[Dict]:
    """Загружает ж/д пути и создает на их основе связи между станциями."""
    print("Загрузка железнодорожных путей для создания связей...")
    query = f"""
    [out:json][timeout:90];
    way["railway"="rail"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
    out body; >; out skel qt;
    """
    try:
        result = api.query(query)
        connections = []

        # Создаем "карту" координат для быстрого поиска станций
        station_coords_map = {f"{s['latitude']:.5f},{s['longitude']:.5f}": s for s in stations}

        for way in result.ways:
            # Находим все станции, которые лежат на данном пути
            stations_on_way = []
            for node in way.nodes:
                if hasattr(node, 'lat') and hasattr(node, 'lon'):
                    coord_key = f"{float(node.lat):.5f},{float(node.lon):.5f}"
                    if coord_key in station_coords_map:
                        stations_on_way.append(station_coords_map[coord_key])

            # Создаем связи между соседними станциями на пути
            for i in range(len(stations_on_way) - 1):
                station_from = stations_on_way[i]
                station_to = stations_on_way[i + 1]
                
                distance = calculate_distance(
                    station_from['latitude'], station_from['longitude'],
                    station_to['latitude'], station_to['longitude']
                )

                connections.append({
                    'connection_id': generate_id(f"{station_from['station_id']}_{station_to['station_id']}"),
                    'station_from': station_from['station_id'],
                    'station_to': station_to['station_id'],
                    'distance_km': distance,
                    'electrified': way.tags.get('electrified', 'no') == 'yes'
                })

        print(f"Создано {len(connections)} связей между станциями.")
        return connections
    except Exception as e:
        print(f"Ошибка при загрузке путей: {e}")
        time.sleep(2)
        return []

