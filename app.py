import folium
from flask import Flask, render_template

from database import SessionLocal
from models import Station, Connection, Junction

app = Flask(__name__)

@app.route("/")
def index():
    """Главная страница, которая отображает карту."""
    print("Запрос на главную страницу, генерируем карту...")
    db = SessionLocal()

    try:
        stations = db.query(Station).all()
        connections = db.query(Connection).all()
        junctions_ids = {j.station_id for j in db.query(Junction).all()}

        if not stations:
            return "База данных пуста. Сначала выполните команду 'python main.py import'"

        map_center = [stations[0].latitude, stations[0].longitude]
        m = folium.Map(location=map_center, zoom_start=10)

        stations_map = {station.station_id: station for station in stations}

        for station in stations:
            is_junction = station.station_id in junctions_ids
            folium.Marker(
                location=[station.latitude, station.longitude],
                popup=f"<b>{station.name}</b><br>Тип: {'Узловая' if is_junction else 'Станция'}",
                icon=folium.Icon(color="red" if is_junction else "blue", icon="info-sign")
            ).add_to(m)

        for conn in connections:
            start = stations_map.get(conn.station_from)
            end = stations_map.get(conn.station_to)
            if start and end:
                points = [(start.latitude, start.longitude), (end.latitude, end.longitude)]
                folium.PolyLine(locations=points, color="gray", weight=2).add_to(m)

        map_html = m._repr_html_()

    finally:
        db.close()

    return render_template("index.html", map_html=map_html)
