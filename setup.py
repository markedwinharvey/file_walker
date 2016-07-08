#!/usr/bin/env python
from setuptools import setup
def main():

	setup(
		name='file_walker',
		version='0.1',
		description='walk and log a file hierarchy',
		packages=['file_walker'],
		author='meh',	
	)

if __name__ == '__main__':
	main()