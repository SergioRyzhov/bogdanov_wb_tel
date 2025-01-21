from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.db.database import engine, init_db
from app.tasks.scheduler import scheduler
from app.api.v1.products import router as products_router
from app.core.auth import create_access_token


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await init_db()
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)

app.include_router(products_router, prefix="/api/v1/products")


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Эндпоинт для генерации JWT токена.
    """
    if form_data.username != "user" or form_data.password != "password":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}
