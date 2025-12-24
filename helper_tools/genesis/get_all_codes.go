package main

import (
	"fmt"

	"github.com/kaiachain/kaia/blockchain/system"
	"github.com/kaiachain/kaia/common/hexutil"
)

func main() {
	fmt.Println("RegistryMockCode:")
	fmt.Println(hexutil.Encode(system.RegistryMockCode))
	fmt.Println()
	fmt.Println("ERC1967ProxyCode:")
	fmt.Println(hexutil.Encode(system.ERC1967ProxyCode))
	fmt.Println()
	fmt.Println("Kip113Code:")
	fmt.Println(hexutil.Encode(system.Kip113Code))
}
