from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, sum as spark_sum
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.linalg import Vectors
from pyspark.ml import Pipeline
from pyspark.ml.linalg import DenseVector
from pyspark.ml.stat import Correlation

class RecommendationModel:
    def __init__(self, orders_df: DataFrame):
        self.orders_df = orders_df
        self.user_product_matrix = None
        self.user_similarity = None

    def fit(self):
        # матрица пользователей и продуктов
        self.user_product_matrix = (self.orders_df
                                     .groupBy('user_id')
                                     .agg(*[spark_sum(col(product)).alias(product) for product in self.orders_df.columns if product != 'user_id']))

        # векторное представление
        vector_assembler = VectorAssembler(inputCols=self.user_product_matrix.columns[1:], outputCol='features')
        self.user_product_matrix = vector_assembler.transform(self.user_product_matrix)

        # косинусное сходство
        correlation_matrix = Correlation.corr(self.user_product_matrix, 'features').head()[0]
        self.user_similarity = correlation_matrix.toArray()

    def recommend(self, user_id, top_n=5):
        if user_id not in self.user_product_matrix.select('user_id').rdd.flatMap(lambda x: x).collect():
            raise ValueError("Пользователь не найден в данных.")

        user_index = self.user_product_matrix.filter(col('user_id') == user_id).collect()[0][0]

        # сходство пользователя с другими
        user_similarities = self.user_similarity[user_index]

        # индексы пользователей, отсортированные по убыванию сходства
        similar_users_indices = user_similarities.argsort()[::-1]

        product_scores = {}

        # цикл по схожим пользователям и суммирование их покупок
        for index in similar_users_indices:
            if index == user_index:
                continue  
            
            similar_user_vector = self.user_product_matrix.collect()[index]['features'].toArray()
            num_products = len(similar_user_vector)  

            for product_index in range(num_products):
                if similar_user_vector[product_index] > 0:  # Если продукт куплен
                    product = self.user_product_matrix.columns[product_index + 1]  # +1, чтобы пропустить user_id
                    if product not in product_scores:
                        product_scores[product] = 0
                    product_scores[product] += user_similarities[index]

        # уже купленные продукты текущего пользователя из рекомендаций не включаются
        user_orders = self.user_product_matrix.filter(col('user_id') == user_id).collect()[0]['features'].toArray()
        for product_index in range(num_products):
            product = self.user_product_matrix.columns[product_index + 1]  # +1, чтобы пропустить user_id
            if user_orders[product_index] > 0 and product in product_scores:
                del product_scores[product]

        # сортировка продуктов по оценкам и возврат топ N
        recommended_products = sorted(product_scores.items(), key=lambda x: x[1], reverse=True)
    
        return [product for product, score in recommended_products[:top_n]]

