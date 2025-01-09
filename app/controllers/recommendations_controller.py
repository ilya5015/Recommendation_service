from fastapi import HTTPException
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
import json

class RecommendationsController:
    def __init__(self, redis_service):
        self.redis_service = redis_service

    def get_recommendations(self, user_id: int):
        recommendations = self.redis_service.get(user_id)
        return {"user_id": user_id, "recommendations": recommendations}

    def set_recommendations(self, user_id: int, product_ids: list[int]):
        self.redis_service.set(user_id, json.dumps(product_ids))
        return {"message": "Recommendations set", "user_id": user_id, "recommendations": json.dumps(product_ids)}

    def delete_recommendations(self, user_id: int):
        self.redis_service.delete_data(user_id)
        return {"message": "Recommendations deleted", "user_id": user_id}