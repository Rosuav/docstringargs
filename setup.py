from setuptools import setup
setup(
	name="docstringargs",
	version="0.1.1",
	description="Argparse builder using function docstrings",
	long_description=open("README").read(),
	url="https://github.com/Rosuav/docstringargs",
	author="Chris Angelico",
	author_email="rosuav@gmail.com",
	license="MIT",
	classifiers=[
		"Development Status :: 3 - Alpha",
		"Intended Audience :: Developers",
		"Topic :: Software Development :: Libraries",
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python :: 2",
		"Programming Language :: Python :: 2.7",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.4",
	],
	keywords="argparse",
	py_modules=["docstringargs"],
)
