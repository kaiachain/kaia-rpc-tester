package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"

	"github.com/kaiachain/kaia/blockchain/system"
	"github.com/kaiachain/kaia/common"
	"github.com/kaiachain/kaia/params"
)

func main() {
	var ownerAddr string
	var kip113Addr string
	flag.StringVar(&ownerAddr, "owner", "0x0000000000000000000000000000000000000001", "Owner address")
	flag.StringVar(&kip113Addr, "kip113", "0x0000000000000000000000000000000000000402", "KIP113 address")
	flag.Parse()

	owner := common.HexToAddress(ownerAddr)
	kip113 := common.HexToAddress(kip113Addr)

	// Generate Registry storage
	registryStorage := system.AllocRegistry(&params.RegistryConfig{
		Records: map[string]common.Address{
			system.Kip113Name: kip113,
		},
		Owner: owner,
	})

	// Output as JSON
	storageJSON := make(map[string]string)
	for k, v := range registryStorage {
		storageJSON[k.Hex()] = v.Hex()
	}

	output := map[string]interface{}{
		"registryAddress": "0x0000000000000000000000000000000000000401",
		"kip113Address":   kip113Addr,
		"owner":           ownerAddr,
		"storage":         storageJSON,
	}

	jsonBytes, err := json.MarshalIndent(output, "", "  ")
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error: failed to marshal JSON: %v\n", err)
		os.Exit(1)
	}

	fmt.Println(string(jsonBytes))
}
