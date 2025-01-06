import pandas as pd
from sqlalchemy import create_engine

class ETL:
    def __init__(self, db_url):
        self.db_url = db_url
        self.engine = create_engine(db_url)

    def extract(self):
        # Извлечение данных из таблицы order_items
        query_items = 'SELECT order_id, product_id, quantity FROM order_items'
        order_items_df = pd.read_sql(query_items, self.engine)

        # Извлечение данных из таблицы orders для получения user_id
        query_orders = "SELECT order_id, user_id FROM orders"
        orders_df = pd.read_sql(query_orders, self.engine)

        return order_items_df, orders_df

    def transform(self, order_items_df, orders_df):
        # Объединение данных по order_id
        merged_df = pd.merge(order_items_df, orders_df, on='order_id', how='left')

        # Выбор необходимых столбцов
        transformed_df = merged_df[['order_id', 'product_id', 'user_id', 'quantity']]
        return transformed_df

    def load(self, transformed_df):
        # Загрузка данных в целевую таблицу (можно настроить под ваши нужды)
        print('pipeline load stage')
        print(transformed_df)

    def run_pipeline(self):
        order_items_df, orders_df = self.extract()
        transformed_df = self.transform(order_items_df, orders_df)
        self.load(transformed_df)