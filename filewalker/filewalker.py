#!/usr/bin/env python
'''
#--filewalker.py--#

#--Recursively walk a file heirarchy while logging data and tracking depth--#

#--install filewalker:
	python setup.py install

#Usage:
#
#!/usr/bin/env python
import filewalker as fw
root='/Users/CountChocula'		#optional argument (default is current directory)
max_depth=None					#optional argument (accepts integers; default is None)
print_all=False					#optional; print files and messages (default is True)
files,dirs,ftree = fw.walk(root=root, max_depth=max_depth)

#--output is tuple of objects--#
#--files & dirs are node lists; ftree is a node tree--#

#Usage:
#
for f in files:
	print f.name, f.rel, f.abs, f.size		#rel=relative, abs=absolute paths; dirs node list is structurally identical


Optional arguments:
	root: root directory as absolute path (defaults to current dir)
	max_depth: maximum depth to descend in hierarchy (default is None)
		e.g., max_depth=0 scans only root (or curr dir if no root specified)
	print_all: show files as they are scanned and print messages

Output (tuple):
	all_file_list, all_dir_list, f_tree

File (file) and directory (dir) objects (which are collected in their respective lists)
are instantiated with name, relative path (to 'root'), and absolute path. 

#Interactive Usage:

$ python
>>> import filewalker
>>> filewalker.walk()
'''

import subprocess as sp
import os
import sys

#------class declarations------#

class file_tree():
	def __init__(self,root):
		self.root=root

class file():
	def __init__(self,name,rel,abs,size):
		self.name=name
		self.rel=rel
		self.abs=abs
		self.size=size

class dir():
	def __init__(self,name,rel,abs):
		self.name=name
		self.rel=rel
		self.abs=abs
		self.children=[]


#------general functions------#

def exit():
	if print_all:
		print; print 'Exiting...'; print
	sys.exit()

def get_root(kwargs):
	root = sp.Popen(['pwd'],stdout=sp.PIPE).communicate()[0].replace('\n','')
	if 'root' in kwargs.keys():
		root = kwargs['root']
		if not os.path.exists(root):
			if print_all:
				print 'not a viable path'
			exit()
	return root

def get_max_depth(kwargs):
	max_depth = None
	if 'max_depth' in kwargs.keys() and kwargs['max_depth'] is not None:
		max_depth = kwargs['max_depth']
		try:
			max_depth = int(max_depth)
		except:
			if print_all:
				print 'invalid depth'
			exit()
		if max_depth < 0:
			max_depth = 0
	return max_depth


#------walk functions------#

def walk(**kwargs):
	'''  accept keyword arguments 'root', 'max_depth' and 'print_all' '''
	
	print_all = True
	if 'print_all' in kwargs.keys():
		print_all = kwargs['print_all']
		
	if print_all:
		print '#--------------------------------#'
		print '#-------- filewalker.py ---------#'
		print '#--------------------------------#'
	
	#---initialize some things---#
	curr_depth = 0
	all_file_list = []
	all_dir_list = []
	curr_node_list = []
	
	root = get_root(kwargs)
	max_depth = get_max_depth(kwargs)
	
	new_node = dir(
		name	= root.split('/')[-1],
		rel		= '',
		abs		= root
	)
	
	f_tree = file_tree(new_node)
	curr_node_list.append(new_node)	
	
	if print_all:
		print 'Scanning:',root
		print root.split('/')[-1]
	
	def do_walk(curr_depth, curr_node_list):
		
		this_dir_path = curr_node_list[-1].abs
		
		cmd = 'ls \'' + str(this_dir_path)+'\''
		folder_contents = [x for x in sp.Popen([cmd],stdout=sp.PIPE,shell=True).communicate()[0].split('\n') if x]
		
		if not folder_contents:
			curr_node_list.pop()
			return curr_depth - 1, curr_node_list
		
		file_size_sum = 0
		
		for this_node in folder_contents:
			
			this_node_path = os.path.abspath(os.path.join(this_dir_path,this_node))
			
			this_node_rel_path = this_node_path[len(root)+1:]	#convert to rel path
				
			if not os.path.isdir(this_node_path):		
				'''node is file'''
				
				new_node = file(
					name	= this_node,
					rel		= this_node_rel_path,
					abs		= this_node_path,
					size	= os.path.getsize(this_node_path)
				)
				all_file_list.append(new_node)
		
				curr_node_list[-1].children.append(new_node)
				
				if print_all: 
					print ' |'+curr_depth*'-'+this_node+' -> ('+str(all_file_list[-1].size)+' bytes)'
			
			else:									
				'''node is dir'''
							
				new_node = dir(
					name	= this_node,
					rel		= this_node_rel_path,
					abs		= this_node_path
				)
				all_dir_list.append(new_node)
				
				curr_node_list[-1].children.append(new_node)
				if print_all: 
					print ' |'+curr_depth*'---'+this_node	
				
				if max_depth is None or curr_depth < max_depth:
					'''recurse through directories'''
					curr_depth+=1
					curr_node_list.append(new_node)
					curr_depth, curr_node_list = do_walk(curr_depth, curr_node_list)					
				else:
				
					return curr_depth -1, curr_node_list
		else:	#contents of folder explored
			pass	
			
					
		return curr_depth - 1, curr_node_list
	
	curr_depth, curr_node_list = do_walk(curr_depth, curr_node_list)
	
	#---output from filewalker
	return all_file_list, all_dir_list, f_tree
	#-------------------------


def main():
	
	pass
if __name__ == '__main__':
	main()