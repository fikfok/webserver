import uuid
from aiohttp import web
import asyncio


routes = web.RouteTableDef()


@routes.get('/')
async def handle(request):
    data = [
        {
            "name": "Сырники",
            "ingredients": [
                {"name": "Творог", "amount": "500", "measurement": "г."},
                {"name": "Яйцо куриное", "amount": "2", "measurement": "шт."},
                {"name": "Пшеничная мука", "amount": "6", "measurement": "ст. л."},
                {"name": "Сахар", "amount": "2", "measurement": "ст. л."},
                {"name": "Подсолнечное масло", "amount": "5", "measurement": "ст. л."},
            ],
            "steps": [
                "Положить творог в ёмкость",
                "Высыпать в творог 5 столовых ложек (с горкой) муки и тщательно перемешайте",
                "Поставить сковороду на средний огонь и налейте в нее подсолнечное масло",
                "Слепить шарики, обкатать в муке, расплющить, выложить на сковороду",
                "Обжаривать с обеих сторон 1–2 минуты до появления золотистой корочки"
            ],
            "rating": 4,
        },
        {
            "name": "Блины",
            "ingredients": [
                {"name": "Пшеничная мука", "amount": "400", "measurement": "г"},
                {"name": "Сахар", "amount": "2", "measurement": "ст. л."},
                {"name": "Яйцо куриное", "amount": "4", "measurement": "шт."},
                {"name": "Молоко", "amount": "1", "measurement": "л."},
                {"name": "Соль", "amount": "1", "measurement": "г."},
                {"name": "Растительное масло", "amount": "2", "measurement": "ст. л."},
            ],
            "steps": [
                "Взбить яйца с сахаром",
                "Постепенно добавить муку и соль, чередуя с молоком и аккуратно размешать до однородной массы",
                "Оставьте на 20 минут",
                "Добавить в тесто растительное масло и жарьте на сильно разогретой сковороде",
            ],
            "rating": 3
        },
        {
            "name": "Шарлотка",
            "ingredients": [
                {"name": "Сахар", "amount": "1", "measurement": "стакан"},
                {"name": "Яйцо куриное", "amount": "4", "measurement": "шт."},
                {"name": "Пшеничная мука", "amount": "1", "measurement": "стакан"},
                {"name": "Яблоко", "amount": "1", "measurement": "кг."},
                {"name": "Соль", "amount": "1", "measurement": "г."},
                {"name": "Сода", "amount": "1/5", "measurement": "ч. л."}
            ],
            "steps": [
                "Белки взбить с половиной стакана сахара",
                "Желтки взбить с оставшимся сахаром",
                "Соединить все вместе и постепенно добавить муку",
                "Добавить соль и соду",
                "Добавить нарезанные кубиками яблоки",
                "Форму для выпекания смазать маслом и посыпать манной крупой",
                "Выложить массу в форму и поставить в духовку, разогретую до 180 градусов",
                "Выпекать 30-40 минут"
            ],
            "rating": 5
        }
    ]
    for item in data:
        item['id'] = str(uuid.uuid4())
    await asyncio.sleep(2)
    return web.json_response(data, headers={'Access-Control-Allow-Origin': '*'})

app = web.Application()
app.add_routes(routes)

web.run_app(app)
