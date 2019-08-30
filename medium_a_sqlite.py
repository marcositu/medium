# -*- coding: utf-8 -*-
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler, CallbackQueryHandler)

import requests
import json
import sqlite3
BOT_API = 'xxxxXXXXXXXXXX'


def start(bot, update): # para iniciar
    app=['malcomvetter','danielabloom','adam.toscher','alt3kx','clowens0716','reegun','albeckshahar','ehsahil']
    for apps in app:
        url = "https://api.rss2json.com/v1/api.json?rss_url=https://medium.com/feed/@%s" %apps
        r = requests.get(url)
        data = json.loads(r.content.decode())
        db_mail = sqlite3.connect('medium_store.db',isolation_level=None)
        cursor = db_mail.cursor()
        for x in range(0, 3):
            Nulo = None
            persona = "%s" %apps
            titulo = data["items"][x]['title']
            link = data["items"][x]['link']
            guid = data["items"][x]['guid']
            fecha = data["items"][x]['pubDate']
            row = (guid,)
            cursor.execute("SELECT count(ID) FROM app WHERE guid LIKE ? LIMIT 1",row)
            mirow=cursor.fetchone()
            if mirow[0]==0:
                row = (Nulo,persona,titulo,link,guid,fecha)
                print("[+]" + apps )
                print(" [-]" + titulo)
                print("\t[-]" + guid + " " + fecha)
                cursor.execute("INSERT INTO app VALUES(?,?,?,?,?,?)", row)
                db_mail.commit()
                chat_id = update.message.chat_id
                bot.send_message(chat_id=chat_id, text="[+]" + apps)
                bot.send_message(chat_id=chat_id, text="[+] " + data["items"][x]['title'])
                bot.send_message(chat_id=chat_id, text="\t[-] " + data["items"][x]['link'])


def mensaje_nocomando(bot, update):
    update.message.reply_text("Por favor envia un comando adecuado.\n\nPara conocer los comandos implementados consulta la /ayuda") # Respondemos al comando con el mensaje

def archivo_recibido(bot, update):
    update.message.reply_text("Por favor envia un comando adecuado.\n\nPara conocer los comandos implementados consulta la /ayuda") # Respondemos al comando con el mensaje

def main():
    updater = Updater(BOT_API)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, mensaje_nocomando))
    dp.add_handler(MessageHandler(Filters.document, archivo_recibido))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
