import json
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
TIMEZONE = ZoneInfo("America/Toronto")


# ===============================================================================================================================
# 1. RUN RECEIPTS
# ===============================================================================================================================

RECEIPTS_FILE = Path("receipts/runs.jsonl")

def write_run_receipt(receipt):
    RECEIPTS_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
   )
   
    receipt["timestamp"] = datetime.now(
         TIMEZONE
    ).isoformat()

    with RECEIPTS_FILE.open("a") as file:
        file.write(
            json.dumps(receipt) + "\n"
        )
