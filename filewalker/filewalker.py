#!/usr/bin/env python
'''
filewalker.py

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
	>>> import filewalker
	>>> filewalker.walk()
	
	>>> files, dirs, ftree = filewalker.walk()
	>>> ftree
	<filewalker.filewalker.file_tree instance at 0x10cf74c20>
	>>> dir(ftree.root)
	['__doc__', '__init__', '__module__', 'abs', 'children', 'depth', 'fsize', 'name', 'parent', 'rel', 'size', 'type']
	
'''

import subprocess as sp
import os
import sys
import operator

#--------------------------#
#--- class declarations ---#
#--------------------------#

class file_tree():
	def __init__(self,root):
		self.root=root

class file():
	def __init__(self, name, rel, abs, size, parent, depth):
		self.name	= name
		self.rel	= rel
		self.abs	= abs
		self.size	= size
		self.parent	= parent
		self.depth	= depth
		self.type	= 'f'
		self.fsize	= format_size(size)
		self.fsize0	= self.fsize.split(' ')[0]
		self.fsize1 = self.fsize.split(' ')[1]

class dir():
	def __init__(self, name, rel, abs, size, parent, depth):
		self.name		= name
		self.rel		= rel
		self.abs		= abs
		self.children	= []
		self.size 		= size
		self.parent		= parent
		self.depth		= depth
		self.type		= 'd'
		self.fsize		= '0 B'
		self.fsize0 	= self.fsize.split(' ')[0]
		self.fsize1 	= self.fsize.split(' ')[1]


#-------------------------#
#---- misc. functions ----#
#-------------------------#

def exit():
	print; print 'Exiting...'; print
	sys.exit()


def ps(msg):
	''' print messages if print_all == True '''
	if print_all:
		print msg


def get_root(**kwargs):
	'''confirm valid path for **kwarg 'root'; if unspecified, use root = cwd '''
	
	root = kwargs.get('root')
	if not root:
		root = sp.Popen(['pwd'],stdout=sp.PIPE).communicate()[0].replace('\n','')
	else:
		if not os.path.exists(root):
			ps('not a viable path')
			exit()
	return os.path.abspath(root)


def get_max_depth(**kwargs):
	max_depth = None
	if 'max_depth' in kwargs.keys() and kwargs['max_depth'] is not None:
		max_depth = kwargs['max_depth']
		try:
			max_depth = int(max_depth)
		except:
			ps('invalid depth')
			exit()
		if max_depth < 0:
			max_depth = 0
	return max_depth


def format_size(num):
	''' Return formatted file size of input num as string; e.g., 14156348 --> 14.1 MB'''
	rnum = str(int(num))[::-1]
	slist = zip( [rnum[x:x+3][::-1] for x in range(0,len(rnum), 3) ] , 'B KB MB GB TB'.split(' ') )
	size = slist[-1][0]
	if len(slist) > 1:
		size += '.' + slist[-2][0][0]
	return '%s %s' % (size, slist[-1][1])


#------------------------#
#------ FILEWALKER ------#
#------------------------#
def walk(**kwargs):
	'''accept **kwargs: 
		'root'			(default: current dir)
		'max_depth' 	(default: None [i.e., traverse entire tree]; accepts integers)
		'print_all' 	(default: True; print all messages to stdout)
	
	Recursively walk a file hierarchy, depth-first. 
	Each file/dir encountered becomes a node added to the file_tree, 
		and appended to the respective `files` list or `dirs` list
	All nodes are accessible from successive `children` lists starting at the root node. 
	
	'''		
	print_all = False if kwargs.get('print_all') == False else True
	global print_all

	ps('#--------------------------------#\n#-------- filewalker.py ---------#\n#--------------------------------#')
	
	#----------------------------#
	#---initialize some things---#
	#----------------------------#
	curr_depth = 0
	all_file_list = []
	all_dir_list = []
	curr_node_list = []
	
	
	root = get_root(**kwargs)
	max_depth = get_max_depth(**kwargs)
	
	new_node = dir(			#make root node
		name	= root.split('/')[-1],
		rel		= '',
		abs		= root,
		size	= 0,
		parent 	= '',
		depth	= -1
	)
	
	f_tree = file_tree(new_node)
	curr_node_list.append(new_node)	
	
	ps('Scanning: %s' % root)
	ps('|'+root.split('/')[-1]+'        (root dir)')
	
	#----------------------------#
	#------ begin recursion -----#
	#----------------------------#
	
	def do_walk(curr_depth, curr_node_list):
		
		this_dir_path = curr_node_list[-1].abs
		
		cmd = 'ls %s' % str(this_dir_path)
		folder_contents = [x for x in sp.Popen([cmd],stdout=sp.PIPE,shell=True).communicate()[0].split('\n') if x]
		
		if not folder_contents:
			curr_node_list.pop()
			return curr_depth - 1, curr_node_list
		
		file_size_sum = 0
		
		for this_node in folder_contents:
			
			this_node_path = os.path.abspath(os.path.join(this_dir_path,this_node))
			
			this_node_rel_path = this_node_path[len(root)+1:]	#convert to rel path
				
			if not os.path.isdir(this_node_path):		
				#------------------------#
				#----- node is file -----#
				#------------------------#
				
				size = os.path.getsize(this_node_path)
				
				new_node = file(
					name	= this_node,
					rel		= this_node_rel_path,
					abs		= this_node_path,
					size	= size,
					parent 	= curr_node_list[-1],
					depth 	= curr_depth
				)
				all_file_list.append(new_node)
		
				curr_node_list[-1].children.append(new_node)
				
				msg = ' '*curr_depth+'|'+this_node
				ps( msg + (30-len(msg))*' '+ ' f_ (%s)'    % new_node.fsize  )
				
				file_size_sum += size
				
			else:									
				#------------------------#
				#----- node is dir ------#
				#------------------------#
							
				new_node = dir(
					name	= this_node,
					rel		= this_node_rel_path,
					abs		= this_node_path,
					size	= 0,
					parent	= curr_node_list[-1],
					depth 	= curr_depth
				)
				all_dir_list.append(new_node)
				
				curr_node_list[-1].children.append(new_node)
				
				ps(msg = ' |'+curr_depth*'-'+this_node)	
				ps(msg+(30-len(msg))*' '+'_d')
				
				if max_depth is None or curr_depth < max_depth:
					'''recurse through directories'''
					curr_depth+=1
					curr_node_list.append(new_node)
					curr_depth, curr_node_list = do_walk(curr_depth, curr_node_list)					
				else:
				
					return curr_depth -1, curr_node_list
		else:	
			'''contents of folder explored; calculate size of total contents'''
			contents_size = 0
			for child in curr_node_list[-1].children:
				contents_size += child.size
			curr_node_list[-1].size = contents_size
			fsize = format_size(contents_size)
			curr_node_list[-1].fsize = fsize
			curr_node_list[-1].fsize0 = fsize.split(' ')[0]
			curr_node_list[-1].fsize1 = fsize.split(' ')[1]
			curr_node_list.pop()
		
		return curr_depth - 1, curr_node_list
	curr_depth, curr_node_list = do_walk(curr_depth, curr_node_list)
	
	
	
	if print_all:
		print
		print 'File tree with contents sizes:'
		print '------------------------------'
		print f_tree.root.name + '     (root)'
		def post_walk(node):
			for child in node.children:
				#phrase = '|' + '-'*child.depth + child.name
				phrase = ' '*child.depth + '|' + child.name
				print phrase,(26-len(phrase))*' ','|'+'('+child.type+')',child.fsize0 + ' '*(6 - len(child.fsize0))+child.fsize1

				if child.type == 'd':
					post_walk(child)
		
		post_walk(f_tree.root)
	
	
	#----------- print largest dirs and files -------------#
	#---------------------------------------------#
	#
	print '#----- Largest dirs: -----#'
	large_dirs = [(x.rel,x.size) for x in sorted(all_dir_list,key=operator.attrgetter('size'))[::-1]][:10]
	for d in large_dirs:
		print d[0]
		mod_size = str(d[1])[::-1]
		print '  ', ','.join( mod_size[x:x+3] for x in range(0,len(mod_size),3) )[::-1],'b'
	print '#-------------------------#'
	
	print
	
	print '#----- Largest files: -----#'
	large_files = [(x.rel,x.size) for x in sorted(all_file_list,key=operator.attrgetter('size'))[::-1]][:10]
	for f in large_files:
		print f[0]
		mod_size = str(f[1])[::-1]
		print '  ', ','.join( mod_size[x:x+3] for x in range(0,len(mod_size),3) )[::-1],'b'
	print '#-------------------------#'
	
	print 'Total directories: %d' 	% len( all_dir_list )
	print 'Total files: %d' 		% len( all_file_list ) 
	
	tfs =  sum([ x.size for x in all_file_list ])
	fsize = format_size(tfs)
	
	print 'Total file(s) size: %s' % fsize
	
	#
	#---------------------------------------------#
	#----------- print largest dirs and files -------------#
	
	
	#--- output from filewalker	---#
	return all_file_list, all_dir_list, f_tree
	#------------------------------#


def main():
	pass
if __name__ == '__main__':
	main()