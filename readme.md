<h4>file_walker.py</h4>

Recursively walk a file hierarchy, logging data and tracking depth. 

Installation: 

`python setup.py install`


Usage:

`#!/usr/bin/env python`


`import file_walker as fw`
`root='/Users/CountChocula'	`	#optional arg (default is current directory)

`max_depth=None`				#optional arg (default is None; accepts integers)

`files,dirs,ftree = fw.walk(root=root, max_depth=max_depth)`

		or simply
		
`fw.walk()`

Files and directories are printed to stdout as they are assessed, showing current depth. 

To extract file or dir data:

`for f in files:`

`	print f.name, f.rel, f.abs`		#filename, relative path, absolute path
