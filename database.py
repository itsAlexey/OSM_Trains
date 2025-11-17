from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Указываем, что наша база данных будет файлом 'railway.db' в папке 'instance'
SQLALCHEMY_DATABASE_URL = "sqlite:///instance/railway.db"

# Создаем "движок" для подключения к базе данных
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Создаем "фабрику" для сессий (подключений к БД)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаем базовый класс, от которого будут наследоваться все наши модели таблиц
Base = declarative_base()
