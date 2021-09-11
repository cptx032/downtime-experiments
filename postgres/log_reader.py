import argparse
from datetime import datetime
from typing import List, Optional, Tuple


def get_metrics(
    file_path: str,
) -> Tuple[List[float], List[float], List[float], float]:
    migration_started: bool = False
    migration_ends: bool = False
    times_before_migration: List[float] = []
    times_during_migration: List[float] = []
    times_after_migration: List[float] = []
    migration_start: datetime
    migration_duration: float

    with open(file_path) as log_file:
        for line in log_file.readlines():
            line = line.strip()
            if not line:
                continue
            if line.startswith("START MIGRATION"):
                migration_started = True
                migration_start = datetime.fromisoformat(
                    line.split()[-1].replace(",", ".")[:-9]
                )
            elif line.startswith("END MIGRATION"):
                migration_ends = True
                migration_end = datetime.fromisoformat(
                    line.split()[-1].replace(",", ".")[:-9]
                )
                migration_duration = (
                    migration_end - migration_start
                ).total_seconds()
            else:
                start, end, success, error_description = line.split(";")
                timedelta = datetime.fromisoformat(
                    end
                ) - datetime.fromisoformat(start)
                milliseconds: float = timedelta.total_seconds() * 1000
                if not migration_started:
                    times_before_migration.append(milliseconds)
                elif migration_started and (not migration_ends):
                    times_during_migration.append(milliseconds)
                elif migration_started and migration_ends:
                    times_after_migration.append(milliseconds)
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
    # the A10 is not possible in normal django applications
    operations: List[str] = [
        "A18",
        "A2",
        "A12",
        "A21",
        "A1",
        "A6",
        "A8",
        "A13",
        "A20",
        "A7",
        "A4",
        "A24",
        "A16",
        "A5",
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
