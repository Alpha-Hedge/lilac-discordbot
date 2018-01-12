# IMPORTS
print('lilac.py: Importing time...')
import time
print('Done. 1/8')
print('RUN DATE: '+time.strftime("%m/%d/%Y")+' '+time.strftime("%H:%M"))
print('lilac.py: Importing random...')
import random
print('Done. 2/8')
print('lilac.py: Importing asyncio...')
import asyncio
print('Done. 3/8')
print('lilac.py: Importing discord...')
import discord
print('Done. 4/8')
print('lilac.py: Importing threading...')
import threading
print('Done. 5/8')
from discord.ext import commands
print('lilac.py: Importing db.py...')
import db
print('Done. 6/8')
print('lilac.py: Getting client token...')
from CONF_bot import token
print('Done. 7/8')
print('lilac.py: Getting server ID...')
from CONF_servid import servid
print('Done. 8/8')

client = discord.Client()

bot_pref = '+'
bot_version = '1.1.0'

def getDate():
	return time.strftime("%m/%d/%Y")

def getTime():
	return time.strftime("%H:%M")

cmnds_info = [bot_pref+'commands', bot_pref+'help', bot_pref+'version', bot_pref+'developer']
cmnds_testing = [bot_pref+'bugreport', bot_pref+'hello', bot_pref+'args']
cmnds_database = [bot_pref+'score_add', bot_pref+'score_del', bot_pref+'score_get', bot_pref+'score_reset', bot_pref+'latest_doggo_update_URL', bot_pref+'latest_doggo_get_URL']

categories = ['info', 'testing', 'database']

spottedEmojis = [
	'<:SpottedOrange:%s>' % (int(servid)), 
	'<:SpottedRed:%s>' % (int(servid)), 
	'<:SpottedGreen:%s>' % (int(servid)), 
	'<:SpottedGreen:%s>' % (int(servid)), 
	'<:SpottedBlue:%s>' % (int(servid)), 
	'<:SpottedIndigo:%s>' % (int(servid)), 
	'<:SpottedYellow:%s>' % (int(servid)), 
	'<:SpottedPurple:%s>' % (int(servid))
]

def create_role_dict():
	global role_dict
	role_dict = {}
	for i in client.get_server(servid).roles:
		role_dict[i.name] = i

	print('Roles:')
	print(role_dict)


def create_emoji_dict():
	global emoji_dict
	emoji_dict = {}
	for i in client.get_server(servid).emojis:
		emoji_dict[i.name] = i

	print('Emojis:')
	print(emoji_dict)


def create_member_list():
	global member_list
	member_list = []
	for i in client.get_all_members():
		member_list.append(i)
		print(i)


def get_role(server_roles, target_name):
	for each in server_roles:
		if each.name == target_name:
			return each
	return None


def findInt(li):
	for i in range(len(li)):
		try:
			return int(li[i])
			break
		except ValueError:
			pass


@asyncio.coroutine 
def background_loop(): 
	yield from client.wait_until_ready()
	while not client.is_closed:
		channel = client.get_channel("************")
		messages = ["Hello!", "How are you doing?", "Testing!!"]
		yield from client.send_message(channel, random.choice(messages))
		yield from asyncio.sleep(120)


@client.event
@asyncio.coroutine
def on_ready():
	print('Logged in as')
	print(client.user)
	create_role_dict()
	create_emoji_dict()
	create_member_list()
	print(member_list)
	print('START TIMESTAMP: '+getDate()+' '+getTime())


@client.event
@asyncio.coroutine
def on_message(message):
	developer = message.server.get_member_named('Alphys Hedge#1031')
	# comment this out to toggle logging
	# print(message.content)

	# So the bot won't respond to itself
	if message.author == client.user:
		return

	# DEV-ONLY COMMANDS
	# These commands can only be used by someone with the 'lilac developer' role; in the case of debugging or beta commands/features
	# if role_dict['lilac developer'] in message.author.roles:
	# 	pass

	# Category: Roles
	if message.content.startswith(bot_pref+'color'):
		role = discord.utils.get(message.server.roles, name='[col] blue')
		print(role)
		msg_split = (message.content.split())
		if message.content.endswith('--list'):
			embed=discord.Embed(title="Color Role List", description="All color roles.", color=0xff00ff)
			embed.set_author(name="Lilac", icon_url='https://images.discordapp.net/avatars/346529910212526090/9e87ca1be76d6ab16f43615d362ef740.png?size=1024')
			for i in role_dict:
				if i.startswith('col.'):
					print(i)
					r = str(role_dict[i].color.r)
					g = str(role_dict[i].color.g)
					b = str(role_dict[i].color.b)
					col = [r, g, b]
					embed.add_field(name=i, value='rgb'+str(col), inline=False)

			yield from client.send_message(message.channel, embed=embed)

	# Category: Database Handling
	if message.content.startswith(bot_pref+'scoreAdd'):
		msg_split = message.content.split()
		if len(msg_split) > 2:
			if role_dict['scorekeeper'] in message.author.roles:
				u = msg_split[1]

				if message.content.endswith('-u'):
					u = u.replace('_',' ')

				if db.check_for_user(u):
					pscr = db.score_get(u)

					db.score_add(u, msg_split[2])

					cscr = db.score_get(u)

					embed=discord.Embed(title="Score Changed", description=u+"\'s score has been updated.", color=0xff00ff)
					embed.set_author(name="Lilac", icon_url='https://images.discordapp.net/avatars/346529910212526090/9e87ca1be76d6ab16f43615d362ef740.png?size=1024')
					embed.add_field(name="Previous value:", value=str(pscr), inline=False)
					embed.add_field(name="Current value:", value=str(cscr), inline=False)
					yield from client.send_message(message.channel,embed=embed)

				elif db.check_for_user(u) == False:
					if db.check_for_alias(u)[0] == True:
						u = db.check_for_alias(u)[1]
						pscr = db.score_get(u)

						db.score_add(u, msg_split[2])

						cscr = db.score_get(u)

						embed=discord.Embed(title="Score Changed", description=u+"\'s score has been updated.", color=0xff00ff)
						embed.set_author(name="Lilac", icon_url='https://images.discordapp.net/avatars/346529910212526090/9e87ca1be76d6ab16f43615d362ef740.png?size=1024')
						embed.add_field(name="Previous value:", value=str(pscr), inline=False)
						embed.add_field(name="Current value:", value=str(cscr), inline=False)
						yield from client.send_message(message.channel,embed=embed)

				else:
					yield from client.send_message(message.channel,"The user '"+u+"' is not in the database. Use `&&user_register` to add them.")

			elif role_dict['scorekeeper'] not in message.author.roles:
				yield from client.send_message(message.channel, 'You don\'t have the scorekeeper role.')

	if message.content.startswith(bot_pref+'scoreDel'):
		msg_split = message.content.split()
		if len(msg_split) > 2:
			if role_dict['scorekeeper'] in message.author.roles:
				u = msg_split[1]

				if message.content.endswith('-u'):
					u = u.replace('_',' ')

				if db.check_for_user(u):
					pscr = db.score_get(u)

					db.score_del(u, msg_split[2])

					cscr = db.score_get(u)

					embed=discord.Embed(title="Score Changed", description=u+"\'s score has been updated.", color=0xff00ff)
					embed.set_author(name="Lilac", icon_url='https://images.discordapp.net/avatars/346529910212526090/9e87ca1be76d6ab16f43615d362ef740.png?size=1024')
					embed.add_field(name="Previous value:", value=str(pscr), inline=False)
					embed.add_field(name="Current value:", value=str(cscr), inline=False)
					yield from client.send_message(message.channel,embed=embed)
					
				elif db.check_for_user(u) == False:
					if db.check_for_alias(u)[0] == True:
						u = db.check_for_alias(u)[1]
						pscr = db.score_get(u)

						db.score_del(u, msg_split[2])

						cscr = db.score_get(u)

						embed=discord.Embed(title="Score Changed", description=u+"\'s score has been updated.", color=0xff00ff)
						embed.set_author(name="Lilac", icon_url='https://images.discordapp.net/avatars/346529910212526090/9e87ca1be76d6ab16f43615d362ef740.png?size=1024')
						embed.add_field(name="Previous value:", value=str(pscr), inline=False)
						embed.add_field(name="Current value:", value=str(cscr), inline=False)
						yield from client.send_message(message.channel,embed=embed)

				else:
					yield from client.send_message(message.channel,"The user '"+u+"' is not in the database. Use &&registerUser to add them.")

			elif role_dict['scorekeeper'] not in message.author.roles:
				yield from client.send_message(message.channel, 'You don\'t have the scorekeeper role.')

	if message.content.startswith(bot_pref+'scoreGet'):
		msg_split = message.content.split()
		if message.content.endswith('--all'):
			yield from client.send_message(message.channel, embed=db.score_get_all_embed())
		else:
			u = msg_split[1]
			if message.content.endswith('-u'):
					u = u.replace('_',' ')

			if db.check_for_user(u):
				yield from client.send_message(message.channel, db.score_get(u))

			elif db.check_for_user(u) == False:
				if db.check_for_alias(u)[0] == True:
					u = db.check_for_alias(u)[1]
					yield from client.send_message(message.channel, db.score_get(u))

			else:
				yield from client.send_message(message.channel, 'That user could not be found. Names are case-sensitive, maybe you used the wrong capitalization?')

	if message.content.startswith(bot_pref+'registerUser'):
		msg_split = message.content.split()
		u = msg_split[1]
		if message.content.endswith('-u'):
			u = u.replace('_',' ')
			db.user_register(u)
		else:
			db.user_register(u)

		yield from client.send_message(message.channel, u+' has been added into the scoreboard database.')

	# Aliasing
	if message.content.startswith(bot_pref+'aliasAdd'):
		msg_split = message.content.split()
		u = msg_split[1]
		a = msg_split[2]
		if message.content.endswith('-u'):
			u = u.replace('_',' ')
			a = a.replace('_',' ')

		db.user_alias_add(u,a)
		yield from client.send_message(message.channel, 'The alias "'+a+'" was created for the user "'+u+'". Try `+scoreGet '+a+'` to confirm.')

	if message.content.startswith(bot_pref+'aliasRemove'):
		msg_split = message.content.split()
		a = msg_split[1]
		if message.content.endswith('-u'):
			a = a.replace('_',' ')

		db.user_alias_remove(a)
		yield from client.send_message(message.channel, 'The alias "'+a+'" was removed.')

	# Category: Misc
	if message.content in spottedEmojis:
		yield from client.send_message(message.channel, role_dict['scorekeeper'].mention)
		yield from client.send_message(message.channel, 'A new spotted doggo!')

	if message.content.startswith(bot_pref+'modForm'):
		yield from client.send_message(message.channel, 'Please visit this link: https://goo.gl/forms/EhFTThutYoL6wfxQ2\nModerator applications are open 24/7, unless specified by staff.')

	# Misc Math Functions
	if message.content.startswith(bot_pref+'math.FtoP'):
		msg_split = message.content.split()
		f = msg_split[1].split('/')
		p = int(f[0]) / int(f[1])
		p*=100
		yield from client.send_message(message.channel, msg_split[1] + ' is equal to ' + str(p) + '%')

	if message.content.startswith(bot_pref+'math.FtoD'):
		msg_split = message.content.split()
		f = msg_split[1].split('/')
		d = int(f[0]) / int(f[1])
		yield from client.send_message(message.channel, msg_split[1] + ' is equal to ' + str(d))

	# Category: Misc; Sub-Category: Jokes/Memes
	# Category: Misc; Sub-Category: Jokes/Memes; Sub-Category: Videos
	if message.content.startswith('+video'):
		if message.content.endswith('ascend'):
			yield from client.send_message(message.channel, 'https://www.youtube.com/watch?v=vGyHXW0lwZY')
		if message.content.endswith('inthewoods'):
			yield from client.send_message(message.channel, 'https://www.youtube.com/watch?v=E3Pv4c4Qz9w')
		if message.content.endswith('masterpiece'):
			yield from client.send_message(message.channel, 'https://www.youtube.com/watch?v=NhBktFVTjf8')
		if message.content.endswith('knifetentacle'):
			yield from client.send_message(message.channel, 'https://www.youtube.com/watch?v=qwqP95Am2mA')
		if message.content.endswith('smoothgamecube'):
			yield from client.send_message(message.channel, 'https://www.youtube.com/watch?v=VlmDPC6ai4Y')
		if message.content.endswith('itiswednesday'):
			yield from client.send_message(message.channel, 'https://www.youtube.com/watch?v=du-TY1GUFGk')
		if message.content.endswith('dabonem'):
			yield from client.send_message(message.channel, 'https://www.youtube.com/watch?v=PVHxztbT71o')
	
	# Category: Misc; Sub-Category: Jokes/Memes; Sub-Category: Images
	if message.content.startswith('+image'):
		if message.content.endswith('praisebagman'):
			yield from client.send_message(message.channel, 'https://cdn.discordapp.com/attachments/342835715236954115/346359947908612096/bagmanHOLY.png')
		if message.content.endswith('wheezd'):
			yield from client.send_message(message.channel, 'https://cdn.discordapp.com/attachments/301185018057719809/353962163515162625/youvebeenwheezd.png')

	if message.content.startswith('i would like to purchase bamboozle insurance'):
		yield from client.send_message(message.channel, 'https://i.redd.it/e8rf2wd4zvxy.png')

	if message.content.startswith(bot_pref+'EMBED'):
		embed=discord.Embed(title="Embed Test!", description="This is a test command for the embed object feature.", color=0xff00ff)
		embed.set_author(name="Lilac", icon_url='https://images.discordapp.net/avatars/346529910212526090/9e87ca1be76d6ab16f43615d362ef740.png?size=1024')
		embed.add_field(name="Field No. 1", value="Value of Field No. 1", inline=True)
		embed.add_field(name="Field No. 2", value="Value of Field No. 2", inline=True)
		embed.add_field(name="Field No. 3", value="Value of Field No. 3", inline=True)
		embed.add_field(name="Field No. 4", value="etc", inline=False)
		embed.add_field(name="Field No. 5", value="etc", inline=False)
		embed.add_field(name="Field No. 6", value="etc", inline=False)
		embed.set_footer(text="Footer text!")
		yield from client.send_message(message.channel, embed=embed)

	if message.content.startswith(bot_pref+'role-list'):
		print(message.author.roles)

	if message.content.startswith(bot_pref+'hello'):
		yield from client.send_message(message.channel, 'Hi! :D')

	if message.content.startswith(bot_pref+'args'):
		msg_split = message.content.split()
		if len(msg_split) > 1:
			if msg_split[1] == 'valid':
				yield from client.send_message(message.channel, 'Valid second argument.')
			else:
				yield from client.send_message(message.channel, 'Invalid second argument.')
		else:
			yield from client.send_message(message.channel, 'No arguments specified.')

	# Category: Help commands
	if message.content.startswith(bot_pref+'help') or message.content.startswith('readme'):
		yield from client.send_message(message.channel, 'Please read the README file on GitHub: https://github.com/Alpha-Hedge/lilac-discordbot/blob/master/README.md')

client.run(token)