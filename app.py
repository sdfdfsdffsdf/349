import asyncio
import openai

from pyrogram import Client, filters, idle
from pyrogram.handlers import MessageHandler
from loguru import logger

from config import api_id, api_hash, key

proxy = {
     "scheme": "socks5",  # "socks4", "socks5" and "http" are supported
     "hostname": "45.192.135.158",
     "port": 50101,
     "username": "unipayday0",
     "password": "BgifgQ53VM"
 }

app = Client('my_session', api_id=api_id, api_hash=api_hash, proxy=proxy)


@app.on_message(filters.channel)
async def comment_sender(Client, message):
    try:
        post = await Client.get_discussion_message(message.chat.id, message.id)
        msg = await post.reply('Знали чим відрізняються росіяни від українців? - росіяни яйця несуть 🐔, а українці носять ✊')
        if message.photo is None and message.video is None:
            promt_text = 'Прокомментируй это как реальный человек, но не больше 15 слов:\n ' + str(message.text)
        else:
            if message.caption is not None:
                promt_text = 'Прокомментируй это как реальный человек, но не больше 15 слов:\n ' + str(message.caption)
        if promt_text is not None:
            engine = "text-davinci-003"
            openai.api_key = key
            completion = await openai.Completion.acreate(model=engine,
                                                         prompt=promt_text,
                                                         temperature=0.5,
                                                         max_tokens=1000)
            text_for_comment = str(completion.choices[0]['text']).replace('\n', '')

            if text_for_comment == '':
                text_for_comment = ' '
            if text_for_comment[0] in '.,!?:;':
                text_for_comment = text_for_comment[1:]
            if len(text_for_comment) < 5:
                text_for_comment = 'капец...'
            await msg.edit_text(text_for_comment)

            logger.info(f"Оставил комментарий -> {text_for_comment}.")
    except Exception as e:
        logger.error(e)


if __name__ == '__main__':
    logger.info("Успешно запущено!")
    app.run()
