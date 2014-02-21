from hashlib import sha256
import math

class Node():
	def __init__(self, value, hashdigest):
		self.value = value
		self.hashdigest = hashdigest
	
def NodeCombiner(left, right):
	newvalue = left.value + right.value
	lefthash, righthash = left.hashdigest, right.hashdigest
	hashdigest = sha256(str(newvalue) + lefthash + righthash).hexdigest()
	
	return Node(newvalue, hashdigest)

class HashTree():
	def __init__(self, nodelist):
		self.nodelist = nodelist
		self.roothash = ''
		self.tree = []
		self.GenTree(nodelist)
		self.lookup = {}
		self.GenLookup()
	
	def GenTree(self, nodelist):
		self.tree.append(nodelist)
		newnodelist = []
		
		if len(nodelist) % 2:
			nodelist.append(Node(0.0, sha256('0').hexdigest()))
		
		for x in range(int(math.ceil(len(nodelist)/2.0))):
			print nodelist[(x * 2)].value, nodelist[(x * 2)].hashdigest, nodelist[(x * 2 + 1)].value, nodelist[(x * 2 + 1)].hashdigest
			newnodelist.append(NodeCombiner(nodelist[(x * 2)], nodelist[(x * 2 + 1)]))
		
		if len(newnodelist) > 1:
			return self.GenTree(newnodelist)
		else:
			self.tree.append(newnodelist)
			self.roothash = newnodelist[0].hashdigest
			for x in self.tree[0]:
				print x.value, x.hashdigest
			return self.roothash
	
	def RegenTree(self):
		self.tree = []
		return self.GenTree(self.nodelist)
	
	def GetNodeInfo(self, index):
		return self.tree[0][index].value, self.tree[0][index].hashdigest
	
	def GetNodePairList(self, index, pairlist=[], tree=None):
		if tree == None:
			tree = self.tree
		elif len(tree) == 1:
			return self.roothash, pairlist
		pairlist.append((tree[0][index - 1 if index % 2 else 0].value, tree[0][index - 1 if index % 2 else 0].hashdigest, index % 2))
		index = index / 2
		return self.GetNodePairList(index, pairlist=pairlist, tree=tree[1:])
		
	def GenLookup(self):
		index = 0
		for x in self.nodelist:
			self.lookup[x.hashdigest] = index
			index += 1
	

def ValidateNode(node, roothash, pairlist):
	print pairlist
	print node.hashdigest, node.value
	for x in pairlist:
		# If this was an even node, put the paired node on the right, otherwise it goes on the left.
		if x[2]:
			node = NodeCombiner(Node(x[0], x[1]), node)
		else:
			node = NodeCombiner(node, Node(x[0], x[1]))
	print node.hashdigest, roothash
	return node.hashdigest == roothash




