from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from decimal import Decimal

# RPC CONFIGURATION
RPC_USER = "labuser"
RPC_PASSWORD = "labpass123"
RPC_PORT = 18443

print("Connecting to Bitcoin Core...")

NODE = AuthServiceProxy(f"http://{RPC_USER}:{RPC_PASSWORD}@127.0.0.1:{RPC_PORT}")

print("NODE CONNECTION SUCCESSFUL")

WALLET_NAME = "labwallet"

# LOAD WALLET
try:
    NODE.loadwallet(WALLET_NAME)
    print("Wallet loaded")
except:
    print("Wallet already loaded")

# CONNECT TO WALLET
WALLET = AuthServiceProxy(
    f"http://{RPC_USER}:{RPC_PASSWORD}@127.0.0.1:{RPC_PORT}/wallet/{WALLET_NAME}"
)

print("Connected to wallet")

# CREATE ADDRESS C
ADDRESS_C = WALLET.getnewaddress("NODE_C", "legacy")

print("DESTINATION ADDRESS (C):", ADDRESS_C)

# FETCH ALL UTXOS
UTXO_LIST = WALLET.listunspent()

if not UTXO_LIST:
    print("No UTXO available for transaction")
    exit()

# SELECT LARGEST UTXO (usually from B)
SELECTED_UTXO = max(UTXO_LIST, key=lambda x: x["amount"])

print("Selected UTXO:", SELECTED_UTXO)

INPUTS = [{
    "txid": SELECTED_UTXO["txid"],
    "vout": SELECTED_UTXO["vout"]
}]

FEE = Decimal("0.0001")

TOTAL_AMOUNT = SELECTED_UTXO["amount"]

SEND_AMOUNT = (TOTAL_AMOUNT / 2).quantize(Decimal("0.00000001"))
CHANGE_AMOUNT = (TOTAL_AMOUNT - SEND_AMOUNT - FEE).quantize(Decimal("0.00000001"))

if CHANGE_AMOUNT <= 0:
    print("Insufficient balance")
    exit()

print("Send amount:", SEND_AMOUNT)
print("Change amount:", CHANGE_AMOUNT)

OUTPUTS = {
    ADDRESS_C: float(SEND_AMOUNT),
    SELECTED_UTXO["address"]: float(CHANGE_AMOUNT)
}

# CREATE RAW TRANSACTION
RAW_TX = WALLET.createrawtransaction(INPUTS, OUTPUTS)

print("\nRAW TRANSACTION:")
print(RAW_TX)

# SIGN TRANSACTION
SIGNED_TX = WALLET.signrawtransactionwithwallet(RAW_TX)

if not SIGNED_TX["complete"]:
    print("Signing failed")
    exit()

print("\nSIGNED TRANSACTION:")
print(SIGNED_TX["hex"])

# BROADCAST
TX_ID = WALLET.sendrawtransaction(SIGNED_TX["hex"])

print("\nTRANSACTION ID (B -> C):", TX_ID)

# CONFIRM TRANSACTION
WALLET.generatetoaddress(1, ADDRESS_C)

print("Transaction confirmed")

# DECODE TRANSACTION
FINAL_TX = WALLET.gettransaction(TX_ID)

print("\nDECODED TRANSACTION:")
print(FINAL_TX)