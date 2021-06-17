from flask import Flask,render_template,g,request,redirect,flash
import requests
import json
import sqlite3
import os
import re

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
key = "e84267a6-e22c-4f9d-8e5d-7e162e6dc79b"

#🖥🖥🖥
DATABASE = 'luckybw.db'
'''
#✊💾
data = requests.get("https://api.mojang.com/users/profiles/minecraft/"+player).json()
data1 = requests.get("https://api.hypixel.net/player?key=e84267a6-e22c-4f9d-8e5d-7e162e6dc79b&uuid="+data["id"]).json()
print(data["id"])
'''


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.route("/data")
def lucky():
    cursor = get_db().cursor()
    sql = "SELECT name,wins,kills,final_kills,bed_breaks FROM user WHERE uuid='" +uuid+ "'"
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("contents.html", results=results, player = player,uuid = uuid)

@app.route("/friends")
def disfriends():
    cursor = get_db().cursor()
    sql = "SELECT id FROM user WHERE uuid='" +uuid+ "'"
    cursor.execute(sql)
    u_id = str(cursor.fetchone())
    u_id = re.sub('[^0-9]', '', u_id)
    friendsql = "SELECT friend_id FROM friends WHERE id='" +u_id+ "'"
    cursor.execute(friendsql)
    results = cursor.fetchall()
    return render_template("contents.html", results=results, player = player,uuid = uuid)

@app.route('/')
def datastuff():
    return render_template("home.html")


@app.route('/contents',methods=["POST","GET"])
def datastuff2():
    if request.method == "POST":
        global player
        player = request.form.get("ign")
        

        #check1
        try:
            y = requests.get("https://api.mojang.com/users/profiles/minecraft/"+player).json()
            requests.get("https://api.hypixel.net/player?key=e84267a6-e22c-4f9d-8e5d-7e162e6dc79b&uuid="+y["id"]).json()   
        except:
            flash("User doesn't exist")
            return render_template("home.html")

        #play data
        data = requests.get("https://api.mojang.com/users/profiles/minecraft/"+player).json()
        data1 = requests.get("https://api.hypixel.net/player?key=e84267a6-e22c-4f9d-8e5d-7e162e6dc79b&uuid="+data["id"]).json()
        
        #check2
        try:
            data1["player"]["stats"]["Bedwars"]["four_four_lucky_wins_bedwars"]
        except:
            flash("user has not played lucky bedwars")
            return render_template("home.html")

        global uuid
        uuid = str(data["id"])
        print(uuid)

        wins = int(data1["player"]["stats"]["Bedwars"]["four_four_lucky_wins_bedwars"])
        kills = int(data1["player"]["stats"]["Bedwars"]["four_four_lucky_kills_bedwars"])
        final_kills = int(data1["player"]["stats"]["Bedwars"]["four_four_lucky_final_kills_bedwars"])
        bed_breaks = int(data1["player"]["stats"]["Bedwars"]["four_four_lucky_beds_broken_bedwars"])
        name = str(player)

        cursor = get_db().cursor()

        sql = "SELECT id FROM user WHERE uuid='" +uuid+ "'"
        cursor.execute(sql)
        u_id = str(cursor.fetchone())
        u_id = re.sub('[^0-9]', '', u_id)
        print(u_id)


        if len(u_id) == 0:
            print("creating user")
            cursor.execute("INSERT INTO user (uuid,name,wins,kills,final_kills,bed_breaks) VALUES (?,?,?,?,?,?)",(uuid,name,wins,kills,final_kills,bed_breaks))
        else:
            print("updating user")
            cursor.execute("""UPDATE user SET name=? WHERE uuid=?""",(name,uuid))
            cursor.execute("""UPDATE user SET wins=? WHERE uuid=?""",(wins,uuid))
            cursor.execute("""UPDATE user SET kills=? WHERE uuid=?""",(kills,uuid))
            cursor.execute("""UPDATE user SET final_kills=? WHERE uuid=?""",(final_kills,uuid))
            cursor.execute("""UPDATE user SET bed_breaks=? WHERE uuid=?""",(bed_breaks,uuid))

        get_db().commit()
        print(player)     
        return redirect("/data")
    

@app.route("/friend",methods=["POST","GET"])
def friend():
    return render_template("friend.html")



@app.route("/addfriend",methods=["POST","GET"])
def addfriend():
    if request.method == "POST":
        friend = str(request.form.get("monkey"))
        print(friend)
        try:
            y = requests.get("https://api.mojang.com/users/profiles/minecraft/"+friend).json()
            requests.get("https://api.hypixel.net/player?key=e84267a6-e22c-4f9d-8e5d-7e162e6dc79b&uuid="+y["id"]).json()   
        except:
            flash("User doesn't exist")
            return render_template("friend.html")

        data = requests.get("https://api.mojang.com/users/profiles/minecraft/"+friend).json()
        data1 = requests.get("https://api.hypixel.net/player?key=e84267a6-e22c-4f9d-8e5d-7e162e6dc79b&uuid="+data["id"]).json()
        
        try:
            data1["player"]["stats"]["Bedwars"]["four_four_lucky_wins_bedwars"]
        except:
            flash("they have not played lucky bedwars")
            return render_template("friend.html")


        flash("friend added")
        f_uuid = str(data["id"])
        wins = int(data1["player"]["stats"]["Bedwars"]["four_four_lucky_wins_bedwars"])
        kills = int(data1["player"]["stats"]["Bedwars"]["four_four_lucky_kills_bedwars"])
        final_kills = int(data1["player"]["stats"]["Bedwars"]["four_four_lucky_final_kills_bedwars"])
        bed_breaks = int(data1["player"]["stats"]["Bedwars"]["four_four_lucky_beds_broken_bedwars"])
        name = str(friend)

        
        cursor = get_db().cursor()
        sql = "SELECT id FROM user WHERE uuid='" +f_uuid+ "'"
        cursor.execute(sql)
        f_id = str(cursor.fetchone())
        print(f_id)
        f_id = re.sub('[^0-9]', '', f_id)

        if len(f_id) == 0:
            print("creating user")
            cursor.execute("INSERT INTO user (uuid,name,wins,kills,final_kills,bed_breaks) VALUES (?,?,?,?,?,?)",(f_uuid,name,wins,kills,final_kills,bed_breaks))
        else:
            print("updating user")
            cursor.execute("""UPDATE user SET name=? WHERE uuid=?""",(name,f_uuid))
            cursor.execute("""UPDATE user SET wins=? WHERE uuid=?""",(wins,f_uuid))
            cursor.execute("""UPDATE user SET kills=? WHERE uuid=?""",(kills,f_uuid))
            cursor.execute("""UPDATE user SET final_kills=? WHERE uuid=?""",(final_kills,f_uuid))
            cursor.execute("""UPDATE user SET bed_breaks=? WHERE uuid=?""",(bed_breaks,f_uuid))

            
        sql = "SELECT id FROM user WHERE uuid='" +f_uuid+ "'"
        cursor.execute(sql)
        f_id = str(cursor.fetchone())
        print(f_id)
        f_id = re.sub('[^0-9]', '', f_id)


        sql2 = "SELECT id FROM user WHERE uuid='" +uuid+ "'"
        cursor.execute(sql2)
        u_id = str(cursor.fetchone())
        print(u_id)
        u_id = re.sub('[^0-9]', '', u_id)
        
        #inserting friend
        cursor.execute("INSERT INTO friends (user_id,friend_id) VALUES (?,?)",(u_id,f_id))

        print(f_id)
        print(u_id)

        get_db().commit()

        return render_template("friend.html")












if __name__ == "__main__":
    app.run(debug=True)
   
   


