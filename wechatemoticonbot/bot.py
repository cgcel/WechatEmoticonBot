# !/usr/bin/env/python3
# -*- coding: utf-8 -*-
# author: elvin

import telebot
from telebot import types

from utils import EMOTICON_LIST


bot = telebot.TeleBot("your_bot_token")


@bot.message_handler(commands=['start', 'help'])
def help_command(message):
    msg = """*使用 Inline 模式发送微信小黄脸!*

使用方法 -> 对话框中:
`@wechat_emoticon_bot ` -> 默认发单个表情
    不输入任何参数, 可直接选择表情发送
`@wechat_emoticon_bot 文字` -> 发送文字 + 表情
    输入不带空格文字, 然后选择表情, 则按照 "文字[表情]" 格式发送
`@wechat_emoticon_bot 数字` -> 连发表情
    输入不带空格数字, 然后选择表情, 则按照 "[表情]x次数" 格式发送
`@wechat_emoticon_bot 文字 数字` -> 发送文字 + 若干表情

_注意: 由于 Telegram Bot API 限制, 最多只提供 50 个选项, 故可选表情已经过作者筛选_
"""
    bot.send_message(message.chat.id, msg, parse_mode="markdown")


@bot.inline_handler(lambda query: len(query.query) >= 0)
def query_photo(inline_query):
    try:
        inline_query_list = inline_query.query.split(' ')
        default_id = 1
        result_list = []
        if len(inline_query_list) == 1:
            try:
                emoticon_repeat = int(inline_query_list[0])
                for i in EMOTICON_LIST:
                    r = types.InlineQueryResultPhoto(id=str(default_id), photo_url=i['url'], thumb_url=i['url'], photo_width=1,
                                                     photo_height=1, input_message_content=types.InputTextMessageContent('{}'.format(i['text']*emoticon_repeat)))
                    result_list.append(r)
                    default_id += 1
            except:
                input_text = inline_query_list[0]
                for i in EMOTICON_LIST:
                    r = types.InlineQueryResultPhoto(id=str(default_id), photo_url=i['url'], thumb_url=i['url'], photo_width=1,
                                                     photo_height=1, input_message_content=types.InputTextMessageContent('{}{}'.format(input_text, i['text'])))
                    result_list.append(r)
                    default_id += 1
        elif len(inline_query_list) == 2:
            input_text = inline_query_list[0]
            emoticon_repeat = int(inline_query_list[1])
            for i in EMOTICON_LIST:
                r = types.InlineQueryResultPhoto(id=str(default_id), photo_url=i['url'], thumb_url=i['url'], photo_width=1, photo_height=1, input_message_content=types.InputTextMessageContent(
                    '{}{}'.format(input_text, i['text']*emoticon_repeat)))
                result_list.append(r)
                default_id += 1
        bot.answer_inline_query(inline_query.id, result_list, cache_time=1)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    bot.infinity_polling()
