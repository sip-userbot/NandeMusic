#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/sip-userbot/NandeMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/sip-userbot/NandeMusic/blob/master/LICENSE >
#
# All rights reserved.

import asyncio
import os

import speedtest
import wget
from pyrogram import filters

from strings import get_command
from NandeMusic import app
from NandeMusic.misc import SUDOERS

# Commands
SPEEDTEST_COMMAND = get_command("SPEEDTEST_COMMAND")


def testspeed(m):
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        m = m.edit("Menjalankan Unduh Tes Kecepatan")
        test.download()
        m = m.edit("Menjalankan Pengunggahan Tes Kecepatan")
        test.upload()
        test.results.share()
        result = test.results.dict()
        m = m.edit("Berbagi Hasil Tes Kecepatan")
        path = wget.download(result["share"])
    except Exception as e:
        return m.edit(e)
    return result, path


@app.on_message(filters.command(SPEEDTEST_COMMAND) & SUDOERS)
async def speedtest_function(client, message):
    m = await message.reply_text("Menjalankan Tes Kecepatan")
    loop = asyncio.get_event_loop()
    result, path = await loop.run_in_executor(None, testspeed, m)
    output = f"""**Hasil Tes Kecepatan**
    
<u>**Client:**</u>
**__ISP:__** {result['client']['isp']}
**__Country:__** {result['client']['country']}
  
<u>**Server:**</u>
**__Name:__** {result['server']['name']}
**__Country:__** {result['server']['country']}, {result['server']['cc']}
**__Sponsor:__** {result['server']['sponsor']}
**__Latency:__** {result['server']['latency']}  
**__Ping:__** {result['ping']}"""
    msg = await app.send_photo(
        chat_id=message.chat.id, photo=path, caption=output
    )
    os.remove(path)
    await m.delete()
