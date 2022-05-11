import json

errors_json = """
{
    "arg0NoParams":[-32602 ,"missing value for required argument 0"],
    "arg1NoParams":[-32602 ,"missing value for required argument 1"],
    "arg0NumberToString":[-32602 ,"invalid argument 0: json: cannot unmarshal number into Go value of type string"],
    "arg1NumberToString":[-32602 ,"invalid argument 1: json: cannot unmarshal number into Go value of type string"],
    "arg2NumberToString":[-32602 ,"invalid argument 2: json: cannot unmarshal number into Go value of type string"],
    "arg3NumberToString":[-32602 ,"invalid argument 3: json: cannot unmarshal number into Go value of type string"],
    "arg0NumberToRPCID": [-32602 ,"invalid argument 0: json: cannot unmarshal number into Go value of type rpc.ID"],
    "arg0NumberToBlockNonce": [-32602 ,"invalid argument 0: json: cannot unmarshal number into Go value of type *api.BlockNonce"],
    "arg0HexToAddress": [-32602 ,"invalid argument 0: json: cannot unmarshal hex string without 0x prefix into Go value of type common.Address"],
    "arg1HexToAddress": [-32602 ,"invalid argument 1: json: cannot unmarshal hex string without 0x prefix into Go value of type common.Address"],
    "arg0HexToBytes": [-32602 ,"invalid argument 0: json: cannot unmarshal hex string without 0x prefix into Go value of type hexutil.Bytes"],
    "arg1HexToBytes": [-32602 ,"invalid argument 1: json: cannot unmarshal hex string without 0x prefix into Go value of type hexutil.Bytes"],
    "arg0StringToHexutilUint64": [-32602 ,"invalid argument 0: json: cannot unmarshal hex string without 0x prefix into Go value of type hexutil.Uint64"],
    "arg0HexToCallArgsGasUint64": [-32602 ,"invalid argument 0: json: cannot unmarshal hex string without 0x prefix into Go struct field CallArgs.gas of type hexutil.Uint64"],
    "arg0HexToCallArgsGaspriceBig": [-32602 ,"invalid argument 0: json: cannot unmarshal hex string without 0x prefix into Go struct field CallArgs.gasPrice of type *hexutil.Big"],
    "arg0HexToCallArgsValueBig": [-32602 ,"invalid argument 0: json: cannot unmarshal hex string without 0x prefix into Go struct field CallArgs.value of type *hexutil.Big"],
    "arg0HexToCallArgsToAddress": [-32602 ,"invalid argument 0: json: cannot unmarshal hex string without 0x prefix into Go struct field CallArgs.to of type common.Address"],
    "arg0HexToEthTransactionArgsFromAddress": [-32602 ,"invalid argument 0: json: cannot unmarshal hex string of odd length into Go struct field EthTransactionArgs.from of type common.Address"],
    "arg0HexToEthTransactionArgsToAddress": [-32602 ,"invalid argument 0: json: cannot unmarshal hex string of odd length into Go struct field EthTransactionArgs.to of type common.Address"],
    "arg0HexToEthTransactionArgsToAddressWithoutPrefix": [-32602 ,"invalid argument 0: json: cannot unmarshal hex string without 0x prefix into Go struct field EthTransactionArgs.to of type common.Address"],
    "arg0HexToEthTransactionArgsGasUint": [-32602 ,"invalid argument 0: json: cannot unmarshal hex string without 0x prefix into Go struct field EthTransactionArgs.gas of type hexutil.Uint64"],
    "arg0HexToEthTransactionArgsGaspriceBig": [-32602 ,"invalid argument 0: json: cannot unmarshal hex string without 0x prefix into Go struct field EthTransactionArgs.gasPrice of type *hexutil.Big"],
    "arg0HexToEthTransactionArgsValueBig": [-32602 ,"invalid argument 0: json: cannot unmarshal hex string without 0x prefix into Go struct field EthTransactionArgs.value of type *hexutil.Big"],
    "arg0HexToEthTransactionArgsNonceUint": [-32602 ,"invalid argument 0: json: cannot unmarshal hex string without 0x prefix into Go struct field EthTransactionArgs.nonce of type hexutil.Uint64"],
    "arg0HexToHash":[-32602 ,"invalid argument 0: json: cannot unmarshal hex string without 0x prefix into Go value of type common.Hash"],
    "arg1HexToHash":[-32602 ,"invalid argument 1: json: cannot unmarshal hex string without 0x prefix into Go value of type common.Hash"],
    "arg0HexToSendTxArgsFromAddress": [-32602 ,"invalid argument 0: json: cannot unmarshal hex string of odd length into Go struct field SendTxArgs.from of type common.Address"],
    "arg0HexToSendTxArgsToAddress": [-32602 ,"invalid argument 0: json: cannot unmarshal hex string of odd length into Go struct field SendTxArgs.to of type common.Address"],
    "arg0HexToSendTxArgsGasUint": [-32602 ,"invalid argument 0: json: cannot unmarshal hex string without 0x prefix into Go struct field SendTxArgs.gas of type hexutil.Uint64"],
    "arg0HexToSendTxArgsGaspriceBig": [-32602 ,"invalid argument 0: json: cannot unmarshal hex string without 0x prefix into Go struct field SendTxArgs.gasPrice of type *hexutil.Big"],
    "arg0HexToSendTxArgsValueBig": [-32602 ,"invalid argument 0: json: cannot unmarshal hex string without 0x prefix into Go struct field SendTxArgs.value of type *hexutil.Big"],
    "arg0HexToSendTxArgsNonceUint": [-32602 ,"invalid argument 0: json: cannot unmarshal hex string without 0x prefix into Go struct field SendTxArgs.nonce of type hexutil.Uint64"],
    "arg0HexWithoutPrefix": [-32602 ,"invalid argument 0: hex string without 0x prefix"],
    "arg1HexWithoutPrefix": [-32602 ,"invalid argument 1: hex string without 0x prefix"],
    "arg2HexWithoutPrefix": [-32602 ,"invalid argument 2: hex string without 0x prefix"],
    "arg0StringToInt":[-32602 ,"invalid argument 0: json: cannot unmarshal string into Go value of type int"],
    "arg1StringToInt":[-32602 ,"invalid argument 1: json: cannot unmarshal string into Go value of type int"],
    "arg0StringToUint64":[-32602 ,"invalid argument 0: json: cannot unmarshal string into Go value of type uint64"],
    "arg1StringToUint64":[-32602 ,"invalid argument 1: json: cannot unmarshal string into Go value of type uint64"],
    "arg2StringToUint64":[-32602 ,"invalid argument 2: json: cannot unmarshal string into Go value of type uint64"],
    "arg1StringToUint":[-32602 ,"invalid argument 1: json: cannot unmarshal string into Go value of type uint"],
    "arg0StringToBool": [-32602 ,"invalid argument 0: json: cannot unmarshal string into Go value of type bool"],
    "arg0StringToSendtx": [-32602 ,"invalid argument 0: json: cannot unmarshal string into Go value of type api.SendTxArgs"],
    "arg0StringToCallArgsDataBytes": [-32602 ,"invalid argument 0: json: cannot unmarshal hex string without 0x prefix into Go struct field CallArgs.data of type hexutil.Bytes"],
    "arg0StringToEthTransactionArgsDataBytes": [-32602 ,"invalid argument 0: json: cannot unmarshal hex string without 0x prefix into Go struct field EthTransactionArgs.data of type hexutil.Bytes"],
    "arg1StringToBool": [-32602 ,"invalid argument 1: json: cannot unmarshal string into Go value of type bool"],
    "arg0NonstringToHash": [-32602 ,"invalid argument 0: json: cannot unmarshal non-string into Go value of type common.Hash"],
    "arg1NonstringToHash": [-32602 ,"invalid argument 1: json: cannot unmarshal non-string into Go value of type common.Hash"],
    "arg2NonstringToHash": [-32602 ,"invalid argument 2: json: cannot unmarshal non-string into Go value of type common.Hash"],
    "arg0NonstringToAddress": [-32602 ,"invalid argument 0: json: cannot unmarshal non-string into Go value of type common.Address"],
    "arg0NonstringToSendTxArgsFromAddress": [-32602 ,"invalid argument 0: json: cannot unmarshal non-string into Go struct field SendTxArgs.from of type common.Address"],
    "arg0NonstringToSendTxArgsToAddress": [-32602 ,"invalid argument 0: json: cannot unmarshal non-string into Go struct field SendTxArgs.to of type common.Address"],
    "arg0NonstringToSendTxArgsGasUint": [-32602 ,"invalid argument 0: json: cannot unmarshal non-string into Go struct field SendTxArgs.gas of type hexutil.Uint64"],
    "arg0NonstringToSendTxArgsGaspriceBig": [-32602 ,"invalid argument 0: json: cannot unmarshal non-string into Go struct field SendTxArgs.gasPrice of type *hexutil.Big"],
    "arg0NonstringToSendTxArgsValueBig": [-32602 ,"invalid argument 0: json: cannot unmarshal non-string into Go struct field SendTxArgs.value of type *hexutil.Big"],
    "arg0NonstringToEthTransactionArgsFromAddress": [-32602 ,"invalid argument 0: json: cannot unmarshal non-string into Go struct field EthTransactionArgs.from of type common.Address"],
    "arg0NonstringToEthTransactionArgsToAddress": [-32602 ,"invalid argument 0: json: cannot unmarshal non-string into Go struct field EthTransactionArgs.to of type common.Address"],
    "arg0NonstringToEthTransactionArgsGasUint": [-32602 ,"invalid argument 0: json: cannot unmarshal non-string into Go struct field EthTransactionArgs.gas of type hexutil.Uint64"],
    "arg0NonstringToEthTransactionArgsGaspriceBig": [-32602 ,"invalid argument 0: json: cannot unmarshal non-string into Go struct field EthTransactionArgs.gasPrice of type *hexutil.Big"],
    "arg0NonstringToEthTransactionArgsValueBig": [-32602 ,"invalid argument 0: json: cannot unmarshal non-string into Go struct field EthTransactionArgs.value of type *hexutil.Big"],
    "arg0NonstringToEthTransactionArgsDataBytes": [-32602, "invalid argument 0: json: cannot unmarshal non-string into Go struct field EthTransactionArgs.data of type hexutil.Bytes"],
    "arg1NonstringToBytes": [-32602 ,"invalid argument 1: json: cannot unmarshal non-string into Go value of type hexutil.Bytes"],
    "arg0NonstringToCallArgsFromAddress": [-32602 ,"invalid argument 0: json: cannot unmarshal non-string into Go struct field CallArgs.from of type common.Address"],
    "arg0NonstringToCallArgsToAddress": [-32602 ,"invalid argument 0: json: cannot unmarshal non-string into Go struct field CallArgs.to of type common.Address"],
    "arg0NonstringToCallArgsDataBytes": [-32602 ,"invalid argument 0: json: cannot unmarshal non-string into Go struct field CallArgs.data of type hexutil.Bytes"],
    "invalidNodeId": [-32000 ,"invalid kni: invalid node ID (wrong length, want 128 hex chars)"],
    "HTTPRPCNotRunning": [-32000 ,"HTTP RPC not running"],
    "NameResolutionFailure": [-32000 ,"listen tcp4: lookup abcd: no such host"],
    "HTTPAlreadyRunning": [-32000 ,"HTTP RPC already running on 0.0.0.0:8551"],
    "WSAlreadyRunning": [-32000 ,"WebSocket RPC already running on 0.0.0.0:8552"],
    "WSRPCNotRunning": [-32000 ,"WebSocket RPC not running"],
    "NoSuchFile": [-32000 ,"no such file or directory"],
    "PProfServerAlreadyRunning": [-32000 ,"pprof server is already running"],
    "PProfServerNotRunning": [-32000 ,"pprof server is not running"],
    "BlockNotFound": [-32000 ,"block #4294967295 not found"],
    "BlockNotExist": [-32000 ,"the block does not exist (block number: 4294967295)"],
    "HeaderNotFound": [-32000 ,"header #4294967295 not found"],
    "HeaderNotExist": [-32000 ,"the header does not exist (block number: 4294967295)"],
    "CouldNotDecodeBlock": [-32000 ,"could not decode block: rlp: value size exceeds available input length"],
    "TargetShouldBeBetween0And3": [-32000 ,"target should be between 0 and 3"],
    "CPUProfilingAlreadyInProgress": [-32000 ,"CPU profiling already in progress"],
    "CPUProfilingNotInProgress": [-32000 ,"CPU profiling not in progress"],
    "TraceAlreadyInProgress": [-32000 ,"trace already in progress"],
    "TraceNotInProgress": [-32000 ,"trace not in progress"],
    "LogLevelHigherThan6": [-32000 ,"insert log level less than 6"],
    "ExpectCommaSeparatedList": [-32000 ,"expect comma-separated list of filename=N"],
    "InvalidHexString": [-32000 ,"invalid hex string"],
    "CouldntDecryptKey": [-32000 ,"could not decrypt key with given passphrase"],
    "ContractCreationWithoutData": [-32000 ,"contract creation without any data provided"],
    "UnknownAccount": [-32000 ,"unknown account"],
    "BlockDoesNotExist": [-32000 ,"the block does not exist (block hash: 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff)"],
    "HeaderDoesNotExist": [-32000 ,"the header does not exist"],
    "FilterNotFound": [-32000 ,"filter not found"],
    "ExecutionReverted": [-32000 ,"evm: execution reverted"],
    "CallerIsNotOwner": [3,"execution reverted: Caller is not owner"],
    "GivenBlockNotExisted": [-32000 ,"block with the given block number is not existed"],
    "GasTooLow": [-32000 ,"intrinsic gas too low"],
    "InvalidUnitPrice": [-32000 ,"invalid unit price"],
    "InsufficientFunds": [-32000 ,"insufficient funds of the sender for value "],
    "InsufficientBalance": [-32000 ,"insufficient balance for transfer "],
    "InsufficientBalanceFeePayer": [-32000, "insufficient balance of the fee payer to pay for gas"],
    "GasRequiredExceedsAllowance": [-32000, "gas required exceeds allowance (0)"],
    "VMErrorOccurs": [-32000 ,"VM error occurs while running smart contract"],
    "InvalidKlaytnSignature": [-32000 ,"invalid Klaytn signature (V is not 27 or 28)"],
    "UnknownBlock": [-32000 ,"Unknown block"],
    "TransactionNotFound": [-32000 ,"transaction ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff not found"],
    "BlockNumberNotAssigned": [-32000 ,"block number is not assigned"],
    "ExistingFile": [-32000 ,"location would overwrite an existing file"],
    "GasNotSpecified": [-32000, "gas not specified"],
    "UndefinedTxType": [-32000, "undefined tx type"]

}
"""

ERRORS = json.loads(errors_json)