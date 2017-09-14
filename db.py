print('db.py: Importing pyrebase...')
import pyrebase
print('db.py: Importing discord...')
import discord
print('db.py: Getting config from fbconf.py...')
from CONF_fb import config

firebase = pyrebase.initialize_app(config)

fdb = firebase.database()

def root_get():
	# Gets the root of the firebase database and returns it as a dictionary
	return dict(fdb.child('users').get().val())

# score_*
def score_get(user):
	return fdb.child('users').child(user).child('points').get().val()

def score_add(user,value):
	cval = score_get(user)
	fdb.child('users').child(user).set({'points': cval+value})

def score_del(user,value):
	cval = score_get(user)
	fdb.child('users').child(user).set({'points': cval-value})

def score_reset(user):
	fdb.child('users').child(user).set({'points': 0})

def score_get_all_string():
	x = fdb.child('users').get().val()
	# Change from OrderedDict to standard dict
	x = dict(x)
	y = []
	for i in x:
		y.append(str(i)+' '+str(x[i]))

	return '\n'.join(y)

def score_get_all_embed():
	x = fdb.child('users').get().val()
	x = dict(x)
	embed=discord.Embed(title="Scoreboard", description="Current scores of all users.", color=0xff00ff)
	embed.set_author(name="Lilac", icon_url='https://images.discordapp.net/avatars/346529910212526090/9e87ca1be76d6ab16f43615d362ef740.png?size=1024')
	for i in x:
		embed.add_field(name=i, value=str(x[i]['points']), inline=True)

	return embed

def score_get_all_raw():
	x = fdb.child('users').get().val()
	# Change from OrderedDict to standard dict
	x = dict(x)
	print(x)
	return x

# misc
def last_dog_get_url():
	return fdb.child('last_dog').get().val()

def last_dog_update_url(url):
	fdb.child('last_dog').set(url)
	return last_dog_get_url()

# user_*
def user_register(user):
	fdb.child('users').update({user: {'points': 0}})