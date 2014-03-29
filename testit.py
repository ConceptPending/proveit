from proveit import *
import random
import string

NONCE_BITS=128
NYBBLE_BITS=4
HEX_DIGITS="0123456789abcdef"

def RandomWord(alphabet, n):
	r = random.SystemRandom()
	return ''.join([r.choice(list(alphabet)) for i in range(n)])

def RandomNode():
	uid = RandomWord(string.ascii_lowercase, 8)
	nsum = random.uniform(0, 1000)
	nonce = RandomWord(HEX_DIGITS, NONCE_BITS/NYBBLE_BITS)
	return uid, nsum, nonce

def RandomNodeList(n=20):
	nodelist = []
	for x in range(n):
		result = RandomNode()
		nodelist.append(Node(nsum=result[1], uid=result[0], nonce=result[2]))
	return nodelist

if __name__=='__main__':
	nodelist = RandomNodeList(n=40)
	total = 0

	print "Accounts:"
	for x in nodelist:
		total += x.sum
		print str(x)
	print "Expected total: {:f}".format(total)

	print
	h = HashTree(nodelist)
	print "Tree total:     {:f}".format(h.ReturnTotal())
	print "Tree root hash: " + str(h.roothash)

	for x in range(len(nodelist)):
		pairlist = h.GetNodePairList(x)
		included = ValidateNode(nodelist[x], pairlist[0], pairlist[1])
		print "Inclusion verified " + str(included) + " for node " + str(nodelist[x])
