from proveit import *
import string
import sys

USAGE="""
followit.py: produce root or partial tree info in draft standard format.
NOTE: currently produces trees deterministically, for testing only.

To produce a partial tree for a named account:

    followit.py partialtree satoshi accounts.json

or:

    cat accounts.json | followit.py partialtree satoshi

To produce the root sum and hash for an accounts list:

    followit.py root accounts.json
"""

command = ""
if len(sys.argv) >= 2:
	if sys.argv[1] == "partialtree":
		command = sys.argv.pop(1)
		user = sys.argv.pop(1)
	elif sys.argv[1] == "root":
		command = sys.argv.pop(1)
	else:
		print USAGE
		sys.exit(-1)
else:
	print USAGE
	sys.exit(-1)

if len(sys.argv) == 2:
	sys.stdin = file(sys.argv[1])
with sys.stdin as x:
	slurped = x.read()

nodelist = Node.FromJSON(slurped)
total = 0
for x in nodelist:
	total += x.sum
	
h = HashTree(nodelist, deterministic=True)
if command == "root":
	print h.GetRootJSON()
elif command == "partialtree":
	print h.GetPartialTreeJSON(uid=user)
