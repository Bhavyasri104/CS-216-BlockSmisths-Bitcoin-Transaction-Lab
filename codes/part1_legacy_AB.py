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
    print("Wallet already exists, loading...")
    try:
        rpc.loadwallet(wallet_name)
    except:
        pass


rpc = AuthServiceProxy(
    f"http://{rpc_user}:{rpc_password}@127.0.0.1:{rpc_port}/wallet/{wallet_name}"
)


A = rpc.getnewaddress("A", "legacy")
B = rpc.getnewaddress("B", "legacy")
C = rpc.getnewaddress("C", "legacy")

print("Address A:", A)
print("Address B:", B)
print("Address C:", C)


rpc.generatetoaddress(101, A)
print("Mined 101 blocks")


fund_txid = rpc.sendtoaddress(A, Decimal("1.0"))
print("Funding TXID:", fund_txid)

rpc.generatetoaddress(1, A)
print("Block mined to confirm funding")


utxos = rpc.listunspent(1, 9999999, [A])

if not utxos:
    print("No UTXO found for address A")
    exit()

utxo = utxos[0]
print("Selected UTXO:", utxo)

inputs = [{
    "txid": utxo["txid"],
    "vout": utxo["vout"]
}]

fee = Decimal("0.0001")

send_amount = utxo["amount"] / 2
change_amount = utxo["amount"] - send_amount - fee

outputs = {
    B: send_amount,
    A: change_amount
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

print("\nA -> B Transaction ID:", txid)


rpc.generatetoaddress(1, A)

print("Block mined to confirm A -> B")


decoded_tx = rpc.decoderawtransaction(signed_tx["hex"])

print("\nDecoded Final Transaction:")
print(decoded_tx)

print("\nLocking Script (scriptPubKey):")
print(decoded_tx["vout"][0]["scriptPubKey"])

print("\nUnlocking Script (scriptSig):")
print(decoded_tx["vin"][0]["scriptSig"])
