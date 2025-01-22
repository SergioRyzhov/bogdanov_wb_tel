from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from sqlalchemy.future import select

from app.db.database import get_db
from app.db.models import Product

router = Router()

def get_main_keyboard():
    keyboard = [
        [KeyboardButton(text="Получить данные по товару")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

@router.message(Command(commands=["start"]))
async def start_command(message: types.Message):
    await message.answer(
        "Добро пожаловать! Нажмите «Получить данные по товару», чтобы узнать информацию.",
        reply_markup=get_main_keyboard()
    )

@router.message(lambda message: message.text == "Получить данные по товару")
async def request_artikul(message: types.Message):
    await message.answer("Введите артикул товара (только цифры):")

@router.message(lambda message: message.text.isdigit())
async def get_product_data(message: types.Message):
    artikul = message.text.strip()
    try:
        async for db in get_db():
            query = select(Product).where(Product.artikul == artikul)
            result = await db.execute(query)
            product = result.scalars().first()

        if product:
            await message.answer(
                f"Товар: {product.name}\n"
                f"Цена: {product.price}₽\n"
                f"Рейтинг: {product.rating}\n"
                f"Остаток на складе: {product.stock}"
            )
        else:
            await message.answer("Товар с таким артикулом не найден.")
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")
