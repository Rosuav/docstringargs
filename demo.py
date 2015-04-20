"""DocstringArgs demo"""
from docstringargs import cmdline

@cmdline
def hello(where="world"):
	"""Say hello to somewhere

	where: Where to say hello to
	"""
	print("Hello, %s!"%where)

@cmdline
def count(top, step="1"):
	"""Count from 1, human style

	top: Number to count up to
	--step: Increment to count by
	"""
	for i in range(1, int(top)+1, int(step)):
		print(i)

cmdline.main()
