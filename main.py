from typing import Union
from fastapi import FastAPI
from db import mock_db
import uvicorn
import json


app = FastAPI()


@app.get("/items/{item}", tags = ["Работа с JSON"], summary = "Получить сообщение из базы данных")
def read_item(item: str, q: Union[str, None] = None):
    result = mock_db.get(item, "Ключ не найден")
    return result


@app.get("/health", tags = ["Проверки"], summary = "Базовая проверка здоровья")
async def health_check():
    health_status = "Healthy!"
    return health_status


@app.post("/records", tags = ["Работа с JSON"], summary = "Записать сообщение из JSON в базу данных")
def create_record():
    with open("test_data.json", "r", encoding="UTF=8") as rec_file:
        data = json.load(rec_file)
        mock_db.update(data)
        rec_file.close()

    return {"success": "База данных обновлена"}



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)