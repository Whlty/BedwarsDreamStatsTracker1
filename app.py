from flask import Flask,render_template,g,request,redirect
import requests
import json
import sqlite3
import os

app = Flask(__name__)
key = "14356d2e-aeb8-410a-9549-a31f55df1c7b"
player = "TroyWhite"

DATABASE = 'bwdream.db'

data = requests.get("https://api.mojang/users/profiles/minecraft/"+ player).json()
data1 = requests.get("https://api.hypixel.net/player?key=14356d2e-aeb8-410a-9549-a31f55df1c7buuid="+data["id"]).json()
print(data1["player"]["stats"]["Skywars"]["wins"])
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.route("/")
def home():
    cursor = get_db().cursor()
    sql = "SELECT * FROM UltimateV2"
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("contents.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)
