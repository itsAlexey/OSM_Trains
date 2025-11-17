from sqlalchemy import Column, String, Float, Integer, Boolean, JSON
from database import Base

class Station(Base):
    __tablename__ = "stations"
    station_id = Column(String, primary_key=True, index=True)
    osm_id = Column(Integer, unique=True)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    city = Column(String, nullable=True)
    type = Column(String)

class Connection(Base):
    __tablename__ = "connections"
    connection_id = Column(String, primary_key=True, index=True)
    station_from = Column(String)
    station_to = Column(String)
    distance_km = Column(Float)
    electrified = Column(Boolean)

class Junction(Base):
    __tablename__ = "junctions"
    junction_id = Column(String, primary_key=True, index=True)
    station_id = Column(String)
    connected_stations = Column(JSON)
    connections_count = Column(Integer)

class Train(Base):
    __tablename__ = "trains"
    train_id = Column(String, primary_key=True, index=True)
    train_number = Column(String)
    name = Column(String)
    type = Column(String)
    route = Column(JSON)
