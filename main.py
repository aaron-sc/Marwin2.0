import discord
import json
import asyncio
from discord.ext.commands import Bot
import aiohttp
from discord.utils import get
import json
# from settings import bots
import pyjokes
from discord.ext import commands
#from admin import *
import random
from badwords import arrBad


intents = discord.Intents.all()
TOKEN = open("token.txt").readlines()[0].strip()
prefix = "~"
bot = Bot(command_prefix=prefix, description="Ready to serve!", intents=intents)
options = {0 : "off", 1 : "on"}

def roll_many_six_dice(times):
	toreturn = "Rolling a six sided die " + str(times) + " times! \n \n"
	total = 0
	for t in range(0, times):
		num = str(random.randint(1,6))
		toreturn += ("Roll " + str(t+1) + ": I rolled a {0}\n".format(num))
		total += int(num)
	toreturn += "Total of all rolls: " + str(total)
	return toreturn

bot.remove_command('help')

def get_data():
	with open('settings.json') as settings:
		settings_data = json.load(settings)
	return dict(settings_data)

# Runs when the bot is activated
@bot.event
async def on_ready():
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('------')
	print(discord.utils.oauth_url(bot.user.id))
	
def check_if_valid_user_at(user):
	return "@!" in user

def check_if_valid_role(role):
	return "@&" in role

def get_role_id(role):
	toreturn = role.replace("<","").replace(">", "").replace("@","").replace("&","")
	return str(toreturn)

def get_user_id(user):
	toreturn = user.replace("<","").replace(">", "").replace("@","").replace("!","")
	return str(toreturn)


#Scans every message
@bot.event 
async def on_message(message):
	content = message.content.strip().lower()
	settings_data, guild_id = get_data(), str(message.author.guild.id)
	badwordfilter = settings_data[guild_id]["badwords"]
	if(badwordfilter):
		for word in content.split():
			if word in arrBad and str(message.author.display_name) != "Marwin":
				await message.delete()
				await message.author.send('Hey {0}! That word isn\'t allowed on this server!'.format(message.author.mention))
	await bot.process_commands(message)

@bot.event
async def on_guild_join(guild):
	settings_data, guild_id = get_data(), str(guild.id)
	settings_data[guild_id] = {"bots" : 0, "title" : 1, "badwords" : 0, "accept_role" : ""}
	data = settings_data
	with open('settings.json', 'w') as json_file:
  		json.dump(data, json_file)


@bot.event
async def on_member_join(member):
	settings_data, guild_id = get_data(), str(member.guild.id)
	title = settings_data[guild_id]['title']
	if(title):
		members = 0
		for m in member.guild.members:
			members = m.guild.member_count
		members -= settings_data[guild_id]["bots"]
		await member.guild.edit(name = "The " + str(members) + " Dwarves")


@bot.event
async def on_member_remove(member):
	settings_data, guild_id = get_data(), str(member.guild.id)
	title = settings_data[guild_id]['title']
	if(title):
		members = 0
		for m in member.guild.members:
			members = m.guild.member_count
		members -= settings_data[guild_id]["bots"]
		await member.guild.edit(name = "The " + str(members) + " Dwarves")


@bot.command(pass_context=True)
async def ping(ctx):
	''' @pong! '''
	try:
		await ctx.send('{0} Pong!'.format(ctx.author.mention))
	except:
		await ctx.send('{0} An error occured, make sure you have given me the proper permissions!'.format(ctx.author.mention))


@bot.command(pass_context=True)
async def six_dice(ctx):
	''' roll a 6 sided die '''
	try:
		await ctx.send('{0} I rolled a {1}!'.format(ctx.author.mention, random.randint(1,6)))
	except:
		await ctx.send('{0} An error occured, make sure you have given me the proper permissions!'.format(ctx.author.mention))


@bot.command(pass_context=True)
async def m_six_dice(ctx, times : int):
	''' Roll many 6 sided die (max of 15) [~m_six_dice #ofdice]'''
	try:
		if(times <= 15):
			result = roll_many_six_dice(times)
			await ctx.send('{0} \n {1}'.format(ctx.author.mention, result))
		else:
			await ctx.send('{0} I can\'t roll {1} times!'.format(ctx.author.mention, times))
	except:
		await ctx.send('{0} An error occured, make sure you have given me the proper permissions!'.format(ctx.author.mention))


@bot.command(pass_context=True)
async def joke(ctx):
	''' Tells a random programmer joke '''
	try:
		await ctx.send('{0} {1}'.format(ctx.author.mention, pyjokes.get_joke()))
	except:
		await ctx.send('{0} An error occured, make sure you have given me the proper permissions!'.format(ctx.author.mention))


@bot.command(pass_context=True)
async def help(ctx):
	''' help '''
	try:
		await ctx.send('{0} \n Commands: https://docs.google.com/document/d/1Byoy80eZQE3TDe2pFB2SGLzSRuSgE7M1SamY_MOFci0/edit?usp=sharing'.format(ctx.author.mention))
	except:
		await ctx.send('{0} An error occured, make sure you have given me the proper permissions!'.format(ctx.author.mention))

@bot.command(pass_context=True)
async def get_server_id(ctx):
	''' Get's the server's ID! '''
	try:
		await ctx.send('{0}, {1}'.format(ctx.author.mention, ctx.message.guild.id))
	except:
		await ctx.send('{0} An error occured, make sure you have given me the proper permissions!'.format(ctx.author.mention))


@bot.command(pass_context=True)
async def simp(ctx, user):
	''' Simp for a user [~simp @user]'''
	try:
		if(check_if_valid_user_at(user)):
			await ctx.send('Hey {0} :wink: .... {1} is simping for you...'.format(user, ctx.author.mention))
	except:
		await ctx.send('{0} An error occured, make sure you have given me the proper permissions!'.format(ctx.author.mention))

@bot.command(pass_context=True)
async def members(ctx):
	''' Get members '''
	try:
		# include in every command
		settings_data, guild_id = get_data(), str(ctx.message.guild.id)
		# if(guild_id not in settings_data):
		# 	await ctx.send('{0} Please run the bot_command first!'.format(ctx.author.mention)+str(members)+" members")
		# else:
		members = 0
		for m in ctx.guild.members:
			members = m.guild.member_count
		members -= settings_data[guild_id]['bots']
		await ctx.send('{0} There are '.format(ctx.author.mention)+str(members)+" members")
	except:
		await ctx.send('{0} An error occured, make sure you have given me the proper permissions!'.format(ctx.author.mention))

@bot.command(pass_context=True)
async def accept_terms(ctx):
	''' Accept Server Terms '''
	settings_data, guild_id = get_data(), str(ctx.message.guild.id)
	user = ctx.message.author 
	role = int(settings_data[guild_id]["accept_role"])
	try:
		await user.add_roles(discord.utils.get(user.guild.roles, id=role))
		await ctx.send('{0} Thank you for accepting this server\'s terms!'.format(ctx.author.mention))
	except:
		await ctx.send('{0} An error occured, make sure you have given me the proper permissions!'.format(ctx.author.mention))


# Server Member Commands

@bot.command(pass_context=True)
@commands.has_any_role("Server Member")
async def follow(ctx, user):
	''' Follow a user [~follow @user - MUST BE A SERVER MEMBER]'''
	settings_data, guild_id = get_data(), str(ctx.message.guild.id)
	toFollow = get_user_id(user)
	author = ctx.message.author
	if(check_if_valid_user_at(user)):
		if(toFollow in settings_data[guild_id]["follower_roles"]):
			role = int(settings_data[guild_id]["follower_roles"][toFollow])
			try:
				await author.add_roles(discord.utils.get(author.guild.roles, id=role))
				await ctx.send('{0} You are now following that user!'.format(ctx.author.mention))
			except:
				await ctx.send('{0} An error occured, make sure you have given me the proper permissions!'.format(ctx.author.mention))
		else:
			await ctx.send('Hey {0} that\'s not a valid user! Either they\'re not a content creator, or they haven\'t set that up.'.format(ctx.author.mention))
	else:
		await ctx.send('Hey {0} that\'s not a valid user!.'.format(ctx.author.mention))


@bot.command(pass_context=True)
@commands.has_any_role("Server Member")
async def unfollow(ctx, user):
	''' Follow a user [~unfollow @user - MUST BE A CONTENT CREATOR]'''
	settings_data, guild_id = get_data(), str(ctx.message.guild.id)
	toFollow = get_user_id(user)
	author = ctx.message.author
	if(check_if_valid_user_at(user)):
		if(toFollow in settings_data[guild_id]["follower_roles"]):
			role = int(settings_data[guild_id]["follower_roles"][toFollow])
			try:
				await author.remove_roles(discord.utils.get(author.guild.roles, id=role))
				await ctx.send('{0} You are unfollowed that user!'.format(ctx.author.mention))
			except:
				await ctx.send('{0} An error occured, make sure you have given me the proper permissions!'.format(ctx.author.mention))
		else:
			await ctx.send('Hey {0} that\'s not a valid user! Either they\'re not a content creator, or they haven\'t set that up.'.format(ctx.author.mention))
	else:
		await ctx.send('Hey {0} that\'s not a valid user!.'.format(ctx.author.mention))

# BELOW ARE ADMIN COMMANDS

@bot.command(pass_context=True)
@commands.has_any_role("Tech Support", 713413177567739917) 
async def bad_word_filter(ctx, onoff : int):
	''' Turn on or off the bad word filter [1 = on, 0 = off] '''
	# include in every command
	global options
	try:
		settings_data, guild_id = get_data(), str(ctx.message.guild.id)
		if(onoff == 1 or onoff == 0):
			settings_data[guild_id] = {"badwords" : onoff}
			data = settings_data
			with open('settings.json', 'w') as json_file:
				json.dump(data, json_file)
			await ctx.send('{0} The bad word filter is turned {1} for this server!'.format(ctx.author.mention, options[onoff]))
		else:
			await ctx.send('{0} Not a valid option! [1 = on, 0 = off]'.format(ctx.author.mention))
	except:
		await ctx.send('{0} An error occured, make sure you have given me the proper permissions!'.format(ctx.author.mention))

@bot.command(pass_context=True)
@commands.has_any_role("Tech Support", 713413177567739917)
async def set_accept_role(ctx, role):
	''' Set what role users get when they accept the terms of service '''
	settings_data, guild_id = get_data(), str(ctx.message.guild.id)
	try:
		if(check_if_valid_role(role)):
			role = get_role_id(role)
			if(guild_id in settings_data):
				settings_data[guild_id]["accept_role"] = role
			else:
				settings_data[guild_id] = {"accept_role" : role}
			data = settings_data
			with open('settings.json', 'w') as json_file:
				json.dump(data, json_file)
			await ctx.send('{0} Configured the server to give that role when users accept the terms for the server!'.format(ctx.author.mention))
		else:
			await ctx.send('{0} Not a valid role!'.format(ctx.author.mention))
	except:
		await ctx.send('{0} An error occured, make sure you have given me the proper permissions!'.format(ctx.author.mention))


# Admin commands
# @bot.command(pass_context=True)
# @commands.has_role("Mod's")
# async def change_name(ctx):
# 	''' Change the server name! '''
# 	members = 0
# 	for m in ctx.guild.members:
# 		members = m.guild.member_count
# 	members -= bots[ctx.message.guild.id]
# 	await ctx.guild.edit(name = "The " + str(members) + " Dwarves")

@bot.command(pass_context=True)
@commands.has_any_role("Tech Support", 713413177567739917) 
async def bot_count(ctx, number : int):
	''' Update Your Server's Bot Count [~bot_count #ofbots] '''
	settings_data, guild_id = get_data(), str(ctx.message.guild.id)
	try:
		if(guild_id in settings_data):
			settings_data[guild_id]["bots"] = number
		else:
			settings_data[guild_id] = {"bots" : number}
		data = settings_data
		with open('settings.json', 'w') as json_file:
			json.dump(data, json_file)
		await ctx.send('{0} Configured the server to have {1} bots!'.format(ctx.author.mention, number))
	except:
		await ctx.send('{0} An error occured, make sure you have given me the proper permissions!'.format(ctx.author.mention))


# BELOW ARE CONTENT CREATOR COMMANDS

@bot.command(pass_context=True)
@commands.has_any_role("Content Creator") 
async def set_follow_role(ctx, role):
	''' Set what role users get if they follow you '''
	settings_data, guild_id = get_data(), str(ctx.message.guild.id)
	author_id = str(ctx.author.id)
	try:
		if(check_if_valid_role(role)):
			role = get_role_id(role)
			if(guild_id in settings_data and author_id in settings_data[guild_id]["follower_roles"]):
				settings_data[guild_id]["follower_roles"][author_id] = role
			else:
				settings_data[guild_id]["follower_roles"] = {author_id : role}
			data = settings_data
			with open('settings.json', 'w') as json_file:
				json.dump(data, json_file)
			await ctx.send('{0} Configured the server to give that role when users follow you!'.format(ctx.author.mention))
		else:
			await ctx.send('{0} Not a valid role!'.format(ctx.author.mention))
	except:
		await ctx.send('{0} An error occured, make sure you have given me the proper permissions!'.format(ctx.author.mention))

bot.run(TOKEN)
