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
            "value": hex(Utils.to_kei(1.5)),
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

    # debug_traceCall
    #
    # probe_bin is `Probe` below, compiled with solc 0.8.30 --optimize. emitBoth()
    # emits one log in the top call frame and then makes a nested call that emits
    # another, which is what makes the callTracer withLog / onlyTopCall
    # combinations observable:
    #
    #   contract Probe {
    #       event Top(uint256 v);
    #       uint256 public counter;
    #       Child public child;
    #       constructor() { child = new Child(); }
    #       function emitBoth() external { emit Top(1); child.ping(); }
    #       function boom() external { counter = 7; emit Top(3); revert("boom"); }
    #       function revertAfterCall() external {
    #           emit Top(4); child.ping(); revert("boom after call");
    #       }
    #   }
    #   contract Child {
    #       event Nested(uint256 v);
    #       function ping() external { emit Nested(2); }
    #   }
    probe_bin = "0x6080604052348015600e575f5ffd5b506040516019906056565b604051809103905ff0801580156031573d5f5f3e3d5ffd5b50600180546001600160a01b0319166001600160a01b03929092169190911790556062565b60b88061033a83390190565b6102cb8061006f5f395ff3fe608060405234801561000f575f5ffd5b5060043610610055575f3560e01c8063237b5e961461005957806361bc221a14610089578063a169ce091461009f578063d5eacee0146100a9578063fc1af250146100b1575b5f5ffd5b60015461006c906001600160a01b031681565b6040516001600160a01b0390911681526020015b60405180910390f35b6100915f5481565b604051908152602001610080565b6100a76100b9565b005b6100a761012b565b6100a76101c3565b60075f55604051600381527ff196745cb6c193223a31ea74a57d4c9948c05f6a2f481008aff46aa41c47d71b9060200160405180910390a160405162461bcd60e51b815260040161012290602080825260049082015263626f6f6d60e01b604082015260600190565b60405180910390fd5b604051600181527ff196745cb6c193223a31ea74a57d4c9948c05f6a2f481008aff46aa41c47d71b9060200160405180910390a160015f9054906101000a90046001600160a01b03166001600160a01b0316635c36b1866040518163ffffffff1660e01b81526004015f604051808303815f87803b1580156101ab575f5ffd5b505af11580156101bd573d5f5f3e3d5ffd5b50505050565b604051600481527ff196745cb6c193223a31ea74a57d4c9948c05f6a2f481008aff46aa41c47d71b9060200160405180910390a160015f9054906101000a90046001600160a01b03166001600160a01b0316635c36b1866040518163ffffffff1660e01b81526004015f604051808303815f87803b158015610243575f5ffd5b505af1158015610255573d5f5f3e3d5ffd5b505060405162461bcd60e51b815260206004820152600f60248201526e189bdbdb4818599d195c8818d85b1b608a1b60448201526064019150610122905056fea2646970667358221220af3c24ba02a1021a2355717ba18d47034eb9f61e7e6641c74c55236c04c8157f64736f6c634300081e00336080604052348015600e575f5ffd5b50609e80601a5f395ff3fe6080604052348015600e575f5ffd5b50600436106026575f3560e01c80635c36b18614602a575b5f5ffd5b60306032565b005b604051600281527f84bccedf5fbad5c802864c2d64e4562a610a468ba28173bd7528588e4429eaf79060200160405180910390a156fea26469706673582212207007672aa893c943049615dca3bfd24b51b1e44c49fa4e8c3a078e23120cc57a64736f6c634300081e0033"
    emit_both_selector = "0xd5eacee0"
    boom_selector = "0xa169ce09"
    revert_after_call_selector = "0xfc1af250"

    def deploy_probe(self):
        sender = test_data_set["account"]["sender"]["address"]
        password = test_data_set["account"]["sender"]["password"]
        tx_fields = {
            "from": sender,
            "gas": hex(1000000),
            "gasPrice": test_data_set["unitGasPrice"],
            "data": self.probe_bin,
        }
        transaction_hash, error = personal_common.send_transaction(self.endpoint, [tx_fields, password])
        self.assertIsNone(error)
        Utils.waiting_count("Waiting for", self.waiting_count, "seconds until the contract is deployed.")
        receipt, error = kaia_common.get_transaction_receipt(self.endpoint, [transaction_hash])
        self.assertIsNone(error)
        self.assertIsNotNone(receipt)
        contract_address = receipt.get("contractAddress")
        self.assertIsNotNone(contract_address)
        return contract_address

    def create_params_for_trace_call(self, to, tracer_config=None):
        call_args = {
            "from": test_data_set["account"]["sender"]["address"],
            "to": to,
            "gas": hex(300000),
            "gasPrice": test_data_set["unitGasPrice"],
            "data": self.emit_both_selector,
        }
        params = [call_args, "latest"]
        if tracer_config is not None:
            params.append(tracer_config)
        return params

    def test_debug_traceCall_error_no_param(self):
        method = f"{self.ns}_traceCall"
        _, error = Utils.call_ws(self.endpoint, method, [], self.log_path)
        Utils.check_error(self, "arg0NoParams", error)

    def test_debug_traceCall_error_wrong_type_param1(self):
        method = f"{self.ns}_traceCall"
        _, error = Utils.call_ws(self.endpoint, method, ["abcd", "latest"], self.log_path)
        Utils.check_error(self, "arg0StringToCallArgs", error)

    def test_debug_traceCall_error_no_param2(self):
        method = f"{self.ns}_traceCall"
        call_args = {"to": test_data_set["account"]["receiver"]["address"]}
        _, error = Utils.call_ws(self.endpoint, method, [call_args], self.log_path)
        Utils.check_error(self, "arg1NoParams", error)

    def test_debug_traceCall_error_wrong_value_param2(self):
        method = f"{self.ns}_traceCall"
        call_args = {"to": test_data_set["account"]["receiver"]["address"]}
        _, error = Utils.call_ws(self.endpoint, method, [call_args, "0xffffffff"], self.log_path)
        Utils.check_error(self, "BlockNotExist", error)

    def test_debug_traceCall_success(self):
        contract_address = self.deploy_probe()

        method = f"{self.ns}_traceCall"
        params = self.create_params_for_trace_call(contract_address)
        result, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)
        self.assertIsNotNone(result)

    def test_debug_traceCall_success_call_tracer(self):
        contract_address = self.deploy_probe()

        method = f"{self.ns}_traceCall"
        params = self.create_params_for_trace_call(contract_address, {"tracer": "callTracer"})
        result, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)
        # The nested call to Child.ping() must appear as a child frame, and no logs
        # are reported unless withLog is set.
        self.assertEqual(1, len(result.get("calls")))
        self.assertNotIn("logs", result)

    def test_debug_traceCall_success_call_tracer_with_log(self):
        contract_address = self.deploy_probe()

        method = f"{self.ns}_traceCall"
        params = self.create_params_for_trace_call(
            contract_address, {"tracer": "callTracer", "tracerConfig": {"withLog": True}}
        )
        result, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)
        # Top(1) in the top frame, Nested(2) in the child frame.
        self.assertIn("logs", result)
        self.assertEqual(1, len(result.get("logs")))
        self.assertEqual(1, len(result.get("calls")[0].get("logs")))
        # logIndex is per transaction, not per frame, so the two logs are 0 and 1.
        self.assertEqual("0x0", result.get("logs")[0].get("index"))
        self.assertEqual("0x1", result.get("calls")[0].get("logs")[0].get("index"))

    def test_debug_traceCall_success_call_tracer_with_log_only_top_call(self):
        contract_address = self.deploy_probe()

        method = f"{self.ns}_traceCall"
        params = self.create_params_for_trace_call(
            contract_address,
            {"tracer": "callTracer", "tracerConfig": {"withLog": True, "onlyTopCall": True}},
        )
        result, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)
        # onlyTopCall drops nested frames, but the top frame keeps its own log.
        # Regressed once by gating log capture on the opcode depth, which is 1 while
        # the top frame executes, so every log was dropped instead of only nested ones.
        self.assertIn("logs", result)
        self.assertEqual(1, len(result.get("logs")))
        self.assertNotIn("calls", result)
        # The nested log must not be captured, nor reattributed to the top frame.
        self.assertEqual("0x0", result.get("logs")[0].get("index"))

    def test_debug_traceCall_success_prestate_tracer(self):
        contract_address = self.deploy_probe()

        method = f"{self.ns}_traceCall"
        params = self.create_params_for_trace_call(contract_address, {"tracer": "prestateTracer"})
        result, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)
        # Flat prestate: the contract the call touches is reported, and without
        # diffMode there is no pre/post split.
        self.assertIn(contract_address.lower(), [address.lower() for address in result])
        self.assertNotIn("pre", result)
        self.assertNotIn("post", result)

    def test_debug_traceCall_success_prestate_tracer_diff_mode(self):
        contract_address = self.deploy_probe()

        method = f"{self.ns}_traceCall"
        params = self.create_params_for_trace_call(
            contract_address, {"tracer": "prestateTracer", "tracerConfig": {"diffMode": True}}
        )
        result, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)
        self.assertIn("pre", result)
        self.assertIn("post", result)
        # The sender's nonce advances, so it must appear on both sides of the diff.
        sender = test_data_set["account"]["sender"]["address"].lower()
        self.assertIn(sender, [address.lower() for address in result.get("pre")])
        self.assertIn(sender, [address.lower() for address in result.get("post")])

    def get_balance(self, address):
        # Named `result` so generate_ws_from_rpc.sh rewrites this to Utils.call_ws
        # for the WS suite; it only matches `result, error =` and `_, error =`.
        result, error = Utils.call_ws(self.endpoint, "kaia_getBalance", [address, "latest"], self.log_path)
        self.assertIsNone(error)
        return result

    def test_debug_traceCall_success_prestate_tracer_synthetic_gas_is_removed(self):
        # traceCall credits the caller gas * effectiveGasPrice so the simulation can
        # run, then subtracts it back out. On a call that moves no value the caller's
        # balance must therefore be reported unchanged: `pre` equal to the real chain
        # balance, and no balance field at all in `post`.
        sender = test_data_set["account"]["sender"]["address"]
        receiver = test_data_set["account"]["receiver"]["address"]

        method = f"{self.ns}_traceCall"
        call_args = {
            "from": sender,
            "to": receiver,
            "value": "0x0",
            "gas": hex(100000),
            "gasPrice": test_data_set["unitGasPrice"],
        }
        params = [call_args, "latest", {"tracer": "prestateTracer", "tracerConfig": {"diffMode": True}}]
        result, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

        pre = {address.lower(): account for address, account in result.get("pre").items()}
        post = {address.lower(): account for address, account in result.get("post").items()}
        self.assertEqual(int(self.get_balance(sender), 16), int(pre[sender.lower()].get("balance"), 16))
        self.assertNotIn("balance", post[sender.lower()])

    def test_debug_traceCall_success_prestate_tracer_value_transfer_delta(self):
        # The caller's balance delta must be exactly the transferred value, with no
        # gas component folded in, and the recipient must gain exactly the same.
        sender = test_data_set["account"]["sender"]["address"]
        receiver = test_data_set["account"]["receiver"]["address"]
        value = Utils.to_kei(1)

        method = f"{self.ns}_traceCall"
        call_args = {
            "from": sender,
            "to": receiver,
            "value": hex(value),
            "gas": hex(100000),
            "gasPrice": test_data_set["unitGasPrice"],
        }
        params = [call_args, "latest", {"tracer": "prestateTracer", "tracerConfig": {"diffMode": True}}]
        result, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

        pre = {address.lower(): account for address, account in result.get("pre").items()}
        post = {address.lower(): account for address, account in result.get("post").items()}

        def balance_of(state, address):
            return int(state.get(address.lower(), {}).get("balance", "0x0"), 16)

        self.assertEqual(-value, balance_of(post, sender) - balance_of(pre, sender))
        self.assertEqual(value, balance_of(post, receiver) - balance_of(pre, receiver))

    def test_debug_traceCall_success_prestate_tracer_zero_balance_caller(self):
        # The synthetic top-up must be sized from the requested gasPrice, not the base
        # fee. A caller holding nothing can only be simulated if that holds, so this
        # fails outright on a regression rather than returning a wrong number. `pre`
        # must still report the caller's real balance, not the inflated one.
        poor = "0x00000000000000000000000000000000000000ff"
        receiver = test_data_set["account"]["receiver"]["address"]
        gas_price = hex(int(test_data_set["unitGasPrice"], 16) * 1000)

        method = f"{self.ns}_traceCall"
        call_args = {
            "from": poor,
            "to": receiver,
            "value": "0x0",
            "gas": hex(100000),
            "gasPrice": gas_price,
        }
        params = [call_args, "latest", {"tracer": "prestateTracer"}]
        result, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

        state = {address.lower(): account for address, account in result.items()}
        self.assertIn(poor.lower(), state)
        self.assertEqual(int(self.get_balance(poor), 16), int(state[poor.lower()].get("balance", "0x0"), 16))

    def test_debug_traceCall_success_call_tracer_reverted_frame_prunes_log(self):
        # boom() writes storage and emits a log and then reverts. The log must be
        # dropped even though withLog was requested, and the discarded write must not
        # show up in a diffMode post.
        contract_address = self.deploy_probe()

        method = f"{self.ns}_traceCall"
        call_args = {
            "from": test_data_set["account"]["sender"]["address"],
            "to": contract_address,
            "gas": hex(300000),
            "gasPrice": test_data_set["unitGasPrice"],
            "data": self.boom_selector,
        }
        result, error = Utils.call_ws(
            self.endpoint,
            method,
            [call_args, "latest", {"tracer": "callTracer", "tracerConfig": {"withLog": True}}],
            self.log_path,
        )
        self.assertIsNone(error)
        self.assertNotIn("logs", result)
        self.assertEqual("execution reverted", result.get("error"))
        self.assertEqual("boom", result.get("revertReason"))

        result, error = Utils.call_ws(
            self.endpoint,
            method,
            [call_args, "latest", {"tracer": "prestateTracer", "tracerConfig": {"diffMode": True}}],
            self.log_path,
        )
        self.assertIsNone(error)
        self.assertNotIn(contract_address.lower(), [address.lower() for address in result.get("post")])

    def test_debug_traceCall_success_call_tracer_reverted_parent_prunes_child_log(self):
        # revertAfterCall() makes a nested call that SUCCEEDS and emits, then reverts
        # the top frame. The child's log has to be pruned as well, so this covers the
        # recursive case that a frame-local implementation would miss.
        contract_address = self.deploy_probe()

        method = f"{self.ns}_traceCall"
        call_args = {
            "from": test_data_set["account"]["sender"]["address"],
            "to": contract_address,
            "gas": hex(300000),
            "gasPrice": test_data_set["unitGasPrice"],
            "data": self.revert_after_call_selector,
        }
        result, error = Utils.call_ws(
            self.endpoint,
            method,
            [call_args, "latest", {"tracer": "callTracer", "tracerConfig": {"withLog": True}}],
            self.log_path,
        )
        self.assertIsNone(error)
        self.assertEqual("boom after call", result.get("revertReason"))
        self.assertNotIn("logs", result)
        self.assertEqual(1, len(result.get("calls")))
        # The child did not fail, yet its log must be gone because the parent reverted.
        self.assertNotIn("error", result.get("calls")[0])
        self.assertNotIn("logs", result.get("calls")[0])

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
        _, error = Utils.call_ws(self.endpoint, method, [profile_file], self.log_path)

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

    def test_debug_isGaslessTx_success(self):
        method = "kaia_getTransactionCount"
        tag = "latest"
        txFrom = test_data_set["account"]["sender"]["address"]
        password = test_data_set["account"]["sender"]["password"]
        txTo = test_data_set["account"]["sender"]["address"]
        txGas = hex(30400)
        txGasPrice = test_data_set["unitGasPrice"]
        txValue = hex(2441406250)

        params = [txFrom, tag]
        result, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)
        nonce = result

        method = "kaia_signTransaction"
        params = [
            {
                "from": txFrom,
                "to": txTo,
                "gas": txGas,
                "gasPrice": txGasPrice,
                "value": txValue,
                "nonce": nonce,
            }
        ]
        result, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)

        rawData = result["raw"]
        method = f"{self.ns}_isGaslessTx"
        params = [[rawData]]
        result, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)
        self.assertIsNotNone(result)
        self.assertFalse(result["isGasless"])
        self.assertEqual(result["reason"], "transaction is not a swap transaction")

    def test_debug_gaslessInfo_success(self):
        method = f"{self.ns}_gaslessInfo"
        params = []
        result, error = Utils.call_ws(self.endpoint, method, params, self.log_path)
        self.assertIsNone(error)
        self.assertIsNotNone(result)
        self.assertFalse(result["isDisabled"])
        self.assertEqual(result["swapRouter"], "0x0000000000000000000000000000000000000000")
        self.assertEqual(result["allowedTokens"], [])
        self.assertEqual(result["maxBundleTxs"], 100)

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
        suite.addTest(TestDebugNamespaceWS("test_debug_isGaslessTx_success"))
        suite.addTest(TestDebugNamespaceWS("test_debug_gaslessInfo_success"))

        return suite
