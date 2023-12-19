from fastapi import FastAPI, Depends
from fastapi_asyncpg import configure_asyncpg
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os


app = FastAPI()
database_url = os.getenv('DB_URI', "postgresql://admin:123456@localhost/m.tex")
db = configure_asyncpg(app, database_url)


class Logs(BaseModel):
    log: str


# Инициализация базы данных
@db.on_init
async def initialization(conn):

    await conn.execute("""CREATE TABLE IF NOT EXISTS public.logs
(
    id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
    created TIMESTAMP WITH TIME ZONE  default current_timestamp,
    ip character varying(15) NOT NULL,
    method character varying(6) NOT NULL,
    uri character varying(10) NOT NULL,
    status_code integer NOT NULL
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.logs
    OWNER to admin;""")


# Получение списка логов
@app.get("/api/data")
async def get_logs(db=Depends(db.connection)):
    query = "SELECT * FROM logs"
    try:
        rows = await db.fetch(query)
        logs = []
        for row in rows:
            logs.append({"id": row["id"], "created": str((row["created"])),
                         "log": {"ip": row['ip'], "method": row['method'],
                         "uri": row['uri'], 'status_code': row['status_code']}})
        return logs
    except Exception as e:
        return {"message": f"Failed to get logs: {e}"}


# Сохранение лога в базу данных
@app.post("/api/data", status_code=201)
async def save_log(log: Logs, db=Depends(db.atomic)):
    print(log)
    try:
        ip, method, uri, status_code = log.log.split()
        status_code = int(status_code)

    except Exception as e:
        print(e)
        return JSONResponse(content={"message": f"Failed to save log: {e}"}, status_code=418)
    query = "INSERT INTO logs (ip, method, uri, status_code) VALUES ($1, $2, $3, $4)"
    try:
        await db.execute(query, ip, method, uri, status_code)
        return {"message": "Log saved successfully"}
    except Exception as e:
        return JSONResponse(content={"message": f"Failed to save log: {e}"}, status_code=418)


