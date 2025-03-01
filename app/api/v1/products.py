from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.core.parser import fetch_product_data
from app.db.database import get_db
from app.db.models import Product
from app.tasks.scheduler import schedule_product_update

router = APIRouter()


@router.post("/products")
async def create_product(
    artikul: str,
    db: AsyncSession = Depends(get_db),
    user: str = Depends(get_current_user),
):
    product_data = await fetch_product_data(artikul)

    if not product_data:
        raise HTTPException(status_code=404, detail="Product not found")

    product = Product(**product_data)

    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product


@router.get("/subscribe/{artikul}")
async def subscribe_to_product(
    artikul: str, user: str = Depends(get_current_user)
):
    schedule_product_update(artikul)
    return {"message": f"Subscribed to updates for product {artikul}"}
