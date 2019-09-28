import asyncpg
from aiohttp import web


routes = web.RouteTableDef()


@routes.get('/')
# @routes.get('/{address}')
async def handle(request):
    address = request.rel_url.query['address']
    conn = await asyncpg.connect('postgresql://postgres:postgres@localhost:5432/fias')
    # address = "митинская 25"
    query = """
    with t as (
        select aoguid, full_name as clear_address, '{address}' as original_address, full_name <-> '{address}' as dist from fias_plain_address
        )
    select * 
    from t
    where dist <= 0.5
    order by dist limit 1; 
    """.format(address=address)

    row = await conn.fetchrow(query)
    await conn.close()
    if row:
        res = tuple(row)
        data = {
            "status": "ok",
            "aoguid": res[0],
            "clear_address": res[1],
            "original_address": res[2],
            "dist": res[3]
        }
    else:
        data = {'status': 'no data', 'original_address': address}
    return web.json_response(data)

app = web.Application()
app.add_routes(routes)

web.run_app(app)
