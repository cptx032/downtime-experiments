import os
from typing import List

codes: List[str] = [
    "A1",
    "A2",
    "A2n",
    "A4",
    "A5",
    "A6",
    "A7",
    "A8",
    "A10",
    "A10n",
    "A12",
    "A12n",
    "A13",
    "A16",
    "A16n",
    "A18",
    "A18n",
    "A20",
    "A21",
    "A24",
]

operations: List[str] = ["delete", "write", "read", "insert"]
sizes: List[str] = ["10", "100", "1000"]

for code in codes:
    for operation in operations:
        for size in sizes:
            file_name: str = f"logs/{operation}-log-{code}-{size}.txt"
            if not os.path.exists(file_name):
                print(f"Log file not found: {file_name}")
