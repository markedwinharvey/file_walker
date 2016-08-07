<h4>filewalker</h4>

<h5>filewalker.py</h5>

Recursively walk a file hierarchy, logging data and tracking depth. 

Installation: 

	python setup.py install


Usage:

	$ python
	>>> import filewalker as fw
	>>> fw.walk()
	
	>>> files,dirs,ftree = fw.walk()
	
	#optional arguments to fw.walk():
	
	root = '/Users/CountChocula'		# default is current directory
	max_depth = None					# default is None; accepts integers
	print_all = False					# default is True
	
	files, dirs, ftree = fw.walk(root=root, max_depth=max_depth, print_all=print_all)
	
File and directory data are displayed during tree-walking, showing depth (unless print_all == False). 
Directory sizes are computed recursively after the tree is generated; 
directory size is calculated as the total size of all files and folders within it. 

Further Usage: (following function return)

	for f in files:
		print f.name, f.size, f.rel, f.abs 	# filename, size (in bytes), relative path, absolute path
	
	for d in dirs:
		print d.name, d.size, d.rel, d.abs

	