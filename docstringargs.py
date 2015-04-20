import argparse

class DocstringArgs(object):
	"""Configure argparse based on function docstrings

	Basic usage:
	from docstringargs import cmdline
	@cmdline
	def subcommand():
		'''Subcommand description goes here'''
	cmdline.main()

	Similar in purpose to docopt, but instead of handling all a program's
	arguments in one place, it handles each subcommand as that function's
	docstring.
	"""
	def __init__(self, desc, defaults=None):
		self.parser = argparse.ArgumentParser(description=desc)
		self.subparsers = self.parser.add_subparsers(dest="command", help="Available commands")
		self.defaults = defaults or {}
		self.handlers = {}

	def __call__(self, f):
		"""Decorator to make a function available via the command line

		The docstring is parsed to construct argparse configs. The function's
		name becomes a subparser keyword; the first docstring line is the
		description. After that, each line should describe one argument:
		a parameter name, followed by a colon, and then its description.

		If the parameter name is prefixed with "--", it becomes an option,
		otherwise it is a positional arg. If it is followed by "=True",
		it becomes a store_true flag (usually best with options rather than
		positionals); followed by "=" and anything else, it gains a default
		value. Parameter defaults can also be provided by the function's
		default arguments, in which case it is the bool value False (rather
		than the string "True") which triggers store_true. Note that this
		appears backward; the default is what happens if the argument is
		NOT provided. TODO: Should the string form change to match this?

		Any argument named in self.defaults will have their defaults set
		automatically.

		Arguments annotated with strings will also be handled by argparse,
		using the annotation as the description (and any function default
		as per the defaults given above).
		"""
		doc = f.__doc__.split("\n") # Require a docstring
		p = self.subparsers.add_parser(f.__name__, help=doc[0])
		c = f.__code__
		defs = self.defaults.copy()
		if f.__defaults__:
			# Is there a better way to do this? I want to take the first argcount names,
			# and match off the tail of those against the function defaults.
			for arg, deflt in zip(c.co_varnames[:c.co_argcount][-len(f.__defaults__):], f.__defaults__):
				defs[arg] = deflt
		try: defs.update(f.__kwdefaults__ or ())
		except AttributeError: pass # Python 2 doesn't have keyword-only args
		try: ann = f.__annotations__
		except AttributeError: ann = {} # Python 2 doesn't have annotations, so assume they weren't used.
		for name, desc in list(ann.items()):
			if isinstance(desc, str):
				# Hack: Stick it into the list, so we don't have to run the loop twice.
				doc.append(name+": "+desc)
				ann.pop(name) # Assume we'll be using it, and remove the annotation.
		# Note that defaults are not significant - explanatory text is. That comes from
		# the docstring.
		for arg in doc[1:]:
			arg = arg.strip().split(":", 1)
			if len(arg) < 2: continue # Blank lines etc
			name = arg[0].strip()
			opts = {}
			clean_name = name.replace("-","")
			if clean_name in defs:
				opts["default"] = defs.pop(clean_name)
			elif "=" in name:
				name, opts["default"] = name.split("=", 1)
				# "arg=True" means store_true rather than an
				# actual default value of "True".
				if opts["default"]=="True": opts["default"] = False
			if "default" in opts:
				if name[0]!="-": opts["nargs"]="?"
				if opts["default"] is False:
					del opts["default"]
					opts["action"]="store_true"
			p.add_argument(name, help=arg[1].strip(), **opts)
		# Squirrel away the function itself for main() to use
		self.handlers[f.__name__] = f
		return f

	def parse_args(self):
		"""Parse args and return a dictionary (more useful than a namespace)"""
		return self.parser.parse_args().__dict__

	def main(self):
		"""Parse arguments and call a function based on the chosen subcommand"""
		arguments = self.parse_args()
		return self.handlers[arguments.pop("command")](**arguments)

# Convenience: Just import cmdline and it'll DTRT in simple cases.
import sys
if "__main__" in sys.modules:
	# Note that we don't "import __main__" here, for several reasons.
	# If there isn't anything there, we just quietly skip creating cmdline.
	# Likewise if it has no docstring; if you want to use the shorthand,
	# make sure there is a useful docstring (at least a one-liner).
	docstring = sys.modules["__main__"].__doc__
	if docstring:
		cmdline = DocstringArgs(desc=docstring.split("\n", 1)[0])
	del docstring # Don't pollute dir()
del sys # Don't pollute dir(), again
