from typing import Dict, List
import networkx as nx


def build_graph(stations: List[Dict], connections: List[Dict]) -> nx.Graph:
    """Строит граф сети: станции - узлы, связи - ребра."""
    print("Построение графа сети...")
    graph = nx.Graph()

    # Добавляем узлы (станции) с их атрибутами
    for station in stations:
        graph.add_node(
            station['station_id'],
            name=station['name'],
            lat=station['latitude'],
            lon=station['longitude']
        )

    # Добавляем ребра (связи) с весом (расстояние)
    for conn in connections:
        graph.add_edge(
            conn['station_from'],
            conn['station_to'],
            weight=conn['distance_km']
        )

    print(f"Граф построен: {graph.number_of_nodes()} узлов, {graph.number_of_edges()} рёбер.")
    return graph


def analyze_network(graph: nx.Graph) -> Dict:
    """Рассчитывает базовые метрики графа."""
    if graph.number_of_nodes() == 0:
        return {}

    # Считаем центральность (важность) узлов по количеству связей
    centrality = nx.degree_centrality(graph)
    top_hubs_ids = sorted(centrality, key=centrality.get, reverse=True)[:5]

    top_hubs = []
    for station_id in top_hubs_ids:
        top_hubs.append({
            'name': graph.nodes[station_id].get('name', station_id),
            'score': centrality[station_id]
        })

    return {
        'nodes': graph.number_of_nodes(),
        'edges': graph.number_of_edges(),
        'components': nx.number_connected_components(graph),
        'avg_degree': sum(dict(graph.degree()).values()) / graph.number_of_nodes(),
        'top_hubs': top_hubs
    }
