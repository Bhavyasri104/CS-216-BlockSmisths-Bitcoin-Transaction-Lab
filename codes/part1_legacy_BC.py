from bitcoinrpc.authproxy import AuthServiceProxy
from decimal import Decimal

rpc_user = "labuser"
rpc_password = "labpass123"
rpc_port = 18443


rpc = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:{rpc_port}")
print("Connected to Bitcoin Core")

wallet_name = "labwallet"


try:
    rpc.loadwallet(wallet_name)
except:
    pass


rpc = AuthServiceProxy(
    f"http://{rpc_user}:{rpc_password}@127.0.0.1:{rpc_port}/wallet/{wallet_name}"
)


utxos = rpc.listunspent()

if not utxos:
    print("No UTXOs found")
    exit()

utxo = utxos[0]

print("Selected UTXO:", utxo)


C = rpc.getnewaddress("C", "legacy")
print("Address C:", C)

inputs = [{
    "txid": utxo["txid"],
    "vout": utxo["vout"]
}]

fee = Decimal("0.0001")

send_amount = utxo["amount"] / 2
change_amount = utxo["amount"] - send_amount - fee

if change_amount <= 0:
    print("Not enough balance after fee")
    exit()

outputs = {
    C: send_amount,
    utxo["address"]: change_amount
}


raw_tx = rpc.createrawtransaction(inputs, outputs)

print("\nRaw Transaction:")
print(raw_tx)


decoded_raw = rpc.decoderawtransaction(raw_tx)

print("\nDecoded Raw Transaction:")
print(decoded_raw)


signed_tx = rpc.signrawtransactionwithwallet(raw_tx)

if not signed_tx["complete"]:
    print("Signing incomplete")
    exit()

print("\nSigned Transaction HEX:")
print(signed_tx["hex"])


txid = rpc.sendrawtransaction(signed_tx["hex"])

print("\nB -> C Transaction ID:", txid)


rpc.generatetoaddress(1, utxo["address"])

print("Block mined to confirm B -> C")


decoded_tx = rpc.decoderawtransaction(signed_tx["hex"])

print("\nDecoded Final Transaction:")
print(decoded_tx)

print("\nLocking Script (scriptPubKey):")
print(decoded_tx["vout"][0]["scriptPubKey"])

print("\nUnlocking Script (scriptSig):")
print(decoded_tx["vin"][0]["scriptSig"])
