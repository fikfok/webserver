from datetime import datetime
from aiohttp import web
from random import randrange


routes = web.RouteTableDef()


@routes.get('/')
@routes.get('/{order_id}')
async def handle(request):
    order_id = request.match_info.get('order_id')
    data = {'order_id': order_id,
            'units_count': randrange(1, 6),
            'create_date': datetime(year=randrange(2017, 2019), month=randrange(1, 13), day=randrange(1, 29)).strftime("%Y-%m-%d"),
            'server': 1,
            }
    return web.json_response(data)

app = web.Application()
app.add_routes(routes)

web.run_app(app)
