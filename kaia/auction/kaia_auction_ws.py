import unittest

from utils import Utils
import json

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
        result, error, ws = Utils.open_ws(self.endpoint, method, [
                                      "newPendingTransactions"], self.log_path)
        try:
            self.assertIsNone(error)
            self.assertIsNotNone(result)
            self.assertTrue(result.startswith("0x"))

            Utils.waiting_count("Waiting for", 2, "seconds for pending transaction data.")

            ws.settimeout(3)
            try:
                response = ws.recv()
                self.assertIsNotNone(response)
            except Exception as e:
                self.assertTrue(result.startswith("0x"))
                self.assertGreater(len(result), 2)
                return

            response_json = json.loads(response)
            self.assertIn("jsonrpc", response_json)
            self.assertIn("method", response_json)
            self.assertIn("params", response_json)
            self.assertEqual(response_json.get("jsonrpc"), "2.0")
            self.assertEqual(response_json.get("method"), "auction_subscription")

            params = response_json.get("params")
            self.assertIsNotNone(params)
            self.assertIn("subscription", params)
            self.assertIn("result", params)
            self.assertEqual(params.get("subscription"), result)

            tx_hash = params.get("result")
            self.assertIsNotNone(tx_hash)

        finally:
            ws.close()

    def test_auction_subscribe_newPendingTransactions_success_with_full_tx_true(self):
        method = f"{self.ns}_subscribe"
        result, error, ws = Utils.open_ws(self.endpoint, method, [
                                      "newPendingTransactions", True], self.log_path)
        try:
            self.assertIsNone(error)
            self.assertIsNotNone(result)
            self.assertTrue(result.startswith("0x"))

            Utils.waiting_count("Waiting for", 2, "seconds for pending transaction data.")

            ws.settimeout(3)
            try:
                response = ws.recv()
                self.assertIsNotNone(response)
            except Exception as e:
                self.assertTrue(result.startswith("0x"))
                self.assertGreater(len(result), 2)
                return

            response_json = json.loads(response)
            self.assertIn("jsonrpc", response_json)
            self.assertIn("method", response_json)
            self.assertIn("params", response_json)
            self.assertEqual(response_json.get("jsonrpc"), "2.0")
            self.assertEqual(response_json.get("method"), "auction_subscription")

            params = response_json.get("params")
            self.assertIsNotNone(params)
            self.assertIn("subscription", params)
            self.assertIn("result", params)
            self.assertEqual(params.get("subscription"), result)

            result_data = params.get("result")
            self.assertIsNotNone(result_data)
            self.assertIsInstance(result_data, dict)

            required_fields = ["hash", "from", "to", "value", "gas", "gasPrice", "nonce"]
            for field in required_fields:
                if field in result_data:
                    self.assertIsNotNone(result_data[field])

            if "time" in result_data:
                self.assertIsNotNone(result_data["time"])

        finally:
            ws.close()

    def test_auction_subscribe_newPendingTransactions_success_with_full_tx_false(self):
        method = f"{self.ns}_subscribe"
        result, error, ws = Utils.open_ws(self.endpoint, method, [
                                      "newPendingTransactions", False], self.log_path)
        try:
            self.assertIsNone(error)
            self.assertIsNotNone(result)
            self.assertTrue(result.startswith("0x"))

            Utils.waiting_count("Waiting for", 2, "seconds for pending transaction data.")

            ws.settimeout(3)
            try:
                response = ws.recv()
                self.assertIsNotNone(response)
            except Exception as e:
                self.assertTrue(result.startswith("0x"))
                self.assertGreater(len(result), 2)
                return

            response_json = json.loads(response)
            self.assertIn("jsonrpc", response_json)
            self.assertIn("method", response_json)
            self.assertIn("params", response_json)
            self.assertEqual(response_json.get("jsonrpc"), "2.0")
            self.assertEqual(response_json.get("method"), "auction_subscription")

            params = response_json.get("params")
            self.assertIsNotNone(params)
            self.assertIn("subscription", params)
            self.assertIn("result", params)
            self.assertEqual(params.get("subscription"), result)

            tx_hash = params.get("result")
            self.assertIsNotNone(tx_hash)

        finally:
            ws.close()

    def test_auction_subscribe_newHeads_error_with_params(self):
        method = f"{self.ns}_subscribe"
        _, error = Utils.call_ws(self.endpoint, method, [
                                 "newHeads", "invalid"], self.log_path)
        Utils.check_error(self, "TooManyArguments", error)

    def test_auction_subscribe_newHeads_success(self):
        method = f"{self.ns}_subscribe"
        result, error, ws = Utils.open_ws(self.endpoint, method, [
                                      "newHeads"], self.log_path)
        try:
            self.assertIsNone(error)
            self.assertIsNotNone(result)
            self.assertTrue(result.startswith("0x"))

            Utils.waiting_count("Waiting for", 2, "seconds for new block data.")

            ws.settimeout(3)
            try:
                response = ws.recv()
                self.assertIsNotNone(response)
            except Exception as e:
                self.assertTrue(result.startswith("0x"))
                self.assertGreater(len(result), 2)
                return


            Utils.check_response_type_newHeads_subscription_kaia(self, response)

        finally:
            ws.close()

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

        result, error, ws = Utils.open_ws(self.endpoint, method, ["logs", filter_criteria], self.log_path)
        try:
            self.assertIsNone(error)
            self.assertIsNotNone(result)
            self.assertTrue(result.startswith("0x"))

            Utils.waiting_count("Waiting for", 2, "seconds for log data.")
            ws.settimeout(3)

            try:
                response = ws.recv()
                self.assertIsNotNone(response)
            except Exception as e:
                self.assertTrue(result.startswith("0x"))
                self.assertGreater(len(result), 2)
                return

            response_json = json.loads(response)
            self.assertIn("jsonrpc", response_json)
            self.assertIn("method", response_json)
            self.assertIn("params", response_json)
            self.assertEqual(response_json.get("jsonrpc"), "2.0")
            self.assertEqual(response_json.get("method"), "auction_subscription")

            params = response_json.get("params")
            self.assertIsNotNone(params)
            self.assertIn("subscription", params)
            self.assertIn("result", params)
            self.assertEqual(params.get("subscription"), result)

            log_result = params.get("result")
            self.assertIsNotNone(log_result)
            self.assertIsInstance(log_result, dict)

            required_fields = ["address", "topics", "data", "blockNumber", "transactionHash"]
            for field in required_fields:
                self.assertIn(field, log_result, f"Missing required field: {field}")
                self.assertIsNotNone(log_result[field])

            optional_fields = ["transactionIndex", "blockHash", "logIndex", "removed"]
            for field in optional_fields:
                if field in log_result:
                    self.assertIsNotNone(log_result[field])

        finally:
            ws.close()

    def test_auction_subscribe_logs_success_with_topics(self):
        method = f"{self.ns}_subscribe"
        filter_criteria = {
            "fromBlock": "latest",
            "toBlock": "latest",
            "address": "0x0000000000000000000000000000000000000000",
            "topics": ["0x0000000000000000000000000000000000000000000000000000000000000000"]
        }

        result, error, ws = Utils.open_ws(self.endpoint, method, ["logs", filter_criteria], self.log_path)
        try:
            self.assertIsNone(error)
            self.assertIsNotNone(result)
            self.assertTrue(result.startswith("0x"))

            Utils.waiting_count("Waiting for", 2, "seconds for log data.")
            ws.settimeout(3)

            try:
                response = ws.recv()
                self.assertIsNotNone(response)
            except Exception as e:
                self.assertTrue(result.startswith("0x"))
                self.assertGreater(len(result), 2)
                return

            response_json = json.loads(response)
            self.assertIn("jsonrpc", response_json)
            self.assertIn("method", response_json)
            self.assertIn("params", response_json)
            self.assertEqual(response_json.get("jsonrpc"), "2.0")
            self.assertEqual(response_json.get("method"), "auction_subscription")

            params = response_json.get("params")
            self.assertIsNotNone(params)
            self.assertIn("subscription", params)
            self.assertIn("result", params)
            self.assertEqual(params.get("subscription"), result)

            log_result = params.get("result")
            self.assertIsNotNone(log_result)
            self.assertIsInstance(log_result, dict)

            required_fields = ["address", "topics", "data", "blockNumber", "transactionHash"]
            for field in required_fields:
                self.assertIn(field, log_result, f"Missing required field: {field}")
                self.assertIsNotNone(log_result[field])

            optional_fields = ["transactionIndex", "blockHash", "logIndex", "removed"]
            for field in optional_fields:
                if field in log_result:
                    self.assertIsNotNone(log_result[field])

        finally:
            ws.close()

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
