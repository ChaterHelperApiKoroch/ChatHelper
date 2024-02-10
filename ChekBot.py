from pyrogram import Client, filters, idle
import random
from re import compile, MULTILINE
from fake_useragent import UserAgent
import aiohttp

api_id = 25686282
api_hash = "850a02941e959e3f5fdceca055f7a459"
app = Client("ChatHelper", api_id=api_id, api_hash=api_hash, device_model="ChatHelper")
regex = compile(r"t\.me\/wmclick_bot\/click\?startapp=r_(\w*)")

#token = "query_id=AAG8y3hYAAAAALzLeFiujN6f&user=%7B%22id%22%3A1484311484%2C%22first_name%22%3A%22Jason%22%2C%22last_name%22%3A%22%22%2C%22username%22%3A%22JasonVurhyz%22%2C%22language_code%22%3A%22ru%22%2C%22allows_write_to_pm%22%3Atrue%7D&auth_date=1706804808&hash=96ebb8f837ad07e8d5712db65e5afc78c1c95fe7b7477d4c868255a5ff70fe40"
token = "query_id=AAHw1tcWAwAAAPDW1xY6iCW4&user=%7B%22id%22%3A6825694960%2C%22first_name%22%3A%22loftmirs%22%2C%22last_name%22%3A%22%22%2C%22username%22%3A%22loftmirs%22%2C%22language_code%22%3A%22en%22%2C%22allows_write_to_pm%22%3Atrue%7D&auth_date=1707498523&hash=92b8eaa1d94ef903fe89038ef385a2c5f5180e801cafb76a6897e7e3db5fb67a"
headers = {"User-Agent": UserAgent().random, "X-Telegram-Init-Data": token}
print(headers)
auto_enabled = False
global session
session = None

@app.on_message(filters.command("info", prefixes=".") & filters.me)
async def show_auto_responses(_, msg):
      bool_to_text = {True: "On", False: "Off"}
      await app.send_message(6164853468, f"Статус скрипта : {bool_to_text[auto_enabled]}")

@app.on_message(filters.command("on", prefixes=".") & filters.me)
async def turn_on_auto_reply(_, msg):
      global auto_enabled
      auto_enabled = True
      await app.send_message(6164853468, f"Я готов пиздить чеки сэр")
      print("Я готов пиздить чеки сэр")

@app.on_message(filters.command("off", prefixes=".") & filters.me)
async def turn_off_auto_reply(_, msg):
      global auto_enabled
      auto_enabled = False
      await app.send_message(6164853468, f"К сожалению я больше не могу ловить чеки для вас(")
      print("К сожалению я больше не могу ловить чеки для вас(")

@app.on_message()
async def on_message(client, message):
    if auto_enabled:
        if not message.text:
            return
        link = regex.search(message.text)
        if not link:
            return
        link = link.groups()[0]
        global session
        async with session.get('/api/receipts/activate/'+link) as resp:
            if resp.status == 200:
                print(f"Чек {link} был собран!\n{message.text}")
                await app.send_message(6164853468, f"Чек {link} был собран!\n{message.text}")
            elif resp.status == 404:
                print(f"Чек {link}: {(await resp.json()).get('code', 'unknown error')}")
            else:
                print(f"[CHECK] error {resp.status}")

async def main():
    global session
    session = aiohttp.ClientSession('https://arbuz.betty.games', headers=headers)
    await app.start()
    await idle()
    await app.stop()
    await session.close()

app.run(main())