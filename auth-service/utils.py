import os
import sys


def check_environnement():
    to_test = ['DBNAME', 'DBUSER', 'DBPASSWORD', 'DBHOST', 'DBPORT', 'AUTHSECRET', 'ADMIN_PASSWORD']
    missing = []

    for v in to_test:
        if v not in os.environ:
            missing.append(v)
    if len(missing) > 0:
        msg = f"Error : Missing value in .env file : {', '.join(missing)}"
        sys.exit(msg)