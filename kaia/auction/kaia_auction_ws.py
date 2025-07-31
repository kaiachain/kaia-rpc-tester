import unittest

from utils import Utils

# test_data_set is injected by rpc-tester/main.py
global test_data_set


class TestKaiaNamespaceAuctionWS(unittest.TestCase):
    config = Utils.get_config()
    _, _, log_path = Utils.get_log_filename_with_path()
    endpoint = config.get("endpoint")
    rpc_port = config.get("rpcPort")
    ws_port = config.get("wsPort")
    ns = "auction"
    waiting_count = 2

    def test_auction_subscribe_newPendingTransactions_error_invalid_param_type(self):
        method = f"{self.ns}_subscribe"
        _, error = Utils.call_ws(self.endpoint, method, [
                                 "newPendingTransactions", "invalid"], self.log_path)
        Utils.check_error(self, "arg1StringToBool", error)

    def test_auction_subscribe_newPendingTransactions_success_no_param(self):
        method = f"{self.ns}_subscribe"
        result, error = Utils.call_ws(self.endpoint, method, [
                                      "newPendingTransactions"], self.log_path)
        self.assertIsNone(error)
        self.assertIsNotNone(result)

    def test_auction_subscribe_newPendingTransactions_success_with_full_tx_true(self):
        method = f"{self.ns}_subscribe"
        result, error = Utils.call_ws(self.endpoint, method, [
                                      "newPendingTransactions", True], self.log_path)
        self.assertIsNone(error)
        self.assertIsNotNone(result)

    def test_auction_subscribe_newPendingTransactions_success_with_full_tx_false(self):
        method = f"{self.ns}_subscribe"
        result, error = Utils.call_ws(self.endpoint, method, [
                                      "newPendingTransactions", False], self.log_path)
        self.assertIsNone(error)
        self.assertIsNotNone(result)

    def test_auction_subscribe_newHeads_error_with_params(self):
        method = f"{self.ns}_subscribe"
        _, error = Utils.call_ws(self.endpoint, method, [
                                 "newHeads", "invalid"], self.log_path)
        Utils.check_error(self, "TooManyArguments", error)

    def test_auction_subscribe_newHeads_success(self):
        method = f"{self.ns}_subscribe"
        result, error = Utils.call_ws(self.endpoint, method, [
                                      "newHeads"], self.log_path)
        self.assertIsNone(error)
        self.assertIsNotNone(result)

    def test_auction_subscribe_logs_error_no_params(self):
        method = f"{self.ns}_subscribe"
        _, error = Utils.call_ws(self.endpoint, method, [
                                 "logs"], self.log_path)
        Utils.check_error(self, "arg1NoParams", error)

    def test_auction_subscribe_logs_error_invalid_filter_criteria(self):
        method = f"{self.ns}_subscribe"
        filter_criteria = {
            "fromBlock": "invalid",
            "toBlock": "invalid"
        }
        _, error = Utils.call_ws(self.endpoint, method, [
                                 "logs", filter_criteria], self.log_path)
        Utils.check_error(self, "arg1HexWithoutPrefix", error)

    def test_auction_subscribe_logs_error_invalid_address(self):
        method = f"{self.ns}_subscribe"
        filter_criteria = {
            "fromBlock": "latest",
            "toBlock": "latest",
            "address": "0xinvalid"
        }
        _, error = Utils.call_ws(self.endpoint, method, [
                                 "logs", filter_criteria], self.log_path)
        Utils.check_error(self, "arg1InvalidAddress", error)

    def test_auction_subscribe_logs_error_invalid_topics_format(self):
        method = f"{self.ns}_subscribe"
        filter_criteria = {
            "fromBlock": "latest",
            "toBlock": "latest",
            "address": "0x0000000000000000000000000000000000000000",
            "topics": ["invalid_topic_format"]  # Invalid topic format
        }
        _, error = Utils.call_ws(self.endpoint, method, [
                                 "logs", filter_criteria], self.log_path)
        Utils.check_error(self, "arg1HexWithoutPrefix", error)

    def test_auction_subscribe_logs_success_basic(self):
        method = f"{self.ns}_subscribe"
        filter_criteria = {
            "fromBlock": "latest",
            "toBlock": "latest",
            "address": "0x0000000000000000000000000000000000000000"
        }
        result, error = Utils.call_ws(self.endpoint, method, [
                                      "logs", filter_criteria], self.log_path)
        self.assertIsNone(error)
        self.assertIsNotNone(result)

    def test_auction_subscribe_logs_success_with_topics(self):
        method = f"{self.ns}_subscribe"
        filter_criteria = {
            "fromBlock": "latest",
            "toBlock": "latest",
            "address": "0x0000000000000000000000000000000000000000",
            "topics": ["0x0000000000000000000000000000000000000000000000000000000000000000"]
        }
        result, error = Utils.call_ws(self.endpoint, method, [
                                      "logs", filter_criteria], self.log_path)
        self.assertIsNone(error)
        self.assertIsNotNone(result)

    @staticmethod
    def suite():
        suite = unittest.TestSuite()

        # newPendingTransactions tests
        suite.addTest(TestKaiaNamespaceAuctionWS(
            "test_auction_subscribe_newPendingTransactions_error_invalid_param_type"))
        suite.addTest(TestKaiaNamespaceAuctionWS(
            "test_auction_subscribe_newPendingTransactions_success_no_param"))
        suite.addTest(TestKaiaNamespaceAuctionWS(
            "test_auction_subscribe_newPendingTransactions_success_with_full_tx_true"))
        suite.addTest(TestKaiaNamespaceAuctionWS(
            "test_auction_subscribe_newPendingTransactions_success_with_full_tx_false"))

        # newHeads tests
        suite.addTest(TestKaiaNamespaceAuctionWS(
            "test_auction_subscribe_newHeads_error_with_params"))
        suite.addTest(TestKaiaNamespaceAuctionWS(
            "test_auction_subscribe_newHeads_success"))

        # logs tests
        suite.addTest(TestKaiaNamespaceAuctionWS(
            "test_auction_subscribe_logs_error_no_params"))
        suite.addTest(TestKaiaNamespaceAuctionWS(
            "test_auction_subscribe_logs_error_invalid_filter_criteria"))
        suite.addTest(TestKaiaNamespaceAuctionWS(
            "test_auction_subscribe_logs_error_invalid_address"))
        suite.addTest(TestKaiaNamespaceAuctionWS(
            "test_auction_subscribe_logs_error_invalid_topics_format"))
        suite.addTest(TestKaiaNamespaceAuctionWS(
            "test_auction_subscribe_logs_success_basic"))
        suite.addTest(TestKaiaNamespaceAuctionWS(
            "test_auction_subscribe_logs_success_with_topics"))

        return suite
