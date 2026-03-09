from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from decimal import Decimal

# RPC CONFIG
rpc_user = "labuser"
rpc_password = "labpass123"
rpc_port = 18443

# Connect to Bitcoin Core
rpc = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:{rpc_port}")

print("Connected to Bitcoin Core")

wallet_name = "segwit_lab"

# Create or Load Wallet
try:
    rpc.createwallet(wallet_name)
    print("Wallet created")
except:
    print("Wallet already exists, loading...")
    try:
        rpc.loadwallet(wallet_name)
    except:
        pass

# Connect to wallet endpoint
rpc = AuthServiceProxy(
    f"http://{rpc_user}:{rpc_password}@127.0.0.1:{rpc_port}/wallet/{wallet_name}"
)

print("Connected to Wallet")

# Generate P2SH-SegWit addresses
address_A = rpc.getnewaddress("A_prime", "p2sh-segwit")
address_B = rpc.getnewaddress("B_prime", "p2sh-segwit")
address_C = rpc.getnewaddress("C_prime", "p2sh-segwit")

print("P2SH-SegWit Address A':", address_A)
print("P2SH-SegWit Address B':", address_B)
print("P2SH-SegWit Address C':", address_C)

# Mine 101 blocks
rpc.generatetoaddress(101, rpc.getnewaddress())
print("Mined 101 blocks")

# Fund A'
fund_txid = rpc.sendtoaddress(address_A, Decimal("5.0"))
print("Funding TXID:", fund_txid)

rpc.generatetoaddress(1, rpc.getnewaddress())
print("Block mined to confirm funding")

# Get UTXO of A'
utxos = rpc.listunspent(1, 9999999, [address_A])

if not utxos:
    print("No UTXO found for A'")
    exit()

utxo = utxos[0]
print("Selected UTXO:", utxo)

inputs = [{
    "txid": utxo["txid"],
    "vout": utxo["vout"]
}]

# Transaction amounts
send_amount = Decimal("3.0")
fee = Decimal("0.0001")
change_amount = utxo["amount"] - send_amount - fee

outputs = {
    address_B: float(send_amount),
    address_A: float(change_amount)
}

# Create raw transaction
raw_tx = rpc.createrawtransaction(inputs, outputs)

print("\nRaw Transaction:")
print(raw_tx)

decoded_raw = rpc.decoderawtransaction(raw_tx)
print("\nDecoded Raw TX (A' -> B'):")
print(decoded_raw)

# Sign transaction
signed_tx = rpc.signrawtransactionwithwallet(raw_tx)

if not signed_tx["complete"]:
    print("Signing incomplete")
    exit()

print("\nSigned Transaction:")
print(signed_tx["hex"])

# Broadcast transaction
txid_AB = rpc.sendrawtransaction(signed_tx["hex"])
print("\nA' -> B' Transaction ID:", txid_AB)

# Mine block
rpc.generatetoaddress(1, rpc.getnewaddress())
print("Block mined to confirm A' -> B'")

# Get final transaction
wallet_tx = rpc.gettransaction(txid_AB)
raw_hex = wallet_tx["hex"]

final_tx = rpc.decoderawtransaction(raw_hex)

print("\nFinal Decoded Transaction:")
print(final_tx)

print("\nLocking Script (scriptPubKey) for B':")
print(final_tx["vout"][0]["scriptPubKey"])