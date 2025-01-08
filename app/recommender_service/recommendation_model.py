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
        self.data = self.spark.createDataFrame(data)

        als = ALS(maxIter=10, regParam=0.01, userCol="user_id", itemCol="product_id", ratingCol="quantity", coldStartStrategy="drop")
        self.model = als.fit(self.data)

    def recommend(self, user_id, num_recommendations=3):
        # Генерируем рекомендации для заданного пользователя
        user_df = self.spark.createDataFrame([(user_id,)], ["user_id"])
        recommendations = self.model.recommendForUserSubset(user_df, num_recommendations).collect()
        return recommendations

    def recommend_all(self, num_recommendations=3):
        recommendations = self.model.recommendForAllUsers(num_recommendations).collect()
        return recommendations
