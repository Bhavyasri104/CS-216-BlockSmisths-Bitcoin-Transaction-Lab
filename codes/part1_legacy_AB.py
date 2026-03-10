from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from decimal import Decimal

rpc_user = "labuser"
rpc_password = "labpass123"
rpc_port = 18443

rpc = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:{rpc_port}")

print("Connected to Bitcoin Core")

wallet_name = "labwallet"

try:
    rpc.createwallet(wallet_name)
    print("Wallet created")
except JSONRPCException:
    print("Wallet may already exist, loading it...")
    try:
        rpc.loadwallet(wallet_name)
        print("Wallet loaded")
    except:
        pass

rpc = AuthServiceProxy(
    f"http://{rpc_user}:{rpc_password}@127.0.0.1:{rpc_port}/wallet/{wallet_name}"
)

# Generate addresses
A = rpc.getnewaddress("A", "legacy")
B = rpc.getnewaddress("B", "legacy")
C = rpc.getnewaddress("C", "legacy")

print("Address A:", A)
print("Address B:", B)
print("Address C:", C)

# Mine blocks
rpc.generatetoaddress(101, A)
print("Mined 101 blocks")

# Send BTC to A
fund_txid = rpc.sendtoaddress(A, Decimal("1.0"))
print("Funding Transaction ID:", fund_txid)

rpc.generatetoaddress(1, A)
print("Block mined to confirm funding")

# Get UTXO
utxos = rpc.listunspent(1, 9999999, [A])

if not utxos:
    print("No UTXO found")
    exit()

utxo = utxos[0]
print("UTXO selected:", utxo)

inputs = [{
    "txid": utxo["txid"],
    "vout": utxo["vout"]
}]

# Fee
fee = Decimal("0.0001")

# Send half of available balance
send_amount = utxo["amount"] / 2

# Change calculation
change_amount = utxo["amount"] - send_amount - fee

outputs = {
    B: send_amount,
    A: change_amount
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

# Broadcast
txid = rpc.sendrawtransaction(signed_tx["hex"])

print("\nA -> B Transaction ID:", txid)

# Confirm transaction
rpc.generatetoaddress(1, A)

print("Block mined to confirm A -> B")

# Decode transaction
decoded_tx = rpc.gettransaction(txid)

print("\nDecoded Transaction:")
print(decoded_tx)
