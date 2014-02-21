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
			newnodelist.append(NodeCombiner(nodelist[(x * 2)], nodelist[(x * 2 + 1)]))
		
		if len(newnodelist) > 1:
			return self.GenTree(newnodelist)
		else:
			self.tree.append(newnodelist)
			self.roothash = newnodelist[0].hashdigest
			return self.roothash
	
	def RegenTree(self):
		self.tree = []
		return self.GenTree(self.nodelist)
	
	def GetNodeInfo(self, index, pairlist=[], tree=None):
		if tree == None:
			tree = self.tree
		pairlist.append(tree[index].value, tree[index].hashdigest, index % 2)
		index = index / 2
		return self.GetNodeInfo(index, pairlist=pairlist, tree=tree[1:])
		
	def GenLookup(self):
		index = 0
		for x in self.nodelist:
			self.lookup[x.hashdigest] = index
			index += 1
	

def ValidateNode(value, hashdigest, roothash, pairlist):
	for x in pairlist:
		# If this was an even node, put the paired node on the right, otherwise it goes on the left.
		if x[2]:
			value, hashdigest = x[0] + value, sha256(str(x[0] + value) + x[1] + hashdigest)
		else:
			value, hashdigest = x[0] + value, sha256(str(x[0] + value) + hashdigest + x[1])
	
	return hashdigest == roothash




