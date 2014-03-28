Prove It!
=========

This is a basic implementation of gmaxwell's suggestion of proving
account balances documented here:
https://iwilcox.me.uk/2014/proving-bitcoin-reserves

This will work for any CryptoCurrency that is based off the Bitcoin protocol.

### Basic Docs

To install the project just use:
```
pip install proveit
```

You will need to provide the HashTree class with a list of customer
balances, user-chosen tokens such as username/e-mail and nonces with
which to create a glorified Merkle tree.

You can supply a manually computed hash instead, in which case you
should consider generating it in way that's [compatible with other
implementations] [s11n] (the default hashing used if you supply
uids/nonces is already compatible).

 [s11n]: https://github.com/olalonde/proof-of-liabilities#serialized-data-formats-work-in-progress--draft

#### Basic Usage
```python
from proveit import *

customers = [ Node(nsum=123, uid='unique user-chosen identifier', nonce='secret shared with exchange'),
              Node(nsum=456, uid='another unique user-chosen id', nonce='another secret shared with exchange')]

# Alternatively:

customers = [ Node(nsum=123, nhash='externally computed hash, preferably produced compatibly'),
              Node(nsum=456, nhash='another externally computed hash, preferably produced compatibly')]

hashtree = HashTree(customers)
```

Now you've generated a hashtree where any customer can validate that you've included their balance into your total.

All you need to do to provide them with the relevant information follows:

```python
info = hashtree.GetInfoFromHash('hash')
```

This provides (account balance, account hash, root hash, partial hash tree)

Now anyone can verify this section of the Merkle tree using the following function.

```python
ValidateNode(Node(nsum=123, uid='user-chosen id', nonce='secret shared with exchange'), info[2], info[3])
```

To add the CryptoCurrency portion of the account verification, use the following code, inserting your own RPC information as required.

```python
coin = Coin(host, port, user, password)

ValidateBalance(coin, Decimal("<insert balance you wish to prove>"), message="Validation message that gives your customers confidence")
```

This will give you a list of signed messages, for at least the amount that you wish to verify (if you have a sufficient balance), and for the amount in your wallet, if you don't have a sufficient balance.

In practice, you can likely get away with something approximating the following since there is a default message that includes a timestamp.

```python
ValidateBalance(coin, hashtree.GetTotal())
```

#### JSON interface

`followit.py` accepts an accounts list and produces either the root
info or a partial tree for a given user, all in JSON format as per the
[draft standard] [s11n].  See [its USAGE] [USAGE] for more
information.

 [USAGE]: followit.py#L5

#### Browser Verification (Work in Progress!)
Included is a JS implementation of the verification code, so that customers can copy & paste the Root Hash + Merkle Tree, then see whether the tree can be verified as well as whether they have proven they hold that amount of Crypto-Currency.

Just use the *static-verify.html* page as well as the *js/* folder, and no server-side code is necessary.

This implementation includes the Merkle Tree verfier while verifying the signed messages and account balances is the next step.

#### Browser Extension (Vaporware for now)
Eventually, a browser extension can be built that will automatically verify this to the end-user whenever they're logged into a platform that uses Prove It!

An alert can then appear if anything is ever amiss.

The way I intend to implement this will require that the site provides proper JSON responses to predetermined endpoints on the domain or subdomain where the site is hosted, but if you're using the Prove It! method of verifying funds anyway, this shouldn't be a big issue.

#### The End
If you see any problems or have an suggestions, please raise an issue or (better yet!) submit a pull request!

Cheers,

Nick
