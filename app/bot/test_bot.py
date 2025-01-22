from unittest.mock import AsyncMock

import pytest
from aiogram import Bot, Dispatcher
from aiogram.types import Update, Chat, Message, User

from app.bot.handlers import router, get_main_keyboard


@pytest.fixture
def bot():
    """Создаем мокнутый бот."""
    return Bot(token="test:token", validate_token=False)


@pytest.fixture
def dispatcher():
    """Создаем диспетчер и регистрируем маршрутизатор."""
    dp = Dispatcher()
    dp.include_router(router)
    return dp


def create_mock_message(text: str, chat_id: int = 12345, user_id: int = 67890) -> Message:
    """Создаем мокнутый объект Message."""
    return Message(
        message_id=1,
        date="2025-01-22T00:00:00Z",
        chat=Chat(id=chat_id, type="private"),
        text=text,
        from_user=User(id=user_id, is_bot=False, first_name="Test User"),
    )


def create_mock_update(message: Message) -> Update:
    """Создаем мокнутый объект Update."""
    return Update(update_id=1, message=message)


@pytest.mark.asyncio
async def test_start_command(bot, dispatcher):
    """Тест команды /start."""
    mock_message = create_mock_message("/start")
    mock_update = create_mock_update(mock_message)

    bot.send_message = AsyncMock()

    await dispatcher.feed_update(bot=bot, update=mock_update)

    bot.send_message.assert_awaited_once_with(
        chat_id=mock_message.chat.id,
        text="Добро пожаловать! Нажмите «Получить данные по товару», чтобы узнать информацию.",
        reply_markup=get_main_keyboard(),
    )


@pytest.mark.asyncio
async def test_request_artikul(bot, dispatcher):
    """Тест нажатия кнопки 'Получить данные по товару'."""
    mock_message = create_mock_message("Получить данные по товару")
    mock_update = create_mock_update(mock_message)

    bot.send_message = AsyncMock()

    await dispatcher.feed_update(bot=bot, update=mock_update)

    bot.send_message.assert_awaited_once_with(
        chat_id=mock_message.chat.id,
        text="Введите артикул товара:",
    )


@pytest.mark.asyncio
async def test_get_product_data(bot, dispatcher):
    """Тест обработки ввода артикула."""
    mock_message = create_mock_message("123456")
    mock_update = create_mock_update(mock_message)

    bot.send_message = AsyncMock()

    await dispatcher.feed_update(bot=bot, update=mock_update)

    bot.send_message.assert_awaited_once_with(
        chat_id=mock_message.chat.id,
        text="Товар с таким артикулом не найден.",
    )
