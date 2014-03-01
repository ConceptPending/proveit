Prove It!
=========

This is a basic implementation of gmaxwell's suggestion of proving account balances documented here: https://iwilcox.me.uk/v/nofrac

### Basic Docs

To install the project just use:
```
pip install proveit
```

You will need to provide the HashTree class with a list of customer accounts and hashes with which to create a glorified Merkle tree.

The hashes should probably just be hashfunction(customer_id + salt), or something of the like.

#### Basic Usage
```python
pip install proveit

from proveit import *

customers = [ Node(123, 'unique identifier, preferably hashed'), Node(456, 'unique identifier2, preferably hashed as well')]

hashtree = HashTree(customers)
```

Now you've generated a hashtree where any customer can validate that you've included their balance into your total.

All you need to do to provide them with the relevant information follows:

```python
info = hashtree.GetInfoFromHash('unique identifier, preferably hashed')
```

This provides (Account Value, Identifier, root hash, Hash Tree)

Now anyone can verify this section of the Merkle tree using the following function.

```python
ValidateNode(Node(info[0], info[1]), info[2], info[3])
```

I will be adding more code and better documentation tomorrow.

If you see any problems or have an suggestions, please raise an issue or (better yet!) submit a pull request!

Cheers,

Nick
