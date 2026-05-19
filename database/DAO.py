from database.DB_connect import DBConnect
from model.genre import Genre


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllGenre():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select name from genre g """

        cursor.execute(query)

        for row in cursor:
            result.append(row["name"])

        cursor.close()
        conn.close()
        return result









