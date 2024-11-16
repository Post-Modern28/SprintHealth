from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine


# Параметры подключения
username = 'your_username'
password = 'your_password'
host = 'localhost'  # Или IP-адрес сервера
port = '5432'       # Стандартный порт PostgreSQL
database = 'your_database'

# Создание подключения
engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}')
