import os
import sys


def check_environnement():
    to_test = ['AUTHSECRET']
    missing = []

    for v in to_test:
        if v not in os.environ:
            missing.append(v)
    if len(missing) > 0:
        msg = f"Error : Missing value in .env file : {', '.join(missing)}"
        sys.exit(msg)