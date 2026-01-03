from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager

from database import engine, Base
from router import router  # Импортируем наш собранный роутер

@asynccontextmanager
async def lifespan(_: FastAPI):
    # Управление таблицами при старте
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Закрытие сессий при выключении
    await engine.dispose()
    print("Соединение с БД закрыто корректно")

app = FastAPI(lifespan=lifespan)

# Подключаем все эндпоинты одной строкой
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)