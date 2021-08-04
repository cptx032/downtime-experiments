import time
from datetime import datetime
from typing import Dict
import sys

import requests

URL: str = "http://localhost:8000/tags/"
delay: float = 0.5  # half second

while True:
    start: str = datetime.now().isoformat()
    success: bool = True
    error: str = ""
    try:
        response = requests.get(URL)
        if not response.ok:
            success = False
            error = str(response.status_code)
    except Exception as e:
        success = False
        error = str(e)
    finally:
        end: str = datetime.now().isoformat()
        with open(sys.argv[1], 'a') as log_file:
            print(
                "{start};{end};{success};{error}".format(
                    start=start, end=end, success=int(success), error=error
                ),
                file=log_file
            )
    time.sleep(delay)
