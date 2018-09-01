import asyncio
from aiohttp import ClientSession
from random import randrange


# BASE_URL = 'http://localhost:2107/'
BASE_URL = 'http://192.168.122.89/'
CONCUR_REQ = 2

async def get_order_data(order_id, semaphore):
    url = BASE_URL + str(order_id)
    # await asyncio.sleep(randrange(1, 3))
    async with semaphore:
        async with ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                print(data)
                return data


def download_many(orders_list):
    semaphore = asyncio.Semaphore(CONCUR_REQ)
    loop = asyncio.get_event_loop()
    coros = [get_order_data(order, semaphore) for order in orders_list]
    wait_coro = asyncio.wait(coros)
    results, _ = loop.run_until_complete(wait_coro)
    print('----------------------')
    for fut in results:
        print(fut.result())
    loop.close()


if __name__ == '__main__':
    download_many(range(100))
