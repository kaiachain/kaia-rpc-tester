import unittest

from utils import Utils
from common import kaia as kaia_common

# test_data_set is injected by rpc-tester/main.py
global test_data_set


class TestKaiaNamespaceAccountWS(unittest.TestCase):
    config = Utils.get_config()
    _, _, log_path = Utils.get_log_filename_with_path()
    endpoint = config.get("endpoint")
    rpc_port = config.get("rpcPort")
    ws_port = config.get("wsPort")
    ns = "kaia"
    waiting_count = 2

    def test_kaia_accountCreated_error_no_param(self):
        method = f"{self.ns}_accountCreated"
        _, error = Utils.call_ws(self.endpoint, method, [], self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

    def test_kaia_accountCreated_error_wrong_type_param1(self):
        block_number = kaia_common.get_block_number(self.endpoint)
        self.assertIsNotNone(block_number)

        method = f"{self.ns}_accountCreated"
        _, error = Utils.call_ws(self.endpoint, method, ["wrongAddress", block_number], self.log_path)
        Utils.check_error(self, "arg0HexToAddress", error)

    def test_kaia_accountCreated_error_wrong_type_param2(self):
        method = f"{self.ns}_accountCreated"
        address = test_data_set["account"]["sender"]["address"]
        _, error = Utils.call_ws(self.endpoint, method, [address, "blockNumber"], self.log_path)
        Utils.check_error(self, "arg1HexWithoutPrefix", error)

    def test_kaia_accountCreated_success(self):
        block_number = kaia_common.get_block_number(self.endpoint)
        self.assertIsNotNone(block_number)

        method = f"{self.ns}_accountCreated"
        address = test_data_set["account"]["sender"]["address"]
        _, error = Utils.call_ws(self.endpoint, method, [address, block_number], self.log_path)
        self.assertIsNone(error)

    def test_kaia_accounts_success_wrong_value_param(self):
        block_number = kaia_common.get_block_number(self.endpoint)
        self.assertIsNotNone(block_number)

        method = f"{self.ns}_accounts"
        _, error = Utils.call_ws(self.endpoint, method, ["abcd"], self.log_path)
        self.assertIsNone(error)

    def test_kaia_accounts_success(self):
        block_number = kaia_common.get_block_number(self.endpoint)
        self.assertIsNotNone(block_number)

        method = f"{self.ns}_accounts"
        _, error = Utils.call_ws(self.endpoint, method, [], self.log_path)
        self.assertIsNone(error)

    def test_kaia_getAccount_error_no_param(self):
        method = f"{self.ns}_getAccount"
        _, error = Utils.call_ws(self.endpoint, method, [], self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

    def test_kaia_getAccount_error_wrong_type_param1(self):
        block_number = kaia_common.get_block_number(self.endpoint)
        self.assertIsNotNone(block_number)

        method = f"{self.ns}_getAccount"
        _, error = Utils.call_ws(self.endpoint, method, ["wrongAddress", block_number], self.log_path)
        Utils.check_error(self, "arg0HexToAddress", error)

    def test_kaia_getAccount_error_wrong_type_param2(self):
        address = test_data_set["account"]["sender"]["address"]
        method = f"{self.ns}_getAccount"
        _, error = Utils.call_ws(self.endpoint, method, [address, "blockNumber"], self.log_path)
        Utils.check_error(self, "arg1HexWithoutPrefix", error)

    def test_kaia_getAccount_error_wrong_value_param1(self):
        address = test_data_set["account"]["sender"]["address"]
        method = f"{self.ns}_getAccount"
        _, error = Utils.call_ws(self.endpoint, method, [address, "0xffffffff"], self.log_path)
        Utils.check_error(self, "HeaderNotExist", error)

    def test_kaia_getAccount_success(self):
        address = test_data_set["account"]["sender"]["address"]
        method = f"{self.ns}_getAccount"
        _, error = Utils.call_ws(self.endpoint, method, [address, "latest"], self.log_path)
        self.assertIsNone(error)

    def test_kaia_getAccountKey_error_no_param(self):
        block_number = kaia_common.get_block_number(self.endpoint)
        self.assertIsNotNone(block_number)

        method = f"{self.ns}_getAccountKey"
        _, error = Utils.call_ws(self.endpoint, method, [], self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

    def test_kaia_getAccountKey_error_wrong_type_param1(self):
        method = f"{self.ns}_getAccountKey"
        _, error = Utils.call_ws(self.endpoint, method, ["wrongAddress", "latest"], self.log_path)
        Utils.check_error(self, "arg0HexToAddress", error)

    def test_kaia_getAccountKey_error_wrong_type_param2(self):
        address = test_data_set["account"]["sender"]["address"]
        method = f"{self.ns}_getAccountKey"
        _, error = Utils.call_ws(self.endpoint, method, [address, "blockNumber"], self.log_path)
        Utils.check_error(self, "arg1HexWithoutPrefix", error)

    def test_kaia_getAccountKey_error_wrong_value_param1(self):
        address = test_data_set["account"]["sender"]["address"]
        method = f"{self.ns}_getAccountKey"
        _, error = Utils.call_ws(self.endpoint, method, [address, "0xffffffff"], self.log_path)
        Utils.check_error(self, "HeaderNotExist", error)

    def test_kaia_getAccountKey_success(self):
        address = test_data_set["account"]["sender"]["address"]
        method = f"{self.ns}_getAccountKey"
        _, error = Utils.call_ws(self.endpoint, method, [address, "latest"], self.log_path)
        self.assertIsNone(error)

    def test_kaia_getBalance_error_no_param(self):
        method = f"{self.ns}_getBalance"
        address = test_data_set["account"]["sender"]["address"]
        tag = "latest"
        params = []
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

    def test_kaia_getBalance_error_wrong_type_param1(self):
        method = f"{self.ns}_getBalance"
        address = test_data_set["account"]["sender"]["address"]
        tag = "latest"
        params = ["address", tag]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0HexToAddress", error)

    def test_kaia_getBalance_error_wrong_type_param2(self):
        method = f"{self.ns}_getBalance"
        address = test_data_set["account"]["sender"]["address"]
        tag = "latest"
        params = [address, "tag"]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg1HexWithoutPrefix", error)

    def test_kaia_getBalance_error_wrong_value_param(self):
        method = f"{self.ns}_getBalance"
        address = test_data_set["account"]["sender"]["address"]
        tag = "latest"
        params = [address, "0xffffffff"]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "HeaderNotExist", error)

    def test_kaia_getBalance_success(self):
        method = f"{self.ns}_getBalance"
        address = test_data_set["account"]["sender"]["address"]
        tag = "latest"
        params = [address, tag]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_kaia_isContractAccount_error_no_param(self):
        method = f"{self.ns}_isContractAccount"
        address = test_data_set["account"]["sender"]["address"]
        tag = "latest"
        params = []
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

    def test_kaia_isContractAccount_error_wrong_type_param1(self):
        method = f"{self.ns}_isContractAccount"
        address = test_data_set["account"]["sender"]["address"]
        tag = "latest"
        params = ["address", tag]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0HexToAddress", error)

    def test_kaia_isContractAccount_error_wrong_type_param2(self):
        method = f"{self.ns}_isContractAccount"
        address = test_data_set["account"]["sender"]["address"]
        tag = "latest"
        params = [address, "tag"]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg1HexWithoutPrefix", error)

    def test_kaia_isContractAccount_error_wrong_value_param(self):
        method = f"{self.ns}_isContractAccount"
        address = test_data_set["account"]["sender"]["address"]
        tag = "latest"
        params = [address, "0xffffffff"]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "HeaderNotExist", error)

    def test_kaia_isContractAccount_success(self):
        method = f"{self.ns}_isContractAccount"
        address = test_data_set["account"]["sender"]["address"]
        tag = "latest"
        params = [address, tag]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_kaia_getTransactionCount_error_no_param(self):
        method = f"{self.ns}_getTransactionCount"
        address = test_data_set["account"]["sender"]["address"]
        tag = "latest"
        params = None
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

    def test_kaia_getTransactionCount_error_wrong_type_param1(self):
        method = f"{self.ns}_getTransactionCount"
        address = test_data_set["account"]["sender"]["address"]
        tag = "latest"
        params = ["address", tag]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0HexToAddress", error)

    def test_kaia_getTransactionCount_error_wrong_type_param2(self):
        method = f"{self.ns}_getTransactionCount"
        address = test_data_set["account"]["sender"]["address"]
        tag = "latest"
        params = [address, "tag"]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg1HexWithoutPrefix", error)

    def test_kaia_getTransactionCount_error_wrong_value_param(self):
        method = f"{self.ns}_getTransactionCount"
        address = test_data_set["account"]["sender"]["address"]
        tag = "latest"
        params = [address, "0xffffffff"]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "HeaderNotExist", error)

    def test_kaia_getTransactionCount_success(self):
        method = f"{self.ns}_getTransactionCount"
        address = test_data_set["account"]["sender"]["address"]
        tag = "latest"
        params = [address, tag]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_kaia_getCode_error_no_param(self):
        method = f"{self.ns}_getCode"
        _, error = Utils.call_ws(self.endpoint, method, [], self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

    def test_kaia_getCode_error_wrong_type_param1(self):
        method = f"{self.ns}_getCode"
        tag = "latest"
        params = ["contractAddress", tag]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0HexToAddress", error)

    def test_kaia_getCode_error_wrong_type_param2(self):
        method = f"{self.ns}_getCode"
        tag = "latest"
        contractAddress = test_data_set["contracts"]["unknown"]["address"][0]
        params = [contractAddress, "tag"]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg1HexWithoutPrefix", error)

    def test_kaia_getCode_error_wrong_value_param(self):
        method = f"{self.ns}_getCode"
        tag = "latest"
        contractAddress = test_data_set["contracts"]["unknown"]["address"][0]
        params = [contractAddress, "0xffffffff"]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "HeaderNotExist", error)

    def test_kaia_getCode_success(self):
        block_number = kaia_common.get_block_number(self.endpoint)
        self.assertIsNotNone(block_number)

        method = f"{self.ns}_getCode"
        tag = "latest"
        contractAddress = test_data_set["contracts"]["unknown"]["address"][0]
        params = [contractAddress, tag]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_kaia_sign_error_no_param(self):
        method = f"{self.ns}_sign"
        _, error = Utils.call_ws(self.endpoint, method, [], self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

    def test_kaia_sign_error_wrong_type_param1(self):
        method = f"{self.ns}_sign"
        message = Utils.convert_to_hex("Hi Utils!")
        params = ["address", message]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0HexToAddress", error)

    def test_kaia_sign_error_wrong_type_param2(self):
        method = f"{self.ns}_sign"
        message = Utils.convert_to_hex("Hi Utils!")
        address = test_data_set["account"]["sender"]["address"]
        params = [address, "message"]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg1HexToBytes", error)

    def test_kaia_sign_success(self):
        block_number = kaia_common.get_block_number(self.endpoint)
        self.assertIsNotNone(block_number)

        method = f"{self.ns}_sign"
        message = Utils.convert_to_hex("Hi Utils!")
        address = test_data_set["account"]["sender"]["address"]
        params = [address, message]
        result, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

        signature = result

        method = "personal_ecRecover"
        message = Utils.convert_to_hex("Hi Utils!")
        params = [message, signature]
        result, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)
        validAddress = result

        self.assertEqual(address.lower(), validAddress.lower())

    @staticmethod
    def suite():
        suite = unittest.TestSuite()
        suite.addTest(TestKaiaNamespaceAccountWS("test_kaia_accountCreated_error_no_param"))
        suite.addTest(TestKaiaNamespaceAccountWS("test_kaia_accountCreated_error_wrong_type_param1"))
        suite.addTest(TestKaiaNamespaceAccountWS("test_kaia_accountCreated_error_wrong_type_param2"))
        suite.addTest(TestKaiaNamespaceAccountWS("test_kaia_accountCreated_success"))
        suite.addTest(TestKaiaNamespaceAccountWS("test_kaia_accounts_success_wrong_value_param"))
        suite.addTest(TestKaiaNamespaceAccountWS("test_kaia_accounts_success"))
        suite.addTest(TestKaiaNamespaceAccountWS("test_kaia_getAccount_error_no_param"))
        suite.addTest(TestKaiaNamespaceAccountWS("test_kaia_getAccount_error_wrong_type_param1"))
        suite.addTest(TestKaiaNamespaceAccountWS("test_kaia_getAccount_error_wrong_type_param2"))
        suite.addTest(TestKaiaNamespaceAccountWS("test_kaia_getAccount_error_wrong_value_param1"))
        suite.addTest(TestKaiaNamespaceAccountWS("test_kaia_getAccount_success"))
        suite.addTest(TestKaiaNamespaceAccountWS("test_kaia_getAccountKey_error_no_param"))
        suite.addTest(TestKaiaNamespaceAccountWS("test_kaia_getAccountKey_error_wrong_type_param1"))
        suite.addTest(TestKaiaNamespaceAccountWS("test_kaia_getAccountKey_error_wrong_type_param2"))
        suite.addTest(TestKaiaNamespaceAccountWS("test_kaia_getAccountKey_error_wrong_value_param1"))
        suite.addTest(TestKaiaNamespaceAccountWS("test_kaia_getAccountKey_success"))
        suite.addTest(TestKaiaNamespaceAccountWS("test_kaia_getBalance_error_no_param"))

        suite.addTest(TestKaiaNamespaceAccountWS("test_kaia_getBalance_error_wrong_type_param1"))
        suite.addTest(TestKaiaNamespaceAccountWS("test_kaia_getBalance_error_wrong_type_param2"))
        suite.addTest(TestKaiaNamespaceAccountWS("test_kaia_getBalance_error_wrong_value_param"))

        suite.addTest(TestKaiaNamespaceAccountWS("test_kaia_getBalance_success"))

        suite.addTest(TestKaiaNamespaceAccountWS("test_kaia_isContractAccount_error_no_param"))

        suite.addTest(TestKaiaNamespaceAccountWS("test_kaia_isContractAccount_error_wrong_type_param1"))
        suite.addTest(TestKaiaNamespaceAccountWS("test_kaia_isContractAccount_error_wrong_type_param2"))
        suite.addTest(TestKaiaNamespaceAccountWS("test_kaia_isContractAccount_error_wrong_value_param"))

        suite.addTest(TestKaiaNamespaceAccountWS("test_kaia_isContractAccount_success"))

        suite.addTest(TestKaiaNamespaceAccountWS("test_kaia_getTransactionCount_error_no_param"))
        suite.addTest(TestKaiaNamespaceAccountWS("test_kaia_getTransactionCount_error_wrong_type_param1"))
        suite.addTest(TestKaiaNamespaceAccountWS("test_kaia_getTransactionCount_error_wrong_type_param2"))
        suite.addTest(TestKaiaNamespaceAccountWS("test_kaia_getTransactionCount_error_wrong_value_param"))

        suite.addTest(TestKaiaNamespaceAccountWS("test_kaia_getTransactionCount_success"))
        suite.addTest(TestKaiaNamespaceAccountWS("test_kaia_getCode_error_no_param"))
        suite.addTest(TestKaiaNamespaceAccountWS("test_kaia_getCode_error_wrong_type_param1"))
        suite.addTest(TestKaiaNamespaceAccountWS("test_kaia_getCode_error_wrong_type_param2"))
        suite.addTest(TestKaiaNamespaceAccountWS("test_kaia_getCode_error_wrong_value_param"))
        suite.addTest(TestKaiaNamespaceAccountWS("test_kaia_getCode_success"))

        suite.addTest(TestKaiaNamespaceAccountWS("test_kaia_sign_error_no_param"))
        suite.addTest(TestKaiaNamespaceAccountWS("test_kaia_sign_error_wrong_type_param1"))
        suite.addTest(TestKaiaNamespaceAccountWS("test_kaia_sign_error_wrong_type_param2"))
        suite.addTest(TestKaiaNamespaceAccountWS("test_kaia_sign_success"))

        return suite
