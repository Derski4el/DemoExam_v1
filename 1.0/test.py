from fastapi import FastAPI, Body,Form
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime,date
from pydantic import BaseModel
from typing import List, Optional, Dict

from datetime import datetime, date
from typing import Optional
from fastapi.responses import FileResponse

app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:2342",
    "http://127.0.0.1:5500"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class OrderCreate(BaseModel):
    id: int
    day: int
    month: int
    year: int
    oborodovanie: Optional[str]
    problema: str
    opicanieproblem: str
    client: str
    status: str
    worker: str = "Не назначен"
    com: str
    
class Orders:
    def __init__(self, id: int, day: int, month: int, year: int, oborodovanie: Optional[str], problema: str, opicanieproblem: str, client: str, status: str, com: str, worker: str) -> None:
        self.id: int = id
        self.startDate: Optional[datetime] = datetime(year, month, day)
        self.endDate: Optional[datetime] = None
        self.oborodovanie: Optional[str] = oborodovanie
        self.problema: str = problema
        self.opicanieproblem: str = opicanieproblem
        self.client: str = client
        self.status: str = status
        self.worker: str = worker
        self.com: str = com
        
        if self.status == "Завершено":
            self.endDate = datetime.now()
today = date.today()
repo = [
    Orders(1, today.day, today.month, today.year, "Рука", "Что-то",          "Болит", "9","Завершено","Помогите пж","Вася"),
    Orders(2, 14, 1, 2024, "Нога", "Где-то",           "Работает", "10","Ожидания","Помогите пж","Вася"),
    Orders(3, 15, 3, 2024, "Голова", "Когда-то",       "Греется", "11","Ожидания","Помогите пж","Вася"),
    Orders(4, today.day, today.month, today.year, "Другая нога", "Почему-то", "Красная", "12","Завершено","Помогите пж","Вася"),
    Orders(5, 13, 5, 2024, "Рука", "Что-то",           "Синия", "9","Ожидания","Помогите пж","Вася"),
    Orders(6, 14, 6, 2024, "Нога", "Где-то",           "Прикорльная", "10","Ожидания","Помогите пж","Вася"),
    Orders(7, 10, 7, 2024, "Голова", "Когда-то",       "Живая", "11","Ожидания","Помогите пж","Вася"),
    Orders(8, 6, 10, 2024, "Другая нога", "Почему-то", "Ходит", "12","Ожидания","Помогите пж","Вася")
]

@app.get("/")
def get_orders():
    return repo

@app.get("/{order_id}")
def get_order(order_id: int):
    for o in repo:
        if o.id == order_id:
            return o
    return {"error": "Заявка не найдена"}, 404


@app.post("/")
def post_orders(data=Body()):
    id = data.get("id")
    oborodovanie = data.get("oborodovanie")
    problema = data.get("problema")
    opicanieproblem = data.get("opicanieproblem")
    client = data.get("client")
    status = data.get("status")
    worker = data.get("worker")
    com = data.get("com")

    if not all([id, oborodovanie, problema, opicanieproblem, client, status, worker, com]):
        return {"error": "Недостаточно данных для создания заказа"}, 400

    try:
        day = int(data.get("day", 1))
        month = int(data.get("month", 1))
        year = int(data.get("year", datetime.now().year))
        start_date = datetime(year, month, day)
    except ValueError:
        return {"error": "Некорректный формат даты"}, 400

    end_date = None
    if status == "Завершено":
        end_date = datetime.now()


    bufer = Orders(
        id,
        day,
        month,
        year,
        oborodovanie,
        problema,
        opicanieproblem,
        client,
        status,
        com
    )

    bufer.endDate = end_date
    repo.append(bufer)

    return {"message": "Заказ добавлен"}, 201

@app.put("/{id}")
def update_order(id: int, data=Body()):
    for o in repo:
        if o.id == id:
            o.oborodovanie = data.get("oborodovanie", o.oborodovanie)
            o.problema = data.get("problema", o.problema)
            o.opicanieproblem = data.get("opicanieproblem", o.opicanieproblem)
            o.client = data.get("client", o.client)
            o.status = data.get("status", o.status)
            o.worker = data.get("worker", o.worker)
            o.com = data.get("com", o.com)

            if o.status == "Завершено" and o.endDate is None:
                o.endDate = datetime.now()
            elif o.status != "Завершено":
                o.endDate = None

            return "Заявка обновлена", repo
    
    return "Заявка не найдена", repo


@app.get("/info_id/{num}")
def find_orders(num):
    for index, Order in enumerate(repo):
        if str(Order.id) == str(num):
            return repo[index], "Заявка обновленна"


@app.get("/info_all/{param}")
def find_orders_par(param):
    #a = {id,year,den,month,oborodovanie,problema,opicanieproblem,client,status}
    for index, Order in enumerate(repo):
        if ((str(Order.id) == str(param)) or
            (str(Order.oborodovanie) == str(param)) or
            (str(Order.problema) == str(param)) or
            (str(Order.opicanieproblem) == str(param)) or
            (str(Order.client) == str(param)) or
            (str(Order.status) == str(param)) or
            (str(Order.com) == str(param)) or
            (str(Order.worker) == str(param))):
            return repo[index], "Заявка обновленна"
    return "Не обноруженно"

@app.get("/stats/1")
def stats_1():
    result = []
    for o in repo:
        if o.status == "Завершено":
            result.append(o)
    return result

@app.get("/stats/2")
def stats_2():
    result = {}
    for o in repo:
        if o.problema in result:
            result[o.problema] += 1
        else:
            result[o.problema] = 1
    return result

@app.get("/stats/3")
def stats_3():
    completed_orders = [o for o in repo if o.status == "Завершено" and o.endDate is not None]
    if not completed_orders:
        return {"error": "Нет завершённых заявок"}

    times = []
    for o in completed_orders:
        delta = o.endDate - o.startDate
        times.append(delta.days)
    time = sum(times) / len(times)
    return {"Среднее время выполнения (дни)": time}



