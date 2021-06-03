import requests
data = requests.get("https://api.mojang.com/users/profiles/minecraft/troywhite").json()
print(data["id"])
data1 = requests.get("https://api.hypixel.net/player?key=9d49337e-bf1c-4825-84e4-71c529e778a3&uuid="+data["id"]).json()

wins = int(data1["player"]["stats"]["Bedwars"]["four_four_ultimate_wins_bedwars"])
losses = int(data1["player"]["stats"]["Bedwars"]["four_four_ultimate_losses_bedwars"])
print(wins)
print(losses)
print(wins/losses)