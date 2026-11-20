window.RUN_VIEWER_DATA = {
  "engineering": {
    "base": {
      "count": "4",
      "result": "OK"
    },
    "candidate": {
      "count": "6",
      "result": "OK"
    },
    "review": {
      "count": "10",
      "result": "FAILED (failures=3)"
    },
    "fixed": {
      "count": "10",
      "result": "OK"
    },
    "conflictExit": "0",
    "fixedExit": "2"
  },
  "research": {
    "query": "Finch seal audit",
    "expected": [
      "V11"
    ],
    "baseline": {
      "ids": [
        "V11",
        "V01"
      ],
      "recall": "1",
      "meanRecall": "2/3",
      "precision": "1/3"
    },
    "candidate": {
      "ids": [
        "V01",
        "V02"
      ],
      "recall": "0",
      "meanRecall": "2/3",
      "precision": "1/2"
    },
    "decision": "retain baseline"
  },
  "automation": {
    "before": {
      "exit": 72,
      "state": "snapshot_ready",
      "evidence": 0,
      "retry": "staged"
    },
    "after": {
      "exit": 73,
      "state": "draft_staged",
      "evidence": 3,
      "retry": "reused"
    }
  }
};
