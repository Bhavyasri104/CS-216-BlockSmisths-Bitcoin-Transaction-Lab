# Bitcoin Transaction Lab Assignment

**Course:** CS 216 – Bitcoin / Blockchain Systems  
**Environment:** Bitcoin Core (Regtest Mode)

This project demonstrates the creation, signing, broadcasting, and validation of **Bitcoin transactions** using **Bitcoin Core RPC and Python**.

Two types of transactions are implemented:

- Legacy Transactions (**P2PKH**)
- SegWit Transactions (**P2SH-P2WPKH**)

All transactions are executed on the **Bitcoin Regtest network** and validated using the **Bitcoin Script Debugger (btcdeb)**.

---

# Team Members

| Name | Roll Number |
|------|-------------|
| Paruchuri Bhavya Sri | 240001049 |
| Usepetla Nancy Sahithi | 240001075 |
| Malothu Haritha | 240001042 |
| Apurva Dinesh Chipte | 240021003 |

---

# Project Objectives

The objective of this assignment is to:

- Understand Bitcoin transaction structure
- Create Legacy (**P2PKH**) transactions
- Create SegWit (**P2SH-P2WPKH**) transactions
- Sign transactions using Bitcoin Core wallet
- Broadcast transactions to the Regtest blockchain
- Validate scripts using **btcdeb**
- Compare Legacy vs SegWit transactions

---

# Tools and Technologies

| Tool | Purpose |
|------|--------|
| Bitcoin Core | Full Bitcoin node |
| bitcoin-cli | Command line RPC interface |
| Python | Transaction automation |
| python-bitcoinrpc | RPC communication |
| btcdeb | Bitcoin Script debugger |

---

# Bitcoin Node Configuration

The Bitcoin node runs in **Regtest mode**.

### bitcoin.conf

```conf
regtest=1
server=1
rest=1

rpcuser=labuser
rpcpassword=labpass123

paytxfee=0.0001
fallbackfee=0.0002
mintxfee=0.00001
txconfirmtarget=6
```

RPC connection:

```
127.0.0.1:18443
```

---

# Repository Structure

```
CS-216-BlockSmiths-Bitcoin-Transaction-Lab
│
├── main.py
├── part1_legacy_AB.py
├── part1_legacy_BC.py
├── part2_segwit_AB.py
├── part2_segwit_BC.py
│
├── bitcoin.conf
│
├── README.md
│
└── CS216_Bitcoin_Transaction_Lab_Report.pdf
```

The **screenshots folder contains btcdeb execution screenshots and terminal outputs used for script validation.**

---

# Running the Project

## 1 Start Bitcoin Core

Run the node in regtest mode:

```bash
bitcoind -regtest
```

---

## 2 Install Python Dependency

```bash
pip install python-bitcoinrpc
```

---

# Run Legacy Transactions

## A → B Transaction

```bash
python part1_legacy_AB.py
```

This script:

- Creates addresses **A, B, C**
- Mines blocks to generate coins
- Funds address **A**
- Sends BTC from **A → B**
- Signs the raw transaction
- Broadcasts the transaction

---

## B → C Transaction

```bash
python part1_legacy_BC.py
```

This script:

- Selects UTXO belonging to **B**
- Sends BTC from **B → C**
- Signs and broadcasts the transaction

---

# Run SegWit Transactions

## A′ → B′ Transaction

```bash
python part2_segwit_AB.py
```

This script:

- Generates **P2SH-SegWit addresses**
- Mines blocks
- Funds address **A′**
- Sends BTC from **A′ → B′**

---

## B′ → C′ Transaction

```bash
python part2_segwit_BC.py
```

This script:

- Selects UTXO belonging to **B′**
- Sends BTC from **B′ → C′**
- Signs and broadcasts the transaction

---

# Transaction IDs

| Transaction | TXID |
|-------------|------|
| A → B | 90fa1e0f68da256fc248bd7ea51da4e70b44631a15143d6495194ca8805c8a2b |
| B → C | 11566f32f647e1f8a11bb881d4343c5fb6869151893ceb40068e25b9d3e370c8 |
| A′ → B′ | 013c4e28466e0f220703273c4e8c417d152ae3550e1b82f687b1a05572bfbb51 |
| B′ → C′ | e267232dbde285e21156b757e19a0e84e97d445c32acf5e6b514b78a136fc14e |

These transactions were successfully confirmed by mining blocks in the **Regtest network**.

---

# Script Validation using btcdeb

The **Bitcoin Script Debugger (btcdeb)** was used to verify script execution.

For each transaction:

```
scriptSig + scriptPubKey
```

was executed.

The execution stack was traced step-by-step using btcdeb.

Screenshots and debugger outputs are included in the following folders:

```
/screenshots
/script_analysis
```

---

# Legacy Transaction Script

Legacy transactions use **Pay-to-Public-Key-Hash (P2PKH)**.

```
OP_DUP
OP_HASH160
<PubKeyHash>
OP_EQUALVERIFY
OP_CHECKSIG
```

Validation steps:

- Duplicate public key
- Hash public key
- Compare with expected hash
- Verify signature

btcdeb execution ends with:

```
stack = 01
```

which means **TRUE**, confirming transaction validity.

---

# SegWit Transaction Script

SegWit transactions use **P2SH-P2WPKH**.

Validation occurs in two stages.

### Stage 1 — P2SH validation

```
OP_HASH160 <scriptHash> OP_EQUAL
```

The redeem script hash must match the locking script hash.

### Stage 2 — Witness validation

Witness data contains:

```
signature
public key
```

The P2WPKH script verifies the signature using:

```
OP_DUP OP_HASH160 <pubKeyHash> OP_EQUALVERIFY OP_CHECKSIG
```

btcdeb confirms successful execution with:

```
stack = 01
```

---

# Legacy vs SegWit Comparison

| Feature | Legacy | SegWit |
|--------|--------|--------|
| Script Type | P2PKH | P2SH-P2WPKH |
| Signature Location | scriptSig | witness field |
| Transaction Size | Larger | Smaller |
| Fee Efficiency | Lower | Higher |
| Transaction Malleability | Possible | Fixed |
| Block Efficiency | Lower | Higher |

SegWit reduces transaction size by moving signature data into the **witness structure**, improving block capacity and lowering fees.

---

# Conclusion

This project successfully demonstrates:

- Creation of **Legacy Bitcoin transactions**
- Creation of **SegWit Bitcoin transactions**
- Transaction signing using **Bitcoin Core wallet**
- Script execution and debugging using **btcdeb**
- Comparison between **Legacy and SegWit transaction formats**

All transactions were successfully executed and validated on the **Bitcoin Regtest network**.
