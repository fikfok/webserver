import requests
import json
import pandas as pd
import asyncio
from aiohttp import ClientSession
import numpy as np


CONCUR_REQ = 3
# for address in addresses:
#     params = {'address': address}
#     resp = requests.get('http://localhost:8080', params=params)
#     if resp.status_code == 200:
#         data = json.loads(resp.text)
#         print(data)

cleared_addresses = []

async def recognise_address(address, semaphore):
    params = {'address': address}
    async with semaphore:
        async with ClientSession() as session:
            async with session.get('http://localhost:8080', params=params) as response:
                data = await response.json()
                # print(data)
                cleared_addresses.append(data)
                return data


# async def recognise_address_wo_sem(address):
#     params = {'address': address}
#     async with ClientSession() as session:
#         async with session.get('http://localhost:8080', params=params) as response:
#             data = await response.json()
#             return data


def do_recognise():
    df = pd.read_excel(io='/home/fikfok/Desktop/Москва.xlsx', sheet_name='Москва')
    addresses = list(df['Address'])
    df['clear'] = np.nan
    semaphore = asyncio.Semaphore(CONCUR_REQ)
    loop = asyncio.get_event_loop()
    coros = [recognise_address(address, semaphore) for address in addresses]
    gather_coro = asyncio.gather(*coros)
    results = loop.run_until_complete(gather_coro)
    print('----------------------')
    for res in results:
        df.loc[df['Address'] == res['original_address'], 'clear'] = res['clear_address']
    loop.close()


if __name__ == '__main__':
    do_recognise()
