from utils import Utils
import json

_, _, log_path = Utils.get_log_filename_with_path()


def send_transaction(endpoint, params):
    transaction_hash, error = Utils.call_rpc(endpoint, "eth_sendTransaction", params, log_path)
    return transaction_hash, error


def get_transaction(endpoint, params):
    transaction, error = Utils.call_rpc(endpoint, "eth_getTransactionByHash", params, log_path)
    return transaction, error


def get_transaction_receipt(endpoint, params):
    receipt, error = Utils.call_rpc(endpoint, "eth_getTransactionReceipt", params, log_path)
    return receipt, error


def get_latest_block_by_number(endpoint):
    method = "eth_getBlockByNumber"
    latest_block, _ = Utils.call_rpc(endpoint, method, ["latest", True], log_path)
    return latest_block


def get_block_number(endpoint):
    method = "eth_blockNumber"
    block_number, _ = Utils.call_rpc(endpoint, method, ["latest", True], log_path)
    return block_number

def get_chain_config(endpoint):
    method = "eth_getChainConfig"
    chain_config, _ = Utils.call_rpc(endpoint, method, [], log_path)
    return chain_config

def checkBaseFeePerGasFieldAndValue(self, result, value=""):
    self.assertIsNotNone(result)
    self.assertIsNotNone(result["baseFeePerGas"])

    if value != "":
        isMagma = get_chain_config(self.endpoint)['magmaCompatibleBlock'] <= int(get_block_number(self.endpoint), 16)
        if isMagma:
            value = "0x5d21dba00"
        else:
            value = "0x0"
        self.assertEqual(result["baseFeePerGas"], value)


def checkGasPriceField(self, result):
    self.assertIsNotNone(result["gasPrice"])
    # TxTypeEthereumDynamicFee: 0x2, TxTypeEthereumBlob: 0x3, TxTypeEthereumSetCode: 0x4
    if result["type"] == "0x2" or result["type"] == "0x3" or result["type"] == "0x4":
        self.assertIsNotNone(result["maxFeePerGas"])
        self.assertIsNotNone(result["maxPriorityFeePerGas"])

def checkBlobField(self, result):
    # TxTypeEthereumBlob: 0x3
    if result["type"] == "0x3":
        self.assertIsNotNone(result["maxFeePerBlobGas"])
        self.assertIsNotNone(result["blobVersionedHashes"])
        self.assertIsNone(result.get("sidecar"))

def checkAuthorizationListField(self, result):
    # TxTypeEthereumSetCode: 0x4
    if result["type"] == "0x4":
        self.assertIsNotNone(result["authorizationList"])

def checkBlobSidecarResult(self, sidecar, blobTx, fullBlob=False):
    self.assertIn("blobSidecar", sidecar)
    self.assertIn("blockHash", sidecar)
    self.assertIn("blockNumber", sidecar)
    self.assertIn("txHash", sidecar)
    self.assertIn("txIndex", sidecar)

    blobSidecar = sidecar["blobSidecar"]
    self.assertIn("version", blobSidecar)
    self.assertIn("blobs", blobSidecar)
    self.assertIn("commitments", blobSidecar)
    self.assertIn("proofs", blobSidecar)

    # Check blob size based on fullBlob flag
    blobs = blobSidecar["blobs"]
    self.assertIsInstance(blobs, list)
    if len(blobs) > 0:
        blob_str = blobs[0]
        self.assertIsInstance(blob_str, str)
        self.assertTrue(blob_str.startswith("0x"))
        if fullBlob:
            # 131072 bytes = 262144 hex characters + 2 for "0x" = 262146 characters total
            self.assertEqual(len(blob_str), 262146)
        else:
            # 32 bytes = 64 hex characters + 2 for "0x" = 66 characters total
            self.assertEqual(len(blob_str), 66)

    self.assertEqual(sidecar["blockHash"], blobTx["result"]["blockHash"])
    self.assertEqual(sidecar["blockNumber"], blobTx["result"]["blockNumber"])
    self.assertEqual(sidecar["txHash"], blobTx["result"]["hash"])
    self.assertEqual(sidecar["txIndex"], blobTx["result"]["index"])

def checkEthereumBlockOrHeaderFormat(self, actualReturn):
    expectedReturn = json.loads(
        """
        {
          "jsonrpc": "2.0",
          "id": 1,
          "result": {
            "baseFeePerGas": "0xf79eb1429",
            "difficulty": "0x29daf6647fd2b7",
            "extraData": "0x75732d656173742d37",
            "gasLimit": "0x1c9c32b",
            "gasUsed": "0x28b484",
            "hash": "0x5de0dc71dec2e724be002dcad135b602810769ce26e16b3b06862405e08ca71b",
            "logsBloom": "0x02200022800002050000084080014015001001004b0002440401060a0830000200014041044010180010430018800119120098000800200241c2090a4020011040004400002201081800440a340020a4000820100848081020003000892050105a05000002100000200012c0800408982000085100000c4040a03814000800200812210100200010004018410d80004214800123210400082002214620100021028800120309200802008291c8e000904210080008110900010100081000101000501002010a0080311886000008000000240900400000100200a402005830200010300804020200000002310000008004004080a58000550000508000000000",
            "miner": "0xea674fdde714fd979de3edf0f56aa9716b898ec8",
            "mixHash": "0x6d266344754999c95ad189f78257d31c276c63c689d864c31fdc62fcb481e5f0",
            "nonce": "0x8b232816a7045c51",
            "number": "0xd208de",
            "parentHash": "0x99fcd33dddd763835ba8bdc842853d973496a7e64ea2f6cf826bc2c338e23b0c",
            "receiptsRoot": "0xd3d70ed54a9274ba3191bf2d4fd8738c5d782fe17c8bfb45c03a25dc04120c35",
            "sha3Uncles": "0x1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347",
            "size": "0x23a",
            "stateRoot": "0x1076e6726164bd6f74720a717242584109f37c55017d004eefccf9ec3be76c18",
            "timestamp": "0x61b0a6c6",
            "uncles": [],
            "transactions": [],
            "transactionsRoot": "0x6ec8daca98c1005d9bbd7716b5e94180e2bf0e6b77770174563a166337369344"
          }
        }
                        """
    )
    ETH_BASEFEE_PER_GAS = "0x5d21dba00"
    ETH_EXTRADATA = "0x"
    ETH_SHA3_UNCLES = "0x1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347"
    ETH_MIX_HASH = "0x0000000000000000000000000000000000000000000000000000000000000000"
    ETH_NONCE = "0x0000000000000000"
    ETH_DIFFICULTY = "0x1"

    immutable_fields = {
        "extraData": ETH_EXTRADATA,
        "sha3Uncles": ETH_SHA3_UNCLES,
        "mixHash": ETH_MIX_HASH,
        "nonce": ETH_NONCE,
        "difficulty": ETH_DIFFICULTY,
    }

    for field in expectedReturn.get("result").keys():
        # check the fields of actualReturn exists also in gethReturn.
        value = expectedReturn.get("result").get(field)
        actualValue = actualReturn.get(field)
        if field in immutable_fields:
            self.assertEqual(immutable_fields.get(field), actualValue)
        elif field == "uncles":
            if actualValue is not None:
                # Uncles must not be existed in actualReturn from Kaia node.
                self.assertTrue(len(actualValue) == 0)
        elif field == "transactions":
            if actualValue is not None:
                for v in actualValue:
                    self.assertTrue(Utils.is_hex(v))
        else:
            self.assertIsNotNone(actualValue)
            self.assertTrue(
                Utils.is_hex(actualValue),
                f"{field} must be a hexadecimal string",
            )
