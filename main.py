import sys

from Db import Db
from RegModel import RegModel
from populate_db import populate_db

if __name__ == '__main__':
    flags = sys.argv[1:]

    # Instantiate database
    db = Db()

    def hasFlag(*args):
        for arg in args:
            if arg in flags:
                return True

    if hasFlag("--help", "-h"):
        print("--populate, -h: Populate database.")
        print("--train, -t: Train model.")

    if hasFlag("--populate", "-p"):
        print("Populating database...")
        populate_db(db)

    if hasFlag("--train", "-t"):
        print("Training model...")
        reg_model = RegModel(db)


