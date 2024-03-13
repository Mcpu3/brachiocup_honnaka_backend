from api.v1.database import LocalSession


def get_database():
    database = LocalSession()
    try:
        yield database
    finally:
        database.close()
