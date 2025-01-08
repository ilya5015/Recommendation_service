from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import Normalizer
from pyspark.ml.clustering import KMeans
from pyspark.ml.recommendation import ALS
from pyspark.sql.types import IntegerType, DoubleType
from pyspark.ml.feature import StringIndexer
from pandas import DataFrame

class RecommendationModel:
    def __init__(self, spark):
        self.spark = spark
        self.model = None
        self.data = None

    def fit(self, data: DataFrame):
        # Преобразуем Pandas DataFrame в Spark DataFrame
        self.data = self.spark.createDataFrame(data)

        # Получаем названия колонок продуктов
        product_columns = self.data.columns[1:]  # Пропускаем user_id

        # Создаем выражение для stack
        stack_expr = "stack({}, {}) as (product, rating)".format(
            len(product_columns),
            ', '.join([f"'{col}', {col}" for col in product_columns])
        )

        # Преобразуем данные в нужный формат
        ratings = self.data.select("user_id", *product_columns)
        ratings = ratings.selectExpr("user_id", stack_expr)
        ratings = ratings.withColumn("product", col("product").cast("int"))

        # Обучаем модель ALS
        als = ALS(maxIter=10, regParam=0.01, userCol="user_id", itemCol="product", ratingCol="rating", coldStartStrategy="drop")
        self.model = als.fit(ratings)

    def recommend(self, user_id, num_recommendations=3):
        # Генерируем рекомендации для заданного пользователя
        user_df = self.spark.createDataFrame([(user_id,)], ["user_id"])
        recommendations = self.model.recommendForUserSubset(user_df, num_recommendations).collect()
        return recommendations


