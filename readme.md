<h4>filewalker</h4>

<h5>filewalker.py</h5>

Depth-first filesystem traversal and logging

filewalker.py returns tuple of objects: 
	files 	(node list)
	dirs 	(node list)
	ftree 	(node tree)


Installation:
 
	python setup.py install


Usage:

	#!/usr/bin/env python
	import filewalker as fw
	
	root='/Users/CountChocula'		#optional kwarg (default is current directory)
	max_depth=None					#optional kwarg (accepts integers; default is None; max_depth=0 scans only root)
	print_all=False					#optional kwarg; print files and messages (default is True)

	files, dirs, ftree = fw.walk( root=root, max_depth=max_depth, print_all=print_all )


Use the returned data (output as tuple): 

	for f in files:								#files is list of file nodes (in order of assessment)
		print f.name, f.rel, f.abs, f.size		#rel=relative path, abs=absolute path
		
	for d in dirs:								#dirs is list of dir nodes
		print d.name, d.rel, d.abs, d.size


Interactive Usage:

	$ python
	>>> import filewalker as fw
	>>> fw.walk()
	
	>>> files, dirs, ftree = fw.walk()
	>>> ftree
	<filewalker.filewalker.file_tree instance at 0x10cf74c20>
	>>> dir(ftree.root)
	['__doc__', '__init__', '__module__', 'abs', 'children', 'depth', 'fsize', 'name', 'parent', 'rel', 'size', 'type']`