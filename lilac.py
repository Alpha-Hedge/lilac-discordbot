# IMPORTS
print('lilac.py: Importing time...')
print('Module 1/5')
import time
print('RUN DATE: '+time.strftime("%m/%d/%Y")+' '+time.strftime("%H:%M"))
print('lilac.py: Importing random...')
print('Module 2/5')
import random
print('lilac.py: Importing asyncio...')
print('Module 3/5')
import asyncio
print('lilac.py: Importing discord...')
print('Module 4/5')
import discord
print('lilac.py: Importing threading...')
print('Module 5/5')
import threading
from discord.ext import commands
print('lilac.py: Importing db.py...')
import db
print('lilac.py: Getting client token...')
from CONF_bot import token

client = discord.Client()

bot_pref = '&&'
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
	'<:SpottedOrange:342831895257808908>', 
	'<:SpottedRed:342831895140237312>', 
	'<:SpottedGreen:342831896574558208>', 
	'<:SpottedGreen:342831896574558208>', 
	'<:SpottedBlue:342831896725815296>', 
	'<:SpottedIndigo:342832174455586828>', 
	'<:SpottedYellow:342831895978967040>', 
	'<:SpottedPurple:342832217271173121>'
]

help_info = {
	bot_pref+'help': bot_pref+'help [category] [command]\nGets a help topic on [command] in [category].',
	bot_pref+'categories': bot_pref+'categories\nLists the current command categories.',
	bot_pref+'version': bot_pref+'version\nGets the current version of Lilac (this bot).',
	bot_pref+'developer': bot_pref+'developer\nGets the name of the Lilac (this bot) developer',
	bot_pref+'commands': bot_pref+'commands [category]\nGets a list of commands in [category].'
}

help_testing = {
	bot_pref+'bugreport': bot_pref+'bugreport [message]\nSends a message to the developer.',
	bot_pref+'hello': bot_pref+'hello\nSimple test command.'
}

help_database = {
	bot_pref+'score_add': bot_pref+'score_add [user] [amount]\nAdds [amount] of points to [user].',
	bot_pref+'score_del': bot_pref+'score_del [user] [amount]\nRemoves [amount] of points from [user].',
	bot_pref+'score_get': bot_pref+'score_get [user]\nGets the current score of [user].',
	bot_pref+'score_reset': bot_pref+'score_reset [user]\nResets the score of [user] to 0. **Use with caution.**'
}

def create_role_dict():
	global role_dict
	role_dict = {}
	for i in client.get_server('342825738350886913').roles:
		role_dict[i.name] = i

	print('Roles:')
	print(role_dict)

def create_emoji_dict():
	global emoji_dict
	emoji_dict = {}
	for i in client.get_server('342825738350886913').emojis:
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

def qCheck(li):
	for i in range(len(li)):
		if li[i].startswith('"'):
			join_start = i
		if li[i].endswith('"'):
			join_end = i
		i+=1

	joined = []
	for i in range(join_start, (join_end)+1):
		joined.append(li[i])

	return ' '.join(joined).replace('"','')

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
	# AUTO-SCOREKEEPER
	def dateloop():
		while True:
			if getDate() == db.scrkeep_date_get():
				for i in member_list:
					print(i)
					scrk_user = i
					if role_dict['scorekeeper'] in i.roles:
						client.remove_roles(client.get_member_named(scrk_user),role_dict['scorekeeper'])
				
				print('Choosing scorekeeper...')
				u = member_list[random.randrange(0,len(member_list))]
				client.add_roles(client.get_member_named(u),role_dict['scorekeeper'])
				db.scrkeep_date_set_next()

	thread = threading.Thread(target=dateloop)
	thread.start()


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
	if role_dict['lilac owner/developer'] in message.author.roles:
		pass

	# Category: Roles
	if message.content.startswith(bot_pref+'color'):
		role = discord.utils.get(message.server.roles, name='[col] blue')
		print(role)
		msg_split = (message.content.split())
		if message.content.endswith('--list'):
			embed=discord.Embed(title="Color Role List", description="All self-assignable color roles.", color=0xff00ff)
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

		# elif message.content.endswith('--changeto'):
		# 	col = msg_split[1]
		# 	print('LINE 130 log:: col')
		# 	print(col)
		# 	print('LINE 133 log:: role_dict[col]')
		# 	print(role_dict[col])
		# 	print(role_dict['colpink'])
		# 	discord.Client.add_roles(message.author, role_dict[col])
		# 	print(message.author.roles)
		# 	for i in message.author.roles:
		# 		print(i)
		# 		if i.name.startswith('[col]'):
		# 			# A (FAILED)
		# 			# client.remove_roles(message.author, role_dict[i])
		# 			# print(role_dict[i])						
		# 			# B (FAILED)
		# 			client.remove_roles(message.author, role_dict[str(i)])
		# 			print(role_dict[str(i)])
		# 			# C (FAILED)
		# 			# client.remove_roles(message.author, i)
		# 			# print('LINE 147 log:: i')
		# 			print(i)

	# Category: Database Handling
	if message.content.startswith(bot_pref+'score_add'):
		msg_split = message.content.split()
		if len(msg_split) > 2:
			if role_dict['scorekeeper'] in message.author.roles:
				u = qCheck(msg_split)

				pscr = db.score_get(u)

				db.score_add(u, findInt(msg_split))

				cscr = db.score_get(u)

				embed=discord.Embed(title="Score Changed", description=u+"\'s score has been updated.", color=0xff00ff)
				embed.set_author(name="Lilac", icon_url='https://images.discordapp.net/avatars/346529910212526090/9e87ca1be76d6ab16f43615d362ef740.png?size=1024')
				embed.add_field(name="Previous value:", value=str(pscr), inline=False)
				embed.add_field(name="Current value:", value=str(cscr), inline=False)
				yield from client.send_message(message.channel,embed=embed)

			elif role_dict['scorekeeper'] not in message.author.roles:
				yield from client.send_message(message.channel, 'You don\'t have the scorekeeper role.')

	if message.content.startswith(bot_pref+'score_del'):
		msg_split = message.content.split()
		if len(msg_split) > 2:
			if role_dict['scorekeeper'] in message.author.roles:
				u = qCheck(msg_split)

				pscr = db.score_get(u)

				db.score_del(u, findInt(msg_split))

				cscr = db.score_get(u)

				embed=discord.Embed(title="Score Changed", description=u+"\'s score has been updated.", color=0xff00ff)
				embed.set_author(name="Lilac", icon_url='https://images.discordapp.net/avatars/346529910212526090/9e87ca1be76d6ab16f43615d362ef740.png?size=1024')
				embed.add_field(name="Previous value:", value=str(pscr), inline=False)
				embed.add_field(name="Current value:", value=str(cscr), inline=False)
				yield from client.send_message(message.channel,embed=embed)

			elif role_dict['scorekeeper'] not in message.author.roles:
				yield from client.send_message(message.channel, 'You don\'t have the scorekeeper role.')

	if message.content.startswith(bot_pref+'score_get'):
		msg_split = message.content.split()
		if msg_split[1] == '--all':
			if message.content.endswith('--raw'):
				yield from client.send_message(message.channel, db.score_get_all_string())
			else:
				yield from client.send_message(message.channel, embed=db.score_get_all_embed())

		if len(msg_split) > 1:
			u = qCheck(msg_split)
			yield from client.send_message(message.channel, db.score_get(u))

	# if (message.content.startswith(bot_pref+'score_get_all')) or (message.content.startswith(bot_pref+'scoreboard')):
	# 	msg_split = message.content.split()
	# 	if message.content.endswith('--embed'):
	# 		yield from client.send_message(message.channel, embed=db.score_get_all_embed())
	# 	else:
	# 		yield from client.send_message(message.channel, db.score_get_all_string())

	if message.content.startswith('&:score_get_all_raw'):
		scr_RAW = db.score_get_all_raw()
		print(scr_RAW)

	if message.content.startswith(bot_pref+'score_reset'):
		msg_split = message.content.split()
		u = qCheck(msg_split)

		yield from client.send_message(message.channel, 'Are you sure you want to reset '+u+'\'s score? [Yes/No]')
		msg = yield from client.wait_for_message(author=message.author, content='Yes')
		db.score_reset(u)
		yield from client.send_message(message.channel, u+'\'s score has been reset to 0.')

	# if message.channel == "spotted-doggos":
	# 	if message.content.startswith('https://cdn.discordapp.com/attachments/'):
	# 		db.last_dog_update_url(message.content)

	if message.content.startswith(bot_pref+'latest_doggo_get_URL'):
		yield from client.send_message(message.channel, db.last_dog_get_url())

	if message.content.startswith(bot_pref+'latest_doggo_update_URL'):
		msg_split = message.content.split()
		URL = qCheck(msg_split)
		db.last_dog_update_url(URL)

		yield from client.send_message(message.channel, db.last_dog_get_url())


	if message.content.startswith(bot_pref+'register_user'):
		msg_split = message.content.split()
		u = qCheck(msg_split)
		db.user_register(u)
		yield from client.send_message(message.channel, u+' has been added into the scoreboard database.')

	# Category: Misc
	if message.content in spottedEmojis:
		yield from client.send_message(message.channel, role_dict['scorekeeper'].mention)
		yield from client.send_message(message.channel, 'A new spotted doggo!')

	if message.content.startswith(bot_pref+'mod-application'):
		yield from client.send_message(message.channel, 'Please visit this link: https://goo.gl/forms/EhFTThutYoL6wfxQ2\nModerator applications are open 24/7, unless specified by staff.')

	# Category: Misc; Sub-Category: Jokes/Memes
	# Category: Misc; Sub-Category: Jokes/Memes; Sub-Category: Videos
	if message.content.startswith('&&video'):
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
	if message.content.startswith('&&image'):
		if message.content.endswith('praisebagman'):
			yield from client.send_message(message.channel, 'https://cdn.discordapp.com/attachments/342835715236954115/346359947908612096/bagmanHOLY.png')
		if message.content.endswith('wheezd'):
			yield from client.send_message(message.channel, 'https://cdn.discordapp.com/attachments/301185018057719809/353962163515162625/youvebeenwheezd.png')

	if message.content.startswith('i would like to purchase bamboozle insurance'):
		yield from client.send_message(message.channel, 'https://i.redd.it/e8rf2wd4zvxy.png')

	# Category: Info
	if message.content.startswith(bot_pref+'commands'):
		msg_split = message.content.split()
		if msg_split[1] == 'info':
			yield from client.send_message(message.channel, cmnds_info)

		if msg_split[1] == 'database':
			yield from client.send_message(message.channel, 'Database commands can only be used by someone with the scorekeeper role.')
			yield from client.send_message(message.channel, cmnds_database)

		if msg_split[1] == 'testing':
			yield from client.send_message(message.channel, cmnds_testing)

	if message.content.startswith(bot_pref+'categories'):
		yield from client.send_message(message.channel, categories)

	if message.content.startswith(bot_pref+'help'):
		msg_split = message.content.split()
		if msg_split[1] == 'info':
			yield from client.send_message(message.channel, help_info[msg_split[2]])

		if msg_split[1] == 'database':
			yield from client.send_message(message.channel, help_database[msg_split[2]])

		if msg_split[1] == 'testing':
			yield from client.send_message(message.channel, help_testing[msg_split[2]])

		else:
			yield from client.send_message(message.channel, 'No help entry for this command yet.')

	if message.content.startswith(bot_pref+'info'):
		if message.content.endswith('--version'):
			yield from client.send_message(message.channel, 'Current version: Lilac v'+bot_version)

		elif message.content.endswith('--developer'):
			yield from client.send_message(message.channel, 'This bot is developed by Alphys Hedge.')

	# Category: Testing / Troubleshooting
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

	if message.content.startswith(bot_pref+'bugreport'):
		msg_split = message.content.split()
		rmsg = qCheck(msg_split)

		yield from client.send_message(developer, str(message.author)+' has sent a bug report: '+rmsg)
		yield from client.send_message(message.channel, 'Your bug report has been sent to the developer.')

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

client.run(token)