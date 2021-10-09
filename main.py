from telethon import events
from config import bot
from FastTelethonhelper import fast_upload, fast_download
import subprocess
import asyncio

BASE = -1001719008145
FFMPEG = -1001600031692
FFMPEGID = (2, 3, 4)
FFMPEGCMD = 5
CMD = ''


loop = asyncio.get_event_loop()

async def dl_ffmpeg():
    global CMD
    message = "Starting up..."
    a = await bot.send_message(BASE, "Starting up...")
    r = await bot.send_message(BASE, "Downloading ffmpeg files now.....")
    msgs = await bot.get_messages(FFMPEG, ids=FFMPEGID)
    cmd = await bot.get_messages(FFMPEG, ids=FFMPEGCMD)
    CMD = cmd.text
    for msg in msgs:
        s = await fast_download(bot, msg, r, "")
        message = f"{message}\n{s} Downloaded" 
        await a.edit(message)        
    await r.edit(f"FFMPEG download complete, and the active command is: \n\n`{CMD}`")
    


@bot.on(events.NewMessage(pattern="/encode",))
async def _(event):
    msg = await event.get_reply_message()
    r = await event.reply("Downloading..")
    file = await fast_download(bot, msg, r, "")
    file = "Getter Robo Arc - 13.mkv"
    await r.edit("Encoding........")
    print(f'ffmpegFDK -i "{file}" -map 0 -c:v libx265 -crf 32 -s 846x480 -pix_fmt yuv420p -preset veryfast -c:a libfdk_aac  -profile:a aac_he_v2 -vbr 2 "[Encoded] {file}"')
    subprocess.call(f'./ffmpegFDK -i "{file}" -map 0 -c:v libx265 -crf 32 -s 846x480 -pix_fmt yuv420p  -preset veryfast -c:a libfdk_aac  -profile:a aac_he_v2 -vbr 2 "[Encoded] {file}"', shell=True)
    await asyncio.sleep(1)
    res_file = await fast_upload(bot, f"[Encoded] {file}", r)
    await r.reply(file=res_file, force_document=True)
    







loop.run_until_complete(dl_ffmpeg())

bot.start()

bot.run_until_disconnected()

