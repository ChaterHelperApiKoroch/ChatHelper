import asyncio
import aiohttp
from fake_useragent import UserAgent
from time import sleep
import os

async def send_click(url, headers, data, session):
    async with session.post(url, headers=headers, json=data) as response:
        return await response.text()

async def click(col, pov):
    url = "https://arbuz.betty.games/api/click/apply"
    headers = {"User-Agent": UserAgent().random, "X-Telegram-Init-Data": "query_id=AAEF9sYDAwAAAAX2xgPhGHwQ&user=%7B%22id%22%3A6505821701%2C%22first_name%22%3A%22f0x3r0k%22%2C%22last_name%22%3A%22%22%2C%22username%22%3A%22f0x9r0k%22%2C%22language_code%22%3A%22en%22%2C%22allows_write_to_pm%22%3Atrue%7D&auth_date=1710851623&hash=34ba4dbc4f61830bc892d7d3c082c8ed0c18ab56c8c01bc779b6ca26a845cde8"}
    data = {"count": 10, "hash": "ca1a97a3cdec77b7e1e0de9f420c296bd057f3a82a1e76a1a1dde2f84d73d23f"}

    async with aiohttp.ClientSession() as session:
        tasks = [send_click(url, headers, data, session) for _ in range(pov)]
        responses = await asyncio.gather(*tasks)

    for i, response_text in enumerate(responses):
        print(f"Request {i+1} || text: {response_text}")


while True:
	asyncio.run(click(10, 200))
	sleep(15)
	os.system("cls||clear")
	print("Lets GO")
	sleep(5)
