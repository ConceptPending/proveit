from hashlib import sha256
import math
from decimal import Decimal
from bitcoinrpc import *
import time
import json

class Node():
	def __init__(self, nsum, **kwargs):
		self.sum = Decimal(str(nsum))
		if kwargs.keys() == ['nhash']:
			self.hash = kwargs['nhash']
		elif sorted(kwargs.keys()) == ['nonce', 'uid']:
			self.uid = kwargs['uid']
			self.nonce = kwargs['nonce']
			self.hash = sha256("{k[uid]}|{sum:f}|{k[nonce]}".format(sum=self.sum.normalize(), k=kwargs)).hexdigest()
		else:
			raise ValueError('must pass either:  nhash=...	or:  uid=..., nonce=... --- but got ' + str(kwargs))

	def __str__(self):
		d = {'sum': str(self.sum), 'hash': self.hash}
		uid = getattr(self, "uid", None)
		if uid:
			d['uid']=uid
		return str(d)

	@staticmethod
	def FromJSON(json_str):
		"""Parse a JSON-encoded leaf node list.

		Given a JSON-encoded array of maps of user/balance/nonce, return
		a list of Node objects ready to pass to HashTree.
		"""
		structured = json.loads(json_str)
		if (type(structured) is not list
		    or any([type(x) is not dict for x in structured])):
			raise ValueError('must supply an array of maps')
		return [Node(nsum=account['balance'], nonce=account['nonce'],
			     uid=account['user'])
			for account in structured]


def NodeCombiner(left, right):
	newsum = left.sum + right.sum
	newsum = newsum.normalize()
	newhash = sha256("{:f}|{}|{}".format(newsum, left.hash, right.hash)).hexdigest()

	return Node(newsum, nhash=newhash)

class HashTree():
	def __init__(self, nodelist, deterministic=False):
		self.nodelist = nodelist
		self.roothash = ''
		self.tree = []
		self.GenTree(nodelist, deterministic)
		self.byhash = {}
		self.byuid = {}
		self.GenLookup()
	
	def ReturnTotal(self):
		return self.tree[-1][0].sum
	
	def GenTree(self, nodelist, deterministic):
		self.tree.append(nodelist)
		newnodelist = []

		# FIXME: Add tree layout randomisation as the default and leave
		#	 this as an option for compatibility testing.
		if deterministic:
			dummies_needed = int(math.pow(2, (math.ceil(math.log(len(nodelist), 2)))))
			dummies_needed -= len(nodelist)
			if dummies_needed:
				nodelist.extend([Node(0, uid="dummy", nonce="0")] * dummies_needed)
		elif len(nodelist) % 2:
			nodelist.extend([Node(0, uid="dummy", nonce="0")])

		for x in range(int(math.ceil(len(nodelist)/2.0))):
			newnodelist.append(NodeCombiner(nodelist[(x * 2)], nodelist[(x * 2 + 1)]))
		
		if len(newnodelist) > 1:
			return self.GenTree(newnodelist, deterministic)
		else:
			self.tree.append(newnodelist)
			self.roothash = newnodelist[0].hash
			return self.roothash
	
	def ValidateTree(self, tree=None):
		if tree == None:
			tree = self.tree
		for x in tree:
			print x
	
	def RegenTree(self):
		self.tree = []
		return self.GenTree(self.nodelist)
	
	def GetInfoFromHash(self, nhash):
		index = self.byhash[nhash]
		info = self.GetNodeInfo(index)
		verifyinfo = self.GetNodePairList(index)
		return info[0], info[1], verifyinfo[0], verifyinfo[1]
	
	def GetNodeInfo(self, index):
		return str(self.tree[0][index].sum), self.tree[0][index].hash
	
	def GetNodePairList(self, index, pairlist=[], tree=None):
		if tree == None:
			tree = self.tree
			pairlist = []
		elif len(tree) == 1:
			return self.roothash, pairlist
		pairlist.append((str(tree[0][index + (-1 if index % 2 else 1)].sum), tree[0][index + (-1 if index % 2 else 1)].hash, 0 if index % 2 else 1))
		index = index / 2
		return self.GetNodePairList(index, pairlist=pairlist, tree=tree[1:])
		
	def GenLookup(self):
		index = 0
		for x in self.nodelist:
			self.byhash[x.hash] = index
			self.byuid[getattr(x, "uid", None)] = index
			index += 1

	def GetPartialTreeJSON(self, nhash=None, uid=None):
		if nhash:
			index = self.byhash[nhash]
		elif uid:
			index = self.byuid[uid]
		else:
			raise ValueError('must supply either uid or nhash')

		structure = {}
		nonce = getattr(self.nodelist[index], "nonce", None)
		if nonce:
			structure["nonce"] = nonce

		_, pairs = self.GetNodePairList(index)
		while pairs:
			sibsum, sibhash, sibside = pairs.pop(0)
			sibsum = "{:f}".format(Decimal(sibsum).normalize())
			if sibside == 0:
				structure = {"left": {"data": {"hash": sibhash,
							       "sum": sibsum}},
					     "right": structure}
			else:
				structure = {"right": {"data": {"hash": sibhash,
								"sum": sibsum}},
					     "left": structure}
		return json.dumps(structure, indent=4)

	def GetRootJSON(self):
		rootsum = "{:f}".format(self.tree[-1][0].sum.normalize())
		return json.dumps({"root": {"sum": rootsum,
					    "hash": self.roothash}},
				  indent=4)

def ValidateNode(node, roothash, pairlist):
	for x in pairlist:
		# If this was an even node, put the paired node on the right, otherwise it goes on the left.
		if x[2]:
			node = NodeCombiner(node, Node(nsum=x[0], nhash=x[1]))
		else:
			node = NodeCombiner(Node(nsum=x[0], nhash=x[1]), node)
	return node.hash == roothash

class Coin():
	def __init__(self, host, port, user, password, use_https=False):
		self.conn = connect_to_remote(user, password, host=host, port=port, use_https=use_https)

def ValidateBalance(coin, amount, message="Coin Balance Verified for %s" % time.strftime("%a, %d %b %Y %H:%M:%S +0000")):
	if type(amount) is str:
		amount = Decimal(amount)
	vfdamount = Decimal('0')
	msgs = []
	for x in coin.conn.listunspent():
		if vfdamount < amount:
			vfdamount += x.amount
			msgs.append((x.address, coin.conn.proxy.signmessage(x.address, message)))
	return msgs, vfdamount, message
