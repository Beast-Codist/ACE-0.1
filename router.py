from fastapi import APIRouter, Depends
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, Union
import anyio
import json

# Импорты ваших ресурсов
from database import new_session
from models import PooCoords
from schemas import PooCoordsAddSchema, PooCoordsSchema
from db import mock_db  # Импортируем ваш временный словарь

router = APIRouter()

# --- Зависимость сессии (внутренняя для роутера) ---
async def get_session():
    async with new_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]

# --- Группа: Работа с базой данных ---

@router.post("/poocoords", tags=["Работа с Базой данных"])
async def add_poocoords(session: SessionDep):
    try:
        file_path = anyio.Path("user_toilet.json")
        if not await file_path.exists():
            return {"error": "Файл не найден"}
        content = await file_path.read_text(encoding="utf-8")
        data_json = json.loads(content)
        data = PooCoordsAddSchema(**data_json)
    except Exception as e:
        return {"error": str(e)}

    new_coords = PooCoords(**data.model_dump())
    session.add(new_coords)
    await session.commit()
    await session.refresh(new_coords)
    return {"success": "Запись создана", "id": new_coords.id}

@router.get("/poocoords", tags=["Работа с Базой данных"], response_model=PooCoordsSchema)
async def get_last_poocoord(session: SessionDep):
    query = select(PooCoords).order_by(desc(PooCoords.id)).limit(1)
    result = await session.execute(query)
    return result.scalar_one_or_none()

# --- Группа: Работа с JSON (Ваш временный блок) ---

@router.get("/items/{item}", tags=["Работа с JSON"], summary="Получить сообщение из базы данных")
def read_item(item: str, q: Union[str, None] = None):
    result = mock_db.get(item, "Ключ не найден")
    return result

@router.post("/records", tags=["Работа с JSON"], summary="Записать сообщение из JSON в базу данных")
def create_record():
    # Оставляем синхронным, так как это временный код для mock_db
    with open("test_data.json", "r", encoding="UTF-8") as rec_file:
        data = json.load(rec_file)
        mock_db.update(data)
    return {"success": "База данных обновлена"}

# --- Группа: Проверки ---

@router.get("/health", tags=["Проверки"], summary="Базовая проверка здоровья")
async def health_check():
    return "Healthy!"