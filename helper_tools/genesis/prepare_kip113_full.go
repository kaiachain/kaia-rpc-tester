package main

import (
	"encoding/hex"
	"encoding/json"
	"flag"
	"fmt"
	"os"

	"github.com/kaiachain/kaia/blockchain/system"
	"github.com/kaiachain/kaia/common"
	"github.com/kaiachain/kaia/crypto"
	"github.com/kaiachain/kaia/crypto/bls"
)

func main() {
	var nodekeyHex string
	var blsNodekeyHex string
	var ownerAddr string
	flag.StringVar(&nodekeyHex, "nodekey", "", "Node key in hex format")
	flag.StringVar(&blsNodekeyHex, "bls-nodekey", "", "BLS node key in hex format")
	flag.StringVar(&ownerAddr, "owner", "0x0000000000000000000000000000000000000001", "Owner address")
	flag.Parse()

	if nodekeyHex == "" {
		fmt.Fprintf(os.Stderr, "Error: nodekey is required\n")
		os.Exit(1)
	}

	// Remove 0x prefix if present
	if len(nodekeyHex) >= 2 && nodekeyHex[0:2] == "0x" {
		nodekeyHex = nodekeyHex[2:]
	}

	// Parse private key
	privateKey, err := crypto.HexToECDSA(nodekeyHex)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error: failed to parse nodekey: %v\n", err)
		os.Exit(1)
	}

	// Calculate address from public key
	address := crypto.PubkeyToAddress(privateKey.PublicKey)

	// Calculate BLS public key
	var blsPriv bls.SecretKey
	if blsNodekeyHex != "" {
		// Remove 0x prefix if present
		if len(blsNodekeyHex) >= 2 && blsNodekeyHex[0:2] == "0x" {
			blsNodekeyHex = blsNodekeyHex[2:]
		}
		blsKeyBytes, err := hex.DecodeString(blsNodekeyHex)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error: failed to parse bls-nodekey: %v\n", err)
			os.Exit(1)
		}
		blsPriv, err = bls.SecretKeyFromBytes(blsKeyBytes)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error: failed to parse bls secret key: %v\n", err)
			os.Exit(1)
		}
	} else {
		// Derive from nodekey
		blsPriv, err = bls.DeriveFromECDSA(privateKey)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error: failed to derive BLS key: %v\n", err)
			os.Exit(1)
		}
	}

	blsPub := blsPriv.PublicKey().Marshal()
	blsPop := bls.PopProve(blsPriv).Marshal()

	// Create BlsPublicKeyInfos
	infos := make(system.BlsPublicKeyInfos)
	infos[address] = system.BlsPublicKeyInfo{
		PublicKey: blsPub,
		Pop:       blsPop,
	}

	// Generate storage
	owner := common.HexToAddress(ownerAddr)
	kip113Storage := system.AllocKip113Proxy(system.AllocKip113Init{
		Infos: infos,
		Owner: owner,
	})

	// Proxy storage (implementation slot)
	kip113LogicAddr := common.HexToAddress("0x0000000000000000000000000000000000000403")
	proxyStorage := system.AllocProxy(kip113LogicAddr)

	// Merge proxy and kip113 storage
	proxyStorageMerged := system.MergeStorage(proxyStorage, kip113Storage)

	// Logic storage
	logicStorage := system.AllocKip113Logic()

	// Output as JSON
	proxyStorageJSON := make(map[string]string)
	for k, v := range proxyStorageMerged {
		proxyStorageJSON[k.Hex()] = v.Hex()
	}

	logicStorageJSON := make(map[string]string)
	for k, v := range logicStorage {
		logicStorageJSON[k.Hex()] = v.Hex()
	}

	output := map[string]interface{}{
		"nodeAddress":  address.Hex(),
		"blsPublicKey": hex.EncodeToString(blsPub),
		"blsPop":       hex.EncodeToString(blsPop),
		"proxyStorage": proxyStorageJSON,
		"logicStorage": logicStorageJSON,
		"proxyAddress": "0x0000000000000000000000000000000000000402",
		"logicAddress": "0x0000000000000000000000000000000000000403",
	}

	jsonBytes, err := json.MarshalIndent(output, "", "  ")
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error: failed to marshal JSON: %v\n", err)
		os.Exit(1)
	}

	fmt.Println(string(jsonBytes))
}
