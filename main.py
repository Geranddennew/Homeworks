import sqlite3
from urllib import request, parse
from urllib.request import urlopen
from urllib.error import HTTPError
from datetime import datetime

conn = sqlite3.connect("tracker.db")
cursor = conn.cursor()
cursor.execute(
    "CREATE TABLE `hosts` ( `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `url` TEXT, `msg` TEXT )")
cursor.execute(
    "CREATE TABLE `events` ( `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `host_id` INTEGER NOT NULL, `event` TEXT, `time` TEXT NOT NULL )")
conn.commit()
hosts = [['http://ggwa.ga/webmail/'], ['https://ggwa.ga/']]
cursor.executemany("INSERT INTO hosts (url, msg) VALUES (?, 'New')", hosts)


class NoRedirectHandler(request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


noRedirect = request.build_opener(NoRedirectHandler)


def tg_send(msg):
    base_url = 'https://api.telegram.org/bot5166413715:AAFFo6TuBkXGlek-DleCHACmrR08rP2ZqzA/sendMessage?chat_id=1889834495&text='
    return urlopen(base_url + parse.quote_plus(msg)).status


conn = sqlite3.connect("tracker.db")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
for host in cursor.execute("SELECT * FROM hosts").fetchall():
    url = host['url']
    try:
        response = urlopen(url, timeout=20)
    except (HTTPError) as e:
        msg = str(e)
    except Exception as e:
        msg = str(e.__class__.__name__) + ': ' + str(getattr(e, 'reason', e))
    else:
        msg = 'OK ' + str(response.status)
    if host['msg'] == msg: continue
    cursor.execute("UPDATE hosts SET msg = ? WHERE id = ?", (msg, host['id']))
    cursor.execute("INSERT INTO events (host_id, event, time) VALUES (?, ?, ?)", (host['id'], msg, datetime.now()))
    conn.commit()
    tg_send(url + ' ' + msg)
