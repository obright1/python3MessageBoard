import sqlite3
import time

from flask import Flask, request, render_template, redirect, url_for

conn = sqlite3.connect("./test.db", check_same_thread=False)
cursor = conn.cursor()
try:
    sql = 'CREATE TABLE msg(id integer primary key autoincrement, user varchar(64), title varchar(200), say text, date datetime) '
    cursor.execute(sql)
except Exception as e:
    print("表已存在")
finally:
    conn.commit()

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        cursor.execute('select * from msg')
        msgs = cursor.fetchall()
        return render_template("index.html", msgs=msgs)
    else:
        user = request.form.get("user")
        title = request.form.get("title")
        text = request.form.get("say")
        date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        cursor.execute('INSERT INTO "msg" ("user", "title", "say", "date") VALUES (?, ?, ?, ?)',
                       [user, title, text, date])
        conn.commit()
        return redirect(url_for("index"))


@app.route('/delete/<id>', methods=['GET'])
def delete(id):
    cursor.execute('DELETE FROM msg where id=?', [id, ])
    conn.commit()
    return redirect(url_for("index"))


@app.route("/edit/", methods=["GET", "POST"])
def edit():
    if request.method == "GET":
        id = request.args.get("id")
        cursor.execute("SELECT * FROM msg WHERE id=?", [id, ])
        msg = cursor.fetchone()
        return render_template("edit.html", msg=msg)
    else:
        id = request.form.get("id")
        user = request.form.get("user")
        title = request.form.get("title")
        say = request.form.get("say")
        cursor.execute('UPDATE "msg" SET "user"=?, "title"=?, "say"=? WHERE id=?', [user, title, say, id])
        conn.commit()
        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
