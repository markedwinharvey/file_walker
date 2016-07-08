#!/usr/bin/env python
'''
#--file_walker.py--#

#--Recursively walk a file heirarchy while logging data and tracking depth--#

#Usage:
#
#!/usr/bin/env python
import file_walker as fw
root='/Users/CountChocula'		#optional argument (default is current directory)
max_depth=None					#optional argument (accepts integers; default is None)
files,dirs,ftree = fw.walk(root=root, max_depth=max_depth)

#--output is tuple of objects--#
#--files & dirs are node lists; ftree is a node tree--#

#Usage:
#
for f in files:
	print f.name, f.rel, f.abs		#rel=relative, abs=absolute paths; dirs node list is structurally identical


Optional arguments:
	root: root directory as absolute path (defaults to current dir)
	max_depth: maximum depth to descend in hierarchy (default is None)
		e.g., max_depth=0 scans only root (or curr dir if no root specified)

Output (tuple):
	all_file_list, all_dir_list, f_tree

File (file) and directory (dir) objects (which are collected in their respective lists)
are instantiated with name, relative path (to 'root'), and absolute path. 

#Interactive Usage:

$ python
>>> import file_walker
>>> file_walker.walk()
'''

import subprocess as sp
import os
import sys

def walk(**kwargs):
	'''  accept keyword arguments 'root' and 'max_depth'  '''
	print '#--------------------------------#'
	print '#-------- file_walker.py --------#'
	print '#--------------------------------#'
	
	def exit():
		print; print 'Exiting...'; print
		sys.exit()
	
	class file_tree():
		def __init__(self,root):
			self.root=root
	
	class node():
		def __init__(self, path, parent, is_dir, is_root):
			self.path=path
			self.parent=parent
			self.is_dir=is_dir
			self.is_root=is_root
			self.children=[]
	
	class file():
		def __init__(self,name,rel,abs):
			self.name=name
			self.rel=rel
			self.abs=abs
	
	class dir():
		def __init__(self,name,rel,abs):
			self.name=name
			self.rel=rel
			self.abs=abs
			
	#initialize some things
	curr_depth = 0
	all_file_list = []
	all_dir_list = []
	curr_node_list = []
	
	#initialize root and depth
	root = sp.Popen(['pwd'],stdout=sp.PIPE).communicate()[0].replace('\n','')
	max_depth = None
	
	if 'root' in kwargs.keys():
		root = kwargs['root']
		if not os.path.exists(root):
			print 'not a viable path'
			exit()
			
	if 'max_depth' in kwargs.keys() and kwargs['max_depth'] is not None:
		max_depth = kwargs['max_depth']
		try:
			max_depth = int(max_depth)
		except:
			print 'invalid depth'
			exit()
		if max_depth < 0:
			max_depth = 0
	
	new_node = node(path=root, parent=None, is_dir=True, is_root=True)
	f_tree = file_tree(new_node)

	curr_node_list.append(new_node)
	
	def do_walk(curr_depth, curr_node_list):
		this_dir_path = curr_node_list[-1].path
		
		cmd = 'ls \'' + str(this_dir_path)+'\''
		folder_contents = [x for x in sp.Popen([cmd],stdout=sp.PIPE,shell=True).communicate()[0].split('\n') if x]
		
		if not folder_contents:
			curr_node_list.pop()
			return curr_depth - 1, curr_node_list
			
		
		for this_node in folder_contents:
			print curr_depth*'---'+this_node
			this_node_path = os.path.abspath(os.path.join(this_dir_path,this_node))
			
			#convert to rel path
			this_node_rel_path = this_node_path[len(root)+1:]
				
			if not os.path.isdir(this_node_path):		
				#node is file
				all_file_list.append( 
					file(
						name=this_node,
						rel=this_node_rel_path,
						abs=this_node_path
					)
				)
				new_node = node(
					path=this_node_path, 
					parent=curr_node_list[-1], 
					is_dir=False, 
					is_root=False
				)					
				curr_node_list[-1].children.append(new_node)

			else:									
				#node is dir
				all_dir_list.append(
					dir(
						name=this_node,
						rel=this_node_rel_path,
						abs=this_node_path
					)
				)
				new_node = node(
					path=this_node_path, 
					parent=curr_node_list[-1], 
					is_dir=True, 
					is_root=False
				)
				curr_node_list[-1].children.append(new_node)
				
				if max_depth is None or curr_depth < max_depth:
					#recurse through directories
					curr_depth+=1
					curr_node_list.append(new_node)
					curr_depth, curr_node_list = do_walk(curr_depth, curr_node_list)					
				else:
					return curr_depth -1, curr_node_list

		return curr_depth - 1, curr_node_list
	
	curr_depth, curr_node_list = do_walk(curr_depth, curr_node_list)
	
	#---output from file_walker
	return all_file_list, all_dir_list, f_tree
	#-------------------------


def main():
	
	pass
if __name__ == '__main__':
	main()