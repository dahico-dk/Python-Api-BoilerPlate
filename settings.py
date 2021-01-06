# db connection string formats
# mssql (using pymssql)
# mssql+pymssql://<username>:<password>@<freetds_name>/?charset=utf8

# postgresql
# postgresql://[username]:[pass]@[db url]/[db_name]

# mysql
# mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]


settings = {
    "SQL_Database_url": "mssql+pyodbc://hakkisagdic:kodluyoruz.!2020@kodluyoruz.database.windows.net:1433/daghaninki2?driver=SQL+Server",
    "SQLDB": "SQLDB",
    "MongoDB": "mongodb+srv://dhc:6cILUsDI3BBIPeHn@cluster0.ubhyi.mongodb.net/?retryWrites=true&w=majority",
    "MongoDB_dbName": "Test_DB",
    "Socket": "Socket",
}


def db_url():
    return settings["SQL_Database_url"]


def sqldb():
    return settings["SQLDB"]


def mongodb():
    return settings["MongoDB"], settings["MongoDB_dbName"]


def socket():
    return settings["Socket"]
