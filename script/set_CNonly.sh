rm -rf cn/data/kaia/chaindata/ network-local/cn/data/kaia/LOCK network-local/cn/data/kaia/transactions.rlp
cn/bin/kcn init --datadir cn/data genesis.json
./cn/bin/kcnd start
