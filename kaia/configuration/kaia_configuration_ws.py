import unittest
from utils import Utils
from common import kaia as kaia_common

# test_data_set is injected by rpc-tester/main.py
global test_data_set


class TestKaiaNamespaceConfigurationWS(unittest.TestCase):
    config = Utils.get_config()
    _, _, log_path = Utils.get_log_filename_with_path()
    endpoint = config.get("endpoint")
    rpc_port = config.get("rpcPort")
    ws_port = config.get("wsPort")
    ns = "kaia"
    waiting_count = 2

    def test_kaia_protocolVersion_success_wrong_value_param(self):
        method = f"{self.ns}_protocolVersion"
        _, error = Utils.call_ws(self.endpoint, method, ["abcd"], self.log_path)
        self.assertIsNone(error)

    def test_kaia_protocolVersion_success(self):
        method = f"{self.ns}_protocolVersion"
        _, error = Utils.call_ws(self.endpoint, method, [], self.log_path)
        self.assertIsNone(error)

    def test_kaia_gasPrice_success_wrong_value_param(self):
        method = f"{self.ns}_gasPrice"
        _, error = Utils.call_ws(self.endpoint, method, ["abcd"], self.log_path)
        self.assertIsNone(error)

    def test_kaia_gasPrice_success(self):
        method = f"{self.ns}_gasPrice"
        _, error = Utils.call_ws(self.endpoint, method, [], self.log_path)
        self.assertIsNone(error)

    def test_kaia_isParallelDBWrite_success_wrong_value_param(self):
        method = f"{self.ns}_isParallelDBWrite"
        _, error = Utils.call_ws(self.endpoint, method, ["abcd"], self.log_path)
        self.assertIsNone(error)

    def test_kaia_isParallelDBWrite_success(self):
        method = f"{self.ns}_isParallelDBWrite"
        _, error = Utils.call_ws(self.endpoint, method, [], self.log_path)
        self.assertIsNone(error)

    def test_kaia_isSenderTxHashIndexingEnabled_success_wrong_value_param(self):
        method = f"{self.ns}_isSenderTxHashIndexingEnabled"
        _, error = Utils.call_ws(self.endpoint, method, ["abcd"], self.log_path)
        self.assertIsNone(error)

    def test_kaia_isSenderTxHashIndexingEnabled_success(self):
        method = f"{self.ns}_isSenderTxHashIndexingEnabled"
        _, error = Utils.call_ws(self.endpoint, method, [], self.log_path)
        self.assertIsNone(error)

    def test_kaia_rewardbase_success_wrong_value_param(self):
        method = f"{self.ns}_rewardbase"
        _, error = Utils.call_ws(self.endpoint, method, ["abcd"], self.log_path)
        self.assertIsNone(error)

    def test_kaia_rewardbase_success(self):
        method = f"{self.ns}_rewardbase"
        _, error = Utils.call_ws(self.endpoint, method, [], self.log_path)
        self.assertIsNone(error)

    # getChainConfig, getParams APIs override deprecated parameters depending on hardfork:
    # see here https://github.com/kaiachain/kaia/pull/92
    def test_kaia_getChainConfig_success_with_value_param(self):
        method = f"{self.ns}_getChainConfig"
        blockNum, _ = Utils.call_ws(self.endpoint, f"{self.ns}_blockNumber", [], self.log_path)
        res, error = Utils.call_ws(self.endpoint, method, [blockNum], self.log_path)
        if 'kaiaCompatibleBlock' in res and int(blockNum, 16) >= res['kaiaCompatibleBlock']:
            self.assertEqual(1, res['governance']['reward']['stakingUpdateInterval'], 1)
        if 'RandaoCompatibleBlock' in res and int(blockNum, 16) >= res['RandaoCompatibleBlock']:
            self.assertEqual(1, res['governance']['reward']['proposerUpdateInterval'], 1)
        if 'koreCompatibleBlock' in res and int(blockNum, 16) >= res['koreCompatibleBlock']:
            self.assertEqual(False, res['governance']['reward']['useGiniCoeff'], False)

    def test_kaia_getChainConfig_error_wrong_type_value(self):
        method = f"{self.ns}_getChainConfig"
        _, error = Utils.call_ws(self.endpoint, method, ["abcd"], self.log_path)
        Utils.check_error(self, "arg0HexWithoutPrefix", error)

    def test_kaia_getChainConfig_success_without_value_param(self):
        method = f"{self.ns}_getChainConfig"
        _, error = Utils.call_ws(self.endpoint, method, [], self.log_path)
        self.assertIsNone(error)

    def test_kaia_getParams_success_with_value_param(self):
        method = f"{self.ns}_getParams"
        blockNum, _ = Utils.call_ws(self.endpoint, f"{self.ns}_blockNumber", [], self.log_path)
        res, error = Utils.call_ws(self.endpoint, method, [blockNum], self.log_path)
        if 'kaiaCompatibleBlock' in res and int(blockNum, 16) >= res['kaiaCompatibleBlock']:
            self.assertEqual(1, res['reward.stakingupdateinterval'], 1)
        if 'RandaoCompatibleBlock' in res and int(blockNum, 16) >= res['RandaoCompatibleBlock']:
            self.assertEqual(1, res['reward.proposerupdateinterval'], 1)
        if 'koreCompatibleBlock' in res and int(blockNum, 16) >= res['koreCompatibleBlock']:
            self.assertEqual(False, res['reward.useginicoeff'], False)

    def test_kaia_getParams_error_wrong_type_value(self):
        method = f"{self.ns}_getParams"
        _, error = Utils.call_ws(self.endpoint, method, ["abcd"], self.log_path)
        Utils.check_error(self, "arg0HexWithoutPrefix", error)

    def test_kaia_getParams_success_without_value_param(self):
        method = f"{self.ns}_getParams"
        _, error = Utils.call_ws(self.endpoint, method, [], self.log_path)
        self.assertIsNone(error)

    def test_kaia_chainId_success(self):
        method = f"{self.ns}_chainId"
        params = None
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_kaia_chainId_success_wrong_value_param(self):
        method = f"{self.ns}_chainId"
        params = ["abcd"]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_kaia_clientVersion_success_wrong_value_param(self):
        method = f"{self.ns}_clientVersion"
        params = ["abcd"]
        _, error = Utils.call_ws(self.endpoint, method, [], self.log_path)
        self.assertIsNone(error)

    def test_kaia_clientVersion_success(self):
        method = f"{self.ns}_clientVersion"
        params = []
        _, error = Utils.call_ws(self.endpoint, method, [], self.log_path)
        self.assertIsNone(error)

    def test_kaia_isConsoleLogEnabled_success_wrong_value_param(self):
        method = f"{self.ns}_isConsoleLogEnabled"
        result, error = Utils.call_ws(self.endpoint, method, ["abcd"], self.log_path)
        self.assertIsNone(error)
        self.assertEqual(result, False) # as default value

    def test_kaia_isConsoleLogEnabled_success(self):
        method = f"{self.ns}_isConsoleLogEnabled"
        result, error = Utils.call_ws(self.endpoint, method, [], self.log_path)
        self.assertIsNone(error)
        self.assertEqual(result, False) # as default value

    @staticmethod
    def suite():
        suite = unittest.TestSuite()

        suite.addTest(TestKaiaNamespaceConfigurationWS("test_kaia_protocolVersion_success_wrong_value_param"))
        suite.addTest(TestKaiaNamespaceConfigurationWS("test_kaia_protocolVersion_success"))
        suite.addTest(TestKaiaNamespaceConfigurationWS("test_kaia_gasPrice_success_wrong_value_param"))
        suite.addTest(TestKaiaNamespaceConfigurationWS("test_kaia_gasPrice_success"))

        suite.addTest(TestKaiaNamespaceConfigurationWS("test_kaia_isParallelDBWrite_success_wrong_value_param"))
        suite.addTest(TestKaiaNamespaceConfigurationWS("test_kaia_isParallelDBWrite_success"))
        suite.addTest(
            TestKaiaNamespaceConfigurationWS("test_kaia_isSenderTxHashIndexingEnabled_success_wrong_value_param")
        )
        suite.addTest(TestKaiaNamespaceConfigurationWS("test_kaia_isSenderTxHashIndexingEnabled_success"))
        suite.addTest(TestKaiaNamespaceConfigurationWS("test_kaia_rewardbase_success_wrong_value_param"))
        suite.addTest(TestKaiaNamespaceConfigurationWS("test_kaia_rewardbase_success"))
        suite.addTest(TestKaiaNamespaceConfigurationWS("test_kaia_chainId_success"))
        suite.addTest(TestKaiaNamespaceConfigurationWS("test_kaia_chainId_success_wrong_value_param"))
        suite.addTest(TestKaiaNamespaceConfigurationWS("test_kaia_clientVersion_success_wrong_value_param"))
        suite.addTest(TestKaiaNamespaceConfigurationWS("test_kaia_clientVersion_success"))
        suite.addTest(TestKaiaNamespaceConfigurationWS("test_kaia_getChainConfig_success_with_value_param"))
        suite.addTest(TestKaiaNamespaceConfigurationWS("test_kaia_getChainConfig_error_wrong_type_value"))
        suite.addTest(TestKaiaNamespaceConfigurationWS("test_kaia_getChainConfig_success_without_value_param"))
        suite.addTest(TestKaiaNamespaceConfigurationWS("test_kaia_getParams_success_with_value_param"))
        suite.addTest(TestKaiaNamespaceConfigurationWS("test_kaia_getParams_error_wrong_type_value"))
        suite.addTest(TestKaiaNamespaceConfigurationWS("test_kaia_getParams_success_without_value_param"))
        suite.addTest(TestKaiaNamespaceConfigurationWS("test_kaia_isConsoleLogEnabled_success_wrong_value_param"))
        suite.addTest(TestKaiaNamespaceConfigurationWS("test_kaia_isConsoleLogEnabled_success"))
        return suite
