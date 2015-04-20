"""Annotation-based docstringargs demo"""
from docstringargs import cmdline

@cmdline
def init():
	"""Initialize everything"""
	print("Initializing... done.")

@cmdline
def adduser(user: "Name of user to add", password: "Password for the new user"=""):
	"""Add a new user"""
	if not password: password = input("Enter the user's password: ")
	print("Adding a new user named %s" % user)

@cmdline
def spam(count: "How much spam to eat"="3", user=None, password=None):
	# There's currently no way to create optional arguments using annotations.
	"""Eat some spam

	--user: User to purchase spam as, otherwise anonymously
	--password: Password (ignored if user not specified)
	"""
	if user:
		if not password: password = input("Enter the user's password: ")
		# We don't save users anywhere, so clearly they got the wrong password :)
		print("User name and password do not match.")
		return
	count = int(count)
	if count > 5: print("We don't have that much spam.")
	elif count < 1: print("This is Python. We eat spam here.")
	else: print("Spam" + ", spam"*(count-1) + "!")

cmdline.main()
