# !/usr/bin/env/python3
# -*- coding: utf-8 -*-
# author: elvin

import re

import telebot
from telebot import types

from utils import EMOTICON_LIST

bot = telebot.TeleBot("your_bot_token")


@bot.message_handler(commands=['start', 'help'])
def help_command(message):
    msg = """*使用 Inline 模式发送微信小黄脸!*

使用方法:

1. 不输入任何参数, 直接发送表情
    `@wechat_emoticon_bot `

2. 添加整数, 连发表情
    `@wechat_emoticon_bot 2`

3. 添加字符串+整数, 发送带表情文字
    `@wechat_emoticon_bot 2 你好 1 朋友`

_注意: 由于 Telegram Bot API 限制, 最多只提供 50 个选项, 故可选表情已经过作者筛选_
"""
    bot.send_message(message.chat.id, msg, parse_mode="markdown")


@bot.inline_handler(lambda query: len(query.query) >= 0)
def query_emoticons(inline_query):
    default_id = 1
    result_list = []

    if ' ' not in inline_query.query:  # 队列中只有一个参数
        if inline_query.query.isdecimal():  # 判断是否为数字
            emoticon_repeat = int(inline_query.query)
            for i in EMOTICON_LIST:
                r = types.InlineQueryResultPhoto(id=str(default_id), photo_url=i['url'], thumb_url=i['url'], photo_width=1,
                                                 photo_height=1, input_message_content=types.InputTextMessageContent('{}'.format(i['text']*emoticon_repeat)))
                result_list.append(r)
                default_id += 1
        else:  # 不为数字则当作字符串处理, 表情默认加在最后
            input_text = inline_query.query
            for i in EMOTICON_LIST:
                r = types.InlineQueryResultPhoto(id=str(default_id), photo_url=i['url'], thumb_url=i['url'], photo_width=1,
                                                 photo_height=1, input_message_content=types.InputTextMessageContent('{}{}'.format(input_text, i['text'])))
                result_list.append(r)
                default_id += 1

    else:  # 队列中含有空格
        result_text = inline_query.query
        if not bool(re.search(r'\d', result_text)):  # 队列中只有空格, 没有数字. 说明用户输入了含空格文本, 默认将表情加在最后
            result_text = result_text + '{e}'
        else:
            # 队列开头为数字 + 空格, 表示此处需要转化为表情
            while result_text[0].isdecimal() and result_text[1] == ' ':
                result_text = int(result_text[0]) * '{e}' + result_text[2:]
            # 队列结尾为空格 + 数字, 表示此处需要转化为表情
            while result_text[-1].isdecimal() and result_text[-2] == ' ':
                result_text = result_text[:-2] + int(result_text[-1]) * '{e}'
            if bool(re.search(r' \d ', result_text)):  # 队列中含有空格 + 数字 + 空格, 表示此处需要转化为表情
                while bool(re.search(r' \d ', result_text)):
                    result_text = re.sub(r' \d ', int(
                        re.search(r' \d ', result_text)[0])*'{e}', result_text, 1)
        for i in EMOTICON_LIST:
            r = types.InlineQueryResultPhoto(id=str(default_id), photo_url=i['url'], thumb_url=i['url'], photo_width=1,
                                             photo_height=1, input_message_content=types.InputTextMessageContent(result_text.format(e=i['text'])))
            result_list.append(r)
            default_id += 1

    bot.answer_inline_query(inline_query.id, result_list, cache_time=1)


if __name__ == "__main__":
    bot.infinity_polling()
