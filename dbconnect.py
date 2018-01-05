import MySQLdb

def connection():
    conn = MySQLdb.connect(host="localhost",
                           user = "root",
                           passwd = "oudjira",
                           db = "pythonprogramming")
    c = conn.cursor()

    return c, conn