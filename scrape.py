import requests
from bs4 import BeautifulSoup
from roblox import Client
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
user_input=input("Please enter the roblox ID you wish to track: ")
async def main():
	load_dotenv()
	cookies={'.ROBLOSECURITY': os.getenv("ROBLOXTOKEN")}
	# print(cookies)
	client = Client(os.getenv("ROBLOXTOKEN"))
	user = await client.get_authenticated_user()
	# print("ID:", user.id)
	# print("Name:", user.name)
	r = requests.get("https://www.roblox.com/users/"+user_input+"/profile", cookies=cookies)
	soup = BeautifulSoup(r.content, "html.parser")
	# print(results2)
	try:
		print("Attempting to get the game they are playing...\n")
		results=soup.find_all('span', {'class' : 'icon-game profile-avatar-status'})[0]
		tmp=str(results).split("title=\"")[1]
		tmp=tmp.split("\"></span>")[0]
		print("Player is playing " + tmp)
	except:
		print("Player cannot be tracked (Privacy settings)\nAttempting to see if they are playing at all.")

	try:
		# print("Attempting to see if they are playing...\n")
		results2=soup.find_all('span',{'class': 'avatar-status game icon-game profile-avatar-status'})[0]
		print("Player is currently online roblox and playing some game on roblox.")
	except:
        	print("Player not in game or unable to see. (Privacy settings)\n")
	# print(results2)
	# tmp=str(results).split("title=\"")[1]
	# tmp=tmp.split("\"></span>")[0]
	# print("Player is playing " + tmp)
# spans = soup.find_all('span', {'class' : 'icon-game profile-avatar-status'})
asyncio.get_event_loop().run_until_complete(main())
