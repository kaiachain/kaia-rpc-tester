package main

import (
	"bytes"
	"crypto/sha256"
	"flag"
	"fmt"
	"hash"
	"math/big"
	"os"

	"github.com/kaiachain/kaia/blockchain/types"
	"github.com/kaiachain/kaia/common"
	"github.com/kaiachain/kaia/common/hexutil"
	"github.com/kaiachain/kaia/crypto"
	"github.com/kaiachain/kaia/crypto/kzg4844"
)

const BLOB_SIZE = 131072 // 4096 * 32 bytes

func main() {
	var (
		blobFilePath  string
		chainID       int64
		nonce         uint64
		to            string
		gasLimit      uint64
		gasTipCap     int64
		gasFeeCap     int64
		blobFeeCap    int64
		value         int64
		privateKeyHex string
	)
	flag.StringVar(&blobFilePath, "blob", "", "Path to blob file")
	flag.Int64Var(&chainID, "chainid", 1, "Chain ID")
	flag.Uint64Var(&nonce, "nonce", 0, "Nonce")
	flag.StringVar(&to, "to", "", "Recipient address")
	flag.Uint64Var(&gasLimit, "gas", 21000, "Gas limit")
	flag.Int64Var(&gasTipCap, "gasTipCap", 1, "Gas tip cap")
	flag.Int64Var(&gasFeeCap, "gasFeeCap", 1, "Gas fee cap")
	flag.Int64Var(&blobFeeCap, "blobFeeCap", 1, "Blob fee cap")
	flag.Int64Var(&value, "value", 0, "Value")
	flag.StringVar(&privateKeyHex, "privateKey", "", "Private key in hex format (with or without 0x prefix)")
	flag.Parse()

	if blobFilePath == "" {
		fmt.Fprintf(os.Stderr, "Error: blob file path is required\n")
		os.Exit(1)
	}

	// Read blob data from file
	blobData, err := os.ReadFile(blobFilePath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error: failed to read blob file: %v\n", err)
		os.Exit(1)
	}

	// Blob must be exactly 131072 bytes (4096 * 32 bytes)
	if len(blobData) < BLOB_SIZE {
		// Pad with zeros if needed
		padded := make([]byte, BLOB_SIZE)
		copy(padded, blobData)
		blobData = padded
	} else if len(blobData) > BLOB_SIZE {
		// Truncate if too large
		blobData = blobData[:BLOB_SIZE]
	}

	// Convert to kzg4844.Blob
	var blob kzg4844.Blob
	copy(blob[:], blobData)

	// Generate commitment and cell proofs (for version 1 sidecar)
	var (
		commitment, _ = kzg4844.BlobToCommitment(&blob)
		cellProofs, _ = kzg4844.ComputeCellProofs(&blob)
	)

	// Calculate blob versioned hash
	var hasher hash.Hash = sha256.New()
	blobHash := kzg4844.CalcBlobHashV1(hasher, &commitment)

	// Parse recipient address
	var recipient common.Address
	if to != "" {
		recipient = common.HexToAddress(to)
	}

	// Create sidecar
	sidecar := types.NewBlobTxSidecar(
		byte(1), // BlobSidecarVersion1
		[]kzg4844.Blob{blob},
		[]kzg4844.Commitment{commitment},
		cellProofs,
	)

	// Create TxInternalDataEthereumBlob using NewTransactionWithMap
	chainIDBig := big.NewInt(chainID)
	gasTipCapBig := big.NewInt(gasTipCap)
	gasFeeCapBig := big.NewInt(gasFeeCap)
	blobFeeCapBig := big.NewInt(blobFeeCap)
	valueBig := big.NewInt(value)

	txValues := map[types.TxValueKeyType]interface{}{
		types.TxValueKeyChainID:    chainIDBig,
		types.TxValueKeyNonce:      nonce,
		types.TxValueKeyTo:         recipient,
		types.TxValueKeyAmount:     valueBig,
		types.TxValueKeyGasLimit:   gasLimit,
		types.TxValueKeyGasTipCap:  gasTipCapBig,
		types.TxValueKeyGasFeeCap:  gasFeeCapBig,
		types.TxValueKeyBlobFeeCap: blobFeeCapBig,
		types.TxValueKeyBlobHashes: []common.Hash{common.Hash(blobHash)},
		types.TxValueKeySidecar:    sidecar,
		types.TxValueKeyAccessList: types.AccessList{},
		types.TxValueKeyData:       []byte{},
	}

	tx, err := types.NewTransactionWithMap(types.TxTypeEthereumBlob, txValues)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error: failed to create transaction: %v\n", err)
		os.Exit(1)
	}

	// Sign the transaction if private key is provided
	if privateKeyHex != "" {
		// Parse private key
		privateKeyBytes := common.FromHex(privateKeyHex)
		if len(privateKeyBytes) != 32 {
			fmt.Fprintf(os.Stderr, "Error: invalid private key length\n")
			os.Exit(1)
		}

		privateKey, err := crypto.ToECDSA(privateKeyBytes)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error: failed to parse private key: %v\n", err)
			os.Exit(1)
		}

		// Create signer
		signer := types.NewOsakaSigner(chainIDBig)

		// Sign the transaction
		signedTx, err := types.SignTx(tx, signer, privateKey)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error: failed to sign transaction: %v\n", err)
			os.Exit(1)
		}
		tx = signedTx
	}

	// Encode the transaction to RLP
	var buf bytes.Buffer
	if err := tx.EncodeRLP(&buf); err != nil {
		fmt.Fprintf(os.Stderr, "Error: failed to RLP encode transaction: %v\n", err)
		os.Exit(1)
	}

	// Output hex-encoded RLP data
	encoded := hexutil.Encode(buf.Bytes())
	os.Stdout.WriteString(encoded)
	os.Stdout.WriteString("\n")
}
