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
    def getAllNodes(genre):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct(a.ArtistId), a.Name 
                    from artist a , album a2 , track t 
                    where a.ArtistId = a2.ArtistId 
                    and a2.AlbumId = t.AlbumId 
                    and t.GenreId = %s"""

        cursor.execute(query, (genre,))

        for row in cursor:
            result.append(Artist(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdges(genre):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """with ca as (
                    select distinct inv.CustomerId as cust, a.ArtistId as art
                    from album a, track t, invoiceline il, invoice inv
                    where a.AlbumId = t.AlbumId
                    and t.TrackId = il.TrackId
                    and il.InvoiceId = inv.InvoiceId
                    and t.GenreId = %s
                ),
                pop as (
                    select a.ArtistId as art, sum(il.Quantity) as p
                    from album a, track t, invoiceline il
                    where a.AlbumId = t.AlbumId
                    and t.TrackId = il.TrackId
                    and t.GenreId = %s
                    group by a.ArtistId
                )
                select distinct ca1.art as art1, ca2.art as art2,
                       p1.p as pop1, p2.p as pop2,
                       p1.p + p2.p as peso
                from ca ca1, ca ca2, pop p1, pop p2
                where ca1.cust = ca2.cust
                and ca1.art < ca2.art
                and p1.art = ca1.art
                and p2.art = ca2.art"""

        cursor.execute(query, (genre,genre,))

        for row in cursor:
            result.append((row["art1"],row["art2"],row["pop1"],row["pop2"], row["peso"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getFillArtist(genre):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct(a.ArtistId), a.Name 
                    from artist a , album a2 , track t 
                    where a2.ArtistId = a.ArtistId 
                    and t.AlbumId = a2.AlbumId 
                    and t.GenreId = %s"""

        cursor.execute(query, (genre,))

        for row in cursor:
            result.append(Artist(**row))

        cursor.close()
        conn.close()
        return result














