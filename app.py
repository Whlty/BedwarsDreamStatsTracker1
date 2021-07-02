#import rando garbo
from flask import Flask,render_template,g,request,redirect,flash
import requests
import json
import sqlite3
import os
import re

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
key = "e84267a6-e22c-4f9d-8e5d-7e162e6dc79b"
DATABASE = 'luckybw.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.route("/data")
def lucky():
    #stats display for one user
    # 
    #     cursor = get_db().cursor()
    sql = "SELECT name,wins,losses,kills,final_kills,bed_breaks FROM user WHERE uuid='" +uuid+ "'" #add more data
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("contents.html", results=results, player = player,uuid = uuid)

#stats display for user and friends
@app.route("/friends")
def disfriends():
    try:
        cursor = get_db().cursor()
        #gets the users id
        sql = "SELECT id FROM user WHERE uuid='" +uuid+ "'"
        cursor.execute(sql)
        u_id = str(cursor.fetchone())
        u_id = re.sub('[^0-9]', '', u_id)
        #selects all users friends
        friendsql = "SELECT friend_id FROM friends WHERE user_id='" +u_id+ "'"
        cursor.execute(friendsql)
        #puts all friends ids in a string
        allfriends = cursor.fetchall()
        allfriends = ''.join(str(e) for e in allfriends)
        allfriends = allfriends.replace(")","")
        allfriends = allfriends.replace("(","")
        allfriends = allfriends[:-1]

        #displays all users friends
        s_friend = "SELECT name,wins,losses,kills,final_kills,bed_breaks from user WHERE id in ("+allfriends+","+u_id+")"#add more data
        cursor.execute(s_friend)
        results = cursor.fetchall()
        return render_template("test.html", results=results, player = player,uuid = uuid)
    #if user has no friends
    except:
        flash("You have no friends L")
        return redirect("/data")

@app.route('/')
def datastuff():
    return render_template("home.html")

#adding or updating user
@app.route('/contents',methods=["POST","get"])
def datastuff2():
    if request.method == "POST":
        global player
        player = request.form.get("ign")
 
        try:
            data = requests.get("https://api.mojang.com/users/profiles/minecraft/"+player).json()
        
        #if that account doesn't exist
        except:
            flash("User Doesn't Exist")
            return render_template("home.html")

        #made global for adding friends
        global uuid
        uuid = str(data["id"])

        #check if api id down
        try: 
            i = requests.get("https://api.hypixel.net/player?key=e84267a6-e22c-4f9d-8e5d-7e162e6dc79b&uuid="+data["id"]).json()
            i =i 
            #request players stats from hypixel
            try:#add more data
                data1 = requests.get("https://api.hypixel.net/player?key=e84267a6-e22c-4f9d-8e5d-7e162e6dc79b&uuid="+data["id"]).json()
                wins = int(data1["player"]["stats"]["Bedwars"]["four_four_lucky_wins_bedwars"])
                losses = int(data1["player"]["stats"]["Bedwars"]["four_four_lucky_losses_bedwars"])
                kills = int(data1["player"]["stats"]["Bedwars"]["four_four_lucky_kills_bedwars"])
                final_kills = int(data1["player"]["stats"]["Bedwars"]["four_four_lucky_final_kills_bedwars"])
                bed_breaks = int(data1["player"]["stats"]["Bedwars"]["four_four_lucky_beds_broken_bedwars"]) 
                
                name = str(player)
            #if the user hasn't played the gamemode
            except:
                flash("user has not played lucky bedwars or Api is down")
                return render_template("home.html")

            cursor = get_db().cursor()
            #get the user id from table and make it show as only the id 
            sql = "SELECT id FROM user WHERE uuid='" +uuid+ "'"
            cursor.execute(sql)
            u_id = str(cursor.fetchone())
            u_id = re.sub('[^0-9]', '', u_id)

            #check if the id exists if not, creates the user
            if len(u_id) == 0:
                cursor.execute("INSERT INTO user (uuid,name,wins,losses,kills,final_kills,bed_breaks) VALUES (?,?,?,?,?,?,?)",(uuid,name,wins,losses,kills,final_kills,bed_breaks))#add more data

            #updates the user if their id exists
            else:#add more data
                cursor.execute("""UPDATE user SET name=? WHERE uuid=?""",(name,uuid))
                cursor.execute("""UPDATE user SET wins=? WHERE uuid=?""",(wins,uuid))
                cursor.execute("""UPDATE user SET losses=? WHERE uuid=?""",(losses,uuid))
                cursor.execute("""UPDATE user SET kills=? WHERE uuid=?""",(kills,uuid))
                cursor.execute("""UPDATE user SET final_kills=? WHERE uuid=?""",(final_kills,uuid))
                cursor.execute("""UPDATE user SET bed_breaks=? WHERE uuid=?""",(bed_breaks,uuid))
            
            get_db().commit()  
            return redirect("/data")
        #if api is down    
        except:
            flash("Can't update because Api is down")
            return redirect("/data")
    else:
        print("you're stupid")


@app.route("/friend",methods=["POST","GET"])
def friend():
    return render_template("friend.html")

#request data for you hypixel friends
@app.route("/addfriend",methods=["POST","GET"])
def addfriend():
    if request.method == "POST":
        friend = str(request.form.get("monkey"))
        #checks if user exists
        try:
            y = requests.get("https://api.mojang.com/users/profiles/minecraft/"+friend).json()
            requests.get("https://api.hypixel.net/player?key=e84267a6-e22c-4f9d-8e5d-7e162e6dc79b&uuid="+y["id"]).json()   
        except:
            flash("User doesn't exist or Api is down")
            return render_template("friend.html")

        data = requests.get("https://api.mojang.com/users/profiles/minecraft/"+friend).json()
        data1 = requests.get("https://api.hypixel.net/player?key=e84267a6-e22c-4f9d-8e5d-7e162e6dc79b&uuid="+data["id"]).json()
        
        #checks if user has played luckyblock gamemode
        try:
            data1["player"]["stats"]["Bedwars"]["four_four_lucky_wins_bedwars"]
        except:
            flash("they have not played lucky bedwars")
            return render_template("friend.html")

        #add more data
        #gets friends data
        flash("friend added")
        f_uuid = str(data["id"])
        wins = int(data1["player"]["stats"]["Bedwars"]["four_four_lucky_wins_bedwars"])
        kills = int(data1["player"]["stats"]["Bedwars"]["four_four_lucky_kills_bedwars"])
        final_kills = int(data1["player"]["stats"]["Bedwars"]["four_four_lucky_final_kills_bedwars"])
        bed_breaks = int(data1["player"]["stats"]["Bedwars"]["four_four_lucky_beds_broken_bedwars"])
        losses = int(data1["player"]["stats"]["Bedwars"]["four_four_lucky_losses_bedwars"])
        name = str(friend)
        
        cursor = get_db().cursor()
        #gets friends id
        sql = "SELECT id FROM user WHERE uuid='" +f_uuid+ "'"
        cursor.execute(sql)
        f_id = str(cursor.fetchone())
        f_id = re.sub('[^0-9]', '', f_id)

        #if the id doesnt exist, creates the friend
        if len(f_id) == 0:
            cursor.execute("INSERT INTO user (uuid,name,wins,losses,kills,final_kills,bed_breaks) VALUES (?,?,?,?,?,?,?)",(f_uuid,name,wins,losses,kills,final_kills,bed_breaks))#add more data
        #if friend already exists will update old data
        else:#add more data
            
            
            cursor.execute("""UPDATE user SET name=? WHERE uuid=?""",(name,f_uuid))
            cursor.execute("""UPDATE user SET wins=? WHERE uuid=?""",(wins,f_uuid))
            cursor.execute("""UPDATE user SET losses=? WHERE uuid=?""",(losses,f_uuid))
            cursor.execute("""UPDATE user SET kills=? WHERE uuid=?""",(kills,f_uuid))
            cursor.execute("""UPDATE user SET final_kills=? WHERE uuid=?""",(final_kills,f_uuid))
            cursor.execute("""UPDATE user SET bed_breaks=? WHERE uuid=?""",(bed_breaks,f_uuid))
       

        #gets friends id
        sql = "SELECT id FROM user WHERE uuid='" +f_uuid+ "'"
        cursor.execute(sql)
        f_id = str(cursor.fetchone())
        f_id = re.sub('[^0-9]', '', f_id)
        
        #gets the user id
        sql2 = "SELECT id FROM user WHERE uuid='" +uuid+ "'"
        cursor.execute(sql2)
        u_id = str(cursor.fetchone())
        u_id = re.sub('[^0-9]', '', u_id)
        
        #inserting friend into friends table
        cursor.execute("INSERT INTO friends (user_id,friend_id) VALUES (?,?)",(u_id,f_id))

        get_db().commit()

        return render_template("friend.html")

if __name__ == "__main__":
    app.run(debug=True)
   
   


