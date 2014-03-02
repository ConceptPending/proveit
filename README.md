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

To add the CryptoCurrency portion of the account verification, use the following code, inserting your own RPC information as required.

```python
coin = Coin(host, port, user, password)

ValidateBalance(coin, Decimal("<insert balance you wish to prove>"), message="Validation message that gives your customers confidence")
```

This will give you a list of signed messages, for at least the amount that you wish to verify (if you have a sufficient balance), and for the amount in your wallet, if you don't have a sufficient balance.

If you see any problems or have an suggestions, please raise an issue or (better yet!) submit a pull request!

Cheers,

Nick
