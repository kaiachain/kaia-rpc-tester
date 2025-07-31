import unittest

from utils import Utils

# test_data_set is injected by rpc-tester/main.py
global test_data_set


class TestKaiaNamespaceAuctionRPC(unittest.TestCase):
    config = Utils.get_config()
    _, _, log_path = Utils.get_log_filename_with_path()
    endpoint = config.get("endpoint")
    rpc_port = config.get("rpcPort")
    ws_port = config.get("wsPort")
    ns = "auction"
    waiting_count = 2

    def test_auction_submitBid_error_no_param(self):
        method = f"{self.ns}_submitBid"
        _, error = Utils.call_rpc(self.endpoint, method, [], self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

    def test_auction_submitBid_error_wrong_type_param(self):
        method = f"{self.ns}_submitBid"
        _, error = Utils.call_rpc(self.endpoint, method, [
                                  "invalid_param"], self.log_path)
        Utils.check_error(self, "arg0InvalidBidParams", error)

    def test_auction_submitBid_error_empty_target_tx_raw(self):
        method = f"{self.ns}_submitBid"
        bid_input = {
            "targetTxRaw": "",
            "targetTxHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
            "blockNumber": 0,
            "sender": "0x0000000000000000000000000000000000000000",
            "to": "0x0000000000000000000000000000000000000000",
            "nonce": 0,
            "bid": "0x0",
            "callGasLimit": 0,
            "data": "0x",
            "searcherSig": "0x",
            "auctioneerSig": "0x"
        }
        result, error = Utils.call_rpc(self.endpoint, method, [
                                       bid_input], self.log_path)
        self.assertIsNone(error)
        self.assertIsNotNone(result)
        self.assertIn("err", result)
        self.assertEqual(result["err"], "Empty target tx raw")

    def test_auction_submitBid_error_invalid_target_tx_raw(self):
        method = f"{self.ns}_submitBid"
        bid_input = {
            "targetTxRaw": "0xinvalid",
            "targetTxHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
            "blockNumber": 0,
            "sender": "0x0000000000000000000000000000000000000000",
            "to": "0x0000000000000000000000000000000000000000",
            "nonce": 0,
            "bid": "0x0",
            "callGasLimit": 0,
            "data": "0x",
            "searcherSig": "0x",
            "auctioneerSig": "0x"
        }
        _, error = Utils.call_rpc(self.endpoint, method, [
                                  bid_input], self.log_path)
        self.assertIsNotNone(error)

    def test_auction_submitBid_error_invalid_target_tx_hash(self):
        method = f"{self.ns}_submitBid"
        bid_input = {
            "targetTxRaw": "0x",
            "targetTxHash": "0xinvalid",
            "blockNumber": 0,
            "sender": "0x0000000000000000000000000000000000000000",
            "to": "0x0000000000000000000000000000000000000000",
            "nonce": 0,
            "bid": "0x0",
            "callGasLimit": 0,
            "data": "0x",
            "searcherSig": "0x",
            "auctioneerSig": "0x"
        }
        _, error = Utils.call_rpc(self.endpoint, method, [
                                  bid_input], self.log_path)
        self.assertIsNotNone(error)

    def test_auction_submitBid_error_invalid_sender_address(self):
        method = f"{self.ns}_submitBid"
        bid_input = {
            "targetTxRaw": "0x",
            "targetTxHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
            "blockNumber": 0,
            "sender": "0xinvalid",
            "to": "0x0000000000000000000000000000000000000000",
            "nonce": 0,
            "bid": "0x0",
            "callGasLimit": 0,
            "data": "0x",
            "searcherSig": "0x",
            "auctioneerSig": "0x"
        }
        _, error = Utils.call_rpc(self.endpoint, method, [
                                  bid_input], self.log_path)
        self.assertIsNotNone(error)

    def test_auction_submitBid_error_invalid_to_address(self):
        method = f"{self.ns}_submitBid"
        bid_input = {
            "targetTxRaw": "0x",
            "targetTxHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
            "blockNumber": 0,
            "sender": "0x0000000000000000000000000000000000000000",
            "to": "0xinvalid",
            "nonce": 0,
            "bid": "0x0",
            "callGasLimit": 0,
            "data": "0x",
            "searcherSig": "0x",
            "auctioneerSig": "0x"
        }
        _, error = Utils.call_rpc(self.endpoint, method, [
                                  bid_input], self.log_path)
        self.assertIsNotNone(error)

    def test_auction_submitBid_error_wrong_field_types(self):
        method = f"{self.ns}_submitBid"
        bid_input = {
            "targetTxRaw": 123,  # Should be string
            "targetTxHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
            "blockNumber": "invalid",  # Should be number
            "sender": "0x0000000000000000000000000000000000000000",
            "to": "0x0000000000000000000000000000000000000000",
            "nonce": "invalid",  # Should be number
            "bid": "0x3",
            "callGasLimit": "invalid",  # Should be number
            "data": "0x",
            "searcherSig": "0x",
            "auctioneerSig": "0x"
        }
        _, error = Utils.call_rpc(self.endpoint, method, [
                                  bid_input], self.log_path)
        self.assertIsNotNone(error)

    def test_auction_call_error_no_param1(self):
        method = f"{self.ns}_call"
        params = []
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

    def test_auction_call_error_no_param2(self):
        method = f"{self.ns}_call"
        contract = test_data_set["contracts"]["unknown"]["address"][0]
        params = [{"to": contract}, "latest"]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "ExecutionReverted", error)

    def test_auction_call_error_no_param3(self):
        method = f"{self.ns}_call"
        methodName = "auction_call"
        address = test_data_set["account"]["sender"]["address"]
        contract = test_data_set["contracts"]["unknown"]["address"][0]
        code = test_data_set["contracts"]["unknown"]["input"]
        txGas = hex(30400)
        txGasPrice = test_data_set["unitGasPrice"]
        txValue = hex(0)
        params = [{"data": code}, "latest"]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "VMErrorOccurs", error)

    def test_auction_call_error_wrong_type_param1(self):
        method = f"{self.ns}_call"
        address = test_data_set["account"]["sender"]["address"]
        contract = test_data_set["contracts"]["unknown"]["address"][0]
        code = test_data_set["contracts"]["unknown"]["input"]
        txGas = hex(30400)
        txGasPrice = test_data_set["unitGasPrice"]
        txValue = hex(0)
        params = [
            {
                "from": 1234,
                "to": contract,
                "gas": txGas,
                "gasPrice": txGasPrice,
                "value": txValue,
                "data": code,
            },
            "latest",
        ]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0NonstringToCallArgsFromAddress", error)

    def test_auction_call_error_wrong_type_param2(self):
        method = f"{self.ns}_call"
        address = test_data_set["account"]["sender"]["address"]
        contract = test_data_set["contracts"]["unknown"]["address"][0]
        code = test_data_set["contracts"]["unknown"]["input"]
        txGas = hex(30400)
        txGasPrice = test_data_set["unitGasPrice"]
        txValue = hex(0)
        params = [
            {
                "from": address,
                "to": 1234,
                "gas": txGas,
                "gasPrice": txGasPrice,
                "value": txValue,
                "data": code,
            },
            "latest",
        ]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0NonstringToCallArgsToAddress", error)

    def test_auction_call_error_wrong_type_param3(self):
        method = f"{self.ns}_call"
        address = test_data_set["account"]["sender"]["address"]
        contract = test_data_set["contracts"]["unknown"]["address"][0]
        code = test_data_set["contracts"]["unknown"]["input"]
        txGas = hex(30400)
        txGasPrice = test_data_set["unitGasPrice"]
        txValue = hex(0)
        params = [
            {
                "from": address,
                "to": contract,
                "gas": "txGas",
                "gasPrice": txGasPrice,
                "value": txValue,
                "data": code,
            },
            "latest",
        ]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0HexToCallArgsGasUint64", error)

    def test_auction_call_error_wrong_type_param4(self):
        method = f"{self.ns}_call"
        address = test_data_set["account"]["sender"]["address"]
        contract = test_data_set["contracts"]["unknown"]["address"][0]
        code = test_data_set["contracts"]["unknown"]["input"]
        txGas = hex(30400)
        txGasPrice = test_data_set["unitGasPrice"]
        txValue = hex(0)
        params = [
            {
                "from": address,
                "to": contract,
                "gas": txGas,
                "gasPrice": "txGasPrice",
                "value": txValue,
                "data": code,
            },
            "latest",
        ]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0HexToCallArgsGaspriceBig", error)

    def test_auction_call_error_wrong_type_param5(self):
        method = f"{self.ns}_call"
        address = test_data_set["account"]["sender"]["address"]
        contract = test_data_set["contracts"]["unknown"]["address"][0]
        code = test_data_set["contracts"]["unknown"]["input"]
        txGas = hex(30400)
        txGasPrice = test_data_set["unitGasPrice"]
        txValue = hex(0)
        params = [
            {
                "from": address,
                "to": contract,
                "gas": txGas,
                "gasPrice": txGasPrice,
                "value": "txValue",
                "data": code,
            },
            "latest",
        ]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0HexToCallArgsValueBig", error)

    def test_auction_call_error_wrong_type_param6(self):
        method = f"{self.ns}_call"
        address = test_data_set["account"]["sender"]["address"]
        contract = test_data_set["contracts"]["unknown"]["address"][0]
        code = test_data_set["contracts"]["unknown"]["input"]
        txGas = hex(30400)
        txGasPrice = test_data_set["unitGasPrice"]
        txValue = hex(0)
        params = [
            {
                "from": address,
                "to": contract,
                "gas": txGas,
                "gasPrice": txGasPrice,
                "value": txValue,
                "data": 1234,
            },
            "latest",
        ]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0NonstringToCallArgsDataBytes", error)

    def test_auction_call_error_wrong_type_param7(self):
        method = f"{self.ns}_call"
        address = test_data_set["account"]["sender"]["address"]
        contract = test_data_set["contracts"]["unknown"]["address"][0]
        code = test_data_set["contracts"]["unknown"]["input"]
        txGas = hex(30400)
        txGasPrice = test_data_set["unitGasPrice"]
        txValue = hex(0)
        params = [
            {
                "from": address,
                "to": contract,
                "gas": txGas,
                "gasPrice": txGasPrice,
                "value": txValue,
                "data": code,
            },
            "abcd",
        ]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg1HexWithoutPrefix", error)

    def test_auction_call_error_wrong_value_param1(self):
        method = f"{self.ns}_call"
        address = test_data_set["account"]["sender"]["address"]
        contract = test_data_set["contracts"]["unknown"]["address"][0]
        code = test_data_set["contracts"]["unknown"]["input"]
        txGas = hex(30400)
        txGasPrice = test_data_set["unitGasPrice"]
        txValue = hex(100000000000000000000000000000000000000000)
        params = [
            {
                "from": address,
                "to": contract,
                "gas": txGas,
                "gasPrice": txGasPrice,
                "value": txValue,
                "data": code,
            },
            "latest",
        ]
        result, error = Utils.call_rpc(
            self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "ExecutionReverted", error)

    def test_auction_call_error_intrinsic_gas(self):
        method = f"{self.ns}_call"
        contract = test_data_set["contracts"]["unknown"]["address"][0]
        zeroBalanceAddr = "0x15318f21f3dee6b2c64d2a633cb8c1194877c882"
        code = test_data_set["contracts"]["unknown"]["input"]
        txGasPrice = test_data_set["unitGasPrice"]
        params = [
            {
                "from": zeroBalanceAddr,
                "to": contract,
                "data": code,
                "gas": "0x99",
                "gasPrice": txGasPrice,
            },
            "latest",
        ]
        _, error = Utils.call_rpc(
            self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "GasTooLow", error)

    def test_auction_call_error_evm_revert_message(self):
        method = f"{self.ns}_call"
        address = test_data_set["account"]["sender"]["address"]
        ownerContract = test_data_set["contracts"]["unknown"]["address"][0]
        notOwner = "0x15318f21f3dee6b2c64d2a633cb8c1194877c882"
        changeOwnerAbi = "0xa6f9dae10000000000000000000000003e2ac308cd78ac2fe162f9522deb2b56d9da9499"
        params = [
            {"from": notOwner, "to": ownerContract, "data": changeOwnerAbi},
            "latest",
        ]
        result, error = Utils.call_rpc(
            self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "ExecutionReverted", error)

    def test_auction_call_success1(self):
        method = f"{self.ns}_call"
        address = test_data_set["account"]["sender"]["address"]
        contract = test_data_set["contracts"]["unknown"]["address"][0]
        code = test_data_set["contracts"]["unknown"]["input"]
        txGas = hex(30400)
        txGasPrice = test_data_set["unitGasPrice"]
        params = [{"to": contract, "data": code}, "latest"]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_auction_call_success2(self):
        method = f"{self.ns}_call"
        address = test_data_set["account"]["sender"]["address"]
        contract = test_data_set["contracts"]["unknown"]["address"][0]
        code = test_data_set["contracts"]["unknown"]["input"]
        txGas = hex(30400)
        txGasPrice = test_data_set["unitGasPrice"]
        params = [{"from": address, "to": contract, "data": code}, "latest"]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_auction_call_success3(self):
        method = f"{self.ns}_call"
        address = test_data_set["account"]["sender"]["address"]
        contract = test_data_set["contracts"]["unknown"]["address"][0]
        code = test_data_set["contracts"]["unknown"]["input"]
        txGas = hex(30400)
        txGasPrice = test_data_set["unitGasPrice"]
        params = [
            {
                "from": address,
                "to": contract,
                "gas": txGas,
                "gasPrice": txGasPrice,
                "data": code,
            },
            "latest",
        ]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_auction_call_success4(self):
        method = f"{self.ns}_call"
        address = test_data_set["account"]["sender"]["address"]
        contract = test_data_set["contracts"]["unknown"]["address"][0]
        code = test_data_set["contracts"]["unknown"]["input"]
        txGas = hex(30400)
        txGasPrice = test_data_set["unitGasPrice"]
        txValue = hex(0)
        params = [
            {
                "from": address,
                "to": contract,
                "gas": txGas,
                "gasPrice": txGasPrice,
                "value": txValue,
                "data": code,
            },
            "latest",
        ]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_auction_call_success_input_instead_data(self):
        method = f"{self.ns}_call"
        address = test_data_set["account"]["sender"]["address"]
        contract = test_data_set["contracts"]["unknown"]["address"][0]
        code = test_data_set["contracts"]["unknown"]["input"]
        txGas = hex(30400)
        txGasPrice = test_data_set["unitGasPrice"]
        params = [{"to": contract, "input": code}, "latest"]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_auction_subscribe_newPendingTransactions_error_unsupported_rpc(self):
        method = f"{self.ns}_subscribe"
        params = ["newPendingTransactions"]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "NotificationsNotSupported", error)

    def test_auction_subscribe_newHeads_error_unsupported_rpc(self):
        method = f"{self.ns}_subscribe"
        params = ["newHeads"]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "NotificationsNotSupported", error)

    def test_auction_subscribe_logs_error_unsupported_rpc(self):
        method = f"{self.ns}_subscribe"
        filter_criteria = {"fromBlock": "latest"}
        params = ["logs", filter_criteria]
        _, error = Utils.call_rpc(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "NotificationsNotSupported", error)

    @staticmethod
    def suite():
        suite = unittest.TestSuite()

        # submitBid tests
        suite.addTest(TestKaiaNamespaceAuctionRPC(
            "test_auction_submitBid_error_no_param"))
        suite.addTest(TestKaiaNamespaceAuctionRPC(
            "test_auction_submitBid_error_wrong_type_param"))
        suite.addTest(TestKaiaNamespaceAuctionRPC(
            "test_auction_submitBid_error_empty_target_tx_raw"))
        suite.addTest(TestKaiaNamespaceAuctionRPC(
            "test_auction_submitBid_error_invalid_target_tx_raw"))
        suite.addTest(TestKaiaNamespaceAuctionRPC(
            "test_auction_submitBid_error_invalid_target_tx_hash"))
        suite.addTest(TestKaiaNamespaceAuctionRPC(
            "test_auction_submitBid_error_invalid_sender_address"))
        suite.addTest(TestKaiaNamespaceAuctionRPC(
            "test_auction_submitBid_error_invalid_to_address"))

        suite.addTest(TestKaiaNamespaceAuctionRPC(
            "test_auction_submitBid_error_wrong_field_types"))

        # call tests
        suite.addTest(TestKaiaNamespaceAuctionRPC(
            "test_auction_call_error_no_param1"))
        suite.addTest(TestKaiaNamespaceAuctionRPC(
            "test_auction_call_error_no_param2"))
        suite.addTest(TestKaiaNamespaceAuctionRPC(
            "test_auction_call_error_no_param3"))
        suite.addTest(TestKaiaNamespaceAuctionRPC(
            "test_auction_call_error_wrong_type_param1"))
        suite.addTest(TestKaiaNamespaceAuctionRPC(
            "test_auction_call_error_wrong_type_param2"))
        suite.addTest(TestKaiaNamespaceAuctionRPC(
            "test_auction_call_error_wrong_type_param3"))
        suite.addTest(TestKaiaNamespaceAuctionRPC(
            "test_auction_call_error_wrong_type_param4"))
        suite.addTest(TestKaiaNamespaceAuctionRPC(
            "test_auction_call_error_wrong_type_param5"))
        suite.addTest(TestKaiaNamespaceAuctionRPC(
            "test_auction_call_error_wrong_type_param6"))
        suite.addTest(TestKaiaNamespaceAuctionRPC(
            "test_auction_call_error_wrong_type_param7"))
        suite.addTest(TestKaiaNamespaceAuctionRPC(
            "test_auction_call_error_wrong_value_param1"))
        suite.addTest(TestKaiaNamespaceAuctionRPC(
            "test_auction_call_error_evm_revert_message"))

        suite.addTest(TestKaiaNamespaceAuctionRPC(
            "test_auction_call_error_intrinsic_gas"))
        suite.addTest(TestKaiaNamespaceAuctionRPC(
            "test_auction_call_success1"))
        suite.addTest(TestKaiaNamespaceAuctionRPC(
            "test_auction_call_success2"))
        suite.addTest(TestKaiaNamespaceAuctionRPC(
            "test_auction_call_success3"))
        suite.addTest(TestKaiaNamespaceAuctionRPC(
            "test_auction_call_success4"))
        suite.addTest(TestKaiaNamespaceAuctionRPC(
            "test_auction_call_success_input_instead_data"))

        # subscribe tests
        suite.addTest(TestKaiaNamespaceAuctionRPC(
            "test_auction_subscribe_newPendingTransactions_error_unsupported_rpc"))
        suite.addTest(TestKaiaNamespaceAuctionRPC(
            "test_auction_subscribe_newHeads_error_unsupported_rpc"))
        suite.addTest(TestKaiaNamespaceAuctionRPC(
            "test_auction_subscribe_logs_error_unsupported_rpc"))

        return suite
