#!/bin/bash

cat admin/admin_rpc.py \
| sed "s/NamespaceRPC/NamespaceWS/g" \
| sed "s/WebSocket/RPC/g" \
| sed "s/created_by_rpc/created_by_ws/g" \
| sed "s/_, error = Utils.call_rpc/_, error = Utils.call_ws/g" \
| sed "s/result, error = Utils.call_rpc/result, error = Utils.call_ws/g" \
> admin/admin_ws.py

cat debug/debug_rpc.py \
| sed "s/NamespaceRPC/NamespaceWS/g" \
| sed "s/WebSocket/RPC/g" \
| sed "s/created_by_rpc/created_by_ws/g" \
| sed "s/_, error = Utils.call_rpc/_, error = Utils.call_ws/g" \
| sed "s/result, error = Utils.call_rpc/result, error = Utils.call_ws/g" \
> debug/debug_ws.py

cat net/net_rpc.py \
| sed "s/NamespaceRPC/NamespaceWS/g" \
| sed "s/WebSocket/RPC/g" \
| sed "s/created_by_rpc/created_by_ws/g" \
| sed "s/_, error = Utils.call_rpc/_, error = Utils.call_ws/g" \
| sed "s/result, error = Utils.call_rpc/result, error = Utils.call_ws/g" \
> net/net_ws.py

cat personal/personal_rpc.py \
| sed "s/NamespaceRPC/NamespaceWS/g" \
| sed "s/WebSocket/RPC/g" \
| sed "s/created_by_rpc/created_by_ws/g" \
| sed "s/_, error = Utils.call_rpc/_, error = Utils.call_ws/g" \
| sed "s/result, error = Utils.call_rpc/result, error = Utils.call_ws/g" \
> personal/personal_ws.py

cat txpool/txpool_rpc.py \
| sed "s/NamespaceRPC/NamespaceWS/g" \
| sed "s/WebSocket/RPC/g" \
| sed "s/created_by_rpc/created_by_ws/g" \
| sed "s/_, error = Utils.call_rpc/_, error = Utils.call_ws/g" \
| sed "s/result, error = Utils.call_rpc/result, error = Utils.call_ws/g" \
> txpool/txpool_ws.py

cat eth/account/eth_account_rpc.py \
| sed "s/NamespaceAccountRPC/NamespaceAccountWS/g" \
| sed "s/WebSocket/RPC/g" \
| sed "s/created_by_rpc/created_by_ws/g" \
| sed "s/_, error = Utils.call_rpc/_, error = Utils.call_ws/g" \
| sed "s/result, error = Utils.call_rpc/result, error = Utils.call_ws/g" \
> eth/account/eth_account_ws.py

cat eth/block/eth_block_rpc.py \
| sed "s/NamespaceBlockRPC/NamespaceBlockWS/g" \
| sed "s/WebSocket/RPC/g" \
| sed "s/created_by_rpc/created_by_ws/g" \
| sed "s/_, error = Utils.call_rpc/_, error = Utils.call_ws/g" \
| sed "s/result, error = Utils.call_rpc/result, error = Utils.call_ws/g" \
> eth/block/eth_block_ws.py

cat eth/configuration/eth_configuration_rpc.py \
| sed "s/NamespaceConfigurationRPC/NamespaceConfigurationWS/g" \
| sed "s/WebSocket/RPC/g" \
| sed "s/created_by_rpc/created_by_ws/g" \
| sed "s/_, error = Utils.call_rpc/_, error = Utils.call_ws/g" \
| sed "s/result, error = Utils.call_rpc/result, error = Utils.call_ws/g" \
> eth/configuration/eth_configuration_ws.py

cat eth/miscellaneous/eth_miscellaneous_rpc.py \
| sed "s/NamespaceMiscellaneousRPC/NamespaceMiscellaneousWS/g" \
| sed "s/WebSocket/RPC/g" \
| sed "s/created_by_rpc/created_by_ws/g" \
| sed "s/_, error = Utils.call_rpc/_, error = Utils.call_ws/g" \
| sed "s/result, error = Utils.call_rpc/result, error = Utils.call_ws/g" \
> eth/miscellaneous/eth_miscellaneous_ws.py

cat eth/transaction/eth_transaction_rpc.py \
| sed "s/NamespaceTransactionRPC/NamespaceTransactionWS/g" \
| sed "s/WebSocket/RPC/g" \
| sed "s/created_by_rpc/created_by_ws/g" \
| sed "s/_, error = Utils.call_rpc/_, error = Utils.call_ws/g" \
| sed "s/result, error = Utils.call_rpc/result, error = Utils.call_ws/g" \
> eth/transaction/eth_transaction_ws.py

cat eth/filter/eth_filter_rpc.py \
| sed "s/NamespaceFilterRPC/NamespaceFilterWS/g" \
| sed "s/WebSocket/RPC/g" \
| sed "s/created_by_rpc/created_by_ws/g" \
| sed "s/_, error = Utils.call_rpc/_, error = Utils.call_ws/g" \
| sed "s/result, error = Utils.call_rpc/result, error = Utils.call_ws/g" \
> eth/filter/eth_filter_ws.py

cat kaia/account/kaia_account_rpc.py \
| sed "s/NamespaceAccountRPC/NamespaceAccountWS/g" \
| sed "s/WebSocket/RPC/g" \
| sed "s/created_by_rpc/created_by_ws/g" \
| sed "s/_, error = Utils.call_rpc/_, error = Utils.call_ws/g" \
| sed "s/result, error = Utils.call_rpc/result, error = Utils.call_ws/g" \
> kaia/account/kaia_account_ws.py

cat kaia/block/kaia_block_rpc.py \
| sed "s/NamespaceBlockRPC/NamespaceBlockWS/g" \
| sed "s/WebSocket/RPC/g" \
| sed "s/created_by_rpc/created_by_ws/g" \
| sed "s/_, error = Utils.call_rpc/_, error = Utils.call_ws/g" \
| sed "s/result, error = Utils.call_rpc/result, error = Utils.call_ws/g" \
> kaia/block/kaia_block_ws.py

cat kaia/configuration/kaia_configuration_rpc.py \
| sed "s/NamespaceConfigurationRPC/NamespaceConfigurationWS/g" \
| sed "s/WebSocket/RPC/g" \
| sed "s/created_by_rpc/created_by_ws/g" \
| sed "s/_, error = Utils.call_rpc/_, error = Utils.call_ws/g" \
| sed "s/result, error = Utils.call_rpc/result, error = Utils.call_ws/g" \
> kaia/configuration/kaia_configuration_ws.py

cat kaia/miscellaneous/kaia_miscellaneous_rpc.py \
| sed "s/NamespaceMiscellaneousRPC/NamespaceMiscellaneousWS/g" \
| sed "s/WebSocket/RPC/g" \
| sed "s/created_by_rpc/created_by_ws/g" \
| sed "s/_, error = Utils.call_rpc/_, error = Utils.call_ws/g" \
| sed "s/result, error = Utils.call_rpc/result, error = Utils.call_ws/g" \
> kaia/miscellaneous/kaia_miscellaneous_ws.py

cat kaia/transaction/kaia_transaction_rpc.py \
| sed "s/NamespaceTransactionRPC/NamespaceTransactionWS/g" \
| sed "s/WebSocket/RPC/g" \
| sed "s/created_by_rpc/created_by_ws/g" \
| sed "s/_, error = Utils.call_rpc/_, error = Utils.call_ws/g" \
| sed "s/result, error = Utils.call_rpc/result, error = Utils.call_ws/g" \
> kaia/transaction/kaia_transaction_ws.py

cat kaia/filter/kaia_filter_rpc.py \
| sed "s/NamespaceFilterRPC/NamespaceFilterWS/g" \
| sed "s/WebSocket/RPC/g" \
| sed "s/created_by_rpc/created_by_ws/g" \
| sed "s/_, error = Utils.call_rpc/_, error = Utils.call_ws/g" \
| sed "s/result, error = Utils.call_rpc/result, error = Utils.call_ws/g" \
> kaia/filter/kaia_filter_ws.py

cat eth/gas/eth_gas_rpc.py \
| sed "s/NamespaceGasRPC/NamespaceGasWS/g" \
| sed "s/WebSocket/RPC/g" \
| sed "s/created_by_rpc/created_by_ws/g" \
| sed "s/_, error = Utils.call_rpc/_, error = Utils.call_ws/g" \
| sed "s/result, error = Utils.call_rpc/result, error = Utils.call_ws/g" \
> eth/gas/eth_gas_ws.py

cat kaia/gas/kaia_gas_rpc.py \
| sed "s/NamespaceGasRPC/NamespaceGasWS/g" \
| sed "s/WebSocket/RPC/g" \
| sed "s/created_by_rpc/created_by_ws/g" \
| sed "s/_, error = Utils.call_rpc/_, error = Utils.call_ws/g" \
| sed "s/result, error = Utils.call_rpc/result, error = Utils.call_ws/g" \
> kaia/gas/kaia_gas_ws.py
