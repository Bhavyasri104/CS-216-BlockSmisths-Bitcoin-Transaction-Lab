from bitcoinrpc.authproxy import AuthServiceProxy
from decimal import Decimal

# RPC Credentials
rpc_user = "labuser"
rpc_password = "labpass123"
rpc_port = 18443

# Connect to node
rpc = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:{rpc_port}")

print("Connected to Bitcoin Core")

wallet_name = "labwallet"

# Load wallet
try:
    rpc.loadwallet(wallet_name)
except:
    pass

# Connect to wallet endpoint
rpc = AuthServiceProxy(
    f"http://{rpc_user}:{rpc_password}@127.0.0.1:{rpc_port}/wallet/{wallet_name}"
)

# Get all UTXOs
utxos = rpc.listunspent()

if not utxos:
    print("No UTXOs found.")
    exit()

# Select the 2 BTC UTXO from B
utxo = None
for u in utxos:
    if u["amount"] == Decimal("2.00000000"):
        utxo = u
        break

if not utxo:
    print("No suitable 2 BTC UTXO found.")
    exit()

print("Selected UTXO:", utxo)

# Generate address for C
C = rpc.getnewaddress("", "legacy")
print("Address C:", C)

# Prepare inputs
inputs = [{
    "txid": utxo["txid"],
    "vout": utxo["vout"]
}]

# Define send amount and fee
send_amount = Decimal("1.5")
fee = Decimal("0.0001")

change_amount = utxo["amount"] - send_amount - fee

# Outputs
outputs = {
    C: float(send_amount),
    utxo["address"]: float(change_amount)  # change back to B
}

# Create raw transaction
raw_tx = rpc.createrawtransaction(inputs, outputs)

print("\nRaw Transaction:")
print(raw_tx)

# Sign transaction
signed_tx = rpc.signrawtransactionwithwallet(raw_tx)

if not signed_tx["complete"]:
    print("Transaction signing incomplete")
    exit()

print("\nSigned Transaction:")
print(signed_tx["hex"])

# Broadcast transaction
txid = rpc.sendrawtransaction(signed_tx["hex"])

print("\nB -> C Transaction ID:", txid)

# Mine block to confirm
rpc.generatetoaddress(1, C)
print("Block mined to confirm B -> C transaction")

# Get wallet transaction
wallet_tx = rpc.gettransaction(txid)

raw_hex = wallet_tx["hex"]

# Decode transaction
decoded_tx = rpc.decoderawtransaction(raw_hex)

print("\nDecoded Transaction:")
print(decoded_tx)

print("\nUnlocking Script (scriptSig):")
print(decoded_tx["vin"][0]["scriptSig"])