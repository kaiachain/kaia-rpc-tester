import unittest
from unittest import result
from utils import Utils
from common import kaia as kaia_common

# test_data_set is injected by rpc-tester/main.py
global test_data_set


class TestKaiaNamespaceBlockRPC(unittest.TestCase):
    config = Utils.get_config()
    _, _, log_path = Utils.get_log_filename_with_path()
    endpoint = config.get("endpoint")
    rpc_port = config.get("rpcPort")
    ws_port = config.get("wsPort")
    ns = "kaia"
    waiting_count = 2

    def test_kaia_syncing_success_wrong_value_param(self):
        method = f"{self.ns}_syncing"
        _, error = Utils.call_rpc(self.endpoint, method, ["abcd"], self.log_path)
        self.assertIsNone(error)

    def test_kaia_syncing_success(self):
        method = f"{self.ns}_syncing"
        _, error = Utils.call_rpc(self.endpoint, method, [], self.log_path)
        self.assertIsNone(error)

    def test_kaia_blockNumber_success(self):
        method = f"{self.ns}_blockNumber"
        params = []
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_kaia_blockNumber_success_wrong_value_param(self):
        method = f"{self.ns}_blockNumber"
        params = ["abcd"]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_kaia_getStorageAt_error_no_param(self):
        method = f"{self.ns}_getStorageAt"
        contract = test_data_set["contracts"]["unknown"]["address"][0]
        position = "0x0"
        tag = "latest"
        params = []
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

    def test_kaia_getStorageAt_error_wrong_type_param1(self):
        method = f"{self.ns}_getStorageAt"
        contract = test_data_set["contracts"]["unknown"]["address"][0]
        position = "0x0"
        tag = "latest"
        params = ["contract", position, tag]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0HexToAddress", error)

    def test_kaia_getStorageAt_error_wrong_type_param2(self):
        method = f"{self.ns}_getStorageAt"
        contract = test_data_set["contracts"]["unknown"]["address"][0]
        position = "0x0"
        tag = "latest"
        params = [contract, position, "0xffffffff"]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "HeaderNotExist", error)

    def test_kaia_getStorageAt_success_wrong_value_param(self):
        method = f"{self.ns}_getStorageAt"
        contract = test_data_set["contracts"]["unknown"]["address"][0]
        position = "0x0"
        tag = "latest"
        params = [contract, "position", tag]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_kaia_getStorageAt_success(self):
        method = f"{self.ns}_getStorageAt"
        contract = test_data_set["contracts"]["unknown"]["address"][0]
        position = "0x0"
        tag = "latest"
        params = [contract, position, tag]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_kaia_getBlockTransactionCountByHash_error_no_param(self):
        txFrom = test_data_set["account"]["sender"]["address"]
        txTo = test_data_set["account"]["receiver"]["address"]
        txGas = hex(30400)
        txGasPrice = test_data_set["unitGasPrice"]
        txValue = hex(500000000000)
        params = [
            {
                "from": txFrom,
                "to": txTo,
                "gas": txGas,
                "gasPrice": txGasPrice,
                "value": txValue,
            }
        ]
        transaction_hash, error = kaia_common.send_transaction(self.endpoint, params)
        self.assertIsNone(error)

        Utils.waiting_count("Waiting for", 5, "seconds to connect with a peer.")

        result, error = kaia_common.get_transaction(self.endpoint, [transaction_hash])
        self.assertIsNone(error)
        hashOfBlock = result["blockHash"]
        blockNumber = result["blockNumber"]

        method = f"{self.ns}_getBlockTransactionCountByHash"
        params = []
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

    def test_kaia_getBlockTransactionCountByHash_error_wrong_type_param(self):
        txFrom = test_data_set["account"]["sender"]["address"]
        txTo = test_data_set["account"]["receiver"]["address"]
        txGas = hex(30400)
        txGasPrice = test_data_set["unitGasPrice"]
        txValue = hex(500000000000)
        params = [
            {
                "from": txFrom,
                "to": txTo,
                "gas": txGas,
                "gasPrice": txGasPrice,
                "value": txValue,
            }
        ]
        transaction_hash, error = kaia_common.send_transaction(self.endpoint, params)
        self.assertIsNone(error)

        Utils.waiting_count("Waiting for", 5, "seconds to connect with a peer.")

        result, error = kaia_common.get_transaction(self.endpoint, [transaction_hash])
        self.assertIsNone(error)
        hashOfBlock = result["blockHash"]
        blockNumber = result["blockNumber"]

        method = f"{self.ns}_getBlockTransactionCountByHash"
        params = [1234]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0NonstringToHash", error)

    def test_kaia_getBlockTransactionCountByHash_error_wrong_value_param(self):
        txFrom = test_data_set["account"]["sender"]["address"]
        txTo = test_data_set["account"]["receiver"]["address"]
        txGas = hex(30400)
        txGasPrice = test_data_set["unitGasPrice"]
        txValue = hex(500000000000)
        params = [
            {
                "from": txFrom,
                "to": txTo,
                "gas": txGas,
                "gasPrice": txGasPrice,
                "value": txValue,
            }
        ]
        transaction_hash, error = kaia_common.send_transaction(self.endpoint, params)
        self.assertIsNone(error)

        Utils.waiting_count("Waiting for", 5, "seconds to connect with a peer.")

        result, error = kaia_common.get_transaction(self.endpoint, [transaction_hash])
        self.assertIsNone(error)
        hashOfBlock = result["blockHash"]
        blockNumber = result["blockNumber"]

        method = f"{self.ns}_getBlockTransactionCountByHash"
        params = ["0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "BlockDoesNotExist", error)

    def test_kaia_getBlockTransactionCountByHash_success(self):
        txFrom = test_data_set["account"]["sender"]["address"]
        txTo = test_data_set["account"]["receiver"]["address"]
        txGas = hex(30400)
        txGasPrice = test_data_set["unitGasPrice"]
        txValue = hex(500000000000)
        params = [
            {
                "from": txFrom,
                "to": txTo,
                "gas": txGas,
                "gasPrice": txGasPrice,
                "value": txValue,
            }
        ]
        transaction_hash, error = kaia_common.send_transaction(self.endpoint, params)
        self.assertIsNone(error)

        Utils.waiting_count("Waiting for", 5, "seconds to connect with a peer.")

        result, error = kaia_common.get_transaction(self.endpoint, [transaction_hash])
        self.assertIsNone(error)
        hashOfBlock = result["blockHash"]
        blockNumber = result["blockNumber"]

        method = f"{self.ns}_getBlockTransactionCountByHash"
        params = [hashOfBlock]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_kaia_getBlockTransactionCountByNumber_error_no_param(self):
        method = f"{self.ns}_getBlockTransactionCountByNumber"
        params = []
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

    def test_kaia_getBlockTransactionCountByNumber_error_wrong_type_param(self):
        method = f"{self.ns}_getBlockTransactionCountByNumber"
        params = ["blocknumber"]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0HexWithoutPrefix", error)

    def test_kaia_getBlockTransactionCountByNumber_error_wrong_value_param(self):
        method = f"{self.ns}_getBlockTransactionCountByNumber"
        params = ["0xffffffff"]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "BlockNotExist", error)

    def test_kaia_getBlockTransactionCountByNumber_success(self):
        blockNumber = kaia_common.get_block_number(self.endpoint)
        method = f"{self.ns}_getBlockTransactionCountByNumber"
        params = [blockNumber]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_kaia_getBlockByHash_error_no_param(self):
        method = f"{self.ns}_getBlockByNumber"
        num = "latest"
        params = [num, True]
        result, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNotNone(result)
        blockHash = result["hash"]

        method = f"{self.ns}_getBlockByHash"
        params = []
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

    def test_kaia_getBlockByHash_error_wrong_type_param1(self):
        method = f"{self.ns}_getBlockByNumber"
        num = "latest"
        params = [num, True]
        result, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNotNone(result)
        blockHash = result["hash"]

        method = f"{self.ns}_getBlockByHash"
        params = [True, True]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0NonstringToHash", error)

    def test_kaia_getBlockByHash_error_wrong_type_param2(self):
        method = f"{self.ns}_getBlockByNumber"
        num = "latest"
        params = [num, True]
        result, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNotNone(result)
        blockHash = result["hash"]

        method = f"{self.ns}_getBlockByHash"
        params = [blockHash, "True"]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg1StringToBool", error)

    def test_kaia_getBlockByHash_error_wrong_value_param(self):
        method = f"{self.ns}_getBlockByNumber"
        num = "latest"
        params = [num, True]
        result, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNotNone(result)
        blockHash = result["hash"]

        method = f"{self.ns}_getBlockByHash"
        params = [
            "0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
            True,
        ]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "BlockDoesNotExist", error)

    def test_kaia_getBlockByHash_success(self):
        method = f"{self.ns}_getBlockByNumber"
        num = "latest"
        params = [num, True]
        result, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)
        kaia_common.checkBaseFeePerGasFieldAndValue(self, result)
        blockHash = result["hash"]

        method = f"{self.ns}_getBlockByHash"
        params = [blockHash, True]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)
        kaia_common.checkBaseFeePerGasFieldAndValue(self, result)

    def test_kaia_getBlockByNumber_error_no_param(self):
        method = f"{self.ns}_getBlockByNumber"
        num = "latest"
        params = []
        _, error = kaia_common.send_transaction(self.endpoint, params)
        Utils.check_error(self, "arg0NoParams", error)

    def test_kaia_getBlockByNumber_error_wrong_type_param1(self):
        method = f"{self.ns}_getBlockByNumber"
        num = "latest"
        params = [True, True]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0HexWithoutPrefix", error)

    def test_kaia_getBlockByNumber_error_wrong_type_param2(self):
        method = f"{self.ns}_getBlockByNumber"
        num = "latest"
        params = [num, "True"]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg1StringToBool", error)

    def test_kaia_getBlockByNumber_error_wrong_value_param1(self):
        method = f"{self.ns}_getBlockByNumber"
        num = "latest"
        params = ["num", True]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0HexWithoutPrefix", error)

    def test_kaia_getBlockByNumber_error_wrong_value_param2(self):
        method = f"{self.ns}_getBlockByNumber"
        num = "latest"
        params = ["0xffffffff", True]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "BlockNotExist", error)

    def test_kaia_getBlockByNumber_success(self):
        method = f"{self.ns}_getBlockByNumber"
        num = "latest"
        params = [num, True]
        result, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)
        kaia_common.checkBaseFeePerGasFieldAndValue(self, result)

        # before kip71 hardfork
        num = "0x1"
        params = [num, True]
        result, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)
        kaia_common.checkBaseFeePerGasFieldAndValue(self, result, "0x0")
        # self.assertEqual(result["baseFeePerGas"], "0x0")

    def test_kaia_getBlockReceipts_error_no_param(self):
        method = f"{self.ns}_getBlockReceipts"
        params = []
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

    def test_kaia_getBlockReceipts_error_wrong_type_param(self):
        method = f"{self.ns}_getBlockReceipts"
        params = ["abcd"]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0HexWithoutPrefix", error)

    def test_kaia_getBlockReceipts_fail_wrong_value_param(self):
        method = f"{self.ns}_getBlockReceipts"
        params = ["0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "BlockDoesNotExist", error)

    def test_kaia_getBlockReceipts_success(self):
        method = f"{self.ns}_getBlockReceipts"
        params = [10]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_kaia_getHeaderByHash_error_no_param(self):
        method = f"{self.ns}_getHeaderByNumber"
        num = "latest"
        params = [num]
        result, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNotNone(result)
        blockHash = result["hash"]

        method = f"{self.ns}_getHeaderByHash"
        params = []
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

    def test_kaia_getHeaderByHash_error_wrong_type_param1(self):
        method = f"{self.ns}_getHeaderByNumber"
        num = "latest"
        params = [num]
        result, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNotNone(result)
        blockHash = result["hash"]

        method = f"{self.ns}_getHeaderByHash"
        params = [True, True]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0NonstringToHash", error)

    def test_kaia_getHeaderByHash_error_wrong_value_param(self):
        method = f"{self.ns}_getHeaderByHash"
        params = ["0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "HeaderDoesNotExist", error)

    def test_kaia_getHeaderByHash_success(self):
        method = f"{self.ns}_getHeaderByNumber"
        num = "latest"
        params = [num]
        result, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)
        kaia_common.checkBaseFeePerGasFieldAndValue(self, result)
        blockHash = result["hash"]

        method = f"{self.ns}_getHeaderByHash"
        params = [blockHash]
        result, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)
        kaia_common.checkBaseFeePerGasFieldAndValue(self, result)

    def test_kaia_getHeaderByNumber_error_no_param(self):
        method = f"{self.ns}_getHeaderByNumber"
        num = "latest"
        params = []
        _, error = kaia_common.send_transaction(self.endpoint, params)
        Utils.check_error(self, "arg0NoParams", error)

    def test_kaia_getHeaderByNumber_error_wrong_type_param1(self):
        method = f"{self.ns}_getHeaderByNumber"
        num = "latest"
        params = [True]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0HexWithoutPrefix", error)

    def test_kaia_getHeaderByNumber_error_wrong_value_param1(self):
        method = f"{self.ns}_getHeaderByNumber"
        num = "latest"
        params = ["num"]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0HexWithoutPrefix", error)

    def test_kaia_getHeaderByNumber_error_wrong_value_param2(self):
        method = f"{self.ns}_getHeaderByNumber"
        num = "latest"
        params = ["0xffffffff"]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "HeaderDoesNotExist", error)

    def test_kaia_getHeaderByNumber_success(self):
        method = f"{self.ns}_getHeaderByNumber"
        num = "latest"
        params = [num]
        result, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)
        kaia_common.checkBaseFeePerGasFieldAndValue(self, result)

    def test_kaia_getBlockWithConsensusInfoByHash_error_no_param(self):
        method = f"{self.ns}_getBlockWithConsensusInfoByHash"
        params = []
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

    def test_kaia_getBlockWithConsensusInfoByHash_error_wrong_type_param(self):
        method = f"{self.ns}_getBlockByNumber"
        num = "latest"
        params = [num, True]
        result, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNotNone(result)
        blockHash = result["hash"]

        method = f"{self.ns}_getBlockWithConsensusInfoByHash"
        params = [1234]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0NonstringToHash", error)

    def test_kaia_getBlockWithConsensusInfoByHash_error_wrong_value_param(self):
        method = f"{self.ns}_getBlockByNumber"
        num = "latest"
        params = [num, True]
        result, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNotNone(result)
        blockHash = result["hash"]

        method = f"{self.ns}_getBlockWithConsensusInfoByHash"
        params = ["0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "BlockDoesNotExist", error)

    def test_kaia_getBlockWithConsensusInfoByHash_success(self):
        txData = test_data_set["txData"]
        for tx in txData:
            blockHash = tx["result"]["blockHash"]
            method = f"{self.ns}_getBlockWithConsensusInfoByHash"
            params = [blockHash]
            result, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
            self.assertIsNone(error)
            self.assertIsNotNone(result)
            tx = result["transactions"][0]
            self.assertIsNotNone(tx["gasPrice"])

    def test_kaia_getBlockWithConsensusInfoByNumber_error_no_param(self):
        method = f"{self.ns}_getBlockWithConsensusInfoByNumber"
        params = []
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "BlockNumberNotAssigned", error)

    def test_kaia_getBlockWithConsensusInfoByNumber_error_wrong_type_param(self):
        method = f"{self.ns}_getBlockWithConsensusInfoByNumber"
        tag = "0x1"
        params = ["tag"]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0HexWithoutPrefix", error)

    def test_kaia_getBlockWithConsensusInfoByNumber_error_wrong_value_param(self):
        method = f"{self.ns}_getBlockWithConsensusInfoByNumber"
        tag = "0x1"
        params = ["0xffffffff"]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "BlockNotExist", error)

    def test_kaia_getBlockWithConsensusInfoByNumber_success(self):
        txData = test_data_set["txData"]
        for tx in txData:
            blockNumber = tx["result"]["blockNumber"]
            method = f"{self.ns}_getBlockWithConsensusInfoByNumber"
            params = [blockNumber]
            result, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
            self.assertIsNone(error)
            self.assertIsNotNone(result)
            tx = result["transactions"][0]
            self.assertIsNotNone(tx["gasPrice"])

    def test_kaia_getCommittee_success_no_param(self):
        method = f"{self.ns}_getCommittee"
        params = []
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_kaia_getCommittee_error_wrong_type_param(self):
        method = f"{self.ns}_getCommittee"
        tag = "latest"
        params = ["tag"]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0HexWithoutPrefix", error)

    def test_kaia_getCommittee_error_wrong_value_param(self):
        method = f"{self.ns}_getCommittee"
        tag = "latest"
        params = ["0xffffffff"]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "unknownblock", error)

    def test_kaia_getCommittee_success(self):
        method = f"{self.ns}_getCommittee"
        tag = "latest"
        params = [tag]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_kaia_getCommitteeSize_success_no_param(self):
        method = f"{self.ns}_getCommitteeSize"
        params = []
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_kaia_getCommitteeSize_error_wrong_type_param(self):
        method = f"{self.ns}_getCommitteeSize"
        tag = "latest"
        params = ["tag"]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0HexWithoutPrefix", error)

    def test_kaia_getCommitteeSize_error_wrong_value_param(self):
        method = f"{self.ns}_getCommitteeSize"
        tag = "latest"
        params = ["0xffffffff"]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "unknownblock", error)

    def test_kaia_getCommitteeSize_success(self):
        method = f"{self.ns}_getCommitteeSize"
        tag = "latest"
        params = [tag]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_kaia_getCouncil_success_no_param(self):
        method = f"{self.ns}_getCouncil"
        params = []
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_kaia_getCouncil_error_wrong_type_param(self):
        method = f"{self.ns}_getCouncil"
        tag = "latest"
        params = ["tag"]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0HexWithoutPrefix", error)

    def test_kaia_getCouncil_error_wrong_value_param(self):
        method = f"{self.ns}_getCouncil"
        tag = "latest"
        params = ["0xffffffff"]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "unknownblock", error)

    def test_kaia_getCouncil_success(self):
        method = f"{self.ns}_getCouncil"
        tag = "latest"
        params = [tag]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_kaia_getCouncilSize_success_no_param(self):
        method = f"{self.ns}_getCouncilSize"
        params = []
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_kaia_getCouncilSize_error_wrong_type_param(self):
        method = f"{self.ns}_getCouncilSize"
        tag = "latest"
        params = ["tag"]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0HexWithoutPrefix", error)

    def test_kaia_getCouncilSize_error_wrong_value_param(self):
        method = f"{self.ns}_getCouncilSize"
        tag = "latest"
        params = ["0xffffffff"]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "unknownblock", error)

    def test_kaia_getCouncilSize_success(self):
        method = f"{self.ns}_getCouncilSize"
        tag = "latest"
        params = [tag]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    @staticmethod
    def suite():
        suite = unittest.TestSuite()

        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_syncing_success_wrong_value_param"))
        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_syncing_success"))

        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_blockNumber_success"))
        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_blockNumber_success_wrong_value_param"))

        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getStorageAt_error_no_param"))
        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getStorageAt_error_wrong_type_param1"))
        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getStorageAt_error_wrong_type_param2"))
        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getStorageAt_success_wrong_value_param"))

        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getStorageAt_success"))

        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getBlockTransactionCountByHash_error_no_param"))
        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getBlockTransactionCountByHash_error_wrong_type_param"))
        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getBlockTransactionCountByHash_error_wrong_value_param"))
        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getBlockTransactionCountByHash_success"))

        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getBlockTransactionCountByNumber_error_no_param"))
        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getBlockTransactionCountByNumber_error_no_param"))
        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getBlockTransactionCountByNumber_error_wrong_type_param"))
        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getBlockTransactionCountByNumber_error_wrong_value_param"))
        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getBlockTransactionCountByNumber_success"))

        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getBlockByHash_error_no_param"))
        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getBlockByHash_error_wrong_type_param1"))
        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getBlockByHash_error_wrong_type_param2"))

        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getBlockByHash_error_wrong_value_param"))

        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getBlockByHash_success"))

        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getBlockByNumber_error_no_param"))
        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getBlockByNumber_error_wrong_type_param1"))
        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getBlockByNumber_error_wrong_type_param2"))
        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getBlockByNumber_error_wrong_value_param1"))
        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getBlockByNumber_error_wrong_value_param2"))
        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getBlockByNumber_success"))
        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getBlockReceipts_error_no_param"))
        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getBlockReceipts_error_wrong_type_param"))
        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getBlockReceipts_fail_wrong_value_param"))
        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getBlockReceipts_success"))
        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getHeaderByHash_error_no_param"))
        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getHeaderByHash_error_wrong_type_param1"))

        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getHeaderByHash_error_wrong_value_param"))

        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getHeaderByHash_success"))

        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getHeaderByNumber_error_no_param"))
        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getHeaderByNumber_error_wrong_type_param1"))
        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getHeaderByNumber_error_wrong_value_param1"))
        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getHeaderByNumber_error_wrong_value_param2"))
        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getHeaderByNumber_success"))
        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getBlockWithConsensusInfoByHash_error_no_param"))
        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getBlockWithConsensusInfoByHash_error_wrong_type_param"))
        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getBlockWithConsensusInfoByHash_error_wrong_value_param"))

        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getBlockWithConsensusInfoByHash_success"))
        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getBlockWithConsensusInfoByNumber_error_no_param"))
        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getBlockWithConsensusInfoByNumber_error_wrong_type_param"))
        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getBlockWithConsensusInfoByNumber_error_wrong_value_param"))

        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getBlockWithConsensusInfoByNumber_success"))

        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getCommittee_success_no_param"))
        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getCommittee_error_wrong_type_param"))
        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getCommittee_error_wrong_value_param"))

        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getCommittee_success"))

        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getCommitteeSize_success_no_param"))
        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getCommitteeSize_error_wrong_type_param"))
        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getCommitteeSize_error_wrong_value_param"))

        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getCommitteeSize_success"))

        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getCouncil_success_no_param"))
        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getCouncil_error_wrong_type_param"))
        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getCouncil_error_wrong_value_param"))

        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getCouncil_success"))

        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getCouncilSize_success_no_param"))
        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getCouncilSize_error_wrong_type_param"))
        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getCouncilSize_error_wrong_value_param"))

        suite.addTest(TestKaiaNamespaceBlockRPC("test_kaia_getCouncilSize_success"))

        return suite
