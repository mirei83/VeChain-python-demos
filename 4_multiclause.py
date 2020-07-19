from thor_devkit import cry, transaction
import requests


# Sender wallet information
# mnemonic phrase: twenty, jelly, around, appear, approve, version, general, bright, crumble, all, master, sail
# address: 0xbc1497fc775f5cbf42dfeca44d97efaba79462b7
# private key: 61faba91ef7516969e885d197f59feeb2007ea2c6057908d1696d6f056ca69d4
 

# See: https://docs.vechain.org/thor/learn/transaction-model.html#model
body = {
    "chainTag": 39, # chainTag 39 = testnet,  see: https://docs.vechain.org/others/#network-identifier for more details
    "blockRef": '0x006360a563534115', # to get latest blockRef, 
    "expiration": 720, # blockref + expiration = blocknumber where TX expires
    "clauses": [  # here the cause section starts, in later demos, there will be a lot of clauses. In this demo there is only one simple clause: a transfere of vet.
        {
            "to": '0x0000000000000000000000000000000000000000', # destination of vet
            "value": 1000000000000000000, # how much vet will be send. Vet has 18 decimals, so this equals to 1 vet.
            "data": '0x' # data is irrelevant in a vet transactions, but needs to be defined
        },
        {
            "to": '0x0000000000000000000000000000000000000009', # destination of vet
            "value": 1000000000000000000, # how much vet will be send. Vet has 18 decimals, so this equals to 1 vet.
            "data": '0x' # data is irrelevant in a vet transactions, but needs to be defined
        }
    ],
    "gasPriceCoef": 0, # gasPriceCoef can be between 0 and 255 to increase the urgency of your transactions
    "gas": 37000, # maximum gas a tx can consume
    "dependsOn": None, # you can stage transactions, irrelevant for now
    "nonce": 12345678 # nonce for proof-of-work and uniquesness of the transaction
}

# Construct an unsigned transaction.
tx = transaction.Transaction(body)


# Sign the transaction with a private key.
priv_key = bytes.fromhex('61faba91ef7516969e885d197f59feeb2007ea2c6057908d1696d6f056ca69d4')
message_hash = tx.get_signing_hash()
signature = cry.secp256k1.sign(message_hash, priv_key)

# Set the signature on the transaction.
tx.set_signature(signature)

print('Created a transaction from ' + tx.get_origin() + ' to 0x0000000000000000000000000000000000000000 with TXID: ' + tx.get_id() + '.')
print('')

encoded_bytes = tx.encode()

# pretty print the encoded bytes.
print('The transaction "0x' + encoded_bytes.hex() + '" will be send to the testnet node now.')



tx_headers = {'Content-Type': 'application/json', 'accept': 'application/json'}
tx_data = {'raw': '0x' + encoded_bytes.hex()}
	
send_transaction = requests.post('https://testnet.veblocks.net/transactions', json=tx_data, headers=tx_headers)

print('Response from Server: ' + str(send_transaction.content))
