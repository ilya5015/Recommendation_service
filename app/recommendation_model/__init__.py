

basket_data = [(1, 101), (1, 102), (2, 101), (2, 103), (3, 102), (3, 103)]
basket_df = spark.createDataFrame(basket_data, ['userId', 'itemId'])

recommender = BasketRecommender(spark, n_neighbors=2)
transformed_df = recommender.preprocess_data(basket_df)

# Печатаем рекомендации для пользователя с userId = 1
recommendations = recommender.recommend(user_id=1)
print(f"Recommendations for user 1: {recommendations}")