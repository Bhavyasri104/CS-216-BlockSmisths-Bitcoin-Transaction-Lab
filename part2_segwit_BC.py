from bitcoinrpc.authproxy import AuthServiceProxy
from decimal import Decimal

rpc_user = "labuser"
rpc_password = "labpass123"
rpc_port = 18443

rpc = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:{rpc_port}")

print("Connected to Bitcoin Core")

wallet_name = "segwit_lab"

try:
    rpc.loadwallet(wallet_name)
except:
    pass

rpc = AuthServiceProxy(
    f"http://{rpc_user}:{rpc_password}@127.0.0.1:{rpc_port}/wallet/{wallet_name}"
)

print("Connected to wallet")

# Generate SegWit address C'
address_C = rpc.getnewaddress("C_prime", "p2sh-segwit")
print("P2SH-SegWit Address C':", address_C)

# Find UTXO from B'
utxos = rpc.listunspent()

utxo = None
for u in utxos:
    if u["amount"] == Decimal("3.00000000"):
        utxo = u
        break

if not utxo:
    print("No suitable UTXO found")
    exit()

print("Selected UTXO:", utxo)

inputs = [{
    "txid": utxo["txid"],
    "vout": utxo["vout"]
}]

send_amount = Decimal("2.5")
fee = Decimal("0.0001")
change_amount = utxo["amount"] - send_amount - fee

outputs = {
    address_C: float(send_amount),
    utxo["address"]: float(change_amount)
}

raw_tx = rpc.createrawtransaction(inputs, outputs)

print("\nRaw Transaction (B' -> C'):")
print(raw_tx)

decoded_raw = rpc.decoderawtransaction(raw_tx)

print("\nDecoded Raw Transaction:")
print(decoded_raw)

signed_tx = rpc.signrawtransactionwithwallet(raw_tx)

print("\nSigned Transaction:")
print(signed_tx["hex"])

txid = rpc.sendrawtransaction(signed_tx["hex"])

print("\nB' -> C' Transaction ID:", txid)

rpc.generatetoaddress(1, rpc.getnewaddress())

print("Block mined to confirm B' -> C'")

wallet_tx = rpc.gettransaction(txid)
raw_hex = wallet_tx["hex"]

final_tx = rpc.decoderawtransaction(raw_hex)

print("\nFinal Decoded Transaction:")
print(final_tx)

print("\nscriptPubKey:")
print(final_tx["vout"][0]["scriptPubKey"])