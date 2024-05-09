#!/usr/bin/python3
import discord
import datetime
import asyncio
import aiohttp
import contextlib
from discord.ext import tasks
from discord.ext import commands
from discord import app_commands
from typing import Optional, Literal
import requests
import shutil
import subprocess
import uuid
import json
from PIL import Image
import requests
from bs4 import BeautifulSoup
from roblox import Client
import os
from dotenv import load_dotenv
import traceback
class bot(discord.Client):
	def __init__(self):
		super().__init__(intents=discord.Intents.all())
		self.synced = False
#		self.monitor_checker.start()
	async def on_ready(self):
		await self.wait_until_ready()
		await tree.sync(guild=discord.Object(id="1114399245068406787"))
		await tree.sync(guild=discord.Object(id="1152729908406136936"))
		monitor_checker.start()





client = bot()
tree = app_commands.CommandTree(client)

@tree.error
async def on_app_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
	print("We had an oopsie\n" + str(error))
	print(traceback.format_exc())
	if isinstance(error, app_commands.CommandOnCooldown):
		await interaction.response.send_message(error, ephemeral =True)
	return


@client.event
async def on_message(message):
	if isinstance(message.channel, discord.DMChannel):
		channel = client.get_channel(1130298938092691506)
		embed=discord.Embed(title=message.author, description=message.content, color=0x00FF00)
		await channel.send(embed=embed, content="this shouldnt be here\n")
		# print(str(message.author)+"\n"+str(message.content))

async def add_to_file(filename, player, clan):
	with open(filename, "a") as f:
		f.write(player+ ": " + clan)
		f.write("\n")
		f.close()

async def remove_from_file(filename, player, clan):
	with open(filename, "r") as f:
		data=str(f.read())
		f.close()
	tocheck=str(str(player)+": "+str(clan)+"\n")
	if tocheck in data:
		data = data.replace(tocheck, "")
		E=False
	else:
		E=True
	with open(filename, "w") as f:
		f.write(data)
		f.close()
	return E
async def read_file(filename):
	with open(filename, "r") as f:
		data=str(f.read())
		return data

async def update_guild_poo(guild):
	poo = discord.utils.find(lambda r: r.name == 'POO', guild.roles)
	pee = discord.utils.find(lambda r: r.name == 'Pee', guild.roles)
	f=open("members_dict.json")
	members_dict = json.load(f)
	for member in guild.members:
		# print(member)
		if poo in member.roles and member.name not in members_dict or pee in member.roles and member.name not in members_dict:
			members_dict[member.name] = 3
		#elif poo in member.roles and member.global_name in file or pee in member.roles and member.global_name in file:
			#members_dict
	with open("members_dict.json", "w") as g:
		json.dump(members_dict, g)
async def can_beatup(member):
	f=open("members_dict.json")
	members_dict = json.load(f)
	if member.name not in members_dict:
		return False
	current_count=members_dict[member.name]
	if current_count < 1:
		return False
	else:
		return True


@tree.command(description="Give an amount of beat ups to a member", guild=discord.Object(id=1114399245068406787))
async def give_beatup(interaction: discord.Interaction, amount: str, member: discord.Member=None):
	await interaction.response.defer()
	await asyncio.sleep(1)
	await update_guild_poo(interaction.guild)
	f=open("members_dict.json")
	members_dict = json.load(f)
	# caller=await interaction.guild.fetch_member(interaction.user.id)
	amount=int(amount)
	#print(type(amount))
	if int(amount) < 0 and str(interaction.user.id) != "317418749273833473":
		await interaction.followup.send("No negative numbers")
		return False
	if member != None and member.name not in members_dict:
		await interaction.followup.send(str(member.name) + " is not a poo role!")
		return False
	if int(amount) > 3 and str(interaction.user.id) != "317418749273833473":
		await interaction.followup.send("Can only add up to 3 beatups. nerd.")
		return False
	amount=str(amount)
	if member == None and str(interaction.user.id) == "317418749273833473":
		for i in members_dict.keys():
			members_dict[i] = members_dict[i]+int(amount)
	elif member == None and str(interaction.user.id) != "317418749273833473":
		await interaction.followup.send("You do not have permission to add beat ups to everyone. idiot")
		return False
	elif member != None:
		if int(amount) < 0:
			await interaction.followup.send("No negative numbers")
			return False
		if member.name not in members_dict:
			await interaction.followup.send(str(member.name) + " is not a poo role!")
			return False
		if int(amount) > 3 and str(interaction.user.id) != "317418749273833473":
			await interaction.followup.send("Can only add up to 3 beatups. nerd.")
			return False
		members_dict[member.name] = members_dict[member.name]+int(amount)
	with open("members_dict.json", "w") as g:
		json.dump(members_dict, g)
	if member == None:
		await interaction.followup.send("Added "+amount+" beat ups to everyone!")
	else:
		await interaction.followup.send("Added "+amount+" beat ups to "+str(member.name))

@tree.command(description="Take away an amount of beat ups to a member", guild=discord.Object(id=1114399245068406787))
async def remove_beatup(interaction: discord.Interaction, member: discord.Member, amount: str):
	await interaction.response.defer()
	await asyncio.sleep(1)
	await update_guild_poo(interaction.guild)
	f=open("members_dict.json")
	members_dict = json.load(f)
	if member.name not in members_dict:
		await interaction.followup.send(str(member.name) + " is not a poo role!")
		return False
	if int(amount) < 0:
				await interaction.followup.send("No negative numbers")
				return False
	if members_dict[member.name]-int(amount) < 0:
		await interaction.followup.send("Cannot remove past 0")
		return False
	members_dict[member.name] = members_dict[member.name]-int(amount)
	with open("members_dict.json", "w") as g:
		json.dump(members_dict, g)
	await interaction.followup.send("Removed "+amount+" beat ups to "+str(member.name))

@tree.command(description="Check how many beatups you have left", guild=discord.Object(id=1114399245068406787))
async def check_beatups(interaction: discord.Interaction):
	await update_guild_poo(interaction.guild)
	f=open("members_dict.json")
	members_dict = json.load(f)
	if interaction.user.name not in members_dict:
		await interaction.response.send_message("You are not a poo role!")
		return False
	await interaction.response.send_message("You have "+str(members_dict[interaction.user.name]) + " beatups left. Disgusting poo vermin.")

@app_commands.checks.cooldown(1, 120, key=lambda i: i.user.id)
@tree.command(description="Beat up a player!", guild=discord.Object(id=1114399245068406787))
async def beatup(interaction: discord.Interaction, member: discord.Member):
	await interaction.response.defer()
	await asyncio.sleep(1)
	await update_guild_poo(interaction.guild)
	f=open("members_dict.json")
	members_dict = json.load(f)
	duration = datetime.timedelta(seconds=30, minutes=0, hours=0, days=0)
	channel = client.get_channel(interaction.channel_id)
	caller= await interaction.guild.fetch_member(interaction.user.id)
	poo = discord.utils.find(lambda r: r.name == 'POO', interaction.guild.roles)
	pee = discord.utils.find(lambda r: r.name == 'Pee', interaction.guild.roles)
	fem = discord.utils.find(lambda r: r.name == 'Femboy :nerd:', interaction.guild.roles)
	role = discord.utils.find(lambda r: r.name == 'Fodder', interaction.guild.roles)
	can = await can_beatup(caller)
	if poo in caller.roles and can and role not in member.roles or pee in caller.roles and can and role not in member.roles:
		await interaction.followup.send(str(caller.display_name)+" beat up "+str(member.mention)+"!")
		await channel.send("https://media.discordapp.net/attachments/1135338981861642261/1140838348404052088/Shut_up_poo.gif")
		duration=datetime.timedelta(seconds=0, minutes=7, hours=0, days=0)
		await member.timeout(duration)
		members_dict[caller.name]= members_dict[caller.name]-1
	elif role in caller.roles:
		duration=datetime.timedelta(seconds=30, minutes=0, hours=0, days=0)
		if poo in member.roles or pee in member.roles or fem in member.roles:
			if caller.nick == None:
				await interaction.followup.send(str(caller.display_name)+" beat up "+str(member.mention)+"!")
				await channel.send("https://media.discordapp.net/attachments/1135338981861642261/1140838348404052088/Shut_up_poo.gif")
				await member.timeout(duration)
			else:
				await interaction.followup.send(str(caller.nick)+" beat up "+str(member.mention)+"!")
				await channel.send("https://media.discordapp.net/attachments/1135338981861642261/1140838348404052088/Shut_up_poo.gif")
				await member.timeout(duration)
		else:
			await interaction.followup.send("This command can only be used against the disgusting Poo roles")
	else:
		await interaction.followup.send("This command can only be used against other disgusting poos or you have already used your beat ups.")
	with open("members_dict.json", "w") as g:
		json.dump(members_dict, g)
	# player_id=int(player_id)
	# caller = interaction.user.display_name
	# receiver = await client.fetch_user(player_id)
	# print(caller, receiver.display_name)
	# await interaction.followup.send(str(caller)+" beat up "+str(member.nick)+"!")
#	channel = client.get_channel(interaction.channel_id)
#	role = discord.utils.find(lambda r: r.name == 'Fodder', interaction.message.guild.roles)

@tree.command(description="hidden", guild=discord.Object(id=1114399245068406787))
async def hidden(interaction: discord.Interaction, message: str, ids: str):
	if interaction.user.id ==317418749273833473:
		await interaction.response.defer()
		await asyncio.sleep(1)
		user = await client.fetch_user(ids)
		await user.send(message)
		await interaction.followup.send("Done!")
	else:
		await interaction.response.defer()
		await asyncio.sleep(1)
		await interaction.followup.send("You are not allowed to use this command")


# @tree.command(description="Update the monitor_player channel with every added player", guild=discord.Object(id=1152729908406136936))
# async def monitor_checker(interaction: discord.Interaction):

@tasks.loop(minutes=5, reconnect=True)
async def monitor_checker():
	try:
		# await interaction.response.defer()
		f=open("player_id.json")
		player_ids=json.load(f)
		# await asyncio.sleep(1)
		# await interaction.followup.send("Updating!")
		load_dotenv()
		# print(ctx)
		channel=client.get_channel(1165170204762972190)
		messages = [message async for message in channel.history(limit=1,oldest_first=True)][0] # Grab most old message (the monitor list)
		msg = await channel.fetch_message(messages.id) # get the prior monitor list id
		# await msg.edit(content="changed")
		cookies={'.ROBLOSECURITY': os.getenv("ROBLOXTOKEN")}
		# print(cookies)
		client2 = Client(os.getenv("ROBLOXTOKEN"))
		user = await client2.get_authenticated_user()
		# print("ID:", user.id)
		# print("Name:", user.name)
		embed=discord.Embed(title="Monitor List", description="", color=0xFF0000)
		to_send=""
		with open("monitor.txt") as f:
			for roblox_username in f:
				# print(roblox_username)
				roblox_username=roblox_username.strip()[:-1]
				if roblox_username in player_ids:
					roblox_player_id=player_ids[roblox_username]
				requestPayload = {
						"usernames": [
								roblox_username
						]
				}
				# try:
				# 	# print(roblox_username)
				# 	if roblox_username not in player_ids:
				# 		async with aiohttp.ClientSession() as session:
				# 			async with session.post("https://users.roblox.com/v1/usernames/users",json=requestPayload) as r2:
				# 				nameis=(await r2.json())
				# 				# print(nameis["data"][0]["id"])
				# 				roblox_player_id = nameis["data"][0]["id"]
				# 				player_ids[roblox_username]=roblox_player_id
				# 				json_object=json.dumps(player_ids)
				# 				with open("player_id.json", "w") as outfile:
				# 					outfile.write(json_object)

				# 				# r2=requests.post("https://users.roblox.com/v1/usernames/users",json=requestPayload)
				# 				# print("Here")
				# 	async with aiohttp.ClientSession() as session2:
				# 		async with session2.get("http://www.roblox.com/users/"+str(roblox_player_id)+"/profile", cookies=cookies) as r:
				# 			txt=await r.content.read()
				# 			# print("Here")
				# 			soup = BeautifulSoup((str(txt)), "html.parser")
				# 			# r = requests.get("http://www.roblox.com/users/"+str(roblox_player_id)+"/profile", cookies=cookies)
				# 	#print(r)
				# 	#print("https://www.roblox.com/users/"+str(roblox_player_id)+"/profile")
				# 	try:
				# 		# await interaction.response.send_message("Attempting to get the game they are playing...\n")
				# 		results=soup.find_all('span', {'class' : 'profile-avatar-status game icon-game'})[0]
				# 	#	print(results)
				# 		tmp=str(results).split("title=\"")[1]
				# 		tmp=tmp.split("\"></span>")[0]
				# 		# print(results)
				# 	#	print("Player is playing something"+tmp)
				# 		# await channel.send(roblox_username+" is playing " + tmp)
				# 		# print(results)
				# 		to_send+=roblox_username+" is playing " + tmp+"\n"
				# 	except Exception as e:
				# 		# print("err1")
				# 		# await channel.send(roblox_username+" cannot be tracked (Privacy settings)\nAttempting to see if they are playing at all.")
				# 		try:
				# 			# print("Attempting to see if they are playing...\n")
				# 			results2=soup.find_all('span',{'class': 'profile-avatar-status game icon-game'})[0]
				# 			# print(results2)
				# 			# await interaction.edit_original_response(content = roblox_username+" is currently online roblox and playing some game on roblox.")
				# 			to_send+=roblox_username+"\'s online and playing some game on roblox.\n"

				# 		except:
				# 			# await interaction.edit_original_response(content =roblox_username+" not in game or unable to see. (Privacy settings)\n")
				# 			to_send+=roblox_username+" not in game/unable to see.\n"
				# except Exception as e:
				# 	print(e,roblox_username)
				try:
					if roblox_username not in player_ids:
						async with aiohttp.ClientSession() as session:
							async with session.post("https://users.roblox.com/v1/usernames/users",json=requestPayload) as r2:
								nameis=(await r2.json())
								# print(nameis["data"][0]["id"])
								roblox_player_id = nameis["data"][0]["id"]
								player_ids[roblox_username]=roblox_player_id
								json_object=json.dumps(player_ids)
								with open("player_id.json", "w") as outfile:
									outfile.write(json_object)
					headers = {"Content-Type": "application/json"}
					info={"userIds":[roblox_player_id]}
					json_data = json.dumps(info)
					async with aiohttp.ClientSession() as session2:
						async with session2.post("http://presence.roblox.com/v1/presence/users", cookies=cookies, headers=headers,data=json_data) as r:
							txt=await r.content.read()
							# print("Here")
							# print(txt)
							# if '{"userPresenceType":2' in txt:
							# soup = BeautifulSoup((str(txt)), "html.parser")
				except Exception as e:
					print("Error occurred (Likely username doesnt exist)",e)
				txt=json.loads(txt.decode())
				game=txt['userPresences'][0]['lastLocation']
				presence=txt['userPresences'][0]['userPresenceType']
				if game!='Website'and game!=''and presence ==2:
					# await interaction.followup.send(roblox_username+" is playing " +game)
					to_send+=roblox_username+" is playing " + game+"\n"
				elif game==''and presence == 2:
					# await interaction.followup.send(roblox_username+"\'s online and playing some game on roblox.\n")
					to_send+=roblox_username+"\'s online and playing some game on roblox.\n"
				elif game=='Website'and presence == 1:
					# await interaction.followup.send(roblox_username+"\'s online roblox but not playing a game.\n")
					to_send+=roblox_username+"\'s online roblox but not playing a game.\n"
				elif game=="Website" and presence == 0:
					# await interaction.followup.send(roblox_username+" is offline\n")
					to_send+=roblox_username + "is offline\n"

			# embed.add_field(name="", value=to_send)
			with open("monitor_results.txt", "w") as e:
				e.write(to_send)
				e.close()
			length_of_string=len(to_send)
			count=0
			while(length_of_string > 1023):
				new_field=to_send[:1023]
				embed.add_field(name="", value=new_field)
				length_of_string=length_of_string-1023
				count+=1
			to_add=count*1023
			embed.add_field(name="", value=to_send[to_add:])
			# print(embed)
			await msg.edit(embed=embed, content="")
	except Exception as e:
		print(f"An exception occurred: {e}")
		await asyncio.sleep(60)
		monitor_checker.restart()



@tree.command(description="Monitor a players status on roblox!", guild=discord.Object(id=1152729908406136936))
async def monitor(interaction: discord.Interaction, roblox_username: str, add: Literal["True", "False"]):
	mon=open("monitor.txt", "r").read()
	# print(add,roblox_username)
	# print(add == True and roblox_username not in mon)
	await interaction.response.defer()
	await asyncio.sleep(2)
	with open("player_id.json", "r") as f:
		to_check = json.load(f)
	roblox_username=roblox_username.strip()
	load_dotenv()
	if len(roblox_username) >20 or len(roblox_username) <3:
		raise Exception("Sorry, invalid roblox username length must be 6-20")
	else: 
		# print(client)
		embed=discord.Embed(title="Monitor List", description="", color=0xFF0000)
		cookies={'.ROBLOSECURITY': os.getenv("ROBLOXTOKEN")}
		# print(cookies)
		client2 = Client(os.getenv("ROBLOXTOKEN"))
		user = await client2.get_authenticated_user()
		# print("ID:", user.id)
		# print("Name:", user.name)
		channel=client.get_channel(1165170204762972190)
		messages = [message async for message in channel.history(limit=1,oldest_first=True)][0] # Grab most old message (the monitor list)
		msg = await channel.fetch_message(messages.id)
		# await channel.send("h")
		roblox_username=roblox_username.strip()
		# print(roblox_username)
		requestPayload = {
			"usernames": [
				roblox_username
			]
		}
		try:
			if roblox_username not in to_check:
				async with aiohttp.ClientSession() as session:
						async with session.post("https://users.roblox.com/v1/usernames/users",json=requestPayload) as r2:
							nameis=(await r2.json())
							# print(nameis["data"][0]["id"])
							roblox_player_id = nameis["data"][0]["id"]
							to_check[roblox_username]=roblox_player_id
							# r2=requests.post("https://users.roblox.com/v1/usernames/users",json=requestPayload)
							# print("Here")
			else:
				roblox_player_id=to_check[roblox_username]
			json_object=json.dumps(to_check)
			with open("player_id.json", "w") as outfile:
				outfile.write(json_object)
			headers = {"Content-Type": "application/json"}
			info={"userIds":[roblox_player_id]}
			json_data = json.dumps(info)
			async with aiohttp.ClientSession() as session2:
				async with session2.post("http://presence.roblox.com/v1/presence/users", cookies=cookies, headers=headers,data=json_data) as r:
					txt=await r.content.read()
					# print("Here")
					# print(txt)
					# if '{"userPresenceType":2' in txt:
					# soup = BeautifulSoup((str(txt)), "html.parser")
		except Exception as e:
			print("Error occurred (Likely username doesnt exist)",e)
		#print(r)
		# print(add,roblox_username)
		# print(roblox_username not in mon)
		# print(add == True and roblox_username not in mon)
		if add == "True" and roblox_username not in mon:
			print("in check")
			await add_to_file("monitor.txt", roblox_username, "")
		with open('monitor_results.txt', 'r') as file:
			lines = file.readlines()
		filtered_lines = [line for line in lines if roblox_username not in line]
		with open('monitor_results.txt', 'w') as file:
			file.writelines(filtered_lines)
		checker=await read_file("monitor_results.txt")
		#print("https://www.roblox.com/users/"+str(roblox_player_id)+"/profile")
		try:
			# await interaction.response.send_message("Attempting to get the game they are playing...\n")
		# 	print(soup.find_all('span', {'class' : 'profile-avatar-status game icon-game'}))
		# 	results=soup.find_all('span', {'class' : 'profile-avatar-status game icon-game'})[0]
		# #	print(results)
		# 	tmp=str(results).split("title=\"")[1]
		# 	print(tmp)
		# 	tmp=tmp.split("\"></span>")[0]
		# 	print(tmp)
		# #	print("Player is playing something"+tmp)
			txt=json.loads(txt.decode())
			game=txt['userPresences'][0]['lastLocation']
			presence=txt['userPresences'][0]['userPresenceType']
			if game!='Website'and game!=''and presence ==2:
				await interaction.followup.send(roblox_username+" is playing " +game)
				checker+=roblox_username+" is playing " + game+"\n"
			elif game==''and presence == 2:
				await interaction.followup.send(roblox_username+"\'s online and playing some game on roblox.\n")
				checker+=roblox_username+"\'s online and playing some game on roblox.\n"
			elif game=='Website'and presence == 1:
				await interaction.followup.send(roblox_username+"\'s online roblox but not playing a game.\n")
				checker+=roblox_username+"\'s online roblox but not playing a game.\n"
			elif game=="Website" and presence == 0:
				await interaction.followup.send(roblox_username+" is offline\n")
				checker+=roblox_username + "is offline\n"

			# if add !=None and roblox_username not in r:
			# 	await add_to_file("monitor.txt", roblox_username, " is playing "+tmp)

		except Exception as e:
			print(e)
			print(traceback.format_exc())
			# await interaction.followup.send(roblox_username+" cannot be tracked (Privacy settings)\nAttempting to see if they are playing at all.")

			# try:
			# 	# print("Attempting to see if they are playing...\n")
			# 	print(soup.find_all('span', {'class' : 'profile-avatar-status game icon-game'}))
			# 	results2=soup.find_all('span',{'class': 'profile-avatar-status game icon-game'})[0]
			# 	await interaction.edit_original_response(content = roblox_username+"\'s online and playing some game on roblox.")
			# 	# if add !=None and roblox_username not in r:
			# 	# 	await add_to_file("monitor.txt", roblox_username, " is playing "+tmp)
				
			# 	checker+=roblox_username+"\'s online and playing some game on roblox.\n"
			# except:
			# 	await interaction.edit_original_response(content =roblox_username+" not in game/unable to see.\n")
				
			# 	checker+=roblox_username+" not in game/unable to see.\n"
				# if add !=None and roblox_username not in r:
				#	await add_to_file("monitor.txt", roblox_username, " is playing "+tmp)
		if add=="False" and roblox_username not in mon:
			checker=await read_file("monitor_results.txt")
		# print(len(checker))
		length_of_string=len(checker)
		count=0
		while(length_of_string > 1023):
			new_field=checker[:1023]
			embed.add_field(name="", value=new_field)
			length_of_string=length_of_string-1023
			count+=1
		to_add=count*1023
		embed.add_field(name="", value=checker[to_add:])
		await msg.edit(embed=embed, content="")
@tree.command(description="Remove a person from the monitored list",guild=discord.Object(id=1152729908406136936))
async def remove_monitor(interaction: discord.Interaction, roblox_username: str):

	with open('monitor_results.txt', 'r') as file:
		lines = file.readlines()
	filtered_lines = [line for line in lines if roblox_username not in line]
	with open('monitor_results.txt', 'w') as file:
		file.writelines(filtered_lines)

	with open('monitor.txt', 'r') as file:
		lines = file.readlines()
	filtered_lines = [line for line in lines if roblox_username not in line]
	with open('monitor.txt', 'w') as file:
		file.writelines(filtered_lines)
	channel=client.get_channel(1165170204762972190)
	messages = [message async for message in channel.history(limit=1,oldest_first=True)][0] # Grab most old message (the monitor list)
	msg = await channel.fetch_message(messages.id)
	checker=await read_file("monitor_results.txt")
	embed=discord.Embed(title="Monitor List", description="", color=0xFF0000)
	embed.add_field(name="", value=checker)
	await msg.edit(embed=embed, content="")
	await interaction.response.send_message(roblox_username+" removed!")

# TSFC CLAN
@tree.command(description="Speechbubble a nerd!", guild=discord.Object(id=1114399245068406787))
async def speechbubble(interaction: discord.Interaction, url: str, type_of_bubble: Literal["Small/White", "Large/Black"], reverse: bool, color: bool):
	try:
		r = requests.get(url, stream = True)
		# Check if the image was retrieved successfully
		if r.status_code == 200:
			# Set decode_content value to True, otherwise the downloaded image file's size will be zero.
			r.raw.decode_content = True
			random_value=str(uuid.uuid4())
			# Open a local file with wb ( write binary ) permission.
			with open("/tmp/"+random_value+".png",'wb') as f:
				shutil.copyfileobj(r.raw, f)
			print("Successfully downloaded image with random value "+str(random_value))
		# Opening the primary image (used in background)
		img1 = Image.open("/tmp/"+random_value+".png").convert("RGBA")
		print("Opening image file with name  "+str(random_value))
		print("Values of "+str(img1.width)+"x"+str(img1.height))
		if not reverse:
			if img1.height < 200:
				size_here=size_here=str(img1.width+50)+"x"+str(img1.height*.3)
			else:
				size_here=str(img1.width+50)+"x"+str(img1.height*.15)
		else:
			if img1.height < 200:
				size_here=size_here=str(img1.width+40)+"x"+str(img1.height*.2)
			else:
				size_here=str(img1.width+40)+"x"+str(img1.height*.1)
		speech2=str(uuid.uuid4())
		print("Creating new uuid for speech2 "+str(speech2))
		#cmd = ["convert", "speechbubble.png","-resize", size_here+"!", "/tmp/"+speech2+".png"] # Get command created to create a new image matching the aspect ratio
		#fconvert = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		#stdout, stderr = fconvert.communicate()
		if type_of_bubble == "Large/Black" and reverse:
			subprocess.call("convert testspeech2.png -flop -resize "+size_here+"!"+" /tmp/"+speech2+".png",shell=True)
		elif type_of_bubble == "Small/White" and reverse:
			subprocess.call("convert speechbubble2.png -flop -resize "+size_here+"!"+" /tmp/"+speech2+".png",shell=True)
		# elif type_of_bubble == "Grey" and reverse:
		# 	subprocess.call("convert discordspeechbubble.png -flop -resize "+size_here+"!"+" /tmp/"+speech2+".png",shell=True)
		elif type_of_bubble == "Large/Black" and not reverse:
			subprocess.call("convert testspeech2.png -resize "+size_here+"!"+" /tmp/"+speech2+".png",shell=True)
		# elif type_of_bubble == "Grey" and not reverse:
		# 	subprocess.call("convert discordspeechbubble.png -resize "+size_here+"!"+" /tmp/"+speech2+".png",shell=True)
		else:
			subprocess.call("convert speechbubble2.png -resize "+size_here+"!"+" /tmp/"+speech2+".png",shell=True)
		#   convert drawn.png mask_shape.png -compose DstOut -composite drawn_bite3.png
		r4=str(uuid.uuid4())
		img1.save("/tmp/"+r4+".png")
		if color:
			img2 = Image.open(r"/tmp/"+speech2+".png").convert("RGBA")
			img1.paste(img2, (0,0), mask = img2)
			r3=str(uuid.uuid4())
			img1.save("/tmp/"+r3+".png")
			subprocess.call("convert /tmp/"+r3+".png /tmp/babytoad3"+r3+".gif",shell=True) #Convert the image to a gif so it can be saved on discord
		else:
			r3=str(uuid.uuid4())
			subprocess.call("convert /tmp/"+r4+".png /tmp/"+speech2+".png -compose DstOut -composite /tmp/final.png",shell=True)
			subprocess.call("convert /tmp/final.png /tmp/babytoad3"+r3+".gif",shell=True) #Convert the image to a gif so it can be saved on discord

		# img2 = Image.open(r"/tmp/"+speech2+".png").convert("RGBA")
		# img1.paste(img2, (0,0), mask = img2)
		# r3=str(uuid.uuid4())
		# img1.save("/tmp/"+r3+".png")
		await interaction.response.defer() # Defer the response
		# subprocess.call("convert /tmp/final.png /tmp/babytoad3"+r3+".gif",shell=True) #Convert the image to a gif so it can be saved on discord
		await interaction.followup.send("Working on it!") #Respond so we can avoid a timeout
		await asyncio.sleep(2.5) #Give a wait time 
		await interaction.edit_original_response(content = "", attachments=[discord.File("/tmp/babytoad3"+r3+".gif")]) #Send file
	except Exception as e:
		print("Error: "+str(e))

# HUA TAO CLUB
@tree.command(description="Speechbubble a nerd!", guild=discord.Object(id=1152729908406136936))
async def speechbubble(interaction: discord.Interaction, url: str, type_of_bubble: Literal["Small/White", "Large/Black"], reverse: bool, color: bool):
	try:
		r = requests.get(url, stream = True)
		# Check if the image was retrieved successfully
		if r.status_code == 200:
			# Set decode_content value to True, otherwise the downloaded image file's size will be zero.
			r.raw.decode_content = True
			random_value=str(uuid.uuid4())
			# Open a local file with wb ( write binary ) permission.
			with open("/tmp/"+random_value+".png",'wb') as f:
				shutil.copyfileobj(r.raw, f)
			print("Successfully downloaded image with random value "+str(random_value))
		# Opening the primary image (used in background)
		img1 = Image.open("/tmp/"+random_value+".png").convert("RGBA")
		print("Opening image file with name  "+str(random_value))
		print("Values of "+str(img1.width)+"x"+str(img1.height))
		if not reverse:
			if img1.height < 200:
				size_here=size_here=str(img1.width+50)+"x"+str(img1.height*.3)
			else:
				size_here=str(img1.width+50)+"x"+str(img1.height*.15)
		else:
			if img1.height < 200:
				size_here=size_here=str(img1.width+40)+"x"+str(img1.height*.2)
			else:
				size_here=str(img1.width+40)+"x"+str(img1.height*.1)
		speech2=str(uuid.uuid4())
		print("Creating new uuid for speech2 "+str(speech2))
		#cmd = ["convert", "speechbubble.png","-resize", size_here+"!", "/tmp/"+speech2+".png"] # Get command created to create a new image matching the aspect ratio
		#fconvert = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		#stdout, stderr = fconvert.communicate()
		# await asyncio.sleep(2.5) #Give a wait time
		await interaction.response.defer() # Defer the response
		await interaction.followup.send("Working on it!") #Respond so we can avoid a timeout

		await asyncio.sleep(2) #Give a wait time
		if type_of_bubble == "Large/Black" and reverse:
			subprocess.call("convert testspeech2.png -flop -resize "+size_here+"!"+" /tmp/"+speech2+".png",shell=True)
		elif type_of_bubble == "Small/White" and reverse:
			subprocess.call("convert speechbubble2.png -flop -resize "+size_here+"!"+" /tmp/"+speech2+".png",shell=True)
		# elif type_of_bubble == "Grey" and reverse:
		# 	subprocess.call("convert discordspeechbubble.png -flop -resize "+size_here+"!"+" /tmp/"+speech2+".png",shell=True)
		elif type_of_bubble == "Large/Black" and not reverse:
			subprocess.call("convert testspeech2.png -resize "+size_here+"!"+" /tmp/"+speech2+".png",shell=True)
		# elif type_of_bubble == "Grey" and not reverse:
		# 	subprocess.call("convert discordspeechbubble.png -resize "+size_here+"!"+" /tmp/"+speech2+".png",shell=True)
		else:
			subprocess.call("convert speechbubble2.png -resize "+size_here+"!"+" /tmp/"+speech2+".png",shell=True)
		#   convert drawn.png mask_shape.png -compose DstOut -composite drawn_bite3.png
		r4=str(uuid.uuid4())
		
		if color:
			img2 = Image.open(r"/tmp/"+speech2+".png").convert("RGBA")
			img1.paste(img2, (0,0), mask = img2)
			r3=str(uuid.uuid4())
			img1.save("/tmp/"+r3+".png")
			subprocess.call("convert /tmp/"+r3+".png /tmp/babytoad3"+r3+".gif",shell=True) #Convert the image to a gif so it can be saved on discord
		else:
			img1.save("/tmp/"+r4+".png")
			r3=str(uuid.uuid4())
			subprocess.call("convert /tmp/"+r4+".png /tmp/"+speech2+".png -compose DstOut -composite /tmp/final.png",shell=True)
			subprocess.call("convert /tmp/final.png /tmp/babytoad3"+r3+".gif",shell=True) #Convert the image to a gif so it can be saved on discord

		# img2 = Image.open(r"/tmp/"+speech2+".png").convert("RGBA")
		# img1.paste(img2, (0,0), mask = img2)
		# r3=str(uuid.uuid4())
		# img1.save("/tmp/"+r3+".png")
		# await interaction.response.defer() # Defer the response
		# subprocess.call("convert /tmp/final.png /tmp/babytoad3"+r3+".gif",shell=True) #Convert the image to a gif so it can be saved on discord
		# await interaction.followup.send("Working on it!") #Respond so we can avoid a timeout
		# await asyncio.sleep(3) #Give a wait time 
		# print(r3,r4)
		await interaction.edit_original_response(content = "", attachments=[discord.File("/tmp/babytoad3"+r3+".gif")]) #Send file
	except Exception as e:
		print("Error: "+str(e))

#CCAIN SERVER
@tree.command(description="Speechbubble a nerd (For CCains server)!", guild=discord.Object(id=1113068537595048006))
async def speechbubble(interaction: discord.Interaction, url: str, type_of_bubble: Literal["Small/White", "Large/Black"], reverse: bool, color: bool):
	try:
		r = requests.get(url, stream = True)
		# Check if the image was retrieved successfully
		if r.status_code == 200:
			# Set decode_content value to True, otherwise the downloaded image file's size will be zero.
			r.raw.decode_content = True
			random_value=str(uuid.uuid4())
			# Open a local file with wb ( write binary ) permission.
			with open("/tmp/"+random_value+".png",'wb') as f:
				shutil.copyfileobj(r.raw, f)
			print("Successfully downloaded image with random value "+str(random_value))
		# Opening the primary image (used in background)
		img1 = Image.open("/tmp/"+random_value+".png").convert("RGBA")
		print("Opening image file with name  "+str(random_value))
		print("Values of "+str(img1.width)+"x"+str(img1.height))
		if not reverse:
			if img1.height < 200:
				size_here=size_here=str(img1.width+50)+"x"+str(img1.height*.3)
			else:
				size_here=str(img1.width+50)+"x"+str(img1.height*.15)
		else:
			if img1.height < 200:
				size_here=size_here=str(img1.width+40)+"x"+str(img1.height*.2)
			else:
				size_here=str(img1.width+40)+"x"+str(img1.height*.1)
		speech2=str(uuid.uuid4())
		print("Creating new uuid for speech2 "+str(speech2))
		#cmd = ["convert", "speechbubble.png","-resize", size_here+"!", "/tmp/"+speech2+".png"] # Get command created to create a new image matching the aspect ratio
		#fconvert = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		#stdout, stderr = fconvert.communicate()
		if type_of_bubble == "Large/Black" and reverse:
			subprocess.call("convert testspeech2.png -flop -resize "+size_here+"!"+" /tmp/"+speech2+".png",shell=True)
		elif type_of_bubble == "Small/White" and reverse:
			subprocess.call("convert speechbubble2.png -flop -resize "+size_here+"!"+" /tmp/"+speech2+".png",shell=True)
		# elif type_of_bubble == "Grey" and reverse:
		# 	subprocess.call("convert discordspeechbubble.png -flop -resize "+size_here+"!"+" /tmp/"+speech2+".png",shell=True)
		elif type_of_bubble == "Large/Black" and not reverse:
			subprocess.call("convert testspeech2.png -resize "+size_here+"!"+" /tmp/"+speech2+".png",shell=True)
		# elif type_of_bubble == "Grey" and not reverse:
		# 	subprocess.call("convert discordspeechbubble.png -resize "+size_here+"!"+" /tmp/"+speech2+".png",shell=True)
		else:
			subprocess.call("convert speechbubble2.png -resize "+size_here+"!"+" /tmp/"+speech2+".png",shell=True)
		#   convert drawn.png mask_shape.png -compose DstOut -composite drawn_bite3.png
		r4=str(uuid.uuid4())
		img1.save("/tmp/"+r4+".png")
		if color:
			img2 = Image.open(r"/tmp/"+speech2+".png").convert("RGBA")
			img1.paste(img2, (0,0), mask = img2)
			r3=str(uuid.uuid4())
			img1.save("/tmp/"+r3+".png")
			subprocess.call("convert /tmp/"+r3+".png /tmp/babytoad3"+r3+".gif",shell=True) #Convert the image to a gif so it can be saved on discord
		else:
			r3=str(uuid.uuid4())
			subprocess.call("convert /tmp/"+r4+".png /tmp/"+speech2+".png -compose DstOut -composite /tmp/final.png",shell=True)
			subprocess.call("convert /tmp/final.png /tmp/babytoad3"+r3+".gif",shell=True) #Convert the image to a gif so it can be saved on discord

		# img2 = Image.open(r"/tmp/"+speech2+".png").convert("RGBA")
		# img1.paste(img2, (0,0), mask = img2)
		# r3=str(uuid.uuid4())
		# img1.save("/tmp/"+r3+".png")
		await interaction.response.defer() # Defer the response
		# subprocess.call("convert /tmp/final.png /tmp/babytoad3"+r3+".gif",shell=True) #Convert the image to a gif so it can be saved on discord
		await interaction.followup.send("Working on it!") #Respond so we can avoid a timeout
		await asyncio.sleep(2.5) #Give a wait time 
		await interaction.edit_original_response(content = "", attachments=[discord.File("/tmp/babytoad3"+r3+".gif")]) #Send file
	except Exception as e:
		print("Error: "+str(e))

@tree.command(description="Remove a player from a group!",guild=discord.Object(id=1114399245068406787))
async def remove_player(interaction: discord.Interaction, player: str, clan: str, options: Literal["KOS", "Alliance", "Friendly"]): 
	if options=="KOS":
		ans=await remove_from_file("kos.txt", player, clan)
		if ans:
			embed=discord.Embed(title="Error!", description="No such player exists with that clan name in this group", color=0xFF0000)
		else:
			channel = client.get_channel(1130059224353874010) # Get KOS channel name
			messages = [message async for message in channel.history(limit=1,oldest_first=True)][0] # Grab most old message (the KOS list)
			msg = await channel.fetch_message(messages.id) # get the prior KOS list id
			embed=discord.Embed(title="Success!", description="Player successfully removed from KOS!", color=0x00FF00)
			data = await read_file("kos.txt") # Add the new player to KOS and then read the file, which we make into an embed
			embed2=discord.Embed(title="KOS List", description=data, color=0x00FF00)
			await msg.edit(embed=embed2, content="")
		await interaction.response.send_message(embed=embed)
	elif options=="Alliance":
		ans=await remove_from_file("alliances.txt", player, clan)
		if ans:
			embed=discord.Embed(title="Error!", description="No such player exists with that clan name in this group", color=0xFF0000)
		else:
			embed=discord.Embed(title="Success!", description="Player successfully removed from Alliance!", color=0x00FF00)
		await interaction.response.send_message(embed=embed)
	elif options=="Friendly":
		ans=await remove_from_file("friendly.txt", player, clan)
		if ans:
			embed=discord.Embed(title="Error!", description="No such player exists with that clan name in this group", color=FF0000)
		else:
			embed=discord.Embed(title="Success!", description="Player successfully removed from Friendlies!", color=0x00FF00)
		await interaction.response.send_message(embed=embed)
	else:
		embed=discord.Embed(title="Error", description="Error, something went wrong. Make sure all categories are filled!", color=0xFF0000)
		await interaction.channel.send_message(embed=embed)


async def check_dup(filename, player, clan):
	with open(filename, "r") as f:
		data=str(f.read())
		f.close()

	tocheck=str(str(player)+": "+str(clan)+"\n")
	if tocheck in data:
		return True

@tree.command(description="Add a player to a group!",guild=discord.Object(id=1114399245068406787))
async def add_player(interaction: discord.Interaction, player: str, clan: str, options: Literal["KOS", "Alliance", "Friendly"]):	
	if options=="KOS":
		ans=await check_dup("kos.txt", player, clan)
		if ans:
			embed=discord.Embed(title="Error!", description="Player with that clan already exists in this group", color=0xFF0000)
		else:
			channel = client.get_channel(1130059224353874010) # Get KOS channel name
			messages = [message async for message in channel.history(limit=1,oldest_first=True)][0] # Grab most old message (the KOS list)
			msg = await channel.fetch_message(messages.id) # get the prior KOS list id
			await add_to_file("kos.txt", player, clan)
			data = await read_file("kos.txt") # Add the new player to KOS and then read the file, which we make into an embed
			embed2=discord.Embed(title="KOS List", description=data, color=0x00FF00)
			await msg.edit(embed=embed2, content="")
			embed=discord.Embed(title="Success!", description="Player "+player+" successfully added to KOS!", color=0x00FF00)
		await interaction.response.send_message(embed=embed)
	elif options=="Alliance":
		ans=await check_dup("alliances.txt", player, clan)
		if ans:
			embed=discord.Embed(title="Error!", description="Player with that clan already exists in this group", color=0xFF0000)
		else:
			await add_to_file("alliances.txt", player, clan)
			embed=discord.Embed(title="Success!", description="Player "+player+" successfully added to Alliance!", color=0x00FF00)
		await interaction.response.send_message(embed=embed)
	elif options=="Friendly":
		ans=await check_dup("friendly.txt", player, clan)
		if ans:
			embed=discord.Embed(title="Error!", description="Player with that clan already exists in this group", color=0xFF0000)

		else:
			await add_to_file("friendly.txt", player, clan)
			embed=discord.Embed(title="Success!", description="Player "+player+" successfully added to Friendlies!", color=0x00FF00)
		await interaction.response.send_message(embed=embed)
	else:
		embed=discord.Embed(title="Error", description="Error, something went wrong. Make sure all categories are filled!", color=0xFF0000)
		await interaction.response.send_message(embed=embed)


@tree.command(description="Grab all the data from a group",guild=discord.Object(id=1114399245068406787))
async def get(interaction: discord.Interaction, options: Literal["KOS", "Alliance", "Friendly"]):
	if options=="KOS":
		embed=discord.Embed(title="Here are all our Kill On Sights", color=0x00FF00)
		with open("kos.txt", "r") as f:
			data=f.read()
			f.close()
		embed.add_field(name="Player name: Clan name", value=data)
		await interaction.response.send_message(embed=embed)
	elif options=="Alliance":
		embed=discord.Embed(title="Here are all our Alliances", color=0x00FF00)
		with open("alliances.txt", "r") as f:
			data=f.read()
			f.close()
		embed.add_field(name="Player name: Clan name", value=data)
		await interaction.response.send_message(embed=embed)
	elif options=="Friendly":
		embed=discord.Embed(title="Here are all our Friendlys", color=0x00FF00)
		with open("friendly.txt", "r") as f:
			data=f.read()
			f.close()
		embed.add_field(name="Player name: Clan name", value=data)
		await interaction.response.send_message(embed=embed)

client.run("Token")
