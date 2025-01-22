from pydantic import BaseModel, Field

class ProductCreate(BaseModel):
    artikul: str = Field(..., example="12345678")
    name: str
    price: float
    rating: float | None = None
    stock: int
