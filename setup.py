#!/usr/bin/env python
from setuptools import setup
def main():

	setup(
		name='filewalker',
		version='0.1',
		description='walk and log a file hierarchy',
		packages=['filewalker'],
		author='meh',	
	)

if __name__ == '__main__':
	main()