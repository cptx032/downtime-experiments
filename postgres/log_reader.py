from datetime import datetime
from typing import List, Optional, Tuple


def get_metrics(
    file_path: str,
) -> Tuple[List[datetime], List[datetime], List[datetime]]:
    migration_started: bool = False
    migration_ends: bool = False
    times_before_migration: List[datetime] = []
    times_during_migration: List[datetime] = []
    times_after_migration: List[datetime] = []
    migration_start: Optional[datetime] = None
    migration_duration: Optional[float] = None

    with open(file_path) as log_file:
        for line in log_file.readlines():
            line = line.strip()
            if not line:
                continue
            if line.startswith("START MIGRATION"):
                migration_started = True
                migration_start = datetime.fromisoformat(line.split()[-1].replace(',', '.')[:-9])
            elif line.startswith("END MIGRATION"):
                migration_ends = True
                migration_end = datetime.fromisoformat(line.split()[-1].replace(',', '.')[:-9])
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
for population in (1, 10, 100):
    for operation in operations:
        file_path: str = "read-log-{}-{}.txt".format(operation, population)
        before: List[datetime]
        during: List[datetime]
        after: List[datetime]
        migration_duration: float

        before, during, after, migration_duration = get_metrics(file_path)
        values: List[str] = [
            operation,
            str(population * 10000),
            str(migration_duration),
            str(len(before)),
            str(sum(before) / float(len(before))),
            str(len(during)),
            str(sum(during) / float(len(during))),
            str(len(after)),
            str(sum(after) / float(len(after))),
        ]
        print(";".join(values))
