rm -rf cn/data/klay/chaindata/ cn/data/klay/LOCK cn/data/klay/transactions.rlp cn/data/keystore/UTC--* *.profile *.trace
cn/bin/kcn init --datadir cn/data genesis.json
cn/bin/kcnd start

# Wait for klay.ipc to be created (timeout: 30 seconds)
echo "Waiting for cn/data/klay.ipc to be created..."
TIMEOUT=30
ELAPSED=0
while [ ! -f cn/data/klay.ipc ] && [ $ELAPSED -lt $TIMEOUT ]; do
    sleep 1
    ELAPSED=$((ELAPSED + 1))
done

if [ -f cn/data/klay.ipc ]; then
    echo "klay.ipc created successfully after ${ELAPSED} seconds"
else
    echo "ERROR: klay.ipc was not created within ${TIMEOUT} seconds"
    exit 1
fi
