# -*- coding: utf-8 -*-

import requests
import json
import sqlite3


def get_app(app):
    url = "https://api.rss2json.com/v1/api.json?rss_url=https://medium.com/feed/@" + app
    r = requests.get(url)
    data = json.loads(r.content.decode())
    db_mail = sqlite3.connect('medium_store.db',isolation_level=None)
    cursor = db_mail.cursor()
    for x in range(0, 3):
        Nulo = None
        persona = app
        titulo = data["items"][x]['title']
        link = data["items"][x]['link']
        guid = data["items"][x]['guid']
        fecha = data["items"][x]['pubDate']
        row = (guid,)
        cursor.execute("SELECT count(ID) FROM app WHERE guid LIKE ? LIMIT 1",row)
        mirow=cursor.fetchone()
        if mirow[0]==0:
            row = (Nulo,persona,titulo,link,guid,fecha)
            print("[+]" + app )
            print(" [-]" + titulo)
            print("\t[-]" + guid + " " + fecha)
            cursor.execute("INSERT INTO app VALUES(?,?,?,?,?,?)", row)
            db_mail.commit()

if __name__ == '__main__':
    app=['malcomvetter','danielabloom','adam.toscher','alt3kx','clowens0716','reegun','albeckshahar','ehsahil']
    for i in app:
        get_app(i)