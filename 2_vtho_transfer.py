from thor_requests.wallet import Wallet
from thor_requests.connect import Connect
from thor_requests.contract import Contract

# Set up a connection to VeChain blockchain
connector = Connect("http://localhost:8669")

# VTHO token contract address
vtho_contract_address = "0x0000000000000000000000000000456e65726779"

# Set up the VTHO contract object
vtho_contract = Contract.fromFile("./VTHO.json")

# Set up the sender's wallet
sender = Wallet.fromMnemonic(
    [
        "denial",
        "kitchen",
        "pet",
        "squirrel",
        "other",
        "broom",
        "bar",
        "gas",
        "better",
        "priority",
        "spoil",
        "cross",
    ]
)

# Set up the receiver's wallet (a brand new wallet)
receiver =  Wallet.newWallet()

# Try to transfer 3 vtho from sender to receiver
if __name__ == "__main__":

    # Do: transfer 3 VTHO 
    response = connector.transact(
        sender,
        vtho_contract,
        "transfer",
        [receiver.getAddress(), 3 * (10 ** 18)],  # transfer 3 vtho
        vtho_contract_address,
        value=0,
    )

    tx_id = response["id"]
    receipt = connector.wait_for_tx_receipt(tx_id)

    # Check the receiver's vtho balance
    # Should equal to 3 vtho
    response = connector.call(
        receiver.getAddress(),
        vtho_contract,
        "balanceOf",
        [receiver.getAddress()],
        vtho_contract_address,
        value=0,
    )
    assert response["reverted"] == False
    updated_balance = response["decoded"]["balance"]
    assert updated_balance == 3 * (10 ** 18)