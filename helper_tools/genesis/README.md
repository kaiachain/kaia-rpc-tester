# Genesis Configuration Tools

This directory contains utility tools for configuring the `genesis.json` file for the Kaia blockchain.

## Overview

These tools are used to generate and configure the following components required for the Kaia blockchain genesis file:

- **Registry Contract** (0x0000000000000000000000000000000000000401)
- **KIP113 Proxy Contract** (0x0000000000000000000000000000000000000402)
- **KIP113 Logic Contract** (0x0000000000000000000000000000000000000403)

## Tools

### Go Utilities

#### 1. `get_all_codes.go`
Retrieves the bytecode for all contracts.

**Usage:**
```bash
cd helper_tools/genesis
go run get_all_codes.go
```

**Output:**
- `RegistryMockCode`: Registry contract bytecode
- `ERC1967ProxyCode`: ERC1967 Proxy contract bytecode
- `Kip113Code`: KIP113 Logic contract bytecode

#### 2. `prepare_registry_storage.go`
Generates storage for the Registry contract.

**Usage:**
```bash
go run prepare_registry_storage.go \
  -owner 0x0000000000000000000000000000000000000001 \
  -kip113 0x0000000000000000000000000000000000000402
```

**Options:**
- `-owner`: Owner address (default: `0x0000000000000000000000000000000000000001`)
- `-kip113`: KIP113 Proxy address (default: `0x0000000000000000000000000000000000000402`)

**Output:**
Outputs Registry storage in JSON format.

#### 3. `prepare_kip113_full.go`
Generates complete storage for KIP113 Proxy and Logic contracts.

**Usage:**
```bash
go run prepare_kip113_full.go \
  -nodekey <nodekey_hex> \
  -bls-nodekey <bls_nodekey_hex> \
  -owner 0x0000000000000000000000000000000000000001
```

**Options:**
- `-nodekey`: Node key in hex format (required)
- `-bls-nodekey`: BLS node key in hex format (optional, derived from nodekey if not specified)
- `-owner`: Owner address (default: `0x0000000000000000000000000000000000000001`)

**Output:**
Outputs the following in JSON format:
- `nodeAddress`: Node address
- `blsPublicKey`: BLS public key
- `blsPop`: BLS Proof of Possession
- `proxyStorage`: KIP113 Proxy storage
- `logicStorage`: KIP113 Logic storage
- `proxyAddress`: Proxy address (0x0000000000000000000000000000000000000402)
- `logicAddress`: Logic address (0x0000000000000000000000000000000000000403)

### Python Utilities

#### 4. `fix_genesis_hex.py`
Fixes odd-length hex strings in `genesis.json`.

**Usage:**
```bash
python3 fix_genesis_hex.py
```

This script automatically checks `script/genesis.json` and outputs a fixed version to `script/genesis.json.fixed` if odd-length hex strings are found.

**Features:**
- Detects odd-length hex strings in `alloc.code` fields
- Pads with leading zero to make them even-length
- Outputs the fixed file

#### 5. `update_genesis_from_output.py`
Updates `genesis.json` using the output from Go utilities.

**Usage:**
```bash
python3 update_genesis_from_output.py
```

**Features:**
- Updates Registry contract code and storage
- Updates KIP113 Proxy contract code and storage
- Updates KIP113 Logic contract code and storage
- Updates `randaoRegistry` configuration

**Note:** This script uses hardcoded values from the output of `get_all_codes.go`, `prepare_registry_storage.go`, and `prepare_kip113_full.go`. To use actual values, update the values in the script.

## Typical Workflow

1. **Get contract codes:**
   ```bash
   go run get_all_codes.go
   ```
   Update the values in `update_genesis_from_output.py` with the output.

2. **Generate Registry storage:**
   ```bash
   go run prepare_registry_storage.go -owner <owner_address>
   ```
   Update the values in `update_genesis_from_output.py` with the output.

3. **Generate KIP113 storage:**
   ```bash
   go run prepare_kip113_full.go -nodekey <nodekey_hex> -owner <owner_address>
   ```
   Update the values in `update_genesis_from_output.py` with the output.

4. **Update genesis.json:**
   ```bash
   python3 update_genesis_from_output.py
   ```

5. **Fix hex strings (if needed):**
   ```bash
   python3 fix_genesis_hex.py
   ```

## Dependencies

### Go Tools
- `github.com/kaiachain/kaia/blockchain/system`
- `github.com/kaiachain/kaia/common`
- `github.com/kaiachain/kaia/crypto`
- `github.com/kaiachain/kaia/crypto/bls`
- `github.com/kaiachain/kaia/params`

### Python Tools
- Python 3.x
- Standard library only (no additional dependencies)

## Notes

- These tools are specialized for Kaia blockchain genesis configuration
- `update_genesis_from_output.py` uses hardcoded values, so you need to update them according to your actual environment
- `fix_genesis_hex.py` only fixes `alloc.code` fields in `genesis.json`
- All addresses use fixed addresses (system contract addresses)

## Related Files

- `script/genesis.json`: Main genesis configuration file
- `github.com/kaiachain/kaia/blockchain/system/constant.go`: System contract constant definitions

