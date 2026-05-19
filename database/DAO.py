from database.DB_connect import DBConnect


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
    @staticmethod
    def getVerticiPerGenere(genre_name):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        # Uniamo anche la tabella genre 'g' per filtrare direttamente tramite il nome stringa
        query = """
                    SELECT DISTINCT a.ArtistId, a.Name
            FROM artist a
            JOIN album al ON a.ArtistId = al.ArtistId
            JOIN track t ON al.AlbumId = t.AlbumId
            WHERE t.GenreId = %s"
            ORDER BY a.Name
                    """
        cursor.execute(query, (genre_name,))
        for row in cursor:
            result.append(row["Name"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArtistiPerCliente():
        conn = DBConnect.get_connection()
        result = {}
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT i.CustomerId, al.ArtistId
        FROM invoice i
        JOIN invoiceline il ON i.InvoiceId = il.InvoiceId
        JOIN track t ON il.TrackId = t.TrackId
        JOIN album al ON t.AlbumId = al.AlbumId
        GROUP BY i.CustomerId, al.ArtistId
            """
        cursor.execute(query)
        for row in cursor:
            cust_id = row["CustomerId"]
            art_id = row["ArtistId"]
        if cust_id not in result:
            result[cust_id] = set()
            result[cust_id].add(art_id)
        cursor.close()

    @staticmethod
    def getPopolaritaArtisti():
        conn = DBConnect.get_connection()

        result = {}
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT a.ArtistId, SUM(il.Quantity) as Popolarita
        FROM artist a
        JOIN album al ON a.ArtistId = al.ArtistId
        JOIN track t ON al.AlbumId = t.AlbumId
        JOIN invoiceline il ON t.TrackId = il.TrackId
        GROUP BY a.ArtistId
        """
        cursor.execute(query)
        for row in cursor:
            result[row["ArtistId"]] = int(row["Popolarita"])
        cursor.close()
        conn.close()
        return result













