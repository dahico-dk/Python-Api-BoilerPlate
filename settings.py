settings = {
    "Database_url": "mssql+pymssql://test:1234@localhost:1433/testdb?charset=utf8?driver=SQL+Server",
    "SQLDB": "SQLDB",
    "MongoDB": "MongoDB",
    "Socket": "Socket",
}


def db_url():
    return settings["Database_url"]


def sqldb():
    return settings["SQLDB"]


def mongodb():
    return settings["MongoDB"]


def socket():
    return settings["Socket"]
