import pandas as pd
import psycopg2
from redis import Redis

class ETLService:
    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client

    def extract(self, postgres_conn_str: str, query: str = 'SELECT * FROM table_name') -> pd.DataFrame:
        """Извлечение данных из CSV файла."""
        conn = psycopg2.connect(postgres_conn_str)
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        df = pd.DataFrame(data, columns=[desc[0] for desc in cursor.description])
        return df

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Трансформация данных для подготовки к загрузке."""
        # Здесь вы можете добавить свою логику трансформации данных
        return df

    def load(self, df: pd.DataFrame):
        """Загрузка данных в Redis."""
        for index, row in df.iterrows():
            # Сохраняем данные в виде хэша
            self.redis_client.hset(f"item:{index}", mapping=row.to_dict())

    def run_etl(self, file_path: str):
        """Запуск полного ETL процесса."""
        df = self.extract(file_path)
        transformed_data = self.transform(df)
        self.load(transformed_data)