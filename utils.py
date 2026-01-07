import os.path
import time
import pathlib
import json
import unittest
import requests
import codecs
import re
import random
import string
import sys
import subprocess
from websocket._core import create_connection
from datetime import datetime
from errors import ERRORS
from enum import Enum
from test_data import BLOB_TEST_DATA

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT_DIR = pathlib.Path(CURRENT_DIR)

# blob_fee_cap must be gas_fee_cap * 8 (BlobBaseFeeMultiplier)
BLOB_BASE_FEE_MULTIPLIER = 8

class Utils(unittest.TestCase):
    class TestingStatus(Enum):
        START = 1
        FINISHED = 2
        NONE = 3

    @staticmethod
    def get_date_strings():
        """Return date information with various formats to check date."""
        local_datetime = datetime.now()
        dt = datetime(
            local_datetime.year,
            local_datetime.month,
            local_datetime.day,
            local_datetime.hour,
            local_datetime.minute,
            local_datetime.second,
        )
        timestamp = time.mktime(dt.timetuple())
        return (local_datetime, dt, timestamp)

    @staticmethod
    def get_log_filename_with_path():
        """Create log file whenever test is executed and returns path, directory name, and log file name."""

        _, _, timestamp = Utils.get_date_strings()

        log_directory_name = datetime.fromtimestamp(int(timestamp)).strftime("%Y%m%d%H%M%S")

        log_path = f"./reports/{log_directory_name}"
        pathlib.Path(log_path).mkdir(parents=True, exist_ok=True)

        log_file_name = f"{log_path}/kaia.log"

        return log_path, log_directory_name, log_file_name

    @staticmethod
    def get_request_id():
        """Returns a random integer (1 ~ 99) to be used as request id when call API."""
        return random.randint(1, 100)

    @staticmethod
    def save_result_data(log_path, file_name, data):
        """If result value is big like blockdump, store it as a file."""

        # Check path of log and if there is no directory, create a directory.
        pathlib.Path(log_path).mkdir(parents=True, exist_ok=True)

        # Appoint path and file name to store.
        path = f"{log_path}/{file_name}"
        with open(path, "wt") as f:
            f.write(f"{data}")

    @staticmethod
    def convert_to_hex(message):
        """Change string, int data to hex data."""
        hex_data = ""

        if isinstance(message, str):
            hex_data = "0x" + "".join("{:02x}".format(ord(c)) for c in str(message))

        if isinstance(message, int):
            hex_data = hex(message)

        if isinstance(message, dict):
            message = json.dumps(message)
            hex_data = "0x" + "".join("{:02x}".format(ord(c)) for c in str(message))

        return hex_data

    @staticmethod
    def convert_hex_to_string(hex_data):
        """Convert hex data to string."""

        hex_data = Utils.strip_hex_prefix(hex_data)

        string_data = codecs.decode(hex_data, "hex").decode("utf-8", "ignore")

        # replace null character
        string_data = string_data.replace("\x00", "")
        string_data = string_data.replace("\x16", "")

        return string_data

    @staticmethod
    def is_hex(s):
        """Returns true if given string is a hexadecimal."""
        s = Utils.strip_hex_prefix(s)
        return all(c in string.hexdigits for c in s)

    @staticmethod
    def strip_hex_prefix(s):
        """Remove hex prefix and returns hexadecimal without prefix."""
        if len(s) >= 2:
            if s[:2] == "0x" or s[:2] == "0X":
                return s[2:]
            else:
                return s
        return s

    @staticmethod
    def left_pad64(hex_data):
        """Pad zeros and returns 64-length hexadecimal."""
        hex_data = Utils.strip_hex_prefix(hex_data)
        return "{:0>64}".format(hex_data)

    @staticmethod
    def get_config():
        """Read config.json and return parsed json data."""

        with open(f"{PROJECT_ROOT_DIR}/config.json") as f:
            data = json.load(f)

        return data

    @staticmethod
    def call_rpc(endpoint, method, params, log_file, save_result=False, port=8551):
        if endpoint is None or endpoint == "":
            endpoint = Utils.get_config().get("endpoint")
        host = f"http://{endpoint}:{port}"
        headers = {"Content-Type": "application/json"}

        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": [],
            "id": Utils.get_request_id(),
        }
        if params is not None:
            payload["params"] = params

        response = requests.post(host, data=json.dumps(payload), headers=headers, timeout=300)
        if response.status_code != 200:
            return f"Error: Unexpected response {response}"

        Utils.write_log(
            log_file,
            method,
            host,
            payload,
            response.text,
            save_file=save_result,
        )

        response_json = json.loads(response.text)
        result = response_json.get("result")
        error = response_json.get("error")

        return result, error

    @staticmethod
    def call_ws(endpoint, method, params, log_file, save_result=False, port=8552):
        host = f"ws://{endpoint}:{port}"
        if params == None:
            params = []
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": Utils.get_request_id(),
        }

        ws = create_connection(host)
        ws.send(json.dumps(payload))
        response = ws.recv()
        ws.close()

        response_json = json.loads(response)
        result = response_json.get("result")
        error = response_json.get("error")

        Utils.write_log(
            log_file,
            method,
            host,
            payload,
            response,
            save_file=save_result,
            service="ws",
        )
        return result, error

    @staticmethod
    def open_ws(endpoint, method, params, log_file, save_result=False, port=8552):
        host = f"ws://{endpoint}:{port}"
        if params == None:
            params = []
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": Utils.get_request_id(),
        }

        ws = create_connection(host)
        ws.send(json.dumps(payload))
        response = ws.recv()

        response_json = json.loads(response)
        result = response_json.get("result")
        error = response_json.get("error")

        Utils.write_log(
            log_file,
            method,
            host,
            payload,
            response,
            save_file=save_result,
            service="ws",
        )
        return result, error, ws

    @staticmethod
    def get_console_result_with_index(screenshot, command, log_file, save_result=False, columns=0):
        kaia_list, command_index = Utils.parse_command(screenshot, command, columns)

        # Make a string from command_index to last line and remove white spaces.
        result_string = " ".join(kaia_list[command_index:]).replace(" ", "")

        # There is no quotation at key of returned json result from kaia console.
        # Use regular expressions to change it to valid json string.
        valid_json = re.sub(r"(?<={|,)([a-zA-Z][a-zA-Z0-9]*)(?=:)", r'"\1"', result_string)

        try:
            result = json.loads(valid_json)
        except:
            result = valid_json

        if command == "> exit":
            result = None

        Utils.write_console_log(log_file, command_index, command, result, save_file=save_result)
        return result

    @staticmethod
    def parse_command(screenshot, command, columns):
        command = f"> {command}"

        # Split screenshot by lines and convert it to the array and remove ''.
        # Maximum lines of screenshot is 9999.
        kaia_list = list(filter(None, screenshot.splitlines()))

        # Check the last line of an array and remove when it is '>' (waiting command status).
        last_index = len(kaia_list) - 1
        if kaia_list[last_index] == ">":
            del kaia_list[-1]

        # Checks the index of kaia command at the last of array.
        # If command is longer than terminal's width(columns), find after cutting it out.
        if columns == 0:
            command_index = last_index - kaia_list[::-1].index(command)
        else:
            command_index = last_index - kaia_list[::-1].index(command[:columns])

        return kaia_list, command_index

    @staticmethod
    def get_console_sub_command(screenshot, command, logfile, save_result=False, columns=0):
        kaia_list, command_index = Utils.parse_command(screenshot, command, columns)
        Utils.write_console_log(logfile, command_index, command, None, save_file=save_result)
        return command

    @staticmethod
    def write_head_or_tail_log(
        log_file_name,
        testing_status,
        testing_unit="",
    ):
        with open(log_file_name, "at") as f:
            if testing_status == Utils.TestingStatus.START:
                log_string = f"------------ Testing Start ({testing_unit}) ------------- \n\n"
            elif testing_status == Utils.TestingStatus.FINISHED:
                log_string = f"------------ Testing Finished ({testing_unit}) ------------ \n\n"
            print(log_string)
            f.write(f"\n{log_string}")

    @staticmethod
    def write_log(
        log_file_name,
        method,
        host,
        data,
        result_text,
        file_name="",
        save_file=False,
        service="rpc",
    ):
        """
        Write start of testing at log file.
        If result data size is big like debug_dumpBlock, that will be stored as file.
        """
        if save_file and (file_name != "" and file_name is not None):
            with open(file_name, "w") as f:
                f.write(result_text)

        with open(log_file_name, "at") as f:
            if service == "rpc":
                curl_string = f'curl -H "Content-Type: application/json" --data "{str(json.dumps(data))}" {host}'
            else:
                curl_string = f'["{host}"]\n{str(json.dumps(data))}'

            log_string = f"[{str(datetime.now())}] [{method}]\n" f"{curl_string}\n"
            try:
                result_json = json.loads(result_text)
                log_string += f"{json.dumps(result_json, indent=4, sort_keys=True)} \n\n"
            except ValueError as e:
                log_string += f"{result_text} \n\n"

            print(log_string)

            f.write(f"\n{log_string}")

    @staticmethod
    def write_console_log(
        log_file_name,
        search_index,
        command,
        result,
        testing_status,
        testing_unit="",
        save_file=False,
    ):
        """
        Write start of testing at log file.
        If result data size is big like debug_dumpBlock, that will be stored as file.
        """

        if save_file:
            result = {"Utils_Message": "Output data was saved at a specific file."}

        with open(log_file_name, "at") as f:
            if testing_status == Utils.TestingStatus.START:
                log_string = f"------------ Testing Start ({testing_unit}) ------------- \n\n"
            elif testing_status == Utils.TestingStatus.FINISHED:
                log_string = f"------------ Testing Finished ({testing_unit}) ------------ \n\n"
            else:
                log_string = (
                    f"[IDX:{str(search_index)}] [{str(datetime.now())}] \n"
                    f"{command} \n"
                    f"{json.dumps(result, indent=4, sort_keys=True)} \n\n"
                )
            f.write(log_string)

        print(log_string)
        time.sleep(2)

    @staticmethod
    def waiting_count(frontString, second, rearString):
        """
        Lets count number while waiting.
        ex) Utils.waitingCount('Waiting for', 5, 'seconds until writing in block a transaction.')
        """
        for i in range(second, -1, -1):
            sys.stdout.write(f"\r{frontString} {i} {rearString}")
            sys.stdout.flush()
            time.sleep(1)
        sys.stdout.write("\n\n")

    @staticmethod
    def to_kei(kaia):
        """Convert unit KAIA to Kei."""
        kei = 0
        if isinstance(kaia, float):
            kei = int(kaia * 1000000000000000000.0)

        if isinstance(kaia, int):
            kei = kaia * 1000000000000000000

        return kei

    @staticmethod
    def check_error(target_instance, expected_error_key, error):
        """
        Check whether given error is expected error or not by using expected_error_key.
        target_instance must inherit unittest.TestCase class.
        """
        expected_error_code, expected_error_message = ERRORS[expected_error_key]
        target_instance.assertIsNotNone(error)
        target_instance.assertEqual(expected_error_code, error.get("code"), error)
        target_instance.assertIn(expected_error_message, error.get("message"), error)

    @staticmethod
    def check_response_type_newHeads_subscription_kaia(target_instance, response):
        """
        Verify newHeads subscription payload for Kaia header format (RPCMarshalHeader)
        returned by kaia_subscribe and auction_subscribe.
        """
        response_json = json.loads(response)
        params = response_json.get("params")
        target_instance.assertIsNotNone(params)
        target_instance.assertIn("subscription", params)
        target_instance.assertIn("result", params)

        header = params.get("result")
        target_instance.assertIsInstance(header, dict)

        required_fields = [
            "number",
            "hash",
            "parentHash",
            "timestamp",
            "timestampFoS",
            "gasUsed",
            "transactionsRoot",
            "receiptsRoot",
            "stateRoot",
            "logsBloom",
            "extraData",
            "governanceData",
            "voteData",
            "reward",
            "blockScore",
        ]
        for field in required_fields:
            target_instance.assertIn(field, header, f"Missing required field: {field}")
            target_instance.assertIsNotNone(header.get(field))

        # Kaia header extras from RPCMarshalHeader; treat as optional
        optional_fields = [
            "baseFeePerGas",
            "randomReveal",
            "mixhash",
            "excessBlobGas",
            "blobGasUsed",
        ]
        for field in optional_fields:
            if field in header:
                target_instance.assertIsNotNone(header.get(field))

    @staticmethod
    def check_response_type_newHeads_subscription_eth(target_instance, response):
        """
        Verify newHeads subscription payload for Eth-compatible header format
        (RpcMarshalEthHeader) returned by eth_subscribe.
        """
        response_json = json.loads(response)
        params = response_json.get("params")
        target_instance.assertIsNotNone(params)
        target_instance.assertIn("subscription", params)
        target_instance.assertIn("result", params)

        header = params.get("result")
        target_instance.assertIsInstance(header, dict)

        required_fields = [
            "number",
            "hash",
            "parentHash",
            "nonce",
            "mixHash",
            "sha3Uncles",
            "logsBloom",
            "stateRoot",
            "miner",
            "difficulty",
            "extraData",
            "size",
            "gasLimit",
            "gasUsed",
            "timestamp",
            "transactionsRoot",
            "receiptsRoot",
        ]
        for field in required_fields:
            target_instance.assertIn(field, header, f"Missing required field: {field}")
            target_instance.assertIsNotNone(header.get(field))

        # Eth-compatible extras expected from RpcMarshalEthHeader; treat as optional
        optional_fields = [
            "baseFeePerGas",
            "randomReveal",
            "excessBlobGas",
            "blobGasUsed",
        ]
        for field in optional_fields:
            if field in header:
                target_instance.assertIsNotNone(header.get(field))

    @staticmethod
    def parse_conf_value(key: str, conf_path: str = "") -> str:
        """
        Read a value for the given key from kcnd.conf.
        Falls back to the default test path if conf_path is not provided.
        Returns an empty string if the key/path is not found.
        """
        try:
            path = (
                conf_path
                if conf_path
                else f"{PROJECT_ROOT_DIR}/script/cn/conf/kcnd.conf"
            )
            text = pathlib.Path(path).read_text()
            m = re.search(rf'^{key}="?([^"\n#]+)"?', text, flags=re.M)
            return "" if not m else m.group(1).strip()
        except Exception:
            return ""

    @staticmethod
    def snapshot_runtime_apis(
        endpoint: str,
        log_path: str,
        transport: str,
        port: int,
        ) -> str:
        """
        Fetch current runtime modules via rpc_modules for the given transport and port.
        - transport="rpc": query HTTP RPC only
        - transport="ws": query WebSocket only
        Returns CSV string of module names or empty string on failure.
        """
        t = transport.lower()
        if t not in ("rpc", "ws"):
            raise ValueError("transport must be 'rpc' or 'ws'")

        call = Utils.call_rpc if t == "rpc" else Utils.call_ws
        conf_key = "RPC_API" if t == "rpc" else "WS_API"

        try:
            res, err = call(endpoint, "rpc_modules", [], log_path, port=port)
            if err is None and isinstance(res, dict) and len(res) > 0:
                return ",".join(sorted(res.keys()))
        except Exception:
            pass

        return Utils.parse_conf_value(conf_key) or ""

    @staticmethod
    def generate_blob_raw_data(blob_data: str, chain_id: int = 1, nonce: int = 0,
                                to_address: str = "", gas_limit: int = 21000,
                                gas_tip_cap: int = 1, gas_fee_cap: int = 1,
                                blob_fee_cap: int = 1, value: int = 0,
                                private_key: str = "") -> str:
        """
        Generate RLP-encoded raw data for blob transaction using generate_raw_data.go.
        Args:
            blob_data: Blob data as string to pass via stdin
            chain_id: Chain ID (default: 1)
            nonce: Transaction nonce (default: 0)
            to_address: Recipient address (default: empty string)
            gas_limit: Gas limit (default: 21000)
            gas_tip_cap: Gas tip cap (default: 1)
            gas_fee_cap: Gas fee cap (default: 1)
            blob_fee_cap: Blob fee cap (default: 1)
            value: Transaction value (default: 0)
            private_key: Private key in hex format (with or without 0x prefix) for signing (default: empty string)
        Returns:
            str: Hex-encoded RLP data (signed if private_key is provided)
        """
        helper_tools_dir = os.path.join(PROJECT_ROOT_DIR, "helper_tools")
        go_tool_path = os.path.join(helper_tools_dir, "generate_raw_data.go")

        if not os.path.exists(go_tool_path):
            raise FileNotFoundError(f"Go tool not found: {go_tool_path}")

        # Build command arguments
        # Note: blob_data will be passed via stdin (subprocess.run's input parameter)
        cmd_args = [
            "go", "run", "generate_raw_data.go",
            "-chainid", str(chain_id),
            "-nonce", str(nonce),
            "-gas", str(gas_limit),
            "-gasTipCap", str(gas_tip_cap),
            "-gasFeeCap", str(gas_fee_cap),
            "-blobFeeCap", str(blob_fee_cap),
            "-value", str(value),
        ]

        if to_address:
            cmd_args.extend(["-to", to_address])

        if private_key:
            cmd_args.extend(["-privateKey", private_key])

        # Run the Go tool from helper_tools directory as a single app
        try:
            result = subprocess.run(
                cmd_args,
                cwd=helper_tools_dir,
                input=blob_data,
                capture_output=True,
                text=True,
                check=True
            )

            # Return hex-encoded RLP data (strip newline)
            return result.stdout.strip()

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to run generate_raw_data tool: {e.stderr}")

    @staticmethod
    def generate_blob_raw_transaction(endpoint, test_data_set, namespace="kaia",
                                      blob_data=None, gas_limit=60400,
                                      gas_price=None, value=2441, to_address=None,
                                      log_path=None):
        """
        Generate signed raw blob transaction data using generate_raw_data.go.
        Args:
            endpoint: RPC endpoint URL
            test_data_set: Test data dictionary containing account information
            namespace: RPC namespace (default: "kaia", use "eth" for Ethereum format)
            blob_data: Blob data as string (default: BLOB_TEST_DATA constant)
            gas_limit: Gas limit (default: 60400)
            gas_price: Gas price (default: from test_data_set["unitGasPrice"])
            value: Transaction value (default: 2441)
            to_address: Recipient address (default: from test_data_set["account"]["sender"]["address"])
            log_path: Log file path (default: None, will be obtained internally if not provided)
        Returns:
            tuple: (raw_data, nonce, chainId, txHash) or (None, None, None, None) on error
        """
        if log_path is None:
            _, _, log_path = Utils.get_log_filename_with_path()

        # Get nonce (use "pending" to include pending transactions)
        method = f"{namespace}_getTransactionCount"
        tag = "pending"
        txFrom = test_data_set["account"]["sender"]["address"]
        params = [txFrom, tag]
        nonce, error = Utils.call_rpc(endpoint, method, params, log_path)
        if error is not None:
            return None, None, None, None

        # Get chainId
        method = f"{namespace}_chainId"
        params = []
        chainId, error = Utils.call_rpc(endpoint, method, params, log_path)
        if error is not None:
            return None, None, None, None

        # Set transaction parameters
        if to_address is None:
            to_address = test_data_set["account"]["sender"]["address"]

        if gas_price is None:
            gas_price = int(test_data_set["unitGasPrice"], 16)

        private_key = test_data_set["account"]["sender"]["privateKey"]

        # Use BLOB_TEST_DATA constant if blob_data is not provided
        if blob_data is None:
            blob_data = BLOB_TEST_DATA

        # Generate signed raw data using blob_data directly via stdin
        raw_data = Utils.generate_blob_raw_data(
            blob_data=blob_data,
            chain_id=int(chainId, 16),
            nonce=int(nonce, 16),
            to_address=to_address,
            gas_limit=gas_limit,
            gas_tip_cap=gas_price,
            gas_fee_cap=gas_price,
            blob_fee_cap=gas_price * BLOB_BASE_FEE_MULTIPLIER,
            value=value,
            private_key=private_key
        )

        # For Ethereum format, remove EthereumTxTypeEnvelope (0x78) prefix if present
        # Reference: api_eth.go GetRawTransactionByBlockNumberAndIndex
        if namespace == "eth" and raw_data and len(raw_data) >= 4 and raw_data.startswith("0x"):
            # Check if first byte is 0x78 (EthereumTxTypeEnvelope)
            if raw_data[2:4] == "78":
                # Remove the 0x78 prefix
                raw_data = "0x" + raw_data[4:]

        return raw_data, nonce, chainId, None
