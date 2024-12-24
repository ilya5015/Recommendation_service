import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from redis import Redis

class AprioriModel:
    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client

    def get_data_from_redis(self) -> pd.DataFrame:
        """Получение данных из Redis."""
        keys = self.redis_client.keys('item:*')
        data = []
        for key in keys:
            data.append(self.redis_client.hgetall(key))
        return pd.DataFrame(data)

    def generate_rules(self, min_support: float = 0.01, min_confidence: float = 0.5) -> pd.DataFrame:
        """Генерация правил ассоциации."""
        df = self.get_data_from_redis()
        # Предполагаем, что у нас есть столбец 'items' с покупками
        df['items'] = df['items'].apply(lambda x: x.split(','))  # Преобразование строки в список
        basket = df.explode('items').groupby(['user_id', 'items'])['items'].count().unstack().fillna(0)
        basket = basket.applymap(lambda x: 1 if x > 0 else 0)  # Преобразование в бинарный формат

        frequent_itemsets = apriori(basket, min_support=min_support, use_colnames=True)
        rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)
        return rules