print('db.py: Importing datetime...')
import datetime
print('db.py: Importing time...')
import time
print('db.py: Importing pyrebase...')
import pyrebase
print('db.py: Importing discord...')
import discord
print('db.py: Getting config from fbconf.py...')
from CONF_fb import config

firebase = pyrebase.initialize_app(config)

fdb = firebase.database()

def user_ref_get():
	# Gets the root of the firebase database and returns it as a dictionary
	return dict(fdb.child('users').get().val())

def scrkeep_date_get():
	return fdb.child('scorekeeper_info').child('date').get().val()

def scrkeep_date_set_next():
	x = time.strftime("%m/%d/%Y")
	x = datetime.datetime.strptime(x, "%m/%d/%Y")
	x = (x+datetime.timedelta(days=7))
	x = x.strftime("%m/%d/%Y")
	fdb.child('scorekeeper_info').set({'date':x})

def check_for_user(user):
	if user in user_ref_get():
		return True
	else:
		return False


# score_*
def score_get(user):
	return fdb.child('users').child(user).child('points').get().val()

def score_add(user,value):
	print(user)
	print(value)
	cval = score_get(user)
	fdb.child('users').child(user).update({'points': cval+int(value)})

def score_del(user,value):
	print(user)
	print(value)
	cval = score_get(user)
	fdb.child('users').child(user).update({'points': cval-int(value)})

def score_reset(user):
	fdb.child('users').child(user).update({'points': 0})

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
	fdb.child('users').update({user: {'alias':'','points': 0}})

# def user_clone(user,new_user):
# 	fdb.child('users').update({new_user: user})

# def user_name_change(name_prev,name_new):
# 	print(name_prev)
# 	user_clone(name_prev,name_new)
# 	fdb.child('users').child(name_prev).remove()
# 	print(name_new)