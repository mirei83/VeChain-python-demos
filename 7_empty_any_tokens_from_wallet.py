'''
  This demo empties completely any VIP-180/ERC20 tokens from a wallet.
  This is achieved by using a sponsor wallet to do sponsor the transaction
'''

from thor_requests.wallet import Wallet
from thor_requests.connect import Connect
from thor_requests.contract import Contract
import requests

# Config
NODE_URL = "https://sync-testnet.vechain.org" # node connection
TOKEN_LIST = 'https://vechain.github.io/token-registry/test.json' # main net is main.json
SPONSOR = Wallet.fromPrivateKey(...)
SRC_WALLET = Wallet.fromPrivateKey(...)
DST_ADDRESS = '0x...' # fill in your destination wallet address
ERC20_CONTRACT = Contract.fromFile("./VTHO.json")
CONNECTOR = Connect(NODE_URL)

# Gather tokens list
r = requests.get(TOKEN_LIST)
assert r.status_code == 200
tokens = r.json()

# Gather user's tokens balances
balance_clauses = [ CONNECTOR.clause(ERC20_CONTRACT, 'balanceOf', [SRC_WALLET.getAddress()], token['address']) for token in tokens]
results = CONNECTOR.call_multi(SRC_WALLET.getAddress(), balance_clauses)
assert len(results) == len(tokens)
balances = [int(x['decoded']['0']) for x in results]
for token, balance in zip(tokens, balances):
  print(f'{token["symbol"]}: {balance}')

# Use VIP-191 fee delegation to transfer all tokens out
transfer_clauses = []
for token, balance in zip(tokens, balances):
  if int(balance) > 0:
    c = CONNECTOR.clause(ERC20_CONTRACT, 'transfer', [DST_ADDRESS, balance], token['address'])
    transfer_clauses.append(c)

# Do the transaction
if len(transfer_clauses) > 0:
  res = CONNECTOR.transact_multi(
    SRC_WALLET,
    transfer_clauses,
    gas_payer=SPONSOR
  )

print('transfer out all tokens with transaction', res)

# Use vip-191 fee delegation to transfer all VET out
vet_balance_in_wei = CONNECTOR.get_vet_balance(SRC_WALLET.getAddress())
print('vet:', vet_balance_in_wei)
res = CONNECTOR.transfer_vet(SRC_WALLET, DST_ADDRESS, vet_balance_in_wei, SPONSOR)
print('transfer out all VET with transaction', res)