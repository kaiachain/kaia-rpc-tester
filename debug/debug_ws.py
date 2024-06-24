import unittest

from utils import Utils
from common import kaia as kaia_common
from common import personal as personal_common
from utils import PROJECT_ROOT_DIR

# test_data_set is injected by rpc-tester/main.py
global test_data_set


class TestDebugNamespaceWS(unittest.TestCase):
    config = Utils.get_config()
    _, _, log_path = Utils.get_log_filename_with_path()
    endpoint = config.get("endpoint")
    rpc_port = config.get("rpcPort")
    ws_port = config.get("wsPort")
    ns = "debug"
    waiting_count = 2

    def create_params_for_starting_pprof(self):
        ip_address = "0.0.0.0"
        port = 6060
        return [ip_address, port]

    def test_debug_startPProf_error_wrong_type_param1(self):
        method = f"{self.ns}_startPProf"
        params = self.create_params_for_starting_pprof()
        params[0] = 1234  # Invlaid ip address
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0NumberToString", error)

    def test_debug_startPProf_error_wrong_type_param2(self):
        method = f"{self.ns}_startPProf"
        params = self.create_params_for_starting_pprof()
        params[1] = "6060"  # Invlaid port
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg1StringToInt", error)

    def test_debug_startPProf_success_no_param(self):
        method = f"{self.ns}_startPProf"
        _, error = Utils.call_ws(self.endpoint, method, None, self.log_path)
        self.assertIsNone(error)

    def test_debug_startPProf_error_already_running(self):
        method = f"{self.ns}_startPProf"
        params = self.create_params_for_starting_pprof()
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "PProfServerAlreadyRunning", error)

    def test_debug_stopPProf_success(self):
        method = f"{self.ns}_stopPProf"
        _, error = Utils.call_ws(self.endpoint, method, [], self.log_path)
        self.assertIsNone(error)

    def test_debug_stopPProf_error_not_running(self):
        method = f"{self.ns}_stopPProf"
        _, error = Utils.call_ws(self.endpoint, method, [], self.log_path)
        Utils.check_error(self, "PProfServerNotRunning", error)

    def test_debug_startPProf_success(self):
        method = f"{self.ns}_startPProf"
        params = self.create_params_for_starting_pprof()
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

        # Stop pprof server for further tests
        method = f"{self.ns}_stopPProf"
        Utils.call_ws(self.endpoint, method, [], self.log_path)

    def test_debug_isPProfRunning_success_wrong_value_param(self):
        method = f"{self.ns}_isPProfRunning"
        _, error = Utils.call_ws(self.endpoint, method, ["abcd"], self.log_path)
        self.assertIsNone(error)

    def test_debug_isPProfRunning_success(self):
        method = f"{self.ns}_isPProfRunning"
        _, error = Utils.call_ws(self.endpoint, method, [], self.log_path)
        self.assertIsNone(error)

    def test_debug_getModifiedAccountsByHash_error_no_param1(self):
        method = f"{self.ns}_getModifiedAccountsByHash"
        _, error = Utils.call_ws(self.endpoint, method, [], self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

    def test_debug_getModifiedAccountsByHash_error_wrong_type_param1(self):
        method = f"{self.ns}_getModifiedAccountsByHash"
        params = ["startBlockHash", "endBlockHash"]  # Invalid params
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0HexToHash", error)

    def test_debug_getModifiedAccountsByHash_error_wrong_type_param2(self):
        latest_block = kaia_common.get_latest_block_by_number(self.endpoint)
        self.assertIsNotNone(latest_block)
        start_block_hash = latest_block["parentHash"]

        method = f"{self.ns}_getModifiedAccountsByHash"
        params = [start_block_hash, "endBlockHash"]  # Invalid param at index 1.
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg1HexToHash", error)

    def test_debug_getModifiedAccountsByHash_error_wrong_value_param1(self):
        latest_block = kaia_common.get_latest_block_by_number(self.endpoint)
        self.assertIsNotNone(latest_block)
        start_block_hash = latest_block["parentHash"]
        non_existing_start_block_hash = start_block_hash[:-3] + "fff"
        end_block_hash = latest_block["hash"]

        method = f"{self.ns}_getModifiedAccountsByHash"
        params = [non_existing_start_block_hash, end_block_hash]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertEqual(-32000, error.get("code"))
        self.assertEqual(
            f"start block {non_existing_start_block_hash[2:]} not found",
            error.get("message"),
        )

    def test_debug_getModifiedAccountsByHash_error_wrong_value_param2(self):
        latest_block = kaia_common.get_latest_block_by_number(self.endpoint)
        self.assertIsNotNone(latest_block)
        start_block_hash = latest_block["parentHash"]
        end_block_hash = latest_block["hash"]
        non_existing_end_block_hash = end_block_hash[:-3] + "fff"

        method = f"{self.ns}_getModifiedAccountsByHash"
        params = [start_block_hash, non_existing_end_block_hash]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertEqual(-32000, error.get("code"))
        self.assertEqual(
            f"end block {non_existing_end_block_hash[2:]} not found",
            error.get("message"),
        )

    def test_debug_getModifiedAccountsByHash_success(self):
        latest_block = kaia_common.get_latest_block_by_number(self.endpoint)
        self.assertIsNotNone(latest_block)
        start_block_hash = latest_block["parentHash"]
        end_block_hash = latest_block["hash"]

        method = f"{self.ns}_getModifiedAccountsByHash"
        params = [start_block_hash, end_block_hash]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_debug_getModifiedAccountsByNumber_error_no_param1(self):
        method = f"{self.ns}_getModifiedAccountsByNumber"
        _, error = Utils.call_ws(self.endpoint, method, [], self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

    def test_debug_getModifiedAccountsByNumber_error_wrong_type_param1(self):
        method = f"{self.ns}_getModifiedAccountsByNumber"
        _, error = Utils.call_ws(self.endpoint, method, ["startBlockNum", "endBlockNum"], self.log_path)
        Utils.check_error(self, "arg0HexWithoutPrefix", error)

    def test_debug_getModifiedAccountsByNumber_error_wrong_type_param2(self):
        block_number = kaia_common.get_block_number(self.endpoint)
        self.assertIsNotNone(block_number)
        start_block_number = int(block_number, 0)

        method = f"{self.ns}_getModifiedAccountsByNumber"
        params = [start_block_number, "endBlockNum"]  # Invalid param at index 1
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg1HexWithoutPrefix", error)

    def test_debug_getModifiedAccountsByNumber_error_wrong_value_param1(self):
        block_number = kaia_common.get_block_number(self.endpoint)
        self.assertIsNotNone(block_number)
        block_number = int(block_number, 0)
        start_block_number = block_number + 1000
        end_block_number = block_number

        method = f"{self.ns}_getModifiedAccountsByNumber"
        params = [start_block_number, end_block_number]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertEqual(-32000, error.get("code"))
        self.assertEqual(f"start block number #{start_block_number} not found", error.get("message"))

    def test_debug_getModifiedAccountsByNumber_error_wrong_value_param2(self):
        block_number = kaia_common.get_block_number(self.endpoint)
        self.assertIsNotNone(block_number)
        block_number = int(block_number, 0)
        start_block_number = block_number - 1
        end_block_number = block_number + 1000

        method = f"{self.ns}_getModifiedAccountsByNumber"
        params = [start_block_number, end_block_number]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertEqual(-32000, error.get("code"))
        self.assertEqual(f"end block number #{end_block_number} not found", error.get("message"))

    def test_debug_getModifiedAccountsByNumber_success(self):
        block_number = kaia_common.get_block_number(self.endpoint)
        self.assertIsNotNone(block_number)
        block_number = int(block_number, 0)
        start_block_number = block_number - 1
        end_block_number = block_number

        method = f"{self.ns}_getModifiedAccountsByNumber"
        params = [start_block_number, end_block_number]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_debug_backtraceAt_success(self):
        method = f"{self.ns}_backtraceAt"
        params = ["agent.go:97"]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_debug_backtraceAt_error_no_param(self):
        method = f"{self.ns}_backtraceAt"
        _, error = Utils.call_ws(self.endpoint, method, [], self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

    def test_debug_backtraceAt_error_wrong_type_param(self):
        method = f"{self.ns}_backtraceAt"
        _, error = Utils.call_ws(self.endpoint, method, [1234], self.log_path)
        Utils.check_error(self, "arg0NumberToString", error)

    def test_debug_backtraceAt_error_wrong_value_param(self):
        method = f"{self.ns}_backtraceAt"
        _, error = Utils.call_ws(self.endpoint, method, ["abcd"], self.log_path)
        self.assertEqual(-32000, error.get("code"))
        self.assertEqual("expect file.go:234", error.get("message"))

    def test_debug_blockProfile_success(self):
        method = f"{self.ns}_blockProfile"
        params = ["block_created_by_ws.profile", 1]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_debug_blockProfile_error_no_param(self):
        method = f"{self.ns}_blockProfile"
        _, error = Utils.call_ws(self.endpoint, method, None, self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

    def test_debug_blockProfile_error_wrong_type_param1(self):
        method = f"{self.ns}_blockProfile"
        params = [10, 10]  # Invalid param at index 0
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0NumberToString", error)

    def test_debug_blockProfile_error_wrong_type_param2(self):
        method = f"{self.ns}_blockProfile"
        params = [
            "block_created_by_ws.profile",
            "wrongtype",
        ]  # Invalid param at index 1
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg1StringToUint", error)

    def test_debug_cpuProfile_error_no_param(self):
        method = f"{self.ns}_cpuProfile"
        _, error = Utils.call_ws(self.endpoint, method, None, self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

    def test_debug_cpuProfile_error_wrong_type_param1(self):
        method = f"{self.ns}_cpuProfile"
        params = ["cpu_created_by_ws.profile", "wrongTypeParam1"]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg1StringToUint", error)

    def test_debug_cpuProfile_error_wrong_type_param2(self):
        method = f"{self.ns}_cpuProfile"
        params = [10, 10]  # Invalid param at index 0
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0NumberToString", error)

    def test_debug_cpuProfile_success(self):
        method = f"{self.ns}_cpuProfile"
        params = ["cpu_created_by_ws.profile", 1]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_debug_dumpBlock_error_no_param(self):
        method = f"{self.ns}_dumpBlock"
        _, error = Utils.call_ws(self.endpoint, method, None, self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

    def test_debug_dumpBlock_error_wrong_type_param(self):
        method = f"{self.ns}_dumpBlock"
        _, error = Utils.call_ws(self.endpoint, method, ["abcd"], self.log_path)
        Utils.check_error(self, "arg0HexWithoutPrefix", error)

    def test_debug_dumpBlock_error_wrong_value_param(self):
        method = f"{self.ns}_dumpBlock"
        _, error = Utils.call_ws(self.endpoint, method, ["0xffffffff"], self.log_path)
        Utils.check_error(self, "BlockNotFound", error)

    def test_debug_dumpBlock_success(self):
        block_number = kaia_common.get_block_number(self.endpoint)
        # It must be a multiple of state.block-interval value. It is set as 128 now.
        block_number = (int(block_number, 0) // 128) * 128
        block_number = hex(block_number)

        method = f"{self.ns}_dumpBlock"
        _, error = Utils.call_ws(self.endpoint, method, [block_number], self.log_path)
        self.assertIsNone(error)

    def test_debug_gcStats_success_wrong_value_param(self):
        method = f"{self.ns}_gcStats"
        _, error = Utils.call_ws(self.endpoint, method, ["abcd"], self.log_path)
        self.assertIsNone(error)

    def test_debug_gcStats_success(self):
        method = f"{self.ns}_gcStats"
        _, error = Utils.call_ws(self.endpoint, method, None, self.log_path)
        self.assertIsNone(error)

    def test_debug_getBlockRlp_error_no_param(self):
        method = f"{self.ns}_getBlockRlp"
        _, error = Utils.call_ws(self.endpoint, method, None, self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

    def test_debug_getBlockRlp_error_wrong_type_param(self):
        method = f"{self.ns}_getBlockRlp"
        _, error = Utils.call_ws(self.endpoint, method, ["abcd"], self.log_path)
        Utils.check_error(self, "arg0HexWithoutPrefix", error)

    def test_debug_getBlockRlp_error_wrong_value_param(self):
        block_number = kaia_common.get_block_number(self.endpoint)
        invalid_block_number = int(block_number, 0) + 1000

        method = f"{self.ns}_getBlockRlp"
        _, error = Utils.call_ws(self.endpoint, method, [invalid_block_number], self.log_path)
        self.assertEqual(-32000, error.get("code"))
        self.assertEqual(f"block #{invalid_block_number} not found", error.get("message"))

    def test_debug_getBlockRlp_success(self):
        block_number = kaia_common.get_block_number(self.endpoint)
        block_number = int(block_number, 0)

        method = f"{self.ns}_getBlockRlp"
        result, error = Utils.call_ws(self.endpoint, method, [block_number], self.log_path)
        self.assertIsNone(error)
        self.assertIsNotNone(result)

        Utils.write_log(
            self.log_path,
            "",
            "",
            "",
            result,
            "block.rlp",
            True,
        )

    def test_debug_traceBlock_success(self):
        block_number = kaia_common.get_block_number(self.endpoint)
        block_number = int(block_number, 0)

        method = f"{self.ns}_getBlockRlp"
        result, error = Utils.call_ws(self.endpoint, method, [block_number], self.log_path)
        block_rlp = "0x" + result

        method = f"{self.ns}_traceBlock"
        _, error = Utils.call_ws(self.endpoint, method, [block_rlp], self.log_path)
        self.assertIsNone(error)

    def test_debug_traceBlock_error_no_param(self):
        method = f"{self.ns}_traceBlock"
        _, error = Utils.call_ws(self.endpoint, method, [], self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

    def test_debug_traceBlock_error_wrong_type_param(self):
        method = f"{self.ns}_traceBlock"
        _, error = Utils.call_ws(self.endpoint, method, ["abcd"], self.log_path)
        Utils.check_error(self, "arg0HexToBytes", error)

    def test_debug_traceBlock_error_wrong_value_param(self):
        method = f"{self.ns}_traceBlock"
        _, error = Utils.call_ws(self.endpoint, method, ["0xffff"], self.log_path)
        Utils.check_error(self, "CouldNotDecodeBlock", error)

    def test_debug_traceBlockByNumber_error_no_param(self):
        method = f"{self.ns}_traceBlockByNumber"
        _, error = Utils.call_ws(self.endpoint, method, [], self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

    def test_debug_traceBlockByNumber_error_wrong_type_param(self):
        method = f"{self.ns}_traceBlockByNumber"
        _, error = Utils.call_ws(self.endpoint, method, ["abcd"], self.log_path)
        Utils.check_error(self, "arg0HexWithoutPrefix", error)

    def test_debug_traceBlockByNumber_error_wrong_value_param(self):
        method = f"{self.ns}_traceBlockByNumber"
        _, error = Utils.call_ws(self.endpoint, method, ["0xffffffff"], self.log_path)
        Utils.check_error(self, "BlockNotExist", error)

    def test_debug_traceBlockByNumber_success(self):
        block_number = kaia_common.get_block_number(self.endpoint)
        block_number = int(block_number, 0)

        method = f"{self.ns}_traceBlockByNumber"
        _, error = Utils.call_ws(self.endpoint, method, [block_number], self.log_path)
        self.assertIsNone(error)

    def test_debug_traceBlockByHash_error_no_param(self):
        method = f"{self.ns}_traceBlockByHash"
        _, error = Utils.call_ws(self.endpoint, method, [], self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

    def test_debug_traceBlockByHash_error_wrong_type_param(self):
        method = f"{self.ns}_traceBlockByHash"
        _, error = Utils.call_ws(self.endpoint, method, ["abcd"], self.log_path)
        Utils.check_error(self, "arg0HexToHash", error)

    def test_debug_traceBlockByHash_error_wrong_value_param(self):
        latest_block = kaia_common.get_latest_block_by_number(self.endpoint)
        block_hash = latest_block["hash"]
        invalid_block_hash = block_hash[:-3] + "fff"

        method = f"{self.ns}_traceBlockByHash"
        _, error = Utils.call_ws(self.endpoint, method, [invalid_block_hash], self.log_path)
        self.assertEqual(-32000, error.get("code"))
        self.assertEqual(f"the block does not exist (block hash: " + invalid_block_hash + ")", error.get("message"))

    def test_debug_traceBlockByHash_success(self):
        latest_block = kaia_common.get_latest_block_by_number(self.endpoint)
        block_hash = latest_block["hash"]

        method = f"{self.ns}_traceBlockByHash"
        _, error = Utils.call_ws(self.endpoint, method, [block_hash], self.log_path)
        self.assertIsNone(error)

    def test_debug_traceBlockFromFile_error_no_param(self):
        method = f"{self.ns}_traceBlockFromFile"
        _, error = Utils.call_ws(self.endpoint, method, [], self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

    def test_debug_traceBlockFromFile_error_wrong_type_param(self):
        method = f"{self.ns}_traceBlockFromFile"
        _, error = Utils.call_ws(self.endpoint, method, [1234], self.log_path)
        Utils.check_error(self, "arg0NumberToString", error)

    def test_debug_traceBlockFromFile_error_wrong_value_param(self):
        method = f"{self.ns}_traceBlockFromFile"
        _, error = Utils.call_ws(self.endpoint, method, ["invalid_file"], self.log_path)
        self.assertEqual(-32000, error.get("code"))
        self.assertIn("could not read file", error.get("message"))

    def test_debug_traceBlockFromFile_success(self):
        method = f"{self.ns}_traceBlockFromFile"
        _, error = Utils.call_ws(self.endpoint, method, [f"{PROJECT_ROOT_DIR}/block.rlp"], self.log_path)
        self.assertIsNone(error)

    def test_debug_traceTransaction_error_no_param(self):
        method = f"{self.ns}_traceTransaction"
        _, error = Utils.call_ws(self.endpoint, method, [], self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

    def test_debug_traceTransaction_error_wrong_type_param1(self):
        method = f"{self.ns}_traceTransaction"
        _, error = Utils.call_ws(self.endpoint, method, ["abcd"], self.log_path)
        Utils.check_error(self, "arg0HexToHash", error)

    def test_debug_traceTransaction_error_wrong_value_param1(self):
        method = f"{self.ns}_traceTransaction"
        _, error = Utils.call_ws(
            self.endpoint,
            method,
            ["0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"],
            self.log_path,
        )
        Utils.check_error(self, "TransactionNotFound", error)

    def send_transaction(self, data=""):
        sender = test_data_set["account"]["sender"]["address"]
        password = test_data_set["account"]["sender"]["password"]
        to = test_data_set["account"]["receiver"]["address"]
        tx_fields = {
            "from": sender,
            "to": to,
            "gas": hex(304000),
            "gasPrice": test_data_set["unitGasPrice"],
            "value": hex(Utils.to_peb(1.5)),
        }
        if data != "":
            tx_fields["data"] = data
        params = [tx_fields, password]
        transaction_hash, error = personal_common.send_transaction(self.endpoint, params)
        Utils.waiting_count("Waiting for", self.waiting_count, "seconds until tx is finalized.")
        self.assertIsNone(error)
        return transaction_hash

    def test_debug_traceTransaction_error_wrong_value_param2(self):
        transaction_hash = self.send_transaction()
        invalid_tx_hash = transaction_hash[:-3] + "fff"

        method = f"{self.ns}_traceTransaction"
        _, error = Utils.call_ws(self.endpoint, method, [invalid_tx_hash], self.log_path)
        self.assertEqual(-32000, error.get("code"))
        self.assertEqual(f"transaction {invalid_tx_hash[2:]} not found", error.get("message"))

    def test_debug_traceTransaction_success(self):
        transaction_hash = self.send_transaction()

        method = f"{self.ns}_traceTransaction"
        _, error = Utils.call_ws(self.endpoint, method, [transaction_hash], self.log_path)
        self.assertIsNone(error)

    def test_debug_goTrace_error_no_param(self):
        method = f"{self.ns}_goTrace"
        _, error = Utils.call_ws(self.endpoint, method, [], self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

    def test_debug_goTrace_error_wrong_type_param1(self):
        method = f"{self.ns}_goTrace"
        params = [3, 3]  # Invalid param at index 0
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0NumberToString", error)

    def test_debug_goTrace_error_wrong_type_param2(self):
        method = f"{self.ns}_goTrace"
        params = [
            "go_created_by_ws.trace",
            "wrongDuration",
        ]  # Invalid param at index 1
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg1StringToUint", error)

    def test_debug_goTrace_success(self):
        method = f"{self.ns}_goTrace"
        params = ["go_created_by_ws.trace", 3]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_debug_memStats_success_wrong_value_param(self):
        method = f"{self.ns}_memStats"
        params = ["abcd"]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_debug_memStats_success(self):
        method = f"{self.ns}_memStats"
        _, error = Utils.call_ws(self.endpoint, method, None, self.log_path)
        self.assertIsNone(error)

    def test_debug_metrics_error_no_param(self):
        method = f"{self.ns}_metrics"
        _, error = Utils.call_ws(self.endpoint, method, None, self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

    def test_debug_metrics_error_wrong_type_param(self):
        method = f"{self.ns}_metrics"
        params = ["abcd"]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0StringToBool", error)

    def test_debug_metrics_success(self):
        method = f"{self.ns}_metrics"
        params = [True]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_debug_printBlock_error_no_param(self):
        method = f"{self.ns}_printBlock"
        _, error = Utils.call_ws(self.endpoint, method, None, self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

    def test_debug_printBlock_error_wrong_param(self):
        method = f"{self.ns}_printBlock"
        params = ["abcd"]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        Utils.check_error(self, "arg0HexWithoutPrefix", error)

    def test_debug_printBlock_success(self):
        method = f"{self.ns}_printBlock"
        params = [3]
        _, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

    def test_debug_preimage_success(self):
        # The data generate a contract executing sha3('1234') which will be used to test 'debug_preimage'
        data = "0x608060405234801561001057600080fd5b5060405180807f3132333400000000000000000000000000000000000000000000000000000000815250600401905060405180910390206000816000191690555060a98061005f6000396000f300608060405260043610603f576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff168063d46300fd146044575b600080fd5b348015604f57600080fd5b5060566074565b60405180826000191660001916815260200191505060405180910390f35b600080549050905600a165627a7a723058204ebeb407a746293d3b9db38453f9ae086ea38ff3e45ce95c45d27fa2c93259900029"
        transaction_hash = self.send_transaction(data)
        self.assertIsNotNone(transaction_hash)

        method = f"{self.ns}_preimage"
        # The hash value of sha3('1234')
        sha3_hash = "0x387a8233c96e1fc0ad5e284353276177af2186e7afa85296f106336e376669f7"
        _, error = Utils.call_ws(self.endpoint, method, [sha3_hash], self.log_path)
        self.assertIsNone(error)

    def test_debug_freeOSMemory_success_wrong_value_param(self):
        method = f"{self.ns}_freeOSMemory"
        _, error = Utils.call_ws(self.endpoint, method, ["abcd"], self.log_path)
        self.assertIsNone(error)

    def test_debug_freeOSMemory_success(self):
        method = f"{self.ns}_freeOSMemory"
        _, error = Utils.call_ws(self.endpoint, method, [], self.log_path)
        self.assertIsNone(error)

    def test_debug_setHead_success(self):
        method = f"{self.ns}_setHead"
        _, error = Utils.call_ws(self.endpoint, method, ["0x1"], self.log_path)
        self.assertIsNone(error)

    def test_debug_setBlockProfileRate_error_no_param(self):
        method = f"{self.ns}_setBlockProfileRate"
        _, error = Utils.call_ws(self.endpoint, method, None, self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

    def test_debug_setBlockProfileRate_error_wrong_type_param(self):
        method = f"{self.ns}_setBlockProfileRate"
        _, error = Utils.call_ws(self.endpoint, method, ["abcd"], self.log_path)
        Utils.check_error(self, "arg0StringToInt", error)

    def test_debug_setBlockProfileRate_success(self):
        method = f"{self.ns}_setBlockProfileRate"
        _, error = Utils.call_ws(self.endpoint, method, [1], self.log_path)
        self.assertIsNone(error)

    def test_debug_setVMLogTarget_success(self):
        method = f"{self.ns}_setVMLogTarget"
        _, error = Utils.call_ws(self.endpoint, method, [1], self.log_path)
        self.assertIsNone(error)

    def test_debug_setVMLogTarget_error_no_param(self):
        method = f"{self.ns}_setVMLogTarget"
        _, error = Utils.call_ws(self.endpoint, method, [], self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

    def test_debug_setVMLogTarget_error_wrong_type_param(self):
        method = f"{self.ns}_setVMLogTarget"
        _, error = Utils.call_ws(self.endpoint, method, ["abcd"], self.log_path)
        Utils.check_error(self, "arg0StringToInt", error)

    def test_debug_setVMLogTarget_error_wrong_value_param(self):
        method = f"{self.ns}_setVMLogTarget"
        _, error = Utils.call_ws(self.endpoint, method, [1234], self.log_path)
        Utils.check_error(self, "TargetShouldBeBetween0And3", error)

    def test_debug_writeBlockProfile_error_no_param(self):
        method = f"{self.ns}_writeBlockProfile"
        _, error = Utils.call_ws(self.endpoint, method, [], self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

    def test_debug_writeBlockProfile_error_wrong_type_param(self):
        method = f"{self.ns}_writeBlockProfile"
        _, error = Utils.call_ws(self.endpoint, method, [1234], self.log_path)
        Utils.check_error(self, "arg0NumberToString", error)

    def test_debug_writeBlockProfile_success(self):
        method = f"{self.ns}_writeBlockProfile"
        profile_file = "block_rate_1_created_by_ws.profile"
        _, error = Utils.call_ws(self.endpoint, method, [profile_file], self.log_path)
        self.assertIsNone(error)

    def test_debug_stacks_success_no_param(self):
        method = f"{self.ns}_stacks"
        _, error = Utils.call_ws(self.endpoint, method, [], self.log_path)
        self.assertIsNone(error)

    def test_debug_stacks_success_wrong_value_param(self):
        method = f"{self.ns}_stacks"
        _, error = Utils.call_ws(self.endpoint, method, [1234], self.log_path)
        self.assertIsNone(error)

    def test_debug_stacks_success(self):
        method = f"{self.ns}_stacks"
        _, error = Utils.call_ws(self.endpoint, method, [], self.log_path)
        self.assertIsNone(error)

    def test_debug_startCPUProfile_no_param(self):
        method = f"{self.ns}_startCPUProfile"
        _, error = Utils.call_ws(self.endpoint, method, [], self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

    def test_debug_startCPUProfile_success(self):
        method = f"{self.ns}_startCPUProfile"
        profile_file = "start_cpu_30s_created_by_ws.profile"
        _, error = Utils.call_ws(self.endpoint, method, [profile_file], self.log_path)
        self.assertIsNone(error)

    def test_debug_startCPUProfile_error_already_in_progress(self):
        method = f"{self.ns}_startCPUProfile"
        _, error = Utils.call_ws(self.endpoint, method, ["abcd"], self.log_path)
        Utils.check_error(self, "CPUProfilingAlreadyInProgress", error)

    def test_debug_stopCPUProfile_success_wrong_value_param(self):
        method = f"{self.ns}_stopCPUProfile"
        _, error = Utils.call_ws(self.endpoint, method, ["abd"], self.log_path)
        self.assertIsNone(error)

    def test_debug_stopCPUProfile_error_not_in_progress(self):
        method = f"{self.ns}_stopCPUProfile"
        _, error = Utils.call_ws(self.endpoint, method, [], self.log_path)
        Utils.check_error(self, "CPUProfilingNotInProgress", error)

    def test_debug_stopCPUProfile_success(self):
        # To test TC successfully, start cpu profile.
        method = f"{self.ns}_startCPUProfile"
        profile_file = "start_cpu_30s_created_by_ws.profile"
        Utils.call_rpc(self.endpoint, method, [profile_file], self.log_path)

        method = f"{self.ns}_stopCPUProfile"
        _, error = Utils.call_ws(self.endpoint, method, [], self.log_path)
        self.assertIsNone(error)

    def test_debug_startGoTrace_error_no_param(self):
        method = f"{self.ns}_startGoTrace"
        _, error = Utils.call_ws(self.endpoint, method, [], self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

    def test_debug_startGoTrace_success(self):
        method = f"{self.ns}_startGoTrace"
        profileFile = "start_go_30s_created_by_ws.trace"
        _, error = Utils.call_ws(self.endpoint, method, [profileFile], self.log_path)
        self.assertIsNone(error)

    def test_debug_startGoTrace_error_already_in_progress(self):
        method = f"{self.ns}_startGoTrace"
        profileFile = "start_go_30s_created_by_ws.trace"
        _, error = Utils.call_ws(self.endpoint, method, [profileFile], self.log_path)
        Utils.check_error(self, "TraceAlreadyInProgress", error)

    def test_debug_stopGoTrace_success(self):
        method = f"{self.ns}_stopGoTrace"
        _, error = Utils.call_ws(self.endpoint, method, [], self.log_path)
        self.assertIsNone(error)

    def test_debug_stopGoTrace_error_not_in_progress(self):
        method = f"{self.ns}_stopGoTrace"
        _, error = Utils.call_ws(self.endpoint, method, [], self.log_path)
        Utils.check_error(self, "TraceNotInProgress", error)

    def test_debug_verbosity_error_no_param(self):
        method = f"{self.ns}_verbosity"
        _, error = Utils.call_ws(self.endpoint, method, [], self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

    def test_debug_verbosity_error_wrong_type_param(self):
        method = f"{self.ns}_verbosity"
        _, error = Utils.call_ws(self.endpoint, method, ["abcd"], self.log_path)
        Utils.check_error(self, "arg0StringToInt", error)

    def test_debug_verbosity_error_wrong_value_param(self):
        method = f"{self.ns}_verbosity"
        _, error = Utils.call_ws(self.endpoint, method, [100], self.log_path)
        Utils.check_error(self, "LogLevelHigherThan6", error)

    def test_debug_verbosity_success(self):
        method = f"{self.ns}_verbosity"
        _, error = Utils.call_ws(self.endpoint, method, [3], self.log_path)
        self.assertIsNone(error)

    def test_debug_vmodule_error_no_param(self):
        method = f"{self.ns}_vmodule"
        _, error = Utils.call_ws(self.endpoint, method, [], self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

    def test_debug_vmodule_error_wrong_type_param(self):
        method = f"{self.ns}_vmodule"
        _, error = Utils.call_ws(self.endpoint, method, [1234], self.log_path)
        Utils.check_error(self, "arg0NumberToString", error)

    def test_debug_vmodule_error_wrong_value_param(self):
        method = f"{self.ns}_vmodule"
        _, error = Utils.call_ws(self.endpoint, method, ["abcd"], self.log_path)
        Utils.check_error(self, "ExpectCommaSeparatedList", error)

    def test_debug_vmodule_success(self):
        method = f"{self.ns}_vmodule"
        module = "p2p/*=5"
        _, error = Utils.call_ws(self.endpoint, method, [module], self.log_path)
        self.assertIsNone(error)

    def test_debug_writeMemProfile_error_no_param(self):
        method = f"{self.ns}_writeMemProfile"
        _, error = Utils.call_ws(self.endpoint, method, [], self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

    def test_debug_writeMemProfile_error_wrong_type_param(self):
        method = f"{self.ns}_writeMemProfile"
        _, error = Utils.call_ws(self.endpoint, method, [1234], self.log_path)
        Utils.check_error(self, "arg0NumberToString", error)

    def test_debug_writeMemProfile_success(self):
        method = f"{self.ns}_writeMemProfile"
        profile_file = "mem_created_by_ws.profile"
        _, error = Utils.call_ws(self.endpoint, method, [profile_file], self.log_path)
        self.assertIsNone(error)

    def test_debug_setGCPercent_error_no_param(self):
        method = f"{self.ns}_setGCPercent"
        _, error = Utils.call_ws(self.endpoint, method, [], self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

    def test_debug_setGCPercent_error_wrong_type_param(self):
        method = f"{self.ns}_setGCPercent"
        _, error = Utils.call_ws(self.endpoint, method, ["abcd"], self.log_path)
        Utils.check_error(self, "arg0StringToInt", error)

    def test_debug_setGCPercent_success(self):
        method = f"{self.ns}_setGCPercent"
        _, error = Utils.call_ws(self.endpoint, method, [90], self.log_path)
        self.assertIsNone(error)

    def test_debug_standardTraceBlockToFile_error_no_param(self):
        method = f"{self.ns}_standardTraceBlockToFile"
        _, error = Utils.call_ws(self.endpoint, method, [], self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

    def test_debug_standardTraceBlockToFile_error_wrong_type_param(self):
        method = f"{self.ns}_standardTraceBlockToFile"
        _, error = Utils.call_ws(self.endpoint, method, [1234], self.log_path)
        Utils.check_error(self, "arg0NonstringToHash", error)

    def test_debug_standardTraceBlockToFile_error_wrong_value_param(self):
        latest_block = kaia_common.get_latest_block_by_number(self.endpoint)
        invalid_block_hash = latest_block["hash"][:-3] + "fff"

        method = f"{self.ns}_standardTraceBlockToFile"
        _, error = Utils.call_ws(self.endpoint, method, [invalid_block_hash], self.log_path)
        self.assertEqual(-32000, error.get("code"))
        self.assertEqual(f"block {invalid_block_hash[2:]} not found", error.get("message"))

    def test_debug_standardTraceBlockToFile_success(self):
        latest_block = kaia_common.get_latest_block_by_number(self.endpoint)
        block_hash = latest_block["hash"]

        method = f"{self.ns}_standardTraceBlockToFile"
        _, error = Utils.call_ws(self.endpoint, method, [block_hash], self.log_path)
        self.assertIsNone(error)

    def test_debug_traceBadBlock_success(self):
        # TODO: Original code of this test case was basically same with test_debug_standardTraceBlockToFile_success
        # We need to implement this test case correctly.
        pass

    def test_debug_standardTraceBadBlockToFile_success(self):
        # TODO: Original code of this test case was basically same with test_debug_standardTraceBlockToFile_success
        # We need to implement this test case correctly.
        pass

    @staticmethod
    def suite():
        suite = unittest.TestSuite()
        suite.addTest(TestDebugNamespaceWS("test_debug_startPProf_error_wrong_type_param1"))
        suite.addTest(TestDebugNamespaceWS("test_debug_startPProf_error_wrong_type_param2"))
        suite.addTest(TestDebugNamespaceWS("test_debug_startPProf_success_no_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_startPProf_error_already_running"))
        suite.addTest(TestDebugNamespaceWS("test_debug_stopPProf_success"))
        suite.addTest(TestDebugNamespaceWS("test_debug_stopPProf_error_not_running"))
        suite.addTest(TestDebugNamespaceWS("test_debug_startPProf_success"))
        suite.addTest(TestDebugNamespaceWS("test_debug_isPProfRunning_success_wrong_value_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_isPProfRunning_success"))
        suite.addTest(TestDebugNamespaceWS("test_debug_getModifiedAccountsByHash_error_no_param1"))
        suite.addTest(TestDebugNamespaceWS("test_debug_getModifiedAccountsByHash_error_wrong_type_param1"))
        suite.addTest(TestDebugNamespaceWS("test_debug_getModifiedAccountsByHash_error_wrong_type_param2"))
        suite.addTest(TestDebugNamespaceWS("test_debug_getModifiedAccountsByHash_error_wrong_value_param1"))
        suite.addTest(TestDebugNamespaceWS("test_debug_getModifiedAccountsByHash_error_wrong_value_param2"))
        suite.addTest(TestDebugNamespaceWS("test_debug_getModifiedAccountsByHash_success"))
        suite.addTest(TestDebugNamespaceWS("test_debug_getModifiedAccountsByNumber_error_no_param1"))
        suite.addTest(TestDebugNamespaceWS("test_debug_getModifiedAccountsByNumber_error_wrong_type_param1"))
        suite.addTest(TestDebugNamespaceWS("test_debug_getModifiedAccountsByNumber_error_wrong_type_param2"))
        suite.addTest(TestDebugNamespaceWS("test_debug_getModifiedAccountsByNumber_error_wrong_value_param1"))
        suite.addTest(TestDebugNamespaceWS("test_debug_getModifiedAccountsByNumber_error_wrong_value_param2"))
        suite.addTest(TestDebugNamespaceWS("test_debug_getModifiedAccountsByNumber_success"))
        suite.addTest(TestDebugNamespaceWS("test_debug_backtraceAt_success"))
        suite.addTest(TestDebugNamespaceWS("test_debug_backtraceAt_error_no_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_backtraceAt_error_wrong_type_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_backtraceAt_error_wrong_value_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_blockProfile_success"))
        suite.addTest(TestDebugNamespaceWS("test_debug_blockProfile_error_no_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_blockProfile_error_wrong_type_param1"))
        suite.addTest(TestDebugNamespaceWS("test_debug_blockProfile_error_wrong_type_param2"))
        suite.addTest(TestDebugNamespaceWS("test_debug_cpuProfile_error_no_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_cpuProfile_error_wrong_type_param1"))
        suite.addTest(TestDebugNamespaceWS("test_debug_cpuProfile_error_wrong_type_param2"))
        suite.addTest(TestDebugNamespaceWS("test_debug_cpuProfile_success"))
        suite.addTest(TestDebugNamespaceWS("test_debug_dumpBlock_error_no_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_dumpBlock_error_wrong_type_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_dumpBlock_error_wrong_value_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_dumpBlock_success"))
        suite.addTest(TestDebugNamespaceWS("test_debug_gcStats_success_wrong_value_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_gcStats_success"))
        suite.addTest(TestDebugNamespaceWS("test_debug_getBlockRlp_error_no_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_getBlockRlp_error_wrong_type_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_getBlockRlp_error_wrong_value_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_getBlockRlp_success"))
        suite.addTest(TestDebugNamespaceWS("test_debug_traceBlock_success"))
        suite.addTest(TestDebugNamespaceWS("test_debug_traceBlock_error_no_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_traceBlock_error_wrong_type_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_traceBlock_error_wrong_value_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_traceBlockByNumber_error_no_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_traceBlockByNumber_error_wrong_type_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_traceBlockByNumber_error_wrong_value_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_traceBlockByNumber_success"))
        suite.addTest(TestDebugNamespaceWS("test_debug_traceBlockByHash_error_no_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_traceBlockByHash_error_wrong_type_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_traceBlockByHash_error_wrong_value_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_traceBlockByHash_success"))
        suite.addTest(TestDebugNamespaceWS("test_debug_traceBlockFromFile_error_no_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_traceBlockFromFile_error_wrong_type_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_traceBlockFromFile_error_wrong_value_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_traceBlockFromFile_success"))
        suite.addTest(TestDebugNamespaceWS("test_debug_traceTransaction_error_no_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_traceTransaction_error_wrong_type_param1"))
        suite.addTest(TestDebugNamespaceWS("test_debug_traceTransaction_error_wrong_value_param1"))
        suite.addTest(TestDebugNamespaceWS("test_debug_traceTransaction_error_wrong_value_param2"))
        suite.addTest(TestDebugNamespaceWS("test_debug_traceTransaction_success"))
        suite.addTest(TestDebugNamespaceWS("test_debug_goTrace_error_no_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_goTrace_error_wrong_type_param1"))
        suite.addTest(TestDebugNamespaceWS("test_debug_goTrace_error_wrong_type_param2"))
        suite.addTest(TestDebugNamespaceWS("test_debug_goTrace_success"))
        suite.addTest(TestDebugNamespaceWS("test_debug_memStats_success_wrong_value_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_memStats_success"))
        suite.addTest(TestDebugNamespaceWS("test_debug_metrics_error_no_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_metrics_error_wrong_type_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_metrics_success"))
        suite.addTest(TestDebugNamespaceWS("test_debug_printBlock_error_no_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_printBlock_error_wrong_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_printBlock_success"))
        """
        suite.addTest(TestDebugNamespaceWS("test_debug_preimage_success"))
        """
        suite.addTest(TestDebugNamespaceWS("test_debug_freeOSMemory_success_wrong_value_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_freeOSMemory_success"))
        """
        suite.addTest(TestDebugNamespaceWS("test_debug_setHead_success"))
        """
        suite.addTest(TestDebugNamespaceWS("test_debug_setBlockProfileRate_error_no_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_setBlockProfileRate_error_wrong_type_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_setBlockProfileRate_success"))
        suite.addTest(TestDebugNamespaceWS("test_debug_setVMLogTarget_success"))
        suite.addTest(TestDebugNamespaceWS("test_debug_setVMLogTarget_error_no_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_setVMLogTarget_error_wrong_type_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_setVMLogTarget_error_wrong_value_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_writeBlockProfile_error_no_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_writeBlockProfile_error_wrong_type_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_writeBlockProfile_success"))
        suite.addTest(TestDebugNamespaceWS("test_debug_stacks_success_no_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_stacks_success_wrong_value_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_stacks_success"))
        suite.addTest(TestDebugNamespaceWS("test_debug_startCPUProfile_no_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_startCPUProfile_success"))
        suite.addTest(TestDebugNamespaceWS("test_debug_startCPUProfile_error_already_in_progress"))
        suite.addTest(TestDebugNamespaceWS("test_debug_stopCPUProfile_success_wrong_value_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_stopCPUProfile_error_not_in_progress"))
        suite.addTest(TestDebugNamespaceWS("test_debug_stopCPUProfile_success"))
        suite.addTest(TestDebugNamespaceWS("test_debug_startGoTrace_error_no_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_startGoTrace_success"))
        suite.addTest(TestDebugNamespaceWS("test_debug_startGoTrace_error_already_in_progress"))
        suite.addTest(TestDebugNamespaceWS("test_debug_stopGoTrace_success"))
        suite.addTest(TestDebugNamespaceWS("test_debug_stopGoTrace_error_not_in_progress"))
        suite.addTest(TestDebugNamespaceWS("test_debug_verbosity_error_no_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_verbosity_error_wrong_type_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_verbosity_error_wrong_value_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_verbosity_success"))
        suite.addTest(TestDebugNamespaceWS("test_debug_vmodule_error_no_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_vmodule_error_wrong_type_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_vmodule_error_wrong_value_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_vmodule_success"))
        suite.addTest(TestDebugNamespaceWS("test_debug_writeMemProfile_error_no_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_writeMemProfile_error_wrong_type_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_writeMemProfile_success"))
        suite.addTest(TestDebugNamespaceWS("test_debug_setGCPercent_error_no_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_setGCPercent_error_wrong_type_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_setGCPercent_success"))
        suite.addTest(TestDebugNamespaceWS("test_debug_standardTraceBlockToFile_error_no_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_standardTraceBlockToFile_error_wrong_type_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_standardTraceBlockToFile_error_wrong_value_param"))
        suite.addTest(TestDebugNamespaceWS("test_debug_standardTraceBlockToFile_success"))
        suite.addTest(TestDebugNamespaceWS("test_debug_traceBadBlock_success"))
        suite.addTest(TestDebugNamespaceWS("test_debug_standardTraceBadBlockToFile_success"))

        return suite
