// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract LogStorage {
    struct Log {
        string logType;
        string data;
        uint256 timestamp;
    }

    Log[] public logs;

    event NewLog(uint256 indexed id, string logType, string data, uint256 timestamp);

    function addLog(string memory logType, string memory data) public {
        logs.push(Log(logType, data, block.timestamp));
        emit NewLog(logs.length - 1, logType, data, block.timestamp);
    }

    function getLogCount() public view returns (uint256) {
        return logs.length;
    }

    function getLog(uint256 idx) public view returns (string memory, string memory, uint256) {
        Log storage l = logs[idx];
        return (l.logType, l.data, l.timestamp);
    }
}
