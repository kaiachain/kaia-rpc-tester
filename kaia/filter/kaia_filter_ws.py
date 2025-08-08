import unittest
from utils import Utils
from common import kaia as kaia_common

# test_data_set is injected by rpc-tester/main.py
global test_data_set


class TestKaiaNamespaceFilterWS(unittest.TestCase):
    config = Utils.get_config()
    _, _, log_path = Utils.get_log_filename_with_path()
    endpoint = config.get("endpoint")
    rpc_port = config.get("rpcPort")
    ws_port = config.get("wsPort")
    ns = "kaia"
    waiting_count = 2

    def test_kaia_newFilter_error_no_param(self):
        method = f"{self.ns}_newFilter"
        params = []
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

    def test_kaia_newFilter_error_wrong_type_param(self):
        method = f"{self.ns}_newFilter"
        params = [{"fromBlock": "1234"}]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0HexWithoutPrefix", error)

    def test_kaia_newFilter_error_unsupported_fromBlock_tag_param(self):
        method = f"{self.ns}_newFilter"
        params = [{"fromBlock": "pending"}]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "PendingLogsNotSupported", error)

    def test_kaia_newFilter_error_unsupported_toBlock_tag_param(self):
        method = f"{self.ns}_newFilter"
        params = [{"toBlock": "pending"}]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "PendingLogsNotSupported", error)

    def test_kaia_newFilter_success(self):
        method = f"{self.ns}_newFilter"
        fromBlock = "latest"
        params = [{"fromBlock": fromBlock}]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_kaia_newBlockFilter_success_wrong_value_param(self):
        method = f"{self.ns}_newBlockFilter"
        params = ["abcd"]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_kaia_newBlockFilter_success(self):
        method = f"{self.ns}_newBlockFilter"
        params = []
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_kaia_newPendingTransactionFilter_success_wrong_value_param(self):
        method = f"{self.ns}_newPendingTransactionFilter"
        params = ["abcd"]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_kaia_newPendingTransactionFilter_success(self):
        method = f"{self.ns}_newPendingTransactionFilter"
        params = []
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_kaia_uninstallFilter_error_no_param(self):
        method = f"{self.ns}_newFilter"
        fromBlock = "latest"
        params = [{"fromBlock": fromBlock}]
        result, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)
        filterId = result
        Utils.waiting_count("Waiting for", 5, "seconds until writing a block.")

        method = f"{self.ns}_uninstallFilter"
        params = []
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

        params = [filterId]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_kaia_uninstallFilter_error_wrong_type_param(self):
        method = f"{self.ns}_newFilter"
        fromBlock = "latest"
        params = [{"fromBlock": fromBlock}]
        result, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)
        filterId = result
        Utils.waiting_count("Waiting for", 5, "seconds until writing a block.")

        method = f"{self.ns}_uninstallFilter"
        params = [1234]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0NumberToRPCID", error)

        params = [filterId]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_kaia_uninstallFilter_success_false(self):
        method = f"{self.ns}_newFilter"
        fromBlock = "latest"
        params = [{"fromBlock": fromBlock}]
        result, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)
        filterId = result
        Utils.waiting_count("Waiting for", 5, "seconds until writing a block.")

        method = f"{self.ns}_uninstallFilter"
        params = [filterId + "1"]
        result, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)
        self.assertFalse(result)

        method = f"{self.ns}_uninstallFilter"
        params = [filterId]
        result, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)
        self.assertTrue(result)

    def test_kaia_uninstallFilter_success(self):
        method = f"{self.ns}_newFilter"
        fromBlock = "latest"
        params = [{"fromBlock": fromBlock}]
        result, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)
        filterId = result
        Utils.waiting_count("Waiting for", 5, "seconds until writing a block.")

        method = f"{self.ns}_uninstallFilter"
        params = [filterId]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_kaia_getFilterChanges_error_no_param(self):
        method = f"{self.ns}_newFilter"
        fromBlock = "latest"
        params = [{"fromBlock": fromBlock}]
        result, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)
        filterId = result
        Utils.waiting_count("Waiting for", 5, "seconds until writing a block.")

        method = f"{self.ns}_getFilterChanges"
        params = []
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

        method = f"{self.ns}_uninstallFilter"
        params = [filterId]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_kaia_getFilterChanges_error_wrong_type_param(self):
        method = f"{self.ns}_newFilter"
        fromBlock = "latest"
        params = [{"fromBlock": fromBlock}]
        result, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)
        filterId = result
        Utils.waiting_count("Waiting for", 5, "seconds until writing a block.")

        method = f"{self.ns}_getFilterChanges"
        params = [1234]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0NumberToRPCID", error)

        method = f"{self.ns}_uninstallFilter"
        params = [filterId]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_kaia_getFilterChanges_error_wrong_value_param(self):
        method = f"{self.ns}_newFilter"
        fromBlock = "latest"
        params = [{"fromBlock": fromBlock}]
        result, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)
        filterId = result
        Utils.waiting_count("Waiting for", 5, "seconds until writing a block.")

        method = f"{self.ns}_getFilterChanges"
        params = [filterId + "1"]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "FilterNotFound", error)

        method = f"{self.ns}_uninstallFilter"
        params = [filterId]
        result, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_kaia_getFilterChanges_success(self):
        method = f"{self.ns}_newFilter"
        fromBlock = "latest"
        params = [{"fromBlock": fromBlock}]
        result, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)
        filterId = result
        Utils.waiting_count("Waiting for", 5, "seconds until writing a block.")

        method = f"{self.ns}_getFilterChanges"
        params = [filterId]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

        method = f"{self.ns}_uninstallFilter"
        params = [filterId]
        result, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_kaia_getFilterLogs_error_no_param(self):
        method = f"{self.ns}_newFilter"
        fromBlock = "latest"
        params = [{"fromBlock": fromBlock}]
        result, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)
        filterId = result
        Utils.waiting_count("Waiting for", 5, "seconds until writing a block.")

        method = f"{self.ns}_getFilterLogs"
        params = []
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

        method = f"{self.ns}_uninstallFilter"
        params = [filterId]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_kaia_getFilterLogs_error_wrong_type_param(self):
        method = f"{self.ns}_newFilter"
        fromBlock = "latest"
        params = [{"fromBlock": fromBlock}]
        result, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)
        filterId = result
        Utils.waiting_count("Waiting for", 5, "seconds until writing a block.")

        method = f"{self.ns}_getFilterLogs"
        params = [1234]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0NumberToRPCID", error)

        method = f"{self.ns}_uninstallFilter"
        params = [filterId]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_kaia_getFilterLogs_error_wrong_value_param(self):
        method = f"{self.ns}_newFilter"
        fromBlock = "latest"
        params = [{"fromBlock": fromBlock}]
        result, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)
        filterId = result
        Utils.waiting_count("Waiting for", 5, "seconds until writing a block.")

        method = f"{self.ns}_getFilterLogs"
        params = [filterId + "1"]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "FilterNotFound", error)

        method = f"{self.ns}_uninstallFilter"
        params = [filterId]
        result, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_kaia_getFilterLogs_success(self):
        method = f"{self.ns}_newFilter"
        fromBlock = "latest"
        params = [{"fromBlock": fromBlock}]
        result, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)
        filterId = result
        Utils.waiting_count("Waiting for", 5, "seconds until writing a block.")

        method = f"{self.ns}_getFilterLogs"
        params = [filterId]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

        method = f"{self.ns}_uninstallFilter"
        params = [filterId]
        result, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_kaia_getLogs_error_no_param(self):
        method = f"{self.ns}_getLogs"
        params = []
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

    def test_kaia_getLogs_error_wrong_type_param(self):
        method = f"{self.ns}_getLogs"
        params = [{"fromBlock": "fromBlock"}]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0HexWithoutPrefix", error)

    def test_kaia_getLogs_error_unsupported_fromBlock_tag_param(self):
        method = f"{self.ns}_getLogs"
        params = [{"fromBlock": "pending"}]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "PendingLogsNotSupported", error)

    def test_kaia_getLogs_error_unsupported_toBlock_tag_param(self):
        method = f"{self.ns}_getLogs"
        params = [{"toBLock": "pending"}]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "PendingLogsNotSupported", error)

    def test_kaia_getLogs_success_wrong_value_param(self):
        method = f"{self.ns}_getLogs"
        params = [{"fromBlock": "0xffffffff"}]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_kaia_getLogs_success(self):
        method = f"{self.ns}_getLogs"
        fromBlock = "latest"
        params = [{"fromBlock": fromBlock}]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_kaia_subscribe_error_wrong_subscription_name(self):
        method = f"{self.ns}_subscribe"
        params = []
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "InvalidSubscriptionName", error)

    def test_kaia_subscribe_newHeads_success(self):
        method = f"{self.ns}_subscribe"
        params = ["newHeads"]
        result, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)
        subId = result
        Utils.waiting_count("Waiting for", 5, "seconds until writing a block.")

        method = f"{self.ns}_unsubscribe"
        params = [subId]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        #self.assertIsNone(error) # doesn't work well because unsubscribe API has a bug...

    def test_kaia_subscribe_newHeads_success_and_recieved_data(self):
        method = f"{self.ns}_subscribe"
        params = ["newHeads"]
        result, error, ws = Utils.open_ws(self.endpoint, method, params, self.log_path)
        try:
            self.assertIsNone(error)
            self.assertIsNotNone(result)
            Utils.waiting_count("Waiting for", 5, "seconds until writing a block.")

            response = ws.recv()
            Utils.check_response_type_newHeads_subscription_kaia(self, response)

        finally:
            ws.close()

    def test_kaia_subscribe_logs_error_wrong_type_param(self):
        method = f"{self.ns}_subscribe"
        fromBlock = "1234"
        params = ["logs", {"fromBlock": fromBlock}]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg1HexWithoutPrefix", error)

    def test_kaia_subscribe_logs_error_unsupported_fromBlock_tag_param(self):
        method = f"{self.ns}_subscribe"
        params = ["logs", {"fromBlock": "pending"}]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "PendingLogsNotSupported", error)

    def test_kaia_subscribe_logs_error_unsupported_toBlock_tag_param(self):
        method = f"{self.ns}_subscribe"
        params = ["logs", {"toBlock": "pending"}]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "PendingLogsNotSupported", error)

    def test_kaia_subscribe_logs_success(self):
        method = f"{self.ns}_subscribe"
        params = ["logs", {}]
        result, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)
        subId = result
        Utils.waiting_count("Waiting for", 5, "seconds until writing a block.")

        method = f"{self.ns}_unsubscribe"
        params = [subId]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        #self.assertIsNone(error) # doesn't work well because unsubscribe has a bug...

    @staticmethod
    def suite():
        suite = unittest.TestSuite()
        suite.addTest(TestKaiaNamespaceFilterWS("test_kaia_newFilter_error_no_param"))
        suite.addTest(TestKaiaNamespaceFilterWS("test_kaia_newFilter_error_wrong_type_param"))
        suite.addTest(TestKaiaNamespaceFilterWS("test_kaia_newFilter_error_unsupported_fromBlock_tag_param"))
        suite.addTest(TestKaiaNamespaceFilterWS("test_kaia_newFilter_error_unsupported_toBlock_tag_param"))
        suite.addTest(TestKaiaNamespaceFilterWS("test_kaia_newFilter_success"))
        suite.addTest(TestKaiaNamespaceFilterWS("test_kaia_newBlockFilter_success_wrong_value_param"))
        suite.addTest(TestKaiaNamespaceFilterWS("test_kaia_newBlockFilter_success"))
        suite.addTest(TestKaiaNamespaceFilterWS("test_kaia_newPendingTransactionFilter_success_wrong_value_param"))
        suite.addTest(TestKaiaNamespaceFilterWS("test_kaia_newPendingTransactionFilter_success"))
        suite.addTest(TestKaiaNamespaceFilterWS("test_kaia_uninstallFilter_error_no_param"))
        suite.addTest(TestKaiaNamespaceFilterWS("test_kaia_uninstallFilter_error_wrong_type_param"))
        suite.addTest(TestKaiaNamespaceFilterWS("test_kaia_uninstallFilter_success_false"))
        suite.addTest(TestKaiaNamespaceFilterWS("test_kaia_uninstallFilter_success"))
        suite.addTest(TestKaiaNamespaceFilterWS("test_kaia_getFilterChanges_error_no_param"))
        suite.addTest(TestKaiaNamespaceFilterWS("test_kaia_getFilterChanges_error_wrong_type_param"))
        suite.addTest(TestKaiaNamespaceFilterWS("test_kaia_getFilterChanges_error_wrong_value_param"))
        suite.addTest(TestKaiaNamespaceFilterWS("test_kaia_getFilterChanges_success"))
        suite.addTest(TestKaiaNamespaceFilterWS("test_kaia_getFilterLogs_error_no_param"))
        suite.addTest(TestKaiaNamespaceFilterWS("test_kaia_getFilterLogs_error_wrong_type_param"))
        suite.addTest(TestKaiaNamespaceFilterWS("test_kaia_getFilterLogs_error_wrong_value_param"))
        suite.addTest(TestKaiaNamespaceFilterWS("test_kaia_getFilterLogs_success"))
        suite.addTest(TestKaiaNamespaceFilterWS("test_kaia_getLogs_error_no_param"))
        suite.addTest(TestKaiaNamespaceFilterWS("test_kaia_getLogs_error_wrong_type_param"))
        suite.addTest(TestKaiaNamespaceFilterWS("test_kaia_getLogs_error_unsupported_fromBlock_tag_param"))
        suite.addTest(TestKaiaNamespaceFilterWS("test_kaia_getLogs_error_unsupported_toBlock_tag_param"))
        suite.addTest(TestKaiaNamespaceFilterWS("test_kaia_getLogs_success_wrong_value_param"))
        suite.addTest(TestKaiaNamespaceFilterWS("test_kaia_getLogs_success"))
        suite.addTest(TestKaiaNamespaceFilterWS("test_kaia_subscribe_error_wrong_subscription_name"))
        suite.addTest(TestKaiaNamespaceFilterWS("test_kaia_subscribe_newHeads_success"))
        suite.addTest(TestKaiaNamespaceFilterWS("test_kaia_subscribe_newHeads_success_and_recieved_data"))
        suite.addTest(TestKaiaNamespaceFilterWS("test_kaia_subscribe_logs_error_wrong_type_param"))
        suite.addTest(TestKaiaNamespaceFilterWS("test_kaia_subscribe_logs_error_unsupported_fromBlock_tag_param"))
        suite.addTest(TestKaiaNamespaceFilterWS("test_kaia_subscribe_logs_error_unsupported_toBlock_tag_param"))
        suite.addTest(TestKaiaNamespaceFilterWS("test_kaia_subscribe_logs_success"))
        return suite
