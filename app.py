from flask import Flask,render_template,g,request,redirect
import requests
import json
import sqlite3
import os

app = Flask(__name__)
key = "14356d2e-aeb8-410a-9549-a31f55df1c7b"
player = "troywhite"

#🖥🖥🖥
DATABASE = 'bwdata.db'

#✊💾
data = requests.get("https://api.mojang.com/users/profiles/minecraft/"+player).json()
data1 = requests.get("https://api.hypixel.net/player?key=9d49337e-bf1c-4825-84e4-71c529e778a3&uuid="+data["id"]).json()
print(data["id"])




def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.route("/data")
def home():
    cursor = get_db().cursor()
    sql = "SELECT max(Wins), max(Losses), max(Winrate), max(Winstreak) FROM UltimateV2"
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("contents.html", results=results)



@app.route('/')
def datastuff():
    cursor = get_db().cursor()
    wins = int(data1["player"]["stats"]["Bedwars"]["four_four_ultimate_wins_bedwars"])
    losses = int(data1["player"]["stats"]["Bedwars"]["four_four_ultimate_losses_bedwars"])
    winrate = round(wins / (losses+wins) * 100)
    wlratio = round(wins / losses,2)
    winstreak = int(data1["player"]["stats"]["Bedwars"]["four_four_ultimate_winstreak"])

    sql2 = "DELETE FROM UltimateV2"
    sql = "INSERT INTO UltimateV2 (Wins,Losses,Winrate,Winstreak) VALUES (?,?,?,?)"
    cursor.execute(sql2)
    cursor.execute(sql,(wins,losses,wlratio,winstreak))
    get_db().commit()
    return redirect('/data')

'''
@app.route('/search', methods=["GET", "POST"])
def add():
    if request.method == "POST":
        username = request.form["search"]
        get_db().commit()
    return redirect('/')
'''

if __name__ == "__main__":
    app.run(debug=True)