# Kaia RPC-tester

The tester checks basic operations of Kaia RPC/WebSocket APIs.

## How to Setup the Test

*Note: If you use python3.13.x, the installation of requirements.txt will fail for wheel compatibility. Please use a different 3.x.*

### Install Python Libraries
* Python3 should be installed: `python3`
* Create virtual environment: `python3 -m venv venv`
* Activate virtualenv: `source venv/bin/activate`
* Install python libraries: `pip install -r requirements.txt`

### Run the private network
* Copy `config_template.json` as `config.json`
* cd `script` directory. Cautious, below commands will only work at the `script` directory.
* First of all, locate the kcn binary file which has the target test version inside the `cn/bin`. (e.g. kaia-v1.0.1). You can utilize the below script.
* Then, run the provided script to deploy cn1 private network in your local environment: `./set_CNonly.sh`
* Check the log to see the network works well: `tail -f cn/data/kcn/logs/kcnd.out`
* Generate block.rlp: `cn/bin/kcn --exec "debug.getBlockRlp(5)" attach cn/data/klay.ipc | sed 's/"//g' > cn/data/block.rlp` (you can change the block number for block rlp)
For the kcn binary file, if you want to use prebuilt binary, locate next script under `script` directory and run it. You can change the VERSION.
```script
VERSION="v1.0.1"

OS=$(uname -s | tr '[:upper:]' '[:lower:]') # Linux or Darwin
if [ ${OS} = "darwin" ]; then
  URL="https://packages.kaia.io/kaia/${VERSION}/kcn-${VERSION}-0-${OS}-arm64.tar.gz"
else
  URL="https://packages.kaia.io/kaia/${VERSION}/kcn-${VERSION}-0-${OS}-amd64.tar.gz"
fi
echo $URL
wget ${URL} -O bin.tar.gz && tar -xvf bin.tar.gz && mv kcn-*/bin/kcn cn/bin/kcn
rm -rf kcn-* bin.tar.gz
echo "Download complete and moved to cn/bin"
```

If the `set_CNonly.sh` script doesn't work, please run your own EN. If script works, go to `Usage-1`. Then, when finished, check the result(`Usage-4`).
It is fully tested in macos environment, but not in linux.

### Requirement EN (to be tested)
- Faucet Account: You should provide an account which has enough amount KAIA for the test.

- Options: You should give next flags. You can refer script/cn/conf/kcnd.conf file.
  1. `--rpc --rpcapi admin,debug,kaia,eth,miner,net,personal,rpc,txpool,web3 --rpcport 8551 --rpcaddr 0.0.0.0`
  2. `--ws --wsapi admin,debug,kaia,eth,miner,net,personal,rpc,txpool,web3 --wsport 8552 --wsaddr 0.0.0.0`
  3. `--sendertxhashindexing --vmdebug --txpool.allow-local-anchortx`

- `block.rlp`: It should be placed at the EN excution path. The content of `block.rlp` is needed to be updated with the return value of `
  debug_getblockrlp` API.

## Usage
### 0. Set config.json and run generate_ws_from_rpc.sh
`config.json` - The information of EN and the faucet account and fee payer account (both account should have enough KAIA).
```json
{
    "endpoint": "localhost",
    "rpcPort": "8551",
    "wsPort": "8552",
    "chainId": "2019",
    "faucetPrivateKey": "752a08fd165dcc7f37f3e444cf485c5b2020e4096a2cfd02f823a8b8280baaab",
    "faucetAddress": "0xf77e71cf745e14129a344bcfb7e28240a5351beb",
    "faucetPassword": "2524",
    "feePayerPrivateKey": "752a08fd165dcc7f37f3e444cf485c5b2020e4096a2cfd02f823a8b8280baaab",
    "feePayerAddress": "0xf77e71cf745e14129a344bcfb7e28240a5351beb",
    "feePayerPassword": "2524",
    "namespaces": "admin,debug,personal,txpool,eth,kaia"
}
```

`generate-ws_from_rpc.sh` - The script to change protocol `rpc` to `websocket` used by test script. You need to run this script if you have any updates on `{namespace}/*_rpc.py`
 

### 1. Run all tests
```shell
rpc-tester$ source ./venv/bin/activate
(venv) rpc-tester$ python main.py 
```

### 2. Run specific namespace
Change namespaces field of `config.json` file. If you want to run tests about debug and net namespaces, change the value to `debug,net`.

Others are same with "1. Run all tests".

### 3. Run tests for rpc or websocket
If you want to run tests for specific protocol, you can do like below.
```shell
# Run tests only by rpc
(venv) rpc-tester$ python main.py --protocol rpc
# Run tests only by websocket
(venv) rpc-tester$ python main.py --protocol ws
```

### 4. Check test result
The html test report will be created under `testReport` directory. You can drag the file to the browser and read it.
```script
$ ls testReport 
KaiaTestReport_2024-07-23_14-09-44.html
```

# Project structure overview

```shell
.
├── README.md
├── admin
│   ├── admin_rpc.py
│   └── admin_ws.py
├── block.rlp
├── common # This contains common functions which will be used by many test scripts commonly.
│   ├── kaia.py # functions can be used by multiple tests cases with kaia namespace
│   ├── net.py # functions can be used by multiple tests cases with net namespace
│   └── personal.py # functions can be used by multiple tests cases with personal namespace
├── config.json # config file used during tests.
├── config_template.json
├── debug # This contains test scripts about `debug` namespace.
│   ├── block.rlp
│   ├── debug_rpc.py
│   └── debug_ws.py
├── errors.py # This contains expected errors occurred during tests. This is shared resource regardless of namespace.
├── eth # This contains test scripts about `eth` namespace.
│   ├── account
│   │   ├── eth_account_rpc.py
│   │   └── eth_account_ws.py
│   ├── block
│   │   ├── eth_block_rpc.py
│   │   └── eth_block_ws.py
│   ├── configuration
│   │   ├── eth_configuration_rpc.py
│   │   └── eth_configuration_ws.py
│   ├── filter
│   │   ├── eth_filter_rpc.py
│   │   └── eth_filter_ws.py
│   ├── gas
│   │   └── eth_gas_rpc.py
│   ├── miscellaneous
│   │   ├── eth_miscellaneous_rpc.py
│   │   └── eth_miscellaneous_ws.py
│   └── transaction
│   │   ├── eth_transaction_rpc.py
│   │   └── eth_transaction_ws.py
├── generate_ws_from_rpc.sh
├── kaia # This contains test scripts about `kaia` namespace.
│   ├── account
│   │   ├── kaia_account_rpc.py
│   │   └── kaia_account_ws.py
│   ├── block
│   │   ├── kaia_block_rpc.py
│   │   └── kaia_block_ws.py
│   ├── configuration
│   │   ├── kaia_configuration_rpc.py
│   │   └── kaia_configuration_ws.py
│   ├── filter
│   │   ├── kaia_filter_rpc.py
│   │   └── kaia_filter_ws.py
│   ├── miscellaneous
│   │   ├── kaia_miscellaneous_rpc.py
│   │   └── kaia_miscellaneous_ws.py
│   └── transaction
│   │   ├── kaia_transaction_rpc.py
│   │   └── kaia_transaction_ws.py
├── main.py # Run tests by executing main.py
├── net # This contains test scripts about `net` namespace.
│   ├── net_rpc.py
│   └── net_ws.py
├── personal # This contains test scripts about `personal` namespace.
│   ├── personal_rpc.py
│   └── personal_ws.py
├── reports # Contains logs created during each run
├── requirements.txt
├── rpc_tester.egg-info # This is created by executing `pip install -e .`
│   ├── PKG-INFO
│   ├── SOURCES.txt
│   ├── dependency_links.txt
│   └── top_level.txt
├── setup.py 
├── testReport # Contains HTML test reports
├── test_data.py # Contains some constants. This values doesn't need to be initialized.
├── txpool # This contains test scripts about `net` namespace.
│   ├── txpool_rpc.py
│   └── txpool_ws.py
├── utils.py # The Utils class which will be used by many test cases.
├── pre-commit # Place this script to .git/hooks/pre-commit when you maintain this project.
└── venv # Virtual env
```

## Caution

It doesn't test full functionality of APIs, but basic operations.
To maintain this project, please place pre-commit on .git/hooks/pre-commit
