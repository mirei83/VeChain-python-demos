from thor_devkit import cry, transaction
import requests
from random import randint
import json

# Sender wallet information
# mnemonic phrase: twenty, jelly, around, appear, approve, version, general, bright, crumble, all, master, sail
# address: 0xbc1497fc775f5cbf42dfeca44d97efaba79462b7
# private key: 61faba91ef7516969e885d197f59feeb2007ea2c6057908d1696d6f056ca69d4
_privatekey = '61faba91ef7516969e885d197f59feeb2007ea2c6057908d1696d6f056ca69d4'
_node_url = 'https://testnet.veblocks.net'
_ChainTag = 39

# Get infos of best block
BlockInfos = requests.get(_node_url + '/blocks/best')	
# Set BlockRef to best block
_BlockRef = BlockInfos.json()['id'][0:18]
# Generate random noce
_Nonce = randint(10000000, 99999999)


### Create list of clauses
_transaction_clauses = [
	{'to': '0x0000000000000000000000000000000000000000', 'value': 1000000000000000000, 'data': '0x'},
    {'to': '0x0000000000000000000000000000000000000009', 'value': 1000000000000000000, 'data': '0x'},
    {'to': '0x0000000000000000000000000000000000000010', 'value': 1000000000000000000, 'data': '0x'},
    {'to': '0x0000000000000000000000000000000000000011', 'value': 1000000000000000000, 'data': '0x'},
    {'to': '0x0000000000000000000000000000000000000012', 'value': 1000000000000000000, 'data': '0x'}
]

### Build transaction 
body = {}
body['chainTag'] = _ChainTag
body['blockRef'] = _BlockRef
body['expiration'] = 720
body['clauses'] = _transaction_clauses
body['gasPriceCoef'] = 0
body['gas'] = 85000 # 5000 + (5 * 16000)
body['dependsOn'] = None
body['nonce'] = _Nonce

# Construct an unsigned transaction.
tx = transaction.Transaction(body)


# Sign the transaction with a private key.
priv_key = bytes.fromhex(_privatekey)
message_hash = tx.get_signing_hash()
signature = cry.secp256k1.sign(message_hash, priv_key)

# Set the signature on the transaction.
tx.set_signature(signature)

print('Created a transaction from ' + tx.get_origin() + ' with TXID: ' + tx.get_id() + '.')
print('')

encoded_bytes = tx.encode()

# Pretty print the encoded bytes.
print('The transaction "0x' + encoded_bytes.hex() + '" will be send to the testnet node now.')



tx_headers = {'Content-Type': 'application/json', 'accept': 'application/json'}
tx_data = {'raw': '0x' + encoded_bytes.hex()}
	
send_transaction = requests.post(_node_url + '/transactions', json=tx_data, headers=tx_headers)

print('Response from Server: ' + str(send_transaction.content))
