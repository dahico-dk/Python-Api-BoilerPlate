settings = {
    "Database_url": "mssql+pymssql://@localhost:1433/?charset=utf8",
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
