from fastapi import APIRouter

router = APIRouter(
    tags=['Получение ассоциативных правил']
)

@router.get("/generate_rules/")
def generate_rules(min_support: float = 0.01, min_confidence: float = 0.5):
    """Генерация правил ассоциации."""
    rules = 'no rules yet'
    return rules
