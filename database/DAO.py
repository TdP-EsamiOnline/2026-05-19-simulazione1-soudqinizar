from database.DB_connect import DBConnect
from model.artist import Artist
from model.genre import Genre


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllGenre():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * 
                    from genre g """

        cursor.execute(query)

        for row in cursor:
            result.append(Genre(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getNodes(genreId):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct(a.ArtistId) , a.Name 
                    from artist a , album a2 , track t 
                    where a.ArtistId = a2.ArtistId 
                    and t.AlbumId = a2.AlbumId 
                    and t.GenreId = %s """

        cursor.execute(query, (genreId,))

        for row in cursor:
            result.append(Artist(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdges(genreId):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select i.CustomerId, art.ArtistId, count(*) as ntracks
                    from invoice i, invoiceline i2, track t, genre g, artist art,album a
                    where i.InvoiceId  = i2.InvoiceId 
                    and t.TrackId = i2.TrackId 
                    and t.AlbumId = a.AlbumId
                    and g.GenreId = t.GenreId
                    and art.ArtistId = a.ArtistId 
                    and g.GenreId = %s
                    group by i.CustomerId, art.ArtistId """

        cursor.execute(query, (genreId,))

        for row in cursor:
            result.append((row["CustomerId"], row["ArtistId"], row["ntracks"]))

        cursor.close()
        conn.close()
        return result

