import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.v1.products import router as products_router
from app.bot.bot import main as bot_main
from app.core.auth import create_access_token
from app.db.database import engine, init_db
from app.tasks.scheduler import scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await init_db()

    scheduler.start()

    bot_task = asyncio.create_task(bot_main())

    yield

    scheduler.shutdown()
    bot_task.cancel()
    try:
        await bot_task
    except asyncio.CancelledError:
        pass


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
