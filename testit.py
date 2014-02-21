from proveit import *
import os, random
from hashlib import sha256

def RandomNode():
	value = random.uniform(0, 1000)
	hashdigest = sha256(os.urandom(32)).hexdigest()
	return value, hashdigest

def RandomNodeList(n=20):
	nodelist = []
	for x in range(n):
		result = RandomNode()
		nodelist.append(Node(result[0], result[1]))
	return nodelist


if __name__=='__main__':
	nodelist = RandomNodeList(n=2)
	h = HashTree(nodelist)
	info = h.GetNodeInfo(1)
	pairlist = h.GetNodePairList(1)
	print info
	print ValidateNode(Node(info[0], info[1]), pairlist[0], pairlist[1])
