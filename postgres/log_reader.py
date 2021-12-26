import argparse
from datetime import datetime
from typing import Dict, List, Tuple


def get_metrics(
    file_path: str,
) -> Tuple[List[float], List[float], List[float], float]:
    times_before_migration: List[float] = []
    times_during_migration: List[float] = []
    times_after_migration: List[float] = []
    migration_start: datetime
    migration_duration: float

    requests: Dict[datetime, datetime] = {}

    with open(file_path) as log_file:
        for line in log_file.readlines():
            line = line.strip()
            if not line:
                continue
            if line.startswith("START MIGRATION"):
                migration_start = datetime.fromisoformat(
                    line.split()[-1].replace(",", ".")[:-9]
                )
            elif line.startswith("END MIGRATION"):
                migration_end = datetime.fromisoformat(
                    line.split()[-1].replace(",", ".")[:-9]
                )
                migration_duration = (
                    migration_end - migration_start
                ).total_seconds()
            else:
                start, end, success, error_description = line.split(";")
                requests[
                    datetime.fromisoformat(start)
                ] = datetime.fromisoformat(end)
    for start in requests:
        end_date: datetime = requests[start]
        if start <= migration_start:
            times_before_migration.append(
                (end_date - start).total_seconds() * 1000
            )
        elif (start > migration_start) and (start <= migration_end):
            times_during_migration.append(
                (end_date - start).total_seconds() * 1000
            )
        elif start > migration_end:
            times_after_migration.append(
                (end_date - start).total_seconds() * 1000
            )
        else:
            raise ValueError("Unknown state")
    return (
        times_before_migration,
        times_during_migration,
        times_after_migration,
        migration_duration,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="It does a UPDATE in a table at each 0.5 seconds"
    )
    parser.add_argument("read_write", type=str, help="read|write")
    args = parser.parse_args()
    operations: List[str] = [
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

    headers = [
        "Operation",
        "Number of Rows",
        "Migration Duration",
        "Requests Before Migration",
        "Duration Average Before Migration",
        "Requests During Migration",
        "Duration Average During Migration",
        "Requests After Migration",
        "Duration Average After Migration",
    ]

    print(";".join(headers))
    for population in (10, 100, 1000):
        for operation in operations:
            file_path: str = "{}-log-{}-{}.txt".format(
                args.read_write, operation, population
            )
            before: List[float]
            during: List[float]
            after: List[float]
            migration_duration: float

            before, during, after, migration_duration = get_metrics(file_path)
            values: List[str] = [
                operation,
                str(population * 10000),
                str(migration_duration),
                str(len(before)),
                str(sum(before) / float(len(before))) if len(before) else "0",
                str(len(during)),
                str(sum(during) / float(len(during))) if len(during) else "0",
                str(len(after)),
                str(sum(after) / float(len(after))) if len(after) else "0",
            ]
            print(";".join(values))
